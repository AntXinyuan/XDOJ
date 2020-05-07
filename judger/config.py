from XDOJ import settings

# 开启评测线程数目
count_thread = settings.JUDGER_THREAD_COUNT
db_setting = settings.DATABASES['default']
# 数据库地址
db_host = db_setting['HOST']
# 数据库用户名
db_user = db_setting['USER']
# 数据库密码
db_password = db_setting['PASSWORD']
# 数据库名字
db_name = db_setting['NAME']
# 数据库编码
db_charset = "utf8"
# work评判目录
work_dir = settings.JUDGE_ROOT
# data测试数据目录
data_dir = settings.TEST_CASE_ROOT
# 自动清理评work目录
auto_clean = True

python_exe_name = '__pycache__/main.cpython-36.pyc'
