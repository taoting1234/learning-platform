# 定义数据库信息
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://learning_platform:LEARNING123platform" \
                          "@newitd-w.mysql.rds.aliyuncs.com:3306/learning-platform" \
                          "?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = 'aabbcc'
