from flask import Blueprint,render_template,redirect,url_for,flash
from jobplus.models import db,User,Job
from jobplus.forms import RegisterForm,LoginForm
from jobplus.config import configs
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_migrate import Migrate

front = Blueprint('front', __name__)


@front.route('/')
def index():
    newest_jobs = Job.query.order_by(Job.created_at.desc()).limit(8)
    newest_companies = User.query.filter(
            User.role==User.ROLE_COMPANY
    ).order_by(User.created_at.desc()).limit(8)
    return render_template(
            'index.html',
            newest_jobs=newest_jobs,
            newest_companies=newest_companies
            )


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)


@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))

