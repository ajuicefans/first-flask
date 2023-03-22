
# 数据库配置信息
# MySQL所在的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号，默认3306
PORT = '3306'
# 连接MySQL的用户名，用户用自己设置的
USERNAME = "root"
# 连接MySQL的密码，用户自己设置的
PASSWORD = "root"
# MySQL上创建的数据库名称
DATABASE = "juice_qa"

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

