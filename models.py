from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"

    # id 整型，主键，自增
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username 长度不超过100个字符，非空
    username = db.Column(db.String(100), nullable=False)
    # password 长度不超过100个字符，非空
    password = db.Column(db.String(100), nullable=False)
    # email 长度不超过100个字符，非空，唯一
    email = db.Column(db.String(100), nullable=False, unique=True)
    # join_time default=datatime.now 这里是调用函数，不是返回值，所以不加圆括号
    join_time = db.Column(db.DateTime, default=datetime.now)