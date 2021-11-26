import re

from django.core.exceptions import ValidationError

def email_check(email):
    email_regex  = '^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$'
    if not re.match(email_regex,email):
        raise ValidationError("Email_ERROR")

def password_check(password):
    password_regex = '^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,}$'
    if not re.match(password_regex,password):
        raise ValidationError("PassWord_ERROR")