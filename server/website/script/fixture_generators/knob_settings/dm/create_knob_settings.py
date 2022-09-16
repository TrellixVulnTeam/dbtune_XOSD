#
# OtterTune - create_knob_settings.py
#
# Copyright (c) 2017-18,Carnegie Mellon University Database Group
#
import csv
import json
import shutil
from operator import itemgetter
import re


# Ottertune Type:
# STRING = 1
# INTEGER = 2
# REAL = 3
# BOOL = 4
# ENUM = 5
# TIMESTAMP = 6

# KnobResourceType
# MEMORY = 1
# CPU = 2
# STORAGE = 3
# OTHER = 4

# miss:
# OPTIMIZER_MODE
# cursor_sharing

def set_field(fields):
    # if fields['name'] == 'ISOLATION_LEVEL':
    #     fields['default'] = '1'
    #     fields['minval'] = '1'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,3'
    # if fields['name'] == 'MPP_NLI_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,3'
    # if fields['name'] == 'RLOG_APPEND_LOGIC':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SORT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'SVR_LOG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'USE_PLN_POOL':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'ADVANCE_LOG_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ALTER_MODE_STATUS':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ALTER_TABLE_OPT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'AP_PORT_NUM':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '65534'
    #     fields['vartype'] = 1
    # if fields['name'] == 'ARCH_INI':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'AUDIT_FILE_FULL_MODE':
    #     fields['default'] = '1'
    #     fields['minval'] = '1'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,2'
    #     # fields['summary'] = 'operation mode when audit file is full,1: delete old file; 2: no longer to write audit records'
    # if fields['name'] == 'AUDIT_IP_STYLE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 此参数会造成【无效的游标状态 以及 无效的列序号】
    # if fields['name'] == 'AUTOTRACE_LEVEL':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     # fields['vartype'] = 5
    #     fields['vartype'] = 1
    #     # fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'AUTO_COMPILE_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'AUTO_ENCRYPT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'AUTO_STAT_OBJ':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'BACKSLASH_ESCAPE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BAK_USE_AP':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'BASE64_LINE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,2'
    # if fields['name'] == 'BATCH_PARAM_OPT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BDTA_PACKAGE_COMPRESS':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BEXP_CALC_ST_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '32'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,8,16,32'
    # if fields['name'] == 'BINARY_TO_LOB_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BIND_PARAM_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BLANK_PAD_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BTR_SPLIT_MODE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BUFFER_FAST_RELEASE':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BUFFER_MODE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BUILD_FORWARD_RS':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'BUILD_VERTICAL_PK_BTREE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CALC_AS_DECIMAL':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'CASE_COMPATIBLE_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'CAST_VARCHAR_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CHAR_FIX_STORAGE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CHAR_TO_BLOB_DIRECT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CHECK_SVR_VERSION':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CLIENT_UKEY':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CMP_AS_DECIMAL':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'COMM_TRACE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'COMPATIBLE_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '6'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3,4,5,6'
    # if fields['name'] == 'COMPLEX_VIEW_MERGING':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'COMPRESS_MODE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CONCURRENT_TRX_MODE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'COUNT_64BIT':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CTAB_SEL_WITH_CONS':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CTE_OPT_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'CVIEW_STAR_WITH_PREFIX':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DATA_VALIDATE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'DATETIME_FAST_RESTRICT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DATETIME_FMT_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DBLINK_OPT_VIEW':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DCRS_PORT_NUM':
    #     fields['tunable'] = False
    #     fields['default'] = '6236'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '65534'
    #     fields['vartype'] = 1
    # if fields['name'] == 'DDL_AUTO_COMMIT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DDL_TV_TRIGGER':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DECIMAL_FIX_STORAGE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DEC_CALC_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DIRECT_IO':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DISTINCT_USE_INDEX_SKIP':
    #     fields['default'] = '2'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'OPTIMIZER_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DIST_HASH_ALGORITHM_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DM6_TODATE_FMT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DMKEY_POLICY':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4294967294'
    #     fields['vartype'] = 1
    # if fields['name'] == 'DML_TTS_OPT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DOUBLE_MODE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DROP_CASCADE_VIEW':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DTABLE_PULLUP_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DYNAMIC_CALC_NODES':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'DYN_SQL_CAN_CACHE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ELOG_REPORT_LINK_SQL':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'EMPTY_STR_TO_NULL_LOB':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_ADJUST_NLI_COST':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_AUDIT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'ENABLE_BLOB_CMP_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_CREATE_BM_INDEX_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_DBLINK_TO_INV':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_DDL_ANY_PRIV':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_DIST_IN_SUBQUERY_OPT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4'
    # if fields['name'] == 'ENABLE_DIST_VIEW_UPDATE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 参数未知，待定
    # if fields['name'] == 'ENABLE_ECS':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 参数未知，待定
    # if fields['name'] == 'ENABLE_ECS_MSG_CHECK':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_ENCRYPT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 参数未知，待定
    # if fields['name'] == 'ENABLE_EXTERNAL_CALL':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # ENABLE_FAST_UPDATE = 1 #for SQL TRACE SVR_LOG = 100000
    # if fields['name'] == 'ENABLE_FAST_UPDATE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # #设置ENABLE_FLASHBACK 为 1 后，开启闪回功能。DM 会保留回滚段一段时间，回滚段保留的时间代表着可以闪回的时间长度。由 UNDO_RETENTION 参数指定。
    # if fields['name'] == 'ENABLE_FLASHBACK':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_HASH_JOIN':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_HUGE_SECIND':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_IGNORE_PURGE_REC':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_INDEX_FILTER':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 0: 禁止使用索引连接，使用的是HASH INNER JOIN  1:执行相同的语句，使用NEST LOOP INDEX JOIN
    # if fields['name'] == 'ENABLE_INDEX_JOIN':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_INJECT_HINT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_INVISIBLE_COL':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_IPC':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_JOIN_FACTORIZATION':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_LOCAL_OSAUTH':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_MERGE_JOIN':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_MONITOR':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_MONITOR_BP':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_MONITOR_DMSQL':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_NEST_LOOP_JOIN_CACHE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'ENABLE_OBJ_REUSE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_OFFLINE_TS':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'ENABLE_OSLOG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_PAGE_CHECK':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'ENABLE_PARTITION_WISE_OPT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_PL_SYNONYM':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_PRISVC':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_REMOTE_OSAUTH':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_RQ_TO_INV':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_RQ_TO_NONREF_SPL':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '7'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,3,5,6,7'
    # if fields['name'] == 'ENABLE_RQ_TO_SPL':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_SEQ_REUSE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_STRICT_CHECK':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_TABLE_EXP_REF_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_TIMER_TRIG_LOG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_TMP_TAB_ROLLBACK':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_UDP':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENABLE_VERTICAL_TABLE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ENHANCED_SUBQ_MERGING':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'ENHANCE_BIND_PEEKING':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ERROR_COMPATIBLE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ERROR_TRACE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'EXCLUDE_MS_DBO':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'EXCLUDE_PKG_NAME':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'EXP_BALANCE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'FAST_EXTEND_WITH_DS':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否在登录时记录登录失败历史信息
    # if fields['name'] == 'FAST_LOGIN':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 是否通过异步快速释放lob页面
    # if fields['name'] == 'FAST_RELEASE_LOB_PAGE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 通过 msg 对 lob 操作后是否释放 lob 锁，0：保持 1：释放
    # if fields['name'] == 'FAST_RELEASE_LOB_SLOCK':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 快速读写锁标记，0不启用；1表示只有FAST POOL启用，2表示所有POOL都启用
    # if fields['name'] == 'FAST_RW_LOCK':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # V$DATAFILE查询时控制抽样比例，最多抽样10000页； 在50页以下的不抽样。有效值范围（0~100.0），0相当于100
    # if fields['name'] == 'FILE_SCAN_PERCENT':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '100'
    #     fields['vartype'] = 3
    # # 日志中是否记录文件操作，0：不记录；1：记录
    # if fields['name'] == 'FILE_TRACE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'FILL_COL_DESC_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'FILTER_PUSH_DOWN':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '15'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15'
    # # 快速插入锁定表模式 0：保持锁定； 1：锁定且不等待并释放锁定 2：锁定超时并释放锁定
    # if fields['name'] == 'FINS_LOCK_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'FORCE_CERTIFICATE_ENCRYPTION':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 待定：是否在强制模式下回收类实例
    # if fields['name'] == 'FORCE_RECLAIM':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 控制一些涉及FROM项的优化0：不优化；1：尝试将FROM项替换为单个DUAL表
    # if fields['name'] == 'FROM_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 系统强制HALT时，是否打印线程堆栈信息到日志文件中。0：不打印；1：打印
    # if fields['name'] == 'GDB_THREAD_INFO':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 待定：语句块执行是否提前回收空间。0：否；1：是，语句块生成各个SQL计划后，都需尝试回收部分PHA内存空间
    # if fields['name'] == 'GEN_SQL_MEM_RECLAIM':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # if fields['name'] == 'GLOBAL_CHARSET':
    # #     fields['tunable'] = False
    # #     fields['default'] = '0'
    # #     fields['minval'] = '0'
    # #     fields['maxval'] = '2'
    # #     fields['vartype'] = 5
    # #     fields['enumvals'] = '0,1,2'
    # # if fields['name'] == 'GLOBAL_PRIV_FLAG':
    # #     fields['tunable'] = False
    # #     fields['default'] = '0'
    # #     fields['minval'] = '0'
    # #     fields['maxval'] = '1'
    # #     fields['vartype'] = 5
    # #     fields['enumvals'] = '0,1'
    # # 控制分组相关的一些处理和优化，可取值0、1、2、4、8、16、32及这些值的组合值
    # if fields['name'] == 'GROUP_OPT_FLAG':
    #     fields['default'] = '52'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '63'
    #     fields['vartype'] = 5
    #     fields[
    #         'enumvals'] = '0,1,2,4,8,16,32,3,5,9,17,33,6,10,18,34,12,20,36,24,40,48,7,11,19,35,13,21,37,25,41,49,14,22,38,26,42,50,28,44,52,56,15,23,39,27,43,51,29,45,53,57,30,46,54,58,60,31,47,55,59,61,62,63'
    # # 待定： MPP下是否对HAGR+DISTINCT进行优化。可取值0、1、2及这些值的组合值
    # if fields['name'] == 'HAGR_DISTINCT_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'HAGR_HASH_ALGORITHM_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 待定： MPP/LPQ下，对HAGR/AAGR/AFUN/DISTINCT/HRO操作的优化，可取值0、1、2、4、8、16、32、64、128、256、512及这些值的组合使用
    # if fields['name'] == 'HAGR_PARALLEL_OPT_FLAG':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 1023
    #     fields['vartype'] = 2
    # # 是否对HASH比较进行优化，可取值为0、1、2、4、8及这些值的组合值
    # if fields['name'] == 'HASH_CMP_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '15'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15'
    # # 执行阶段优化参数。HASH INNER JOIN执行时，右孩子循环执行的次数，取值范围为[1,10]
    # if fields['name'] == 'HASH_JOIN_LOOP_TIMES':
    #     fields['default'] = 10
    #     fields['minval'] = 1
    #     fields['maxval'] = 10
    #     fields['vartype'] = 2
    # # 当进行HASH SEMI/INNER连接且右表为分区表时，控制是否对分区表连接进行优化以及优化的方式，可取值为0、1、2、4、8、16、32
    # if fields['name'] == 'HASH_PLL_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '32'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,8,16,32'
    # if fields['name'] == 'HA_INST_CHECK_PORT':
    #     fields['default'] = '65534'
    #     fields['minval'] = '1024'
    #     fields['maxval'] = '65534'
    #     fields['vartype'] = 1
    # if fields['name'] == 'HA_OTHER_INST_PORT':
    #     fields['default'] = '65534'
    #     fields['minval'] = '1024'
    #     fields['maxval'] = '65534'
    #     fields['vartype'] = 1
    # # HUGE表数据缓冲区中缓存数据的格式，取值范围：0、1，默认值为0 0：格式与数据文件中的数据块格式一致 1：当数据块是压缩加密时，缓存解密解压后的数据
    # if fields['name'] == 'HBUF_DATA_MODE':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否启动HUGE表查询插入优化。0：否；1：对非HUGE分区表进行优化；2：对HUGE分区表也进行优化
    # if fields['name'] == 'HFINS_PARALLEL_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 是否为HUGE表数据区进行和校验：0：否；1：是
    # if fields['name'] == 'HFS_CHECK_SUM':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 待定：按照hash关联的右表顺序进行排序
    # if fields['name'] == 'HI_RIGHT_ORDER_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 装载最后一个数据区是否强制列存。1：是；0：否
    # if fields['name'] == 'HLDR_FORCE_COLUMN_STORAGE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 使用DMFLDR装载数据时如发生错误，对错误的处理方式：0：完全回滚方式，数据将回到装载前的状态；1：修复方式，系统将数据修复到最后一个完整装载的数据区 注：若此参数为1，DMFLDR装载数据时不能支持支持事务型HUGE表二级索引的维护
    # if fields['name'] == 'HLDR_REPAIR_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 控制多列非相关NOT IN的查询实现方式，1：当数据量较大，HASH BUF放不下时，采用MTAB方式处理；2：当数据量较大，HASH BUF放不下时，采用B树方式处理，使用细粒度扫描；3：当数据量较大，HASH BUF放不下时，采用B树方式处理，使用粗粒度扫描
    # if fields['name'] == 'HLSM_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '1'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,2,3'
    # # 是否支持HUGE表增删改与查询的并发，取值范围：0、1、2。 0：不支持HUGE表增删改与查询的并发； 1：支持HUGE表增删改与查询的并发，操作符HFLKUP检查数据区是否上锁时使用二分查找； 2：支持HUGE表增删改与查询的并发，操作符HFLKUP检查数据区是否上锁时使用遍历查找
    # if fields['name'] == 'HUGE_ACID':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 设置默认情况下是否计算WITH DELTA的HUGE表各列的统计信息，取值范围：0、1、2。 0：不计算统计信息； 1：实时计算统计信息； 2：异步计算统计信息
    # if fields['name'] == 'HUGE_STAT_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '2'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # DDL CREATE 的巨大表开关。 0：有 raux，3：没有 raux
    # if fields['name'] == 'HUGE_TABLE_SWITCH':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # # 是否只支持delta大表，0：NO 1：YES
    # if fields['name'] == 'HUGE_WITH_DELTA':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否开启ID资源回收功能。在服务器启动后，申请新的表ID、索引ID、约束ID，但是ID最终未成功使用后，ID会暂时加入回收缓存中，以备下次申请使用，服务器关闭后，缓存中的ID全部丢弃。1是，0否。
    # if fields['name'] == 'ID_RECYCLE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 系统重启时，是否检查SYSTEM/ROLL/MAIN表空间文件系统；取值范围0，1；默认0，检查文件系统。1，不检查文件系统。在实际使用空间比较大情况下，可以考虑关闭文件系统检查，提高系统启动速度。
    # if fields['name'] == 'IGNORE_FILE_SYS_CHECK':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 复合索引跳跃扫描的代价调节开关。和USE_INDEX_SKIP_SCAN搭配使用。当列的（distinct数/总行数）比值大于该值时，就不再使用索引跳跃扫描的方式。取值范围为[0,1]
    # if fields['name'] == 'INDEX_SKIP_SCAN_RATE':
    #     fields['default'] = '0.0025'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 3
    # # HLDR最多保持重用HLDR_BUF的个数与目标表列数的比例。取值范围：1~65535
    # if fields['name'] == 'HLDR_HOLD_RATE':
    #     fields['default'] = '1.5'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '65535'
    #     fields['vartype'] = 3
    # # 用于DBMS_METADATA包查询索引结果。0: 查询系统的内部索引定义报错；1：允许查询系统的内部索引定义
    # if fields['name'] == 'INNER_INDEX_DDL_SHOW':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否进行函数调用相关优化，可取值为0、1、2、4、8、16、32、64及其组合值
    # # if fields['name'] == 'INVOCATION_OPT_FLAG':
    # #     fields['tunable'] = False
    # #     fields['default'] = '55'
    # #     fields['minval'] = '0'
    # #     fields['maxval'] = '63'
    # #     fields['vartype'] = 5
    # #     fields['enumvals'] = '0,1,2,3,4,5,6,7'
    # if fields['name'] == 'INVOCATION_OPT_FLAG':
    #     fields['default'] = '55'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '63'
    #     fields['vartype'] = 2
    # # 考虑所有用户定义的函数确定性
    # if fields['name'] == 'INV_DETERMINISTIC_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # IN值列表是否能作为多表连接时INDEX JOIN的KEY，可取值0、1
    # if fields['name'] == 'IN_LIST_AS_JOIN_KEY':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 系统默认隔离级别。1：读提交；3：可串行化
    # if fields['name'] == 'ISOLATION_LEVEL':
    #     fields['default'] = '1'
    #     fields['minval'] = '1'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,3'
    # # 是否忽略显示设置的事务隔离级别，1表示忽略，0不忽略。
    # if fields['name'] == 'ISO_IGNORE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 待定：是否使用统计信息优化连接选择性
    # if fields['name'] == 'JOIN_ST_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '7'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3,4,5,6,7'
    # # JSON语法解析兼容模式。0：兼容ORACLE；1：兼容PostgreSQL
    # if fields['name'] == 'JSON_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否开启LOCAL DISTRIBUTE操作符使用与MPP DISTRIBUTE操作符不同的函数来计算哈希值，可取值为0、1
    # if fields['name'] == 'LDIS_NEW_FOLD_FUN':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 序列兼容参数，0：与ORACLE兼容；1：与旧版本DM兼容，不推荐使用
    # if fields['name'] == 'LEGACY_SEQUENCE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'LENGTH_IN_CHAR':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否对LIKE表达式进行优化处理，以及采取何种优化方式，可取值0、1、2、4、8、16、32
    # # if fields['name'] == 'LIKE_OPT_FLAG':
    # #     fields['default'] = '31'
    # #     fields['minval'] = '0'
    # #     fields['maxval'] = '31'
    # #     fields['vartype'] = 5
    # #     fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31'
    # if fields['name'] == 'LIKE_OPT_FLAG':
    #     fields['default'] = '63'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '63'
    #     fields['vartype'] = 2
    # # 默认情况下，创建的表是否为堆表，0：否；1：是
    # if fields['name'] == 'LIST_TABLE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'LLOG_INI':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否在 MVCC 模式下访问 LOB
    # if fields['name'] == 'LOB_MVCC':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'LOCK_DICT_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '2'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'LOCK_TID_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'LOCK_TID_UPGRADE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'MAC_LABEL_OPTION':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 是否开启对所有内存池的校验。0：不开启；1：开启校验，校验码基于分配出的块地址计算，在被分配空间的头部和尾部写入校验码；2：增强校验，在1的基础上，如果是内存池分配的，则对尾部未使用空间也计算校验码，写入未使用空间的头部
    # if fields['name'] == 'MEMORY_MAGIC_CHECK':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2,3'
    # # 在merge into stmt时是否忽略src_multi_rows
    # if fields['name'] == 'MERGE_SRC_MULTI_ROWS_IGNORE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'MESSAGE_CHECK':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # TO_CHAR的结果是否显示毫秒值。0：不显示；1：显示
    # if fields['name'] == 'MILLISECOND_FMT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # MMT存储数据方式。1：按页存储；2：BDTA存储。仅在MMT_SIZE大于0时有效
    # if fields['name'] == 'MMT_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '1'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,2'
    # # 是否对索引进行监控，0：关闭自动监控，可使用ALTER INDEX语句启用索引监控；1：打开自动监控，对用户定义的二级索引进行监控；2：禁止索引监控
    # # if fields['name'] == 'MONITOR_INDEX_FLAG':
    # #     fields['tunable'] = False
    # #     fields['default'] = '0'
    # #     fields['minval'] = '0'
    # #     fields['maxval'] = '2'
    # #     fields['vartype'] = 5
    # #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'MS_PARSE_PERMIT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # # MPP/LPQ下，是否对GROUP/HASH JOIN/OUTER JOIN/MERGE JOIN进行递归判断分组列/连接列是否为分布列，并进行相应优化处理。可取值0、1
    # if fields['name'] == 'MULTI_HASH_DIS_OPT':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否将多列IN转换为EXISTS，可取值0、1
    # if fields['name'] == 'MULTI_IN_CVT_EXISTS':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否使用优化的多列更新。0：不使用，仍按照语句改写方式实现；1：利用多列SPL功能加以实现
    # if fields['name'] == 'MULTI_UPD_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 控制是否启动数据页可见性优化处理。0：关闭数据页可见性优化；1：启用数据页可见性优化
    # if fields['name'] == 'MVCC_PAGE_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'MY_STRICT_TABLES':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 控制布尔表达式的一些优化。0：不优化；1：进行根据展开后的项数控制NOT是否下放展开的优化；2：进行AND分支的OR布尔表达式的公因子上拉优化。 支持使用上述有效值的组合值，如3表示同时进行1、2的优化
    # if fields['name'] == 'NBEXP_OPT_FLAG':
    #     fields['default'] = '7'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '7'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3,4,5,6,7'
    # # 是否支持C风格的嵌套注释，0：不支持；1：支持
    # if fields['name'] == 'NESTED_C_STYLE_COMMENT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否使用代价计算来决定使用的通讯操作符，0：否；1：是
    # if fields['name'] == 'NEW_MOTION':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否开启 IN LIST优化：将不含有常量的OR表达式转换成IN LIST。0表示不开启，1表示开启
    # if fields['name'] == 'NONCONST_OR_CVT_IN_LST_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否将非相关子查询转化为常量处理
    # if fields['name'] == 'NONREFED_SUBQUERY_AS_CONST':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 连接条件上的最大或表达式数
    # if fields['name'] == 'NPLN_OR_MAX_NODE':
    #     fields['tunable'] = False
    #     fields['default'] = '20'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '20'
    #     fields['vartype'] = 1
    # if fields['name'] == 'NUMBER_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 启用联机分析处理，0：不启用；1：启用；2：不启用，同时倾向于使用索引范围扫描
    # if fields['name'] == 'OLAP_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # # 待定：散列标志单元格之一：0 不使用标志
    # if fields['name'] == 'ONE_GROUP_SIZE':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 250000000
    #     fields['vartype'] = 2
    # # 待定：inter can dis 的孩子
    # if fields['name'] == 'OPERATION_NEW_MOTION':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 15
    #     fields['vartype'] = 2
    # # 控制IN表达式的优化
    # if fields['name'] == 'OPTIMIZER_IN_NBEXP':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'OPTIMIZER_VERSION':
    #     fields['tunable'] = False
    #     fields['default'] = '70099'
    #     fields['minval'] = '70000'
    #     fields['maxval'] = '70099'
    #     fields['vartype'] = 1
    # # 待定：内存紧张时，优化器是否缩减计划探测空间，仅OPTIMIZER_MODE=0时生效。0：不缩减计划探测空间；1：缩减计划探测空间；
    # if fields['name'] == 'OPT_MEM_CHECK':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否使用HFSEK优化HUGE表中列的OR过滤条件。0：不使用；1：使用
    # if fields['name'] == 'OPT_OR_FOR_HUGE_TABLE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 当查询条件为=(SUBQUERY)，是否考虑转换为等价的IN(SUBQUERY)。0：不转换；1：转换
    # if fields['name'] == 'OP_SUBQ_CVT_IN_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'ORA_DATE_FMT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 待定：控制排序时NULL值返回的位置
    # if fields['name'] == 'ORDER_BY_NULLS_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 当USE_HTAB=1时才有效。 当查询条件OR中含有公共因子时，是否允许使用HTAB来进行优化。0：不使用；1：使用；2：增强OR表达式转换为HTAB条件检查，当存在嵌套连接时，不生成HTAB，以避免缓存过多数据影响性能
    # if fields['name'] == 'OR_CVT_HTAB_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 是否将OR布尔表达式转换成CASE WHEN表达式
    # if fields['name'] == 'OR_NBEXP_CVT_CASE_WHEN_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 待定：控制外连接转化内连接的优化
    # if fields['name'] == 'OUTER_CVT_INNER_PULL_UP_COND_FLAG':
    #     fields['default'] = '3'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '7'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3,4,5,6,7'
    # # 对左外连接进行平坦化处理时，是否优化连接的执行顺序
    # if fields['name'] == 'OUTER_JOIN_FLATING_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 多个外连接情况下，若下层可转换为INNER JOIN，且与上层表存在连接条件，是否将跨层关联的两张表优化为INDEX JOIN
    # if fields['name'] == 'OUTER_JOIN_INDEX_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否进行外连接、内连接的相关优化
    # if fields['name'] == 'OUTER_OPT_NLO_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '7'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3,4'
    # if fields['name'] == 'PAGE_CHECK_HASH_SIZE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '64'
    #     fields['vartype'] = 1
    # if fields['name'] == 'PAGE_CHECK_ID':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4294967294'
    #     fields['vartype'] = 1
    # if fields['name'] == 'PAGE_ENC_SLICE_SIZE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4096'
    #     fields['vartype'] = 1
    # if fields['name'] == 'PAGE_TAIL_SIZE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4096'
    #     fields['vartype'] = 1
    # # 是否打开本地并行查询（Local Parallel Query）开关
    # if fields['name'] == 'PARALLEL_POLICY':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'PARALLEL_PURGE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否启用并行事务清理，0：不启用；1：启用
    # if fields['name'] == 'PARALLEL_PURGE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否对去除重复值操作的下层连接进行转换
    # if fields['name'] == 'PARTIAL_JOIN_EVALUATION_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # MPP系统中是否进行NTTS计划的优化，打开时可能减少计划中的NTTS操作符。0：不支持；1：支持
    # if fields['name'] == 'PHF_NTTS_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 专门用于MPP环境中，在建表语句中指定了PK列，没有指定分布方式时，是否自动将PK列作为HASH分布列，将整个表转为HASH分布
    # if fields['name'] == 'PK_MAP_TO_DIS':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'PK_WITH_CLUSTER':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'PLACE_GROUP_BY_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'PL_SQLCODE_COMPATIBLE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否将引用列转换为变量VAR，并替换查询表达式中的引用列
    # if fields['name'] == 'PRJT_REPLACE_NPAR':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'PROXY_PROTOCOL_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'PSEG_MGR_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 优化清除段中的页面标志
    # if fields['name'] == 'PSEG_PAGE_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'PSEG_RECV':
    #     fields['tunable'] = False
    #     fields['default'] = '3'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2,3'
    # # 清除删除优化标志
    # if fields['name'] == 'PURGE_DEL_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # # 是否下放子查询使先做
    # if fields['name'] == 'PUSH_SUBQ':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '7'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,3,5,6,7'
    # # 隐藏查询相关参数
    # if fields['name'] == 'QUERY_INFO_BITS':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2147483647'
    #     fields['vartype'] = 1
    # # CASE语句NOT FOUND是否抛出异常
    # if fields['name'] == 'RAISE_CASE_NOT_FOUND':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 指定是否支持备库查询。0：不支持；1：支持。关闭备库查询功能可提升备库重演性能
    # if fields['name'] == 'REDOS_ENABLE_SELECT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 重演REDO日志时是否开启RLOG_PKG预加载功能
    # if fields['name'] == 'REDOS_PRE_LOAD':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'REDO_IGNORE_DB_VERSION':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'REDO_PWR_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否将相关EXISTS查询转化为非相关IN查询
    # if fields['name'] == 'REFED_EXISTS_OPT_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # # 是否将OP ALL/SOME/ANY相关子查询进行转换处理
    # if fields['name'] == 'REFED_OPS_SUBQUERY_OPT_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,3,5,6,7'
    # # 指定正则表达式的匹配模式
    # if fields['name'] == 'REGEXP_MATCH_PATTERN':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'REP_INI':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'RESTRICT_DBA':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'RESULT_SET_FOR_QUERY':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否启用在日志中记录逻辑操作的功能
    # if fields['name'] == 'RLOG_APPEND_LOGIC':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'RLOG_APPEND_SYSTAB_LOGIC':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否检查日志空间
    # if fields['name'] == 'RLOG_CHECK_SPACE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'RLOG_GEN_FOR_HUGE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'RLOG_IGNORE_TABLE_SET':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'RLOG_PKG_SEND_ECPR_ONLY':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 服务器执行出错时的回滚策略选择，0：回滚当前语句；1：回滚整个事务
    # if fields['name'] == 'ROLL_ON_ERR':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否以BDTA形式返回结果集
    # if fields['name'] == 'RS_BDTA_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,2'
    # # 结果集缓存的语句执行时间下限，只有实际执行时间不少于指定时间值的查询，其结果集才会被缓存，仅在RS_CAN_CACHE=1时有效
    # if fields['name'] == 'RS_CACHE_MIN_TIME':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4294967294'
    #     fields['vartype'] = 1
    # # 结果集缓存配置
    # if fields['name'] == 'RS_CAN_CACHE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'RS_PRE_FETCH':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SECUR_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'SEC_PRIV_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 当SELECT项中含有相关子查询时，是否将主体查询转换为HEAP TABLE，可取值为0、1、2、4、8。当SELECT项中含有相关子查询时，将主体转换为HEAP TABLE。当相关子查询结果集较大，但整体结果集较小时，将主体转换为HEAP TABLE可取得较好的优化效果
    # if fields['name'] == 'SEL_ITEM_HTAB_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '15'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15'
    # if fields['name'] == 'SEL_RATE_EQU':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SEL_RATE_SINGLE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SHOW_LOGIN_FAIL_TIMES':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SINGLE_HTAB_REMOVE_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SLCT_ERR_PROCESS_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SLCT_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '15'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15'
    # # 排序机制，0：原排序机制；1：新排序机制
    # if fields['name'] == 'SORT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'SPACE_COMPARE_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否加速半连接的探测过程
    # # if fields['name'] == 'SPEED_SEMI_JOIN_PLAN':
    # #     fields['default'] = '1'
    # #     fields['minval'] = '0'
    # #     fields['maxval'] = '7'
    # #     fields['vartype'] = 5
    # #     fields['enumvals'] = '0,1,2,3,4,5,6,7'
    # if fields['name'] == 'SPEED_SEMI_JOIN_PLAN':
    #     fields['default'] = 9
    #     fields['minval'] = 0
    #     fields['maxval'] = 31
    #     fields['vartype'] = 2
    # if fields['name'] == 'SPIN_TIME':
    #     fields['default'] = '4000'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '4000'
    #     fields['vartype'] = 1
    # if fields['name'] == 'SPL_SHARE_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SQL_LOG_FORBID':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # SQL安全更新控制参数
    # if fields['name'] == 'SQL_SAFE_UPDATE_ROWS':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2147483647'
    #     fields['vartype'] = 1
    # if fields['name'] == 'STARTUP_CHECKPOINT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'STARTUP_TIMEOUT':
    #     fields['tunable'] = False
    #     fields['default'] = '5'
    #     fields['minval'] = '5'
    #     fields['maxval'] = '10000'
    #     fields['vartype'] = 1
    # # 是否允许使用位图连接索引
    # if fields['name'] == 'STAR_TRANSFORMATION_ENABLED':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 在估算分区表行数时，控制一些优化。
    # if fields['name'] == 'STAT_ALL':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # # LIKE运算中是否忽略匹配串的结尾
    # if fields['name'] == 'STR_LIKE_IGNORE_MATCH_END_SPACE':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'STR_NULL_OPS_COMPATIBLE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 控制相关子查询的实现方式
    # if fields['name'] == 'SUBQ_CVT_SPL_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '31'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31'
    # if fields['name'] == 'SUBQ_EXP_CVT_FLAG':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 63
    #     fields['vartype'] = 2
    # if fields['name'] == 'SUSPENDING_FORBIDDEN':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 指定文件切换频度。0：按月；1：按天；2：按小时。
    # if fields['name'] == 'SVR_ELOG_FREQ':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'SVR_LOG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 设置参数SVR_LOG_ASYNC_FLUSH打开SQL日志异步刷盘提高系统性能
    # if fields['name'] == 'SVR_LOG_ASYNC_FLUSH':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 用于记录 sql 请求的文件数
    # if fields['name'] == 'SVR_LOG_FILE_NUM':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1024'
    #     fields['vartype'] = 1
    # # POINT指令是否在服务器端打印，打印信息会记录到LOG目录下的DMSERVERSERIVCE.LOG文件中
    # if fields['name'] == 'SVR_OUTPUT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'SYS_INDEX_MATCH_IGNORE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # MPP环境下，对于RANGE/LIST水平分区表，估算行数时是否优先采用统计信息的收集值
    # if fields['name'] == 'TABLE_STAT_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'TABLE_SWITCH':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '134'
    #     fields['vartype'] = 1
    # # 临时表空间大小上限，以M为单位。0表示不限制临时表空间大小。 有效范围（0~ 4294967294）。 注：TEMP_SPACE_LIMIT一定要大于等于 TEMP_SIZE
    # if fields['name'] == 'TEMP_SPACE_LIMIT':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 4294967294
    #     fields['vartype'] = 2
    # if fields['name'] == 'TIMER_INI':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'TIMESTAMP_WITH_PREC':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'TIME_ZONE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '-780'
    #     fields['maxval'] = '780'
    #     fields['vartype'] = 1
    # # 是否通过禁用HASH JOIN方式来优化TOP查询
    # if fields['name'] == 'TOP_DIS_HASH_FLAG':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # # 是否对带有TOP和ORDER BY子句的查询进行优化，以移除SORT操作符
    # if fields['name'] == 'TOP_ORDER_OPT_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2,3'
    # if fields['name'] == 'TRXID_UNCOVERED':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'TRX_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'TRX_RLOG_WAIT_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'TRX_VIEW_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 排序优化选项。0：排序操作一律使用估算的行数分配内存（至少2M）；1：打开优化，排序操作结果行数较少时，使用实际的记录行数分配内存
    # if fields['name'] == 'TSORT_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'UDP_TRACE_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'UNPIVOT_ORDER_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'UPD_DEL_OPT':
    #     fields['tunable'] = False
    #     fields['default'] = '2'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'UPD_QRY_LOCK_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 系统启动时是否更新表信息（如行数），1：启用更新；0：不更新。
    # if fields['name'] == 'UPD_TAB_INFO':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'USBKEY_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 使用 dhash 标志：0 表示使用静态哈希； 1 表示使用动态哈希； 2 表示使用动态哈希2
    # if fields['name'] == 'USE_DHASH_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'USE_FJ_REMOVE_TABLE_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'USE_FK_REMOVE_TABLES_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否使用FORALL语句的游标属性，0：不使用；1：使用
    # if fields['name'] == 'USE_FORALL_ATTR':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'USE_FTTS':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 集函数包含DISTINCT时，分组查询是否使用HASH分组
    # if fields['name'] == 'USE_HAGR_FLAG':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'USE_HTAB':
    #     fields['tunable'] = False
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 是否开启复合索引跳跃扫描，和INDEX_SKIP_SCAN_RATE搭配使用
    # if fields['name'] == 'USE_INDEX_SKIP_SCAN':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'USE_MCLCT':
    #     fields['tunable'] = False
    #     fields['default'] = '2'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'USE_MD_STAT':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'USE_NEW_HASH':
    #     fields['default'] = '1'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # # 是否重用执行计划。0：禁止执行计划的重用；1：启用执行计划的重用功能 ；2：对不包含显式参数的语句进行常量参数化优化；3：即使包含显式参数的语句，也进行常量参数化优化
    # if fields['name'] == 'USE_PLN_POOL':
    #     fields['default'] = '1'
    #     fields['minval'] = '1'
    #     fields['maxval'] = '3'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '1,2,3'
    # if fields['name'] == 'USE_RDMA':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 待定： 处理相关子查询时是仅将相关的表下放，还是连同上方的SEMI/HASH JOIN一同下放
    # if fields['name'] == 'USE_REFER_TAB_ONLY':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'UTHR_FLAG':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # # 指定是否对视图条件进行优化以及如何优化
    # if fields['name'] == 'VIEW_FILTER_MERGING':
    #     fields['default'] = 138
    #     fields['minval'] = 0
    #     fields['maxval'] = 255
    #     fields['vartype'] = 2
    # # 待定：是否对视图进行上拉优化，把视图转换为其原始定义，消除视图
    # if fields['name'] == 'VIEW_PULLUP_FLAG':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 63
    #     fields['vartype'] = 2
    # # *待定：VM是否使用HEAP分配内存。0：MEMORY POOL模式；1：HEAP模式；2：MEMORY POOL和HEAP混合模式
    # if fields['name'] == 'VM_MEM_HEAP':
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 5
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'VM_STACK_VALIDATE':
    #     fields['tunable'] = False
    #     fields['default'] = '2'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '2'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1,2'
    # if fields['name'] == 'VPD_CAN_CACHE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'XA_COMPATIBLE_MODE':
    #     fields['tunable'] = False
    #     fields['default'] = '0'
    #     fields['minval'] = '0'
    #     fields['maxval'] = '1'
    #     fields['vartype'] = 1
    #     fields['enumvals'] = '0,1'
    # if fields['name'] == 'HLDR_BUF_TOTAL_SIZE':
    #     fields['tunable'] = False
    #     fields['default'] = 4294967294
    #     fields['minval'] = 0
    #     fields['maxval'] = 4294967294
    #     fields['vartype'] = 2
    # if fields['name'] == 'CKPT_DIRTY_PAGES':
    #     fields['default'] = 0
    #     fields['minval'] = 0
    #     fields['maxval'] = 4294967294
    #     fields['vartype'] = 2

    # ====================  产品建议修改参数 ============================#
    if fields['name'] == 'MAX_OS_MEMORY':
        fields['tunable'] = False
        fields['default'] = 100
        fields['minval'] = 100
        fields['maxval'] = 100
        fields['vartype'] = 2
    # 共享内存池大小，以M为单位。共享内存池是由DM管理的内存。有效值范围：32位平台为（64~2000），64位平台为（64~67108864）
    if fields['name'] == 'MEMORY_POOL':
        fields['tunable'] = True
        fields['minval'] = 500
        fields['vartype'] = 2
        fields['resource'] = 1
    if fields['name'] == 'MEMORY_N_POOLS':
        fields['tunable'] = True
        fields['vartype'] = 7
    if fields['name'] == 'MEMORY_EXTENT_SIZE':
        fields['tunable'] = True
        fields['vartype'] = 2
    # 是否开启内存泄漏检测。0：否；1：是，此时系统对每一次内存分配都登记到动态视图V$MEM_REGINFO中， 并在释放时解除登记
    if fields['name'] == 'MEMORY_LEAK_CHECK':
        fields['tunable'] = False
        fields['default'] = '0'
        fields['minval'] = '0'
        fields['maxval'] = '1'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # 系统缓冲区大小
    if fields['name'] == 'BUFFER':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 1
    if fields['name'] == 'BUFFER_POOLS':
        fields['tunable'] = True
        fields['vartype'] = 7
    if fields['name'] == 'FAST_POOL_PAGES':
        fields['tunable'] = True
        fields['vartype'] = 7
    if fields['name'] == 'FAST_ROLL_PAGES':
        fields['tunable'] = True
        fields['vartype'] = 7
    if fields['name'] == 'DICT_BUF_SIZE':
        fields['tunable'] = True
        fields['vartype'] = 2
    # VM是否使用HEAP分配内存。0：MEMORY POOL模式；1：HEAP模式；2：MEMORY POOL和HEAP混合模式
    if fields['name'] == 'VM_MEM_HEAP':
        fields['tunable'] = True
        fields['default'] = '0'
        fields['minval'] = '0'
        fields['maxval'] = '2'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1,2'
    # 是否将相关子查询与外层表优化为CROSS JOIN，0：不优化；1：优化 注：DM早期版本参数，不再推荐使用
    if fields['name'] == 'REFED_SUBQ_CROSS_FLAG':
        fields['tunable'] = True
        fields['default'] = '1'
        fields['minval'] = '0'
        fields['maxval'] = '1'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # 产生多大日志文件后做检查点，以M为单位。有效值范围（0~4294967294）
    if fields['name'] == 'CKPT_RLOG_SIZE':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 3
    if fields['name'] == 'CKPT_DIRTY_PAGES':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 2
    # 指定检查点的时间间隔。以秒为单位，为0时表示不自动定时做检查点。
    if fields['name'] == 'CKPT_INTERVAL':
        fields['tunable'] = True
        fields['maxval'] = 86400
        fields['vartype'] = 2
    # 检查点刷盘比例
    if fields['name'] == 'CKPT_FLUSH_RATE':
        fields['tunable'] = True
        fields['vartype'] = 3
    # 非WINDOWS下有效，表示IO线程组个数。有效值范围（1~512）
    if fields['name'] == 'IO_THR_GROUPS':
        fields['tunable'] = True
        fields['vartype'] = 7
    if fields['name'] == 'MAX_SESSIONS':
        fields['tunable'] = True
        fields['default'] = 10000
        fields['minval'] = 10000
        fields['maxval'] = 65000
        fields['vartype'] = 2
    if fields['name'] == 'MAX_SESSION_STATEMENT':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['minval'] = 2000
    # BDTA缓存的记录数。有效值范围（1~10000）
    if fields['name'] == 'BDTA_SIZE':
        fields['tunable'] = True
        fields['minval'] = 1000
        fields['vartype'] = 2
    # HASH JOIN操作时，HASH表大小，以CELL个数为单位。
    if fields['name'] == 'JOIN_HASH_SIZE':
        fields['tunable'] = True
        fields['minval'] = 5000
        fields['maxval'] = 500000
        fields['vartype'] = 2
    # 服务器日志是否记录通信中产生的警告信息。0：不记录；1：记录
    if fields['name'] == 'COMM_TRACE':
        fields['tunable'] = True
        fields['default'] = '0'
        fields['minval'] = '0'
        fields['maxval'] = '1'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # SQL缓冲池大小，以M为单位。有效值范围：32位平台下为（1~2048）；64位平台下为（1~67108864）。单位：MB
    if fields['name'] == 'CACHE_POOL_SIZE':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 1
    # # 控制连接的实现方式。0：优化器根据代价情况自由选择连接方式；1：考虑使用NEST LOOP INNER JOIN；2：考虑使用索引连接；4：考虑使用哈希连接；8：考虑使用归并连接
    if fields['name'] == 'PHC_MODE_ENFORCE':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15'
    # 当对派生视图进行分组查询，且分组项是派生视图分组项的子集时，是否考虑将两层分组进行合并。0：不优化；1：将两层分组进行合并
    if fields['name'] == 'OPTIMIZER_AGGR_GROUPBY_ELIM':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # 是否允许IN LIST表达式优化
    if fields['name'] == 'ENABLE_IN_VALUE_LIST_OPT':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1,2,4,8,3,5,9,6,10,12,7,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31'
    # 非等值布尔表达式和外连接ON条件中的传递闭包
    if fields['name'] == 'ENHANCED_BEXP_TRANS_GEN':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1,2,3'
    if fields['name'] == 'ENABLE_SPACELIMIT_CHECK':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # 2^14=16384 单个日志缓冲区大小（以日志页个数为单位），取值只能为2的次幂值，最小值为1，最大值为20480
    if fields['name'] == 'RLOG_BUF_SIZE':
        fields['tunable'] = True
        # fields['default'] = '8192'
        # fields['minval'] = None
        # fields['maxval'] = None
        fields['vartype'] = 7
        # fields['enumvals'] = '1024,8192,16384'
    if fields['name'] == 'RLOG_POOL_SIZE':
        fields['tunable'] = True
        fields['minval'] = None
        fields['maxval'] = None
        fields['vartype'] = 5
        fields['enumvals'] = '256,512,1024,2048,4096'
    if fields['name'] == 'RLOG_PARALLEL_ENABLE':
        fields['tunable'] = True
        fields['default'] = '0'
        fields['minval'] = '0'
        fields['maxval'] = '1'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # 是否启用快速释放S锁，1：启用；0：不启用
    if fields['name'] == 'FAST_RELEASE_SLOCK':
        fields['tunable'] = True
        fields['default'] = '1'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    if fields['name'] == 'SESS_CHECK_INTERVAL':
        fields['tunable'] = True
        fields['vartype'] = 2
    # 插入数据时，如果和未提交数据有UNIQUE约束的冲突，是否等待未提交事务结束，0：等待，直至未提交事务结束；1：不等待，立即返回错误
    if fields['name'] == 'NOWAIT_WHEN_UNIQUE_CONFLICT':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    if fields['name'] == 'UNDO_EXTENT_NUM':
        fields['tunable'] = True
        fields['default'] = 4
        fields['vartype'] = 2
        fields['resource'] = 2
    # 事务提交后回滚页保持时间，单位为秒。有效值范围（0~ 86400） 注：类型为DOUBLE，可支持毫秒
    if fields['name'] == 'UNDO_RETENTION':
        fields['tunable'] = True
        fields['maxval'] = 90.00
        fields['vartype'] = 3
    # 与客户端的通信消息是否压缩，0：不压缩；1：压缩；2：系统自动决定每条消息是否压缩
    if fields['name'] == 'MSG_COMPRESS_TYPE':
        fields['tunable'] = True
        fields['vartype'] = 7
    # 是否对消息进行校验。0：不检验；1：检验
    if fields['name'] == 'COMM_VALIDATE':
        fields['tunable'] = True
        fields['default'] = '1'
        fields['minval'] = '0'
        fields['maxval'] = '1'
        fields['vartype'] = 5
        fields['enumvals'] = '0,1'
    # 指定FAST_POOL的管理方式
    if fields['name'] == 'ENABLE_FREQROOTS':
        fields['tunable'] = True
        fields['vartype'] = 5
        fields['enumvals'] = '0,1,2,3'

    # 所有跟DFS相关的参数全部不加入调优列表
    if fields['name'].startswith("DFS_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 所有跟DSC相关的参数全部不加入调优列表
    if fields['name'].startswith("DSC_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 所有跟DW相关的参数全部不加入调优列表
    if fields['name'].startswith("DW_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 所有跟MPP相关的参数全部不加入调优列表
    if fields['name'].startswith("MPP_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 所有跟RAC相关的参数全部不加入调优列表
    if fields['name'].startswith("RAC_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 所有外置参数全部不加入调优列表
    if fields['name'].startswith("EXTERNAL_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 和邮箱相关的参数全部不加入调优列表
    if fields['name'].startswith("MAIL_") or fields['name'].startswith("MAL_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    # 批量提交事务的个数，有效值范围（0~100）
    if fields['name'] == "FAST_COMMIT":
        fields['tunable'] = False
        fields['vartype'] = 1
    if fields['name'] == "COMMIT_WRITE":
        fields['tunable'] = False
        fields['vartype'] = 5
        fields['enumvals'] = 'wait,nowait,immediate,batch'
    # 控制节点启动状态
    if fields['name'] == "MASTER_STARTUP_STATUS":
        fields['tunable'] = False
        fields['vartype'] = 1
    # 允许SSL连接的最低版本
    if fields['name'] == "MIN_SSL_VERSION":
        fields['tunable'] = False
        fields['vartype'] = 1
    if fields['name'] == "PORT_NUM":
        fields['tunable'] = False
        fields['vartype'] = 1
    # COLDATA池的大小，以M为单位
    if fields['name'] == "COLDATA_POOL_SIZE":
        fields['tunable'] = False
        fields['vartype'] = 1
    # MONITOR监控参数全部不加入调优列表
    if "MONITOR" in fields['name']:
        fields['tunable'] = False
        fields['vartype'] = 1
    # 和密码设置相关的参数全部不加入调优列表
    if "PWD" in fields['name']:
        fields['tunable'] = False
        fields['vartype'] = 1
    # 全局设置参数为系统初始设定，不加入调优列表
    if "GLOBAL_" in fields['name']:
        fields['tunable'] = False
        fields['vartype'] = 1
    if fields['name'].startswith("CPU_"):
        fields['tunable'] = False
        fields['vartype'] = 1
    if re.match(r'BASE_(.*)_CPU', fields['name'], re.M | re.I):
        fields['tunable'] = False
        fields['vartype'] = 1

    # ==================内存参数==================#
    if fields['name'] == 'MAX_BUFFER':
        fields['resource'] = 1
    # HUGE表使用的缓冲区大小
    if fields['name'] == 'HUGE_BUFFER':
        fields['resource'] = 1
    # RECYCLE缓冲区大小
    if fields['name'] == 'RECYCLE':
        fields['resource'] = 1
    # KEEP缓冲区大小
    if fields['name'] == 'KEEP':
        fields['resource'] = 1
    # 共享内存池在扩充到此大小以上后，空闲时收缩回此指定大小，以M为单位
    if fields['name'] == 'MEMORY_TARGET':
        fields['resource'] = 1
    # 会话缓冲区大小
    if fields['name'] == 'SESS_POOL_SIZE':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 1
    # 会话缓冲区能扩充到的最大大小，以KB为单位，有效值范围（0~10*1024*1024），0表示不限制
    if fields['name'] == 'SESS_POOL_TARGET':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 1
        # 系统执行时虚拟机内存池大小，在执行过程中用到的内存大部分是从这里申请的，它的空间是从操作系统中直接申请的，有效值范围（32~1024*1024）
    if fields['name'] == 'VM_POOL_SIZE':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 1
    # 虚拟机内存池能扩充到的最大大小，以KB为单位，有效值范围（0~10*1024*1024），0表示不限制
    if fields['name'] == 'VM_POOL_TARGET':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 1

    # ==================CPU参数==================#
    # 工作线程的数目，有效值范围（1~64）
    if fields['name'] == 'WORKER_THREADS':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 2
    # 任务线程个数，有效值范围（1~1000）
    if fields['name'] == 'TASK_THREADS':
        fields['tunable'] = True
        fields['vartype'] = 2
        fields['resource'] = 2
    if fields['name'] == 'GLOBAL_CPU_N':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'SCAN_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'SEEK_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'LKUP_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'NLIJ_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'HI_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'HI_SEARCH_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'MI_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'NL_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'FLT_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'LARGE_SORT_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'SMALL_SORT_CPU':
        fields['resource'] = 2
        fields['vartype'] = 2
    if fields['name'] == 'GLOBAL_CPU_N':
        fields['resource'] = 2
        fields['vartype'] = 2

    # ==================存储参数==================#
    # 磁盘可用空间的报警阀值，单位为兆，有效值范围（50~50000）
    if fields['name'] == 'IDLE_DISK_THRESHOLD':
        fields['resource'] = 3
    # 临时表空间大小上限，以M为单位。0表示不限制临时表空间大小。 有效范围（0~ 4294967294）。 注：TEMP_SPACE_LIMIT一定要大于等于 TEMP_SIZE
    if fields['name'] == 'TEMP_SPACE_LIMIT':
        fields['resource'] = 3
    # 默认创建的临时表空间大小，以M为单位。有效值范围（10~1048576）
    if fields['name'] == 'TEMP_SIZE':
        fields['tunable'] = True
        fields['resource'] = 3
    # 审计文件总存储空间大小限制，以M为单位。有效值范围（0~4294967294），0表示不限制
    if fields['name'] == 'AUDIT_SPACE_LIMIT':
        fields['resource'] = 3
    if fields['name'] == 'CKPT_DIRTY_PAGES':
        fields['resource'] = 3


COLNAMES = ("PARA_NAME", "PARA_VALUE", "DEFAULT_VALUE", "MIN_VALUE", "MAX_VALUE", "DESCRIPTION")


def process_version(version, delim=','):
    fields_list = []
    with open('dm{}.csv'.format(version), 'r', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter=delim)
        header = [h for h in next(reader)]
        idxs = [header.index(c) for c in COLNAMES]
        ncols = len(header)

        ri = 0
        for row in reader:
            assert ncols == len(row), (ri, ncols, len(row))
            fields = {}
            for i, cname in zip(idxs, COLNAMES):
                value = row[i]
                if isinstance(value, str):
                    value = value.strip()
                if cname == 'PARA_NAME':
                    fields['name'] = value.upper()
                elif cname == 'DEFAULT_VALUE':
                    fields['default'] = value
                elif cname == 'MIN_VALUE':
                    fields['minval'] = value
                elif cname == 'MAX_VALUE':
                    if value == "NULL":
                        fields['vartype'] = 1  # STRING
                    else:
                        # intValue = int(value)
                        # if intValue in (3,6):
                        fields['vartype'] = 2  # Integer
                        # else:
                        #     fields['vartype'] = 1  # Assume it's a sting otherwise
                    fields['maxval'] = value
                else:
                    fields['summary'] = value

                fields.update(
                    scope='global',
                    dbms=20,
                    category='',
                    enumvals=None,
                    context='',
                    unit=3,  # Other
                    # tunable=True,
                    tunable=False,
                    # description='',
                    # minval=None,
                    # maxval=None,
                )

            set_field(fields)
            # fields['name'] = ('global.' + fields['name'])
            fields['name'] = ('global.' + fields['name'])
            if fields['default'] != "NULL":
                fields_list.append(fields)
                ri += 1

    fields_list = sorted(fields_list, key=itemgetter('name'))
    final_metrics = [dict(model='website.KnobCatalog', fields=fs) for fs in fields_list]
    filename = 'dm-{}_knobs.json'.format(version)
    with open(filename, 'w') as f:
        json.dump(final_metrics, f, indent=4)
    shutil.copy(filename, "../../../../website/fixtures/{}".format(filename))


def main():
    process_version(8)  # dm8
    # process_version(121,delim='|')  # v12.1c


if __name__ == '__main__':
    main()
