# qa.py
# 问答相关
from flask import Blueprint

bp = Blueprint("qa", __name__, url_prefix="/")	# 首页，所以这里直接用根路径

# http://127.0.0.1:5000
@bp.route("/")
def index():
    pass