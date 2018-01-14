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
            User.role == User.ROLE_COMPANY
    ).order_by(User.created_at.desc()).limit(8)
    return render_template(
            'front/index.html',
            newest_jobs=newest_jobs,
            newest_companies=newest_companies
            )


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_disable:
            flash('该用户已经被禁用')
            return redirect(url_for('front.login'))
        else:
            login_user(user, form.remember_me.data)
            next = 'user.profile'
            if user.iscompany:
                next = 'admin.index'
            elif:
                next = 'company.profile'
            return redirect(url_for(next))
    return render_template('front/login.html', form=form)


@front.route('/userregister', methods=['GET', 'POST'])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('front/userregister.html', form=form)

@front.route('/companyregister', methods=['GET', 'POST'])
def companyregister():
    form = RegisterForm()
    if form.validate_on_submit():
        company_user = form.create_user()
        company_user.role = User.ROLE_COMPANY
        db.session.add(company_user)
        db.session.commit()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('front/companyregister.html',form=form)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))

