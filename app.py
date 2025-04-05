from flask import Flask, render_template, jsonify, request,session, redirect, url_for, flash,send_from_directory,abort,current_app
from chatbot_logic import get_suggestions, get_bot_response,get_auto_replies  # Import the chatbot logic
from flask_wtf import FlaskForm
from wtforms import StringField ,SubmitField,FileField
from wtforms.validators import DataRequired, DataRequired
from models.models import db, ClassAssignment,User,Student,Teacher,StudentMarks,ClassNotice,MessageToTeacher,StudentsInClass
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from forms import MarksUpdateForm,StudentUpdateForm,AssignmentUploadForm,SubmitForm,LoginForm,StudentProfileForm,TeacherProfileForm,ChangePasswordForm,ProfileForm,DeleteForm,TeacherUpdateForm,MarksForm,NoticeForm,MessageForm,ReplyForm
from flask_wtf.file import FileField, FileRequired,FileAllowed
import markdown
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Create database tables before the first request
with app.app_context():
    db.create_all()

# Directory for file uploads
UPLOAD_FOLDER = 'media/assignments'  # Fix the folder path
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



#-------------------------------
@app.route("/trusteesprofile")
def trusteesprofile():
    return render_template("college/trusteesprofile.html")

@app.route("/cse")
def cse():
    return render_template("academics/cse.html")


@app.route("/ai")
def ai():
    return render_template("academics/aids.html")


@app.route("/extc")
def extc():
    return render_template("academics/extc.html")


@app.route("/mech")
def mech():
    return render_template("academics/mech.html")

@app.route("/civil")
def civil():
    return render_template("academics/civil.html")

@app.route("/library")
def library():
    return render_template("infrastructure/library.html")

@app.route("/auditorium")
def auditorium():
    return render_template("infrastructure/auditorium.html")

@app.route("/hostel")
def hostel():
    return render_template("infrastructure/hostel.html")

@app.route("/sports")
def sports():
    return render_template("infrastructure/sports.html")

@app.route("/transport")
def transport():
    return render_template("infrastructure/transport.html")

@app.route("/laboratory")
def laboratory():
    return render_template("infrastructure/laboratory.html")

@app.route("/admission")
def admission():
    return render_template("college/admission.html")

@app.route("/lateral-admission")
def lateraladmission():
    return render_template("college/lateral-admission.html")

@app.route("/research")
def research():
    return render_template("college/research.html")

@app.route("/anti-ragging")
def antiragging():
    return render_template("college/anti-ragging.html")

@app.route("/internal-complaints-committee")
def internalcomplaintscommittee():
    return render_template("college/internal-complaints-committee.html")

@app.route("/grievance-redressal")
def grievanceredressal():
    return render_template("college/grievance-redressal.html")

@app.route("/iqac")
def iqac():
    return render_template("college/iqac.html")
















# Routes
@app.route("/")
def home():
    return render_template("college/index.html")

@app.route("/admin")
def admin():
    return render_template("admin/admin.html")

@app.route("/notice")
def notice():
    return render_template("admin/notice.html")

@app.route("/voiceadmin")
def voiceadmin():
    return render_template("admin/voiceadmin.html")

@app.route("/contact")
def contact():
    return render_template("college/contact.html")

@app.route("/collegemain")
def collegemain():
    return render_template("main/collegemain.html")

