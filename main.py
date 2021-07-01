from flask import Flask,render_template,request,flash
from flask_cors import CORS, cross_origin
from data import Data
from flask.globals import session
from modules.login import Login
from  form import SignUpForm,SignInForm,FormTask
from werkzeug.utils import redirect
import  json
from flask_sqlalchemy import SQLAlchemy
from  flask_migrate import Migrate
import os

# pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package_name>
basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS '] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'any string works here'
db=SQLAlchemy(app)
migrate=Migrate(app,db)

import models
@app.route('/')
@cross_origin(origin='*')
def login_process():
    todolist = [
        {
            'name': 'Đi học',
            'description': 'BVU'
        },
        {
            'name': 'Về nhà',
            'description': 'hasagi'
        }
    ]

    return render_template('index.html', todolist=todolist)

@app.route('/add', methods=['POST'])
@cross_origin(origin='*')
def add_process():
    _data = Data()
    _login = Login()
    s = json.loads(_login.log())
    print(s)

    return json.dumps(s)
@app.route('/signUp', methods=['GET' , 'POST'])
@cross_origin(origin='*')
def sign_up():
    form=SignUpForm()
    if form.validate_on_submit():
        _fname = form.inputFirstName.data
        _lname = form.inputLastName.data
        _email = form.inputEmail.data
        _password = form.inputPassword.data
        if (db.session.query(models.User).filter_by(email=_email).count() == 0):
            _user = models.User(first_name=_fname, last_name=_lname, email=_email)
            _user.set_password(_password)
            db.session.add(_user)
            db.session.commit()
            return render_template('signup_success.html', user=_user)
        else:
            flash('Email {} is alrealy exsits!'.format(_email))
            return render_template('signup.html', form=form)

    return render_template('signup.html',form=form)

@app.route('/signIn', methods=['GET', 'POST'])
def SignIn():
    form = SignInForm()
    if form.validate_on_submit():
        _email = form.inputEmail.data
        _password = form.inputPassword.data

        user = db.session.query(models.User).filter_by(email = _email).first()
        if (user is None):
            flash('Sai Email hoặc mật khẩu!')
        else:
            if(user.check_password(_password)):

                session['user'] = user.user_id
                return redirect('/userHome')
            else:
                flash('Sai Email hoặc mật khẩu!')
    return render_template('signin.html', form = form)

@app.route('/addTodo', methods=['GET', 'POST'])
def AddTodo():
    _user_id = session.get('user')
    if _user_id:
        priorytys=models.Priority.query.all()
        priarr=[]
        for pri in priorytys:
            print(pri.description)
            priarr.append((pri.priority_id,pri.description))

        form = FormTask()
        form.inputPriority.choices=priarr
        print(priarr)
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
       
        if form.validate_on_submit():
            id=request.form['taskId']
            des = form.inputTask.data
            print(id,"ne2 id")
            if id=="0":       
                task=models.Task(description=des,user=user,priority_id=form.inputPriority.data)
                db.session.add(task)
                
            else:         
                 task = db.session.query(models.Task).filter_by(task_id = id).first()
                 print(task)
                 task.description= des
                 task.priority_id=form.inputPriority.data
            db.session.commit()
            return redirect('/userHome')
        return render_template('usertodo.html',form = form,user=user)
    return redirect('/')




@app.route('/userHome', methods=['GET', 'POST'])
def userHome():
    print('long ngu')
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()

        return render_template('userhome.html', user = user)
    else:
        return redirect('/')
@app.route('/completeTask', methods=['GET', 'POST'])
def completeTask():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
        id=request.form['taskId']
        task = db.session.query(models.Task).filter_by(task_id = id).first()
        print(task)
        task.is_completed= True
        db.session.commit()
        return render_template('userhome.html', user = user)
    else:
        return redirect('/')

@app.route('/logOut', methods=['GET', 'POST'])
def logOut():
    session.pop('user',None)
    return redirect('/signIn')

@app.route('/deleteTask', methods=['GET', 'POST'])
def deleteTask():
    _user_id = session.get('user')
    if _user_id:
        task_id= request.form['taskId']
        task = db.session.query(models.Task).filter_by(task_id = task_id).first()
        db.session.delete(task)
        db.session.commit()
        return redirect('/userHome')
        
    else:
        return redirect('/')

@app.route('/editTask', methods=['GET', 'POST'])
def editTask():
    _user_id = session.get('user')
    if _user_id:
        user = db.session.query(models.User).filter_by(user_id = _user_id).first()
        priorytys=models.Priority.query.all()
        priarr=[]
        for pri in priorytys:
            print(pri.description)
            priarr.append((pri.priority_id,pri.description))

        form = FormTask()
        form.inputPriority.choices=priarr

        task_id= request.form['taskId']
        task = db.session.query(models.Task).filter_by(task_id = task_id).first()
        form.inputPriority.default=task.priority_id
        form.inputTask.default=task.description
        form.process()
        return render_template('usertodo.html', form = form,user=user,task=task)
        
    else:
        return redirect('/')


@app.route('/auth', methods=['POST'])
@cross_origin(origin='http://localhost:3000')
def Auth():
    data = request.get_json()
    print(request.get_json())
    print("data Request:", data['email'])


    user = db.session.query(models.User).filter_by(email=data['email']).first()
    if (user is None):
        return json.dumps([{"message":"none"}])
    else:
        if (user.check_password(data["password"])):

            session['user'] = user.user_id
            s={"email" : user.email,"password" : user.password}
            print("ok")

            return json.dumps(s)
        else:
            return json.dumps([{"message":"sai email hoặc mật khẩu"}])

    return "s"

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='3333')




