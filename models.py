from main import db
from  sqlalchemy import  Sequence
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer,Sequence('user_id_seq'),primary_key=True)
    first_name = db.Column(db.String(64), index=True,nullable=False)
    last_name =  db.Column(db.String(64), index=True,nullable=False)
    email =  db.Column(db.String(128), index=True,unique=True,nullable=False)
    password =  db.Column(db.String(128), index=True,nullable=False)

    tasks = db.relationship("Task", back_populates="user")
    # surveys = db.relationship("Survey", back_populates="user")
    # doSurveys = db.relationship('Survey', secondary='userdosurvey')
    def __repr__(self):
        return  '<User full name {} {} ,email {}>'.format(self.first_name,self.last_name,self.email)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
# class Survey(db.Model):
#     survey_id=db.Column(db.Integer,Sequence('survey_id_seq'),primary_key=True)
#     create_by_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     survey_name=db.Column(db.String(128), index=True,nullable=False)
#     user = db.relationship("User", back_populates="survey")
#     do_survey = db.relationship('User', secondary='userdosurvey')
#     limit_time=survey_name=db.Column(db.Integer, index=True,nullable=False)
#     times_tamp=db.Column(db.DateTime, index=True,nullable=False)
#     coins = db.Column(db.Integer, nullable=False)
#
# class Question(db.Model):
#     question_id=db.Column(db.Integer,Sequence('question_id_seq'),primary_key=True)
#     survey_id=db.Column(db.Integer, db.ForeignKey('survey.survey_id'))
#     question_content=db.Column(db.String(128), index=True,nullable=False)
#     options = db.relationship("Option", back_populates="question")
#
# class Option(db.Model):
#     option_id=db.Column(db.Integer,Sequence('option_id_seq'),primary_key=True)
#     question_id=db.Column(db.Integer, db.ForeignKey('question.question_id'))
#     survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'))
#     option_content=db.Column(db.String(254), index=True,nullable=False)
#     question = db.relationship("Question", back_populates="option")
#
# class UserDoSurvey(db.Model):
#     user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'))
#     question_completed = db.Column(db.Integer,nullable=False)
#
#
#
#
#
class Task(db.Model):
    task_id= db.Column(db.Integer,Sequence('task_id_seq'),primary_key=True)
    description=db.Column(db.String(255),nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user=db.relationship("User", back_populates="tasks")
    priority_id=db.Column(db.Integer, db.ForeignKey('priority.priority_id'))
    priority=db.relationship("Priority", back_populates="tasks")
    is_completed=db.Column(db.Boolean,default=False)
    def __repr__(self):
        return 'Task:{} of user {}'.format(self.description,self.user.last_name)

class Priority(db.Model):
    priority_id= db.Column(db.Integer,Sequence('priority_id_seq'),primary_key=True)
    description=db.Column(db.String(255),nullable=True)
    tasks=db.relationship("Task", back_populates="priority")