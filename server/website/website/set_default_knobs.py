#
# OtterTune - set_default_knobs.py
#
# Copyright (c) 2017-18, Carnegie Mellon University Database Group
#
import logging

from .models import KnobCatalog, SessionKnob
from .types import DBMSType, KnobResourceType, VarType

LOG = logging.getLogger(__name__)

# Default tunable knobs by DBMS. If a DBMS is not listed here, the set of
# tunable knobs in the KnobCatalog will be used instead.
DEFAULT_TUNABLE_KNOBS = {
    DBMSType.POSTGRES: {
        "global.autovacuum",
        "global.archive_mode",
        "global.effective_cache_size",
        "global.maintenance_work_mem",
        "global.max_wal_size",
        "global.max_worker_processes",
        "global.shared_buffers",
        "global.temp_buffers",
        "global.wal_buffers",
        "global.work_mem",
    },
    DBMSType.ORACLE: {
        "global.db_cache_size",
        "global.log_buffer",
        "global.hash_area_size",
        "global.open_cursors",
        "global.pga_aggregate_size",
        "global.shared_pool_reserved_size",
        "global.shared_pool_size",
        "global.sort_area_size",
    },
    DBMSType.MYSQL: {
        "global.innodb_buffer_pool_size",
        "global.innodb_thread_sleep_delay",
        "global.innodb_flush_method",
        "global.innodb_log_file_size",
        "global.innodb_max_dirty_pages_pct_lwm",
        "global.innodb_read_ahead_threshold",
        "global.innodb_adaptive_max_sleep_delay",
        "global.innodb_buffer_pool_instances",
        "global.thread_cache_size",
    },
}

# Bytes in a GB
GB = 1024 ** 3
MB = 1024
CPU_CLOCK_CYCLE = 10 ** 9

# Default minval when set to None
MINVAL = 0

# Default maxval when set to None
MAXVAL = 192 * GB
DM_MAXVAL = 1024 * MB

# Percentage of total CPUs to use for maxval
CPU_PERCENT = 2.0

# Percentage of total memory to use for maxval
MEMORY_PERCENT = 0.80

# Percentage of total storage to use for maxval
STORAGE_PERCENT = 0.80

# The maximum connections to the database
SESSION_NUM = 50.0


def set_default_knobs(session, cascade=True):
    dbtype = session.dbms.type
    default_tunable_knobs = DEFAULT_TUNABLE_KNOBS.get(dbtype)

    if not default_tunable_knobs:
        default_tunable_knobs = set(KnobCatalog.objects.filter(
            dbms=session.dbms, tunable=True).values_list('name', flat=True))

    for knob in KnobCatalog.objects.filter(dbms=session.dbms):
        tunable = knob.name in default_tunable_knobs
        minval = knob.minval

        # set session knob tunable in knob catalog
        if tunable and cascade:
            knob.tunable = True
            knob.save()

        if knob.vartype is VarType.ENUM:
            enumvals = knob.enumvals.split(',')
            minval = 0
            maxval = len(enumvals) - 1
        elif knob.vartype is VarType.BOOL:
            minval = 0
            maxval = 1
        elif knob.vartype in (VarType.INTEGER, VarType.REAL):
            vtype = int if knob.vartype == VarType.INTEGER else float

            minval = vtype(minval) if minval is not None else MINVAL
            knob_maxval = vtype(knob.maxval) if knob.maxval is not None else MAXVAL

            if knob.resource == KnobResourceType.CPU:
                maxval = session.hardware.cpu * CPU_PERCENT
            elif knob.resource == KnobResourceType.MEMORY:
                minval = session.hardware.memory * minval if dbtype != DBMSType.DM else minval
                maxval = session.hardware.memory * MB * MEMORY_PERCENT if dbtype == DBMSType.DM else session.hardware.memory * GB * MEMORY_PERCENT
            elif knob.resource == KnobResourceType.STORAGE:
                minval = session.hardware.storage * minval if dbtype != DBMSType.DM else minval
                maxval = session.hardware.storage * MB * STORAGE_PERCENT if dbtype == DBMSType.DM else session.hardware.storage * GB * STORAGE_PERCENT
            else:
                maxval = knob_maxval

            # Special cases
            if dbtype == DBMSType.POSTGRES:
                if knob.name in ('global.work_mem', 'global.temp_buffers'):
                    maxval /= SESSION_NUM
            if dbtype == DBMSType.DM:
                if knob.name == 'global.GLOBAL_CPU_N':
                    minval = int(session.hardware.cpu - 1)
                    maxval = int(session.hardware.cpu)
                if knob.name in ['global.WORKER_THREADS', 'global.TASK_THREADS']:
                    minval = int(session.hardware.cpu)
                    maxval = int(session.hardware.cpu * 2)
                if knob.name in ['global.UNDO_EXTENT_NUM']:
                    maxval = int(session.hardware.cpu ** 2)
                # CPU时钟周期
                if knob.name in ['global.SCAN_CPU', 'global.SEEK_CPU', 'global.LKUP_CPU', 'global.NLIJ_CPU',
                                 'global.HI_CPU', 'global.HI_SEARCH_CPU', 'global.MI_CPU',
                                 'global.NL_CPU', 'global.FLT_CPU', 'global.LARGE_SORT_CPU', 'global.SMALL_SORT_CPU']:
                    maxval = int(session.hardware.cpu * 2 * CPU_CLOCK_CYCLE / 1024 / 1024)

                # 内存
                if knob.name in ['global.BUFFER', 'global.MAX_BUFFER', 'global.AUDIT_SPACE_LIMIT',
                                 'global.CACHE_POOL_SIZE', 'global.MEMORY_POOL']:
                    minval = session.hardware.memory * MB * MEMORY_PERCENT
                    maxval = session.hardware.memory * MB
                # 以KB为单位
                if knob.name in ['global.VM_POOL_TARGET', 'global.SESS_POOL_TARGET', 'global.VM_POOL_SIZE']:
                    minval = session.hardware.memory * MB * MEMORY_PERCENT
                    maxval = session.hardware.memory * MB * MB

                # 存储
                if knob.name in ['global.TEMP_SIZE']:
                    maxval = session.hardware.storage * MB * STORAGE_PERCENT
                if knob.name in ['global.TEMP_SPACE_LIMIT', 'global.CKPT_RLOG_SIZE']:
                    maxval = session.hardware.storage * MB
                # 以KB为单位
                if knob.name in ['global.CKPT_DIRTY_PAGES']:
                    maxval = session.hardware.storage * MB * MB * STORAGE_PERCENT
            if maxval > knob_maxval:
                maxval = knob_maxval
            if maxval < minval:
                LOG.warning(("Invalid range for session knob '%s': maxval <= minval "
                             "(minval: %s, maxval: %s). Setting maxval to the vendor setting: %s."),
                            knob.name, minval, maxval, knob_maxval)
                maxval = knob_maxval

            maxval = vtype(maxval)
            # print("name: {name} 随机值: {minval}-{maxval} ".format(name=knob.name, minval=minval, maxval=maxval))
        else:
            # print("assert name: {name} 随机值: {minval}".format(name=knob.name, minval=minval))
            assert knob.resource == KnobResourceType.OTHER
            maxval = knob.maxval

        SessionKnob.objects.create(session=session,
                                   knob=knob,
                                   minval=minval,
                                   maxval=maxval,
                                   tunable=tunable)
