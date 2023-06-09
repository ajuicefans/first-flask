# 授权相关
from flask import Blueprint, render_template
# 相当于是flask的子模块
from exts import mail
from flask_mail import Message

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

@bp.route("/register")
def register():
    return render_template("register.html")

# @bp.route("/mail/test")
# def mail_test():
#     message = Message(subject="邮箱测试", recipients=["xxx@qq.com"], body="mail test")
#     mail.send(message)
#     return "邮件发送成功！"