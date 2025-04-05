from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField, EmailField,PasswordField, SubmitField, FileField,IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed,FileRequired






# Login Form
# Flask-WTF form for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Flask-WTF form for student sign-up
class StudentProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    roll_no = StringField('Roll Number', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])

# Flask-WTF form for teacher sign-up
class TeacherProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subject_name = StringField('Subject Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm New Password", validators=[
        DataRequired(), EqualTo("new_password", message="Passwords must match")
    ])
    submit = SubmitField("Change Password")
    
class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')

class AssignmentUploadForm(FlaskForm):
    assignment_name = StringField('Assignment Name', validators=[DataRequired()])
    assignment_file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class SubmitForm(FlaskForm):
    submitted_assignment = FileField('Submit Assignment', validators=[FileAllowed(['jpg', 'png', 'pdf', 'docx'])])
    submit = SubmitField('Submit Assignment')
    
class MarksUpdateForm(FlaskForm):
    assignment_name = StringField("Assignment Name", validators=[DataRequired()])
    marks = IntegerField("Marks", validators=[DataRequired()])
    submit = SubmitField("Update")
    
class DeleteForm(FlaskForm):
    submit = SubmitField("Yes")
    
class StudentUpdateForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    
class TeacherUpdateForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    subject_name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    teacher_profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Profile')
    
class MarksForm(FlaskForm):
    subject_name = StringField('Subject', validators=[DataRequired()])
    marks_obtained = IntegerField('Marks Obtained', validators=[DataRequired()])
    max_marks = IntegerField('Maximum Marks', validators=[DataRequired()])  # Ensure this matches the model
    submit = SubmitField('Submit Marks')

class NoticeForm(FlaskForm):
    message = TextAreaField("Write your notice", validators=[DataRequired()])
    submit = SubmitField("Add Notice")
    
class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
    
class ReplyForm(FlaskForm):
    reply = TextAreaField("Reply", validators=[DataRequired()])
    submit = SubmitField("Send Reply")