import importlib
import shutil

shutil.copy2('client/driver/conf/driver_config_template.py', 'client/driver/conf/111-driver_config.py')

path = 'client.driver.conf.111-driver_config'
module = importlib.import_module(path)
# 执行脚本功能
# func = module.poc('')


print(module.__name__)
# 获取脚本描述信息
print(module.DRIVER_HOME)

module.DRIVER_HOME = 'test'

print(module.DRIVER_HOME)

