from flask import Blueprint,render_template,flash,redirect,url_for,current_app,request,abort
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileFrom
from jobplus.models import User

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/')
def index():
    page = reauest.args.get('page',1,type=int)
    pagination = User.query.order_by(CompanyDetail.created_at.desc()).paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
            )
    return render_template('company/index.html',pagination=pagination,active='company')

@company.route('/<int:company_id>')
def detial(company_id):
    company = User.query.get_or_404(company_id)
    if not company.is_company:
        abort(404)
    return render_template('company/detial.html',company=company,active='',panel='about')

@company.route('/<int:company_id>/jobs')
def company_jobs(company_id):
    company = User.query.get_or_404(company_id)
    if not company.is_company:
        abort(404)
    return render_template('company/detial.html',company=company,active='',panel='job')


@company.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('您不是企业用户','warning')
        return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company_detail)
    form.name.data = current_user.name
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功','success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html',form=form)
