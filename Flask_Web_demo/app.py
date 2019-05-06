#encoding:utf-8
from flask import Flask,session
from flask import render_template
from flask import request
from exts import db
import config
from models import User,Question
from flask import redirect,url_for
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    content={
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**content)
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        user=User.query.filter(User.telephone==telephone,User.password==password).first()
        if user:
            session['user_id']=user.id
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，请确认后在登录'
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter(User.telephone==telephone).first()
        if user:
            return u"该手机号码已被注册"
        else:
            if password1==password2:
                user=User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            return{'user':user}
    else:
        return{}

@app.route('/question/',methods=['GET',"POST"])
@login_required
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        question=Question(title=title,content=content)
        user_id=session.get('user_id')
        user=User.query.filter(User.id==user_id).first()
        question.author=user
        db.session.add(question)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
