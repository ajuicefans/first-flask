# 我的第一个Flask项目：问答系统

> 视频地址：[Flask入门](https://www.bilibili.com/video/BV17r4y1y7jJ/?vd_source=f111e229e8ddffc692d57d989194e313)



## 19 项目框架搭建

flask灵活，django开发流程固定

框架如下：

- 问答相关：qa.py
- 授权相关：auth.py
- 配置相关：config.py
- 第三方插件：exts.py
- 模型：models.py
- 汇总：app.py

----

### config.py：配置相关

```python
# app.py
# 在app.py中导入config，跟Flask对象进行绑定
import config

# 绑定配置文件
app.config.from_object(config)
# app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
```

### exts.py：扩展文件👉为了解决循环引用的问题

```python
# flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# 加入到app.py中：db.init_app(app)
```

解决循环引用问题：

<img src="F:/lifeProject/first-flask/images/1.png" alt="1" style="zoom: 50%;" />

### models.py：模型

### blueprint（蓝图）：用来做模块化

> 豆瓣：电影、读书、音乐...
>
> 和啥相关，对应适度函数就放在哪

```python
# auth.py
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

# 要访问 "/auth/login" 才能访问到
@bp.route("/login")
def login():
    pass
```

```python
# qa.py
# 问答相关
from flask import Blueprint

bp = Blueprint("qa", __name__, url_prefix="/")	# 首页，所以这里直接用根路径

# http://127.0.0.1:5000
@bp.route("/")
def index():
    pass
```

加入到app.py中

---

### app.py

```python
from flask import Flask
import config
from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

# 绑定db，init_app()这个方法，可以不在创建时绑定，而是先创建，后续再绑定
db.init_app(app)

# 迁移3步曲之前要做的
migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
```



---

>  [Python注释（多行注释和单行注释）用法详解](https://blog.csdn.net/zihong523/article/details/118896082?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522167947600116800222851562%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=167947600116800222851562&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-2-118896082-null-null.142^v76^insert_down2,201^v4^add_ask,239^v2^insert_chatgpt&utm_term=python%E5%A4%9A%E8%A1%8C%E6%B3%A8%E9%87%8A&spm=1018.2226.3001.4187)

----



## 20 User模型创建

配置user模型，要先连接数据库

这里先创建一下数据库👉Navicat

<img src="F:/lifeProject/first-flask/images/2.png" alt="2" style="zoom:67%;" />

config.py

```python
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
```



models.py

```python
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

# migrate = Migrate(app, db) 加在app.py中
```

迁移三部曲

执行后生成migrations文件夹 和 数据库对应的表

```
flask db init 		# 只需要执行一次
flask db migrate
flask db upgrade
```

![3](F:/lifeProject/first-flask/images/3.png)

---



## 21 注册页面模板渲染

此处前端的代码直接用的现成的，如下图，复制粘贴好后

![4](F:/lifeProject/first-flask/images/4.png)

这里创建了一个base.html文件，**作为各页面的父模板**

```html
<!--base.html文件-->

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../static/bootstrap/bootstrap.4.6.min.css">
    <!--<link rel="stylesheet" href="{{ url_for('static', filename='bootstrap/bootstrap.4.6.min.css')}}"> #}-->
    <link rel="stylesheet" href="../static/css/init.css">
    <!--<link rel="stylesheet" href="{{ url_for('static', filename='css/init.css')}}">-->

    {% block head %}{% endblock %}
    <title>{% block title %}{% endblock %}</title>
</head>

<body>
{#保留不动#}
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="#">Juice问答</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="/">首页 <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">发布问答</a>
                    </li>
                    <li class="nav-item ml-2">
                        <form class="form-inline my-2 my-lg-0" method="GET" action="#">
                            <input class="form-control mr-sm-2" type="search" placeholder="关键字" aria-label="Search" name="q">
                            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">搜索</button>
                        </form>
                    </li>
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="#">登录</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">注册</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% block body %}{% endblock %}
    </div>
</body>
```

此时，register.html文件如下，`title、head、body`继承自base.html

```html
<!--register.html-->
{% extends "base.html" %}

{% block title %}Juice问答-注册{% endblock %}

{% block head %}{% endblock %}

{% block body %}
    <div class="row mt-4">
            <div class="col"></div>
            <div class="col">
                <form method="POST" action="#">
                    <div class="form-group">
                        <label for="exampleInputEmail1">邮箱</label>
                        <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" name="email">
                        <small id="emailHelp" class="form-text text-muted">我们不会把邮箱用于其他用户</small>
                    </div>
                    <div class="form-group">
                        <label for="exampleInputEmail1">验证码</label>
                        <div class="input-group">
                            <input type="text" class="form-control" name="captcha">
                            <div class="input-group-append">
                                <button class="btn btn-outline-secondary" type="button" id="captcha-btn">获取验证码</button>
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="exampleInputEmail1">用户名</label>
                        <input type="text" class="form-control" name="username">
                    </div>
                    <div class="form-group">
                        <label for="exampleInputPassword1">密码</label>
                        <input type="password" class="form-control" id="exampleInputPassword1" name="password">
                    </div>
                    <div class="form-group">
                        <label for="exampleInputPassword1">确认密码</label>
                        <input type="password" class="form-control" name="password_confirm">
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">立即注册</button>
                </form>
            </div>
            <div class="col"></div>
        </div>
{% endblock %}
```

---



## 22 Flask发送邮件功能实现

注册功能的第一步，就是给用户输入的邮箱发送验证码，

在Flask中发送邮件非常简单，总共分为三步：①安装 `Flask-Mail` ；②配置邮箱参数；③发送邮件

---

在终端 安装 `Flask-Mail` 第三方库

```
pip install flask-mail
```



