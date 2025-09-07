# from flask import Blueprint, render_template, redirect, url_for, flash, request
# from flask_login import login_user, logout_user, current_user, login_required
# from functools import wraps
# from . import db
# from .models import User, Test, MCQQuestion, CodingQuestion, TestCase
# from .forms import LoginForm, RegistrationForm, TestForm, MCQQuestionForm, CodingQuestionForm

# main = Blueprint('main', __name__)

# # Custom decorator to check for admin role
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.role != 'admin':
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('main.index'))
#         return f(*args, **kwargs)
#     return decorated_function

# @main.route('/')
# def index():
#     # Later, this will be the student dashboard or a landing page
#     if current_user.is_authenticated and current_user.role == 'admin':
#         return redirect(url_for('main.admin_dashboard'))
#     return render_template('index.html')

# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid email or password', 'danger')
#             return redirect(url_for('main.login'))
#         login_user(user)
#         flash('Logged in successfully.', 'success')
#         if user.role == 'admin':
#             return redirect(url_for('main.admin_dashboard'))
#         return redirect(url_for('main.index'))
#     return render_template('login.html', form=form)

# @main.route('/register', methods=['GET', 'POST'])
# def register():
#     # This route can be restricted later so only admins can create users
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         # Make the first registered user an admin
#         role = 'admin' if not User.query.first() else 'student'
#         user = User(username=form.username.data, email=form.email.data, role=role)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!', 'success')
#         return redirect(url_for('main.login'))
#     return render_template('register.html', form=form)

# @main.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('main.index'))

# # --- Admin Routes ---

# @main.route('/admin/dashboard')
# @login_required
# @admin_required
# def admin_dashboard():
#     tests = Test.query.order_by(Test.id.desc()).all()
#     return render_template('admin/dashboard.html', tests=tests)

# @main.route('/admin/test/new', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def create_test():
#     form = TestForm()
#     if form.validate_on_submit():
#         test = Test(name=form.name.data, duration_minutes=form.duration_minutes.data)
#         db.session.add(test)
#         db.session.commit()
#         flash('Test created successfully!', 'success')
#         return redirect(url_for('main.view_test', test_id=test.id))
#     return render_template('admin/create_test.html', form=form)

# @main.route('/admin/test/<int:test_id>')
# @login_required
# @admin_required
# def view_test(test_id):
#     test = Test.query.get_or_404(test_id)
#     return render_template('admin/view_test.html', test=test)

# @main.route('/admin/test/<int:test_id>/add-mcq', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def add_mcq_question(test_id):
#     test = Test.query.get_or_404(test_id)
#     form = MCQQuestionForm()
#     if form.validate_on_submit():
#         question = MCQQuestion(
#             test_id=test.id,
#             question_text=form.question_text.data,
#             option_a=form.option_a.data,
#             option_b=form.option_b.data,
#             option_c=form.option_c.data,
#             option_d=form.option_d.data,
#             correct_option=form.correct_option.data
#         )
#         db.session.add(question)
#         db.session.commit()
#         flash('MCQ question added!', 'success')
#         return redirect(url_for('main.view_test', test_id=test.id))
#     return render_template('admin/add_mcq_question.html', form=form, test=test)

# @main.route('/admin/test/<int:test_id>/add-coding', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def add_coding_question(test_id):
#     test = Test.query.get_or_404(test_id)
#     form = CodingQuestionForm()
#     if form.validate_on_submit():
#         coding_question = CodingQuestion(
#             problem_statement=form.problem_statement.data,
#             test_id=test.id
#         )
#         db.session.add(coding_question)
#         db.session.commit() # Commit to get the ID for the test cases

#         for tc_form in form.test_cases:
#             test_case = TestCase(
#                 input=tc_form.input.data,
#                 expected_output=tc_form.expected_output.data,
#                 question_id=coding_question.id
#             )
#             db.session.add(test_case)
        
#         db.session.commit()
#         flash('Coding question and test cases added!', 'success')
#         return redirect(url_for('main.view_test', test_id=test.id))
#     return render_template('admin/add_coding_question.html', form=form, test=test)



from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
from . import db
from .models import User, Test, MCQQuestion, CodingQuestion, TestCase, MCQOption
from .forms import LoginForm, RegistrationForm, TestForm, MCQQuestionForm, CodingQuestionForm

main = Blueprint('main', __name__)

# Custom decorator to check for admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('main.admin_dashboard') if user.role == 'admin' else url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        role = 'admin' if not User.query.first() else 'student'
        user = User(username=form.username.data, email=form.email.data, role=role)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# --- Admin Routes ---

