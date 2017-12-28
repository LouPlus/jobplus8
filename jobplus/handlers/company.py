from flask import Blueprint,render_template,flash,redirect,url_for,current_app,request
from flask_login import login_required,current_user
from jobplus.forms import CompanyProfileFrom
from jobplus.models import CompanyDetail

company = Blueprint('company',__name__,url_prefix='/company')

@company.route('/')
def index():
    page = reauest.args.get('page',1,type=int)
    pagination = CompanyDetail.query.order_by(CompanyDetail.created_at.desc()).paginate(
            page=page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
            )
    return render_template('company/index.html',pagination=pagination,active='company')

            

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
