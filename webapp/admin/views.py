from flask import Blueprint, render_template

from webapp.user.decorators import admin_required
from webapp.user.forms import RegistrationForm, LogoutForm
from webapp.market.models import Auto
from webapp.user.models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = 'Панель управления'
    form = RegistrationForm()
    logoutform = LogoutForm()
    auto_list = Auto.query.all()
    auto_active = Auto.query.filter_by(active=True).all()
    auto_all = len(auto_list)
    auto_true = len(auto_active)
    auto_false = auto_all - auto_true
    user_list = User.query.order_by(User.id).all()
    return render_template("admin/index.html", page_title=title,
                           form=form,
                           logoutform=logoutform,
                           auto_all=auto_all,
                           auto_true=auto_true,
                           auto_false=auto_false,
                           user_list=user_list)
