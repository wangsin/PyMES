from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
    # username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持我的登陆状态')
    submit = SubmitField('登陆')


class RegistrationForm(FlaskForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名不合法')])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='密码不匹配')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    # role = SelectMultipleField('用户角色', choices=[(1, "管理员"), (2, "观察者")])
    is_administrator = BooleanField('是否为管理员')
    submit = SubmitField('确认注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮箱已经被注册！')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已经被注册！')
