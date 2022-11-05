from core import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# sqlalchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

# models
class QuizGradesModel(db.Model):
    __tablename__ = 'mdl_quiz_grades'
    id = db.Column(db.Integer, primary_key=True)
    quiz = db.Column(db.Integer)
    userid = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    timemodified = db.Column(db.Integer)

    def __init__(self, quiz, userid, grade, timemodified):
        self.quiz = quiz
        self.userid = userid
        self.grade = grade
        self.timemodified = timemodified

    def json(self):
        return {"quiz":self.quiz, 
                "userid":self.userid, 
                "grade":self.grade, 
                "timemodified":self.timemodified}

# JSON Schema
class QuizGradesSchema(ma.Schema):
    class Meta:
        fields = ('quiz','userid','grade','timemodified')

quiz_grade_schema = QuizGradesSchema()
quiz_grade_schemas = QuizGradesSchema(many=True)
