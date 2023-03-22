# 授权相关
from flask import Blueprint
# 相当于是flask的子模块

'''
    name = "auth"
    __name__ 代表当前这个模块 （固定的写法）
    url_prefix：URL前缀
        例如：访问login这个适度函数的时候："/auth/login"
'''
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login")
def login():
    pass