@main.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    tests = Test.query.order_by(Test.id.desc()).all()
    return render_template('admin/dashboard.html', tests=tests)

@main.route('/admin/test/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create_test():
    form = TestForm()
    if form.validate_on_submit():
        test = Test(name=form.name.data, duration_minutes=form.duration_minutes.data)
        db.session.add(test)
        db.session.commit()
        flash('Test created successfully!', 'success')
        return redirect(url_for('main.view_test', test_id=test.id))
    return render_template('admin/create_test.html', form=form)

@main.route('/admin/test/<int:test_id>')
@login_required
@admin_required
def view_test(test_id):
    test = Test.query.get_or_404(test_id)
    return render_template('admin/view_test.html', test=test)


# In app/routes.py

@main.route('/admin/test/<int:test_id>/add-mcq', methods=['GET', 'POST'])
@login_required
@admin_required
def add_mcq_question(test_id):
    test = Test.query.get_or_404(test_id)
    
    # ==================================================================
    # THE FIX: Instantiate the form WITH the request data on POST.
    # This populates form.options immediately.
    # On a GET request, request.form is empty, so this is safe.
    # ==================================================================
    form = MCQQuestionForm(request.form)
    # ==================================================================

    # If this is a brand new form (a GET request), pre-populate it
    # with 2 blank option fields for the user to start with.
    if request.method == 'GET':
        form.options.append_entry()
        form.options.append_entry()

    # Now, set the choices for the RadioField. This works because on a POST,
    # form.options is already populated thanks to the change above.
    form.correct_option.choices = [
        (i, f'Option {i+1}') for i in range(len(form.options.entries))
    ]

    # Use validate_on_submit() for validation, but not population (which is already done).
    if form.validate_on_submit():
        question = MCQQuestion(
            test_id=test.id,
            question_text=form.question_text.data,
            marks=form.marks.data
        )
        
        db.session.add(question)
        
        options = []
        for option_form in form.options:
            option = MCQOption(option_text=option_form.option_text.data, question=question)
            options.append(option)
            db.session.add(option)
        
        db.session.flush()

        correct_option_index = form.correct_option.data
        if 0 <= correct_option_index < len(options):
            question.correct_option_id = options[correct_option_index].id
        else:
            flash('Invalid correct option selected.', 'danger')
            db.session.rollback()
            return render_template('admin/add_mcq_question.html', form=form, test=test)
        
        db.session.commit()
        flash('MCQ question added!', 'success')
        return redirect(url_for('main.view_test', test_id=test.id))
    
    elif request.method == 'POST':
        # If validation fails, flash the specific errors.
        for field, errors in form.errors.items():
            if field == 'correct_option':
                 flash("Error: You must select one of the options as the correct answer.", 'danger')
            elif field == 'options':
                for i, option_errors in enumerate(errors):
                    for sub_field, sub_errors in option_errors.items():
                        flash(f"Error in Option {i+1}: {' '.join(sub_errors)}", 'danger')
            else:
                 flash(f"Error in {getattr(form, field).label.text}: {' '.join(errors)}", 'danger')
        
    return render_template('admin/add_mcq_question.html', form=form, test=test)

@main.route('/admin/test/<int:test_id>/add-coding', methods=['GET', 'POST'])
@login_required
@admin_required
def add_coding_question(test_id):
    test = Test.query.get_or_404(test_id)
    form = CodingQuestionForm()
    if form.validate_on_submit():
        coding_question = CodingQuestion(
            problem_statement=form.problem_statement.data,
            marks=form.marks.data,
            difficulty=form.difficulty.data,
            starter_code_python=form.starter_code_python.data,
            starter_code_java=form.starter_code_java.data,
            starter_code_cpp=form.starter_code_cpp.data,
            starter_code_c=form.starter_code_c.data,
            starter_code_javascript=form.starter_code_javascript.data,
            test_id=test.id
        )
        db.session.add(coding_question)
        
        # Flush to get the question ID before creating test cases
        db.session.flush()

        for tc_form in form.test_cases:
            test_case = TestCase(
                input=tc_form.input.data,
                expected_output=tc_form.expected_output.data,
                question_id=coding_question.id
            )
            db.session.add(test_case)
        
        db.session.commit()
        flash('Coding question and test cases added!', 'success')
        return redirect(url_for('main.view_test', test_id=test.id))
    elif request.method == 'POST':
        # Flash errors if validation fails on POST
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return render_template('admin/add_coding_question.html', form=form, test=test)