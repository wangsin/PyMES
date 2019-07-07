from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from app.models import Customer, Material


class AddMaterial(FlaskForm):
    name = StringField('材料名称', validators=[DataRequired(), Length(1, 64)])
    rest = IntegerField('剩余材料', validators=[DataRequired()])
    submit = SubmitField('确认注册材料信息')

    def validate_name(self, field):
        if Material.query.filter_by(name=field.data).first():
            raise ValidationError('此材料名称已经被注册！')


class AddCustomer(FlaskForm):
    customer_name = StringField('顾客名称', validators=[DataRequired(), Length(1, 64)])
    customer_tel = StringField('顾客电话', validators=[DataRequired(), Length(1, 64)])
    customer_company = StringField('顾客公司', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('确认注册顾客信息')

    def validate_tel(self, field):
        if Customer.query.filter_by(tel=field.data).first():
            raise ValidationError('此手机号已经被注册！')


class AddOrderForm(FlaskForm):
    customer_tel = StringField('已经注册的顾客电话', validators=[DataRequired(), Length(1, 64)])
    start_date = DateField('起始日期', validators=[DataRequired()])
    is_urgent = BooleanField('是否紧急', validators=[DataRequired()])
    need_material_id = IntegerField('所需材料ID', validators=[DataRequired()])
    need_material = IntegerField('所需材料数', validators=[DataRequired()])
    need_stock = IntegerField('所需库存', validators=[DataRequired()])
    submit = SubmitField('确认注册顾客信息')


class AddJob(FlaskForm):
    order_id = IntegerField('已经注册的订单编号', validators=[DataRequired()])
    upload_file = FileField('排程文件', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'], '只支持excel标准文件格式！')])
    submit = SubmitField('提交模拟任务')


class AddStock(FlaskForm):
    rest_num = IntegerField('剩余库存', validators=[DataRequired()])
    full_num = IntegerField('最大库存', validators=[DataRequired()])
    submit = SubmitField('提交库存信息')


class StartWatchForm(FlaskForm):
    job_id = IntegerField('模拟成功的任务ID', validators=[DataRequired()])
    submit = SubmitField('确定开始运行任务')