@app.route("/Chatboat")
def Chatboat():
    return render_template("chatbot/chatboat.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # Store conversation context
    if "context" not in session:
        session["context"] = {}

    session["context"]["last_query"] = user_message

    # Get chatbot response from chatbot_logic.py
    bot_response = get_bot_response(user_message)
    return jsonify({"message": bot_response})

@app.route("/suggest")
def suggest():
    """ Provides live query suggestions as user types """
    query = request.args.get("query", "").lower()
    suggestions = get_suggestions(query)
    return jsonify(suggestions)

@app.route("/auto-replies")
def auto_replies():
    """ Returns auto-suggested replies based on user query """
    query = request.args.get("query", "").lower()
    auto_suggestions = get_auto_replies(query)
    return jsonify(auto_suggestions)


@app.route("/voice")
def voice():
    return render_template("voice/voice.html")






#-------------------------------------------

#classroom

@app.route("/classroom")
def classroom():
    student = None
    if current_user.is_authenticated and getattr(current_user, 'is_student', False):
        student = Student.query.filter_by(user_id=current_user.id).first()

    return render_template("classroom/index.html", 
                           user_authenticated=current_user.is_authenticated,
                           user_is_teacher=getattr(current_user, 'is_teacher', False),
                           student=student,  # Pass student to template
                           user_id=current_user.id if current_user.is_authenticated else None)


# Route to render login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  # Corrected password verification
            login_user(user)
            flash('Login Successful!', 'success')
            return redirect(url_for('classroom'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('classroom/login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route("/signup")
def signup():
    return render_template("classroom/signup.html")


@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    form = StudentProfileForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('student_signup'))

        # Create the user if email is not taken
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            is_student=True
        )
        new_user.set_password(form.password1.data)  # Hash password
        db.session.add(new_user)
        db.session.commit()

        # Create a Student Profile linked to this user
        new_student = Student(
            user_id=new_user.id,
            name=form.name.data,
            roll_no=form.roll_no.data,
            phone=form.phone.data,
            email=form.email.data
        )
        db.session.add(new_student)
        db.session.commit()

        flash('Student successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('classroom/student_signup.html', form=form)

@app.route('/teacher-signup', methods=['GET', 'POST'])
def teacher_signup():
    teacher_profile_form = TeacherProfileForm()  # Initialize the form
    if teacher_profile_form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=teacher_profile_form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('teacher_signup'))

        # Create the user if email is not taken
        new_user = User(
            username=teacher_profile_form.username.data,
            email=teacher_profile_form.email.data,
            is_teacher=True
        )
        new_user.set_password(teacher_profile_form.password1.data)  # Hash password
        db.session.add(new_user)
        db.session.commit()

        # Create a Teacher Profile linked to this user
        new_teacher = Teacher(
            user_id=new_user.id,
            name=teacher_profile_form.name.data,
            subject_name=teacher_profile_form.subject_name.data,
            phone=teacher_profile_form.phone.data,
            email=teacher_profile_form.email.data
        )
        db.session.add(new_teacher)
        db.session.commit()

        flash('Teacher successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('classroom/teacher_signup.html', form=teacher_profile_form)



@app.route('/marks/<int:pk>')
def all_marks_list(pk):
    # Fetch and display marks for the student with the given ID (Replace this with actual logic)
    return f"Displaying marks for student ID {pk}"











@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash("Incorrect current password!", "danger")
        else:
            current_user.set_password(form.new_password.data)  # Hash and store new password
            db.session.commit()
            flash("Password updated successfully!", "success")
            return redirect(url_for("dashboard"))

    return render_template("classroom/change_password.html", form=form)














#-----------------------------------------------------
#-----------------------------------------------------



@app.route('/upload', methods=['GET', 'POST'])
def upload_assignment():
    form = AssignmentUploadForm()
    assignment_uploaded = False

    if form.validate_on_submit():
        file = form.assignment_file.data
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Store in the database
            new_assignment = ClassAssignment(
                assignment_name=form.assignment_name.data,
                teacher="Prof. XYZ",  # Change this to actual teacher logic
                assignment_file=filename  # Store only the filename
            )
            db.session.add(new_assignment)
            db.session.commit()

            assignment_uploaded = True
            flash('Assignment uploaded successfully', 'success')

    return render_template('classroom/upload_assignment.html', form=form, assignment_uploaded=assignment_uploaded)

@app.route('/assignment/<int:student_id>')
def class_assignment(student_id):
    student = Student.query.get_or_404(student_id)
    assignments = ClassAssignment.query.all()
    submitted_assignments = {sub.assignment_id for sub in student.submitted_assignments}  # Get submitted assignment IDs

    return render_template(
        'classroom/class_assignment.html',
        student=student,
        assignments=assignments,
        submitted_assignments=submitted_assignments
    )

@app.route('/assignments')
def assignment_list():
    assignments = ClassAssignment.query.all()  # Fetch all assignments
    return render_template('classroom/assignment_list.html', assignments=assignments)


@app.route('/update_assignment/<int:id>', methods=['GET', 'POST'])
def update_assignment(id):
    assignment = ClassAssignment.query.get_or_404(id)
    form = MarksUpdateForm(obj=assignment)
    marks_updated = False

    if form.validate_on_submit():
        assignment.assignment_name = form.assignment_name.data
        assignment.marks = form.marks.data
        db.session.commit()
        marks_updated = True
        flash("Marks updated successfully!", "success")
    
    return render_template('classroom/update_assignment.html', form=form, marks_updated=marks_updated)


@app.route('/assignment_delete/<int:id>', methods=['GET', 'POST'])
def assignment_delete(id):
    assignment = ClassAssignment.query.get_or_404(id)
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(assignment)
        db.session.commit()
        flash("Assignment deleted successfully!", "success")
        return redirect(url_for('assignment_list'))

    return render_template('classroom/assignment_delete.html', assignment=assignment, form=form)

@app.route('/download/<filename>')
def download_assignment(filename):
    """ Route to download an assignment file securely """
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')  # Default if not set
    
    # Ensure the directory exists
    if not os.path.exists(upload_folder):
        abort(404, description="Upload directory does not exist")
    
    # Ensure the file exists before sending
    file_path = os.path.join(upload_folder, filename)
    if not os.path.isfile(file_path):
        abort(404, description="File not found")

    return send_from_directory(upload_folder, filename, as_attachment=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}  # ✅ Define this manually

class SubmitAssignmentForm(FlaskForm):
    assignment_name = StringField("Assignment Name", validators=[DataRequired()])
    assignment_file = FileField("Upload File", validators=[
        FileRequired(), 
        FileAllowed(ALLOWED_EXTENSIONS, "Only PDF, DOCX, or TXT files allowed!")
    ])
    submit = SubmitField("Upload")

@app.route('/submit_assignment', methods=['GET', 'POST'])
def submit_assignment():
    form = SubmitAssignmentForm()
    
    if form.validate_on_submit():
        file = form.assignment_file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Save assignment details to the database
        assignment = ClassAssignment(assignment_name=form.assignment_name.data, filename=filename)
        db.session.add(assignment)
        db.session.commit()

        flash("Assignment submitted successfully!", "success")
        return redirect(url_for('submit_assignment'))

    return render_template('classroom/submit_assignment.html', form=form)

@app.route('/submissions/<int:teacher_id>')
def submit_list(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    return render_template('classroom/submit_list.html', teacher=teacher)

#-----------------------------------------------------
#-----------------------------------------------------









#-----------------------------------------------------
#-----------------------------------------------------


@app.route('/student/detail/<int:pk>', methods=['GET', 'POST'])
def student_detail(pk):
    student = Student.query.get_or_404(pk)
    return render_template('classroom/student_detail_page.html', student=student)

@app.route('/student/update/<int:pk>', methods=['GET', 'POST'])
def student_update(pk):
    student = Student.query.get_or_404(pk)
    form = StudentUpdateForm(obj=student)

    if form.validate_on_submit():
        student.name = form.name.data
        student.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student_update', pk=student.id))

    return render_template("classroom/student_update_page.html", form=form, profile_updated=False)


# 🚀 FIXED: Only display teacher details (NO update form here)
@app.route('/teacher/detail/<int:pk>')
def teacher_detail(pk):
    teacher = Teacher.query.get_or_404(pk)
    return render_template('classroom/teacher_detail_page.html', teacher=teacher)




@app.route('/teacher/update/<int:pk>', methods=['GET', 'POST'])
def teacher_update(pk):
    teacher = Teacher.query.get_or_404(pk)
    form = TeacherUpdateForm(obj=teacher)

    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.subject_name = form.subject_name.data
        teacher.phone = form.phone.data
        teacher.email = form.email.data

        # Check if a new profile picture is uploaded
        file = form.teacher_profile_pic.data
        if file and hasattr(file, "filename"):  # Ensure it's a FileStorage object
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            teacher.teacher_profile_pic = file_path  # Save path in DB

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('teacher_detail', pk=teacher.id))

    return render_template('classroom/teacher_update_page.html', form=form, teacher=teacher)

#-----------------------------------------------------
#-----------------------------------------------------












@app.route('/add_student/<int:student_id>', methods=['POST'])
@login_required
def add_student(student_id):
    student = Student.query.get_or_404(student_id)

    if not hasattr(current_user, 'teacher') or not current_user.teacher:
        flash("You are not assigned as a teacher!", "danger")
        return redirect(url_for('dashboard'))  # Redirect to a safer place

    # Check if student already exists in class
    existing_entry = StudentsInClass.query.filter_by(
        teacher_id=current_user.teacher.id, student_id=student.id
    ).first()

    if existing_entry:
        flash(f"{student.name} is already in your class!", "warning")
    else:
        try:
            new_entry = StudentsInClass(teacher_id=current_user.teacher.id, student_id=student.id)
            db.session.add(new_entry)
            db.session.commit()
            flash(f"{student.name} successfully added!", "success")
        except SQLAlchemyError:
            db.session.rollback()
            flash("An error occurred while adding the student!", "danger")

    return redirect(url_for('class_students_list'))


@app.route('/classroom/students', methods=['GET'])
def class_students_list():
    search_query = request.args.get('q', '')
    
    if search_query:
        students = Student.query.filter(Student.name.ilike(f"%{search_query}%")).all()
    else:
        students = Student.query.all()
    
    return render_template('classroom/class_students_list.html', class_students_list=students)

@app.route('/students/<int:student_id>/marks', methods=['GET', 'POST'])
def student_marks_list(student_id):
    student = Student.query.get_or_404(student_id)
    form = MarksForm()

    student_marks = StudentMarks.query.filter_by(student_id=student.id).all()

    if form.validate_on_submit():
        new_marks = StudentMarks(
            student_id=student.id,
            subject_name=form.subject_name.data,
            marks_obtained=form.marks_obtained.data,
            max_marks=form.max_marks.data  # Change this line
        )
        db.session.add(new_marks)
        db.session.commit()
        flash("Marks added successfully!", "success")
        return redirect(url_for('student_marks_list', student_id=student.id))

    return render_template(
        'classroom/student_marks_list.html',
        student=student,
        form=form,
        student_marks=student_marks
    )


@app.route('/update_marks/<int:marks_id>', methods=['GET', 'POST'])
def update_marks(marks_id):
    marks = StudentMarks.query.get_or_404(marks_id)
    form = MarksForm(obj=marks)  # Pre-fill form with existing marks
    
    if form.validate_on_submit():
        marks.subject_name = form.subject_name.data
        marks.marks_obtained = form.marks_obtained.data
        marks.max_marks = form.maximum_marks.data  # Ensure field name is consistent
        db.session.commit()
        flash("Marks updated successfully!", "success")
        return redirect(url_for('student_marks_list', student_id=marks.student_id))

    return render_template('classroom/update_marks.html', form=form)


@app.route('/enter_marks/<int:student_id>', methods=['GET', 'POST'])
def enter_marks(student_id):
    student = Student.query.get_or_404(student_id)
    form = MarksForm()

    given_marks = StudentMarks.query.filter_by(student_id=student.id).all()

    if form.validate_on_submit():
        new_marks = StudentMarks(
            student_id=student.id,
            subject_name=form.subject_name.data,
            marks_obtained=form.marks_obtained.data,
            max_marks=form.maximum_marks.data  # Change this line
        )
        db.session.add(new_marks)
        db.session.commit()
        flash("Marks added successfully!", "success")
        return redirect(url_for('student_marks_list', student_id=student.id))

    return render_template(
        'classroom/add_marks.html',
        student=student,
        given_marks=given_marks,
        form=form
    )


@app.route('/student/<int:pk>/marks')
def student_allmarks_list(pk):
    student = Student.query.get_or_404(pk)
    marks_list = StudentMarks.query.filter_by(student_id=pk).all()  # Fetch marks
    return render_template('classroom/student_allmarks_list.html', student=student, marks_list=marks_list)


@app.route('/students_list', methods=['GET'])
def students_list():
    query = request.args.get('q', '')
    if query:
        students_list = Student.query.filter(Student.name.ilike(f'%{query}%')).all()  # Case-insensitive search
    else:
        students_list = Student.query.all()
    return render_template('classroom/students_list.html', students_list=students_list)




#--------------------------------------------------------------

#NOTICES
#--------------------------------------------------------------

@app.route('/write_notice', methods=['GET', 'POST'])
def write_notice():
    form = NoticeForm()
    if form.validate_on_submit():
        new_notice = ClassNotice(
            teacher_id=1,  # Replace with actual logged-in teacher ID
            message=form.message.data
        )
        new_notice.save()
        flash("📢 Notice added successfully!", "success")
        return redirect(url_for('view_notices'))
    return render_template('classroom/notices.html', form=form)

@app.route('/notices', methods=['GET', 'POST'])
def view_notices():
    form = NoticeForm()
    
    if form.validate_on_submit():
        new_notice = ClassNotice(
            teacher_id=1,  # Replace with actual logged-in teacher ID
            message=form.message.data
        )
        new_notice.save()
        flash("Notice added successfully!", "success")
        return redirect(url_for('view_notices'))

    notices = ClassNotice.query.order_by(ClassNotice.created_at.desc()).all()
    return render_template('classroom/notices.html', notices=notices, form=form)

@app.route('/update_notice/<int:notice_id>', methods=['GET', 'POST'])
def update_notice(notice_id):
    notice = ClassNotice.query.get_or_404(notice_id)
    form = NoticeForm(obj=notice)

    if form.validate_on_submit():
        notice.message = form.message.data
        notice.message_html = markdown.markdown(notice.message)
        db.session.commit()
        flash("Notice updated successfully!", "info")
        return redirect(url_for('view_notices'))

    return render_template('classroom/write_notice.html', form=form, notice=notice)

@app.route('/delete_notice/<int:notice_id>', methods=['GET'])
def delete_notice(notice_id):
    notice = ClassNotice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash("Notice deleted successfully!", "danger")
    return redirect(url_for('view_notices'))

@app.route('/class_notice')
def class_notice():
    notices = ClassNotice.query.join(Teacher).order_by(ClassNotice.created_at.desc()).all()
    return render_template('classroom/class_notice_list.html', notices=notices)


#--------------------------------------------------------------


#--------------------------------------------------------------



@app.route('/teachers')
def teachers_list():
    query = request.args.get("q", "")
    teachers = Teacher.query.filter(Teacher.name.ilike(f"%{query}%")).all() if query else Teacher.query.all()
    return render_template("classroom/teachers_list.html", teachers_list=teachers)

@app.route('/write_message/<int:teacher_id>', methods=['GET', 'POST'])
def write_message(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    
    # Fetch all the messages related to the teacher
    messages = MessageToTeacher.query.filter_by(teacher_id=teacher_id).order_by(MessageToTeacher.created_at.desc()).all()
    
    form = MessageForm()

    # Handle form submission for sending a message
    if form.validate_on_submit():
        new_message = MessageToTeacher(
            student_id=current_user.id,  # Get the logged-in student's ID
            teacher_id=teacher_id,
            message=form.message.data,
            message_html=form.message.data,  # Store HTML version of the message
        )
        new_message.save()  # Save the message to the database
        flash("Message sent successfully!", "success")
        return redirect(url_for('write_message', teacher_id=teacher_id))

    return render_template("classroom/write_message.html", teacher=teacher, form=form, messages=messages)

@app.route('/messages/<int:teacher_id>', methods=['GET', 'POST'])
def messages_list(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    messages = MessageToTeacher.query.filter_by(teacher_id=teacher_id).order_by(MessageToTeacher.created_at.desc()).all()
    
    form = ReplyForm()

    # Handle the teacher's reply submission
    if form.validate_on_submit():
        message_id = request.form.get("message_id")
        message = MessageToTeacher.query.get(message_id)
        if message and message.teacher_id == teacher_id:
            message.reply = form.reply.data
            message.reply_html = form.reply.data  # Store the HTML version of the reply if needed
            message.save()  # Save the reply to the database
            flash("Reply sent successfully!", "success")
        return redirect(url_for("messages_list", teacher_id=teacher_id))

    return render_template("classroom/messages_list.html", messages=messages, teacher=teacher, form=form)


@app.route('/reply/<int:message_id>', methods=['POST'])
def reply_to_message(message_id):
    parent_message = MessageToTeacher.query.get_or_404(message_id)
    
    # Ensure the logged-in user is the teacher of the message (only teachers can reply)
    if current_user.id != parent_message.teacher_id:
        flash("You do not have permission to reply to this message.", "danger")
        return redirect(url_for('messages_list', teacher_id=parent_message.teacher_id))  # Redirect to message list

    message_text = request.form.get('message')
    teacher_id = parent_message.teacher_id  # Same teacher
    student_id = parent_message.student_id  # Same student

    # Create a reply message with a reference to the parent message
    reply = MessageToTeacher(
        student_id=student_id,
        teacher_id=teacher_id,
        message=message_text,
        parent_id=message_id  # Link to the parent message
    )

    reply.save()
    flash('Reply sent successfully!', 'success')
    return redirect(url_for('messages_list', teacher_id=teacher_id))  # Redirect to the messages list


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
