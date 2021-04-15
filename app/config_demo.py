# 定义数据库信息
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1:3306/learning-platform?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 跨域设置
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "none"

# 定义flask信息
SECRET_KEY = "123456"

# 定义文件存放位置
FILE_DIRECTORY = "./file"
