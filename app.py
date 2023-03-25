from flask import Flask
import config
from exts import db, mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

# 绑定db，init_app()这个方法，可以不在创建时绑定，而是先创建，后续再绑定
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
