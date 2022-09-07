import copy
import json
import os

from server.website.website.types import \
    VarType  # pylint: disable=import-error,wrong-import-position,line-too-long  # noqa: E402

DM_DEINFED_METRICS = {
    "throughput": {
        "unit": "transaction / second",
        "short_unit": "txn/s",
        "type": VarType.REAL
    },
}


def get_udm(dconf):
    summary_path = os.path.join(dconf.SYSBENCH_HOME, "results", dconf.UPLOAD_CODE + "_outputfile.summary")
    with open(summary_path, 'r') as f:
        info = json.load(f)
    metrics = copy.deepcopy(DM_DEINFED_METRICS)
    metrics["throughput"]["value"] = info["tps"]
    return metrics


def add_udm(conf):
    """
    写自定义metrics文件
    :param conf:
    :return:
    """
    metrics = get_udm(conf)
    result_dir = os.path.join(conf.CONTROLLER_HOME, 'output', conf.UPLOAD_CODE)
    path = os.path.join(result_dir, 'user_defined_metrics.json')
    with open(path, 'w') as f:
        json.dump(metrics, f, indent=4)
