from wtforms import Form, validators, StringField, PasswordField

class RegisterForm(Form):
    name = StringField('Name:', [validators.length(min=1, max=50)])
    email = StringField('Email:', [validators.length(min=6, max=50)])
    username = StringField('User Name:', [validators.length(min=4, max=25)])
    password = PasswordField('Password:', [validators.DataRequired(),
                                           validators.EqualTo('confirm', message='Passwords do not match')
                                           ])
    confirm = PasswordField('Confirm Password')
