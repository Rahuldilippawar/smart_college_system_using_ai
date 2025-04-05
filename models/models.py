from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import markdown
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)

    # Assuming you have a Teacher model
    teacher = db.relationship('Teacher', backref='user', uselist=False)  # One-to-one relationship

    def set_password(self, password):
        """Hashes the password and stores it"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Student Model
class Student(db.Model):

    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('students', lazy=True))  # Add this line

    name = db.Column(db.String(250), nullable=False)
    roll_no = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    student_profile_pic = db.Column(db.String(300), nullable=True)


    # Relationship with ClassNotice using StudentsInClass as a secondary table
    class_notices = db.relationship(
        'ClassNotice',
        secondary='students_in_class',
        primaryjoin="Student.id == StudentsInClass.student_id",
        secondaryjoin="ClassNotice.teacher_id == StudentsInClass.teacher_id",
        backref="students"
    )
  # Relationship to store student submissions
    submitted_assignments = db.relationship('SubmittedAssignment', backref='student', lazy=True)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    subject_name = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    teacher_profile_pic = db.Column(db.String(255), nullable=True, default="static/images/default-avatar.png") 
    
    # ✅ Add the reverse relationship to SubmittedAssignment
    assignments_received = db.relationship('SubmittedAssignment', back_populates='teacher')
    
    # Only one relationship for messages (use 'messages_received')
    messages_received = db.relationship('MessageToTeacher', backref='message_teacher', lazy=True)

    def __repr__(self):
        return f"Teacher('{self.name}', '{self.subject_name}', '{self.email}', '{self.phone}', '{self.teacher_profile_pic}')"


class StudentsInClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    teacher = db.relationship('Teacher', viewonly=True)
    student = db.relationship('Student', viewonly=True)


# Student Marks Model
class StudentMarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    marks_obtained = db.Column(db.Integer, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)  
    def __repr__(self):
        return f'<StudentMarks {self.subject_name}>'

class MessageToTeacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    message_html = db.Column(db.Text)  # If you want to store HTML version of the message
    reply = db.Column(db.Text)  # Ensure this column exists for replies
    reply_html = db.Column(db.Text)  # If you want to store HTML version of the reply
    parent_id = db.Column(db.Integer, db.ForeignKey('message_to_teacher.id'))  # For thread-based replies
    
    # Relationships
    student = db.relationship('Student', backref='messages_sent')
    teacher = db.relationship('Teacher', backref='received_messages')  # Changed backref here to avoid conflict
    parent = db.relationship('MessageToTeacher', backref='replies', remote_side=[id])
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Message('{self.message}', '{self.created_at}')"
    
    
# Class Notices Model
class ClassNotice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    message_html = db.Column(db.Text, nullable=False)

    def save(self):
        self.message_html = markdown.markdown(self.message)  # Convert markdown to HTML
        db.session.add(self)
        db.session.commit()
        
    teacher = db.relationship('Teacher', backref='notices')    
    
    def __repr__(self):
        return f"ClassNotice(id={self.id}, teacher_id={self.teacher_id}, created_at={self.created_at})"

# Assignments Model
class ClassAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(255), nullable=False)
    teacher = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    assignment_file = db.Column(db.String(255), nullable=False)  # ✅ File path
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('SubmittedAssignment', back_populates='class_assignment', lazy=True)

    def __repr__(self):
        return f"Assignment('{self.assignment_name}', '{self.assignment_file}', '{self.uploaded_at}')"

class SubmittedAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    class_assignment_id = db.Column(db.Integer, db.ForeignKey('class_assignment.id'), nullable=False)
    assignment_name = db.Column(db.String(255), nullable=False)
    submit = db.Column(db.String(255), nullable=False)  # Path to uploaded file
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # ✅ Rename 'assignment' to 'class_assignment'
    class_assignment = db.relationship('ClassAssignment', back_populates='submissions')  # Remove backref and use back_populates
    teacher = db.relationship('Teacher', back_populates='assignments_received')


