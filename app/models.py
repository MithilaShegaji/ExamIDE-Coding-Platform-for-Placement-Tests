# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from . import db, login_manager

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(256))
#     role = db.Column(db.String(10), index=True, default='student') # 'admin' or 'student'

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return f'<User {self.username}>'

# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# class Test(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     duration_minutes = db.Column(db.Integer, nullable=False)
    
#     # Relationships
#     mcq_questions = db.relationship('MCQQuestion', backref='test', lazy='dynamic')
#     coding_questions = db.relationship('CodingQuestion', backref='test', lazy='dynamic')

# class MCQQuestion(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question_text = db.Column(db.String(500), nullable=False)
#     option_a = db.Column(db.String(200))
#     option_b = db.Column(db.String(200))
#     option_c = db.Column(db.String(200))
#     option_d = db.Column(db.String(200))
#     correct_option = db.Column(db.String(1), nullable=False) # 'A', 'B', 'C', or 'D'
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

# class CodingQuestion(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     problem_statement = db.Column(db.Text, nullable=False)
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
#     test_cases = db.relationship('TestCase', backref='coding_question', lazy='dynamic')

# class TestCase(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     input = db.Column(db.Text)
#     expected_output = db.Column(db.Text)
#     is_hidden = db.Column(db.Boolean, default=True)
#     question_id = db.Column(db.Integer, db.ForeignKey('coding_question.id'))


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(10), index=True, default='student') # 'admin' or 'student'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    
    mcq_questions = db.relationship('MCQQuestion', backref='test', lazy='dynamic', cascade="all, delete-orphan")
    coding_questions = db.relationship('CodingQuestion', backref='test', lazy='dynamic', cascade="all, delete-orphan")

class MCQOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(300), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('mcq_question.id'), nullable=False)

class MCQQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    marks = db.Column(db.Integer, nullable=False, default=1)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    
    options = db.relationship(
        'MCQOption', 
        foreign_keys=[MCQOption.question_id], 
        backref='question', 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    correct_option_id = db.Column(db.Integer, db.ForeignKey('mcq_option.id', use_alter=True, name='fk_correct_option_id'))
    correct_option = db.relationship('MCQOption', foreign_keys=[correct_option_id])


class CodingQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_statement = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, nullable=False, default=10)
    difficulty = db.Column(db.String(20), nullable=False, default='Medium')
    
    
    # Starter code for multiple languages
    starter_code_python = db.Column(db.Text)
    starter_code_java = db.Column(db.Text)
    starter_code_cpp = db.Column(db.Text)
    starter_code_c = db.Column(db.Text)
    starter_code_javascript = db.Column(db.Text)

    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    test_cases = db.relationship('TestCase', backref='coding_question', lazy='dynamic', cascade="all, delete-orphan")

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input = db.Column(db.Text)
    expected_output = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=True)
    question_id = db.Column(db.Integer, db.ForeignKey('coding_question.id'), nullable=False)