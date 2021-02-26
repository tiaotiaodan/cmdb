from flask import Flask
from flask import render_template       # 指定模板文件
from flask import request
from  views import  views
from  servers import  servers
from auth import  auth
from flask import redirect
from  flask import session
import datetime

app = Flask(__name__)
app.config['SECRET_KEY']='test123'
app.permanent_session_lifetime = datetime.timedelta(minutes=1440)
app.register_blueprint(views, url_prefix="/views")
app.register_blueprint(servers, url_prefix="/servers")
app.register_blueprint(auth, url_prefix="/auth")

# 判断所有页面是否有cookie，没有返回到 /目录
@app.before_request
def before_request():
    if request.path == "/" or request.path == '/auth/login'  or request.path.endswith(".js") or request.path.endswith(".css") or request.path.endswith(".jpg"):
        pass
    else:
        username = session.get("username")
        if not username:
            return redirect("/")

# 设置login登陆页面，为 /目录
@app.route('/')
def index():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)



