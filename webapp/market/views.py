import os

from flask import Blueprint, render_template, redirect, url_for, \
    request, current_app, flash, jsonify
from flask_login import current_user

from webapp.market.models import Auto, Params, Images, Auto_brand,\
    Auto_models
from webapp.user.forms import RegistrationForm, LogoutForm,\
    LoginForm
from webapp.market.forms import AddForm, DeleteForm, EditForm, FilterForm
from webapp.message.forms import MessageForm
from webapp.db import db
from webapp.user.models import User

blueprint = Blueprint('market', __name__)


@blueprint.route('/')
def index():
    page_title = 'Не бита, не крашена!'
    fform = FilterForm()
    form = LoginForm()
    logoutform = LogoutForm()
    brands = Auto_brand.query.order_by(Auto_brand.id).all()
    count = {}
    for br in brands:
        auto = Auto.query.filter_by(brand_id=br.id).all()
        count[br.name] = len(auto)
    page = request.args.get('page', 1, type=int)
    full_auto_list = Auto.query.order_by(Auto.id).all()
    auto_list = Auto.query.order_by(Auto.id).paginate(
        page, current_app.config['AUTO_PER_PAGE'], False)
    next_url = url_for('market.index', page=auto_list.next_num) \
        if auto_list.has_next else None
    prev_url = url_for('market.index', page=auto_list.prev_num) \
        if auto_list.has_prev else None
    return render_template('market/index.html', page_title=page_title,
                           form=form,
                           logoutform=logoutform,
                           auto_list=auto_list.items,
                           next_url=next_url, prev_url=prev_url,
                           brands=brands, full_auto_list=full_auto_list,
                           count=count, fform=fform
                           )


@blueprint.route('/brand_<brand>')
def filter_brand(brand):
    page_title = 'Не бита, не крашена!'
    form = LoginForm()
    logoutform = LogoutForm()
    brands = Auto_brand.query.filter_by(id=brand).all()
    page = request.args.get('page', 1, type=int)
    auto_list = Auto.query.filter_by(brand_id=brand).paginate(
        page, current_app.config['AUTO_PER_PAGE'], False)
    next_url = url_for('market.index', page=auto_list.next_num) \
        if auto_list.has_next else None
    prev_url = url_for('market.index', page=auto_list.prev_num) \
        if auto_list.has_prev else None
    models = Auto_models.query.filter_by(brand_id=brand).all()
    count = {}
    for model in models:
        auto = Auto.query.filter_by(model_id=model.id).all()
        count[model.name] = len(auto)
    return render_template('market/filter_by_brand.html',
                           page_title=page_title,
                           form=form,
                           logoutform=logoutform,
                           auto_list=auto_list.items,
                           next_url=next_url, prev_url=prev_url,
                           brands=brands, models=models, count=count
                           )

@blueprint.route('/brand_<brand>/<model>')
def filter_model(brand, model):
    page_title = 'Не бита, не крашена!'
    form = LoginForm()
    logoutform = LogoutForm()
    brands = Auto_brand.query.filter_by(id=brand).all()
    page = request.args.get('page', 1, type=int)
    auto_list = Auto.query.filter_by(model_id=model).paginate(
        page, current_app.config['AUTO_PER_PAGE'], False)
    next_url = url_for('market.index', page=auto_list.next_num) \
        if auto_list.has_next else None
    prev_url = url_for('market.index', page=auto_list.prev_num) \
        if auto_list.has_prev else None
    models = Auto_models.query.filter_by(brand_id=brand).all()
    count = {}
    for model in models:
        auto = Auto.query.filter_by(model_id=model.id).all()
        count[model.name] = len(auto)
    return render_template('market/filter_by_brand.html',
                           page_title=page_title,
                           form=form,
                           logoutform=logoutform,
                           auto_list=auto_list.items,
                           next_url=next_url, prev_url=prev_url,
                           brands=brands, models=models, count=count
                           )


@blueprint.route('/registration')
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('market.index'))
    page_title = 'Регистрация на сайте - Не бита, не крашена!'
    form = LoginForm()
    regform = RegistrationForm()
    logoutform = LogoutForm()

    return render_template('user/registration.html', page_title=page_title,
                           form=form, regform=regform,
                           logoutform=logoutform)


@blueprint.route('/auto/add_auto')
def add_auto():
    page_title = 'Разместить объявление на сайте - Не бита, не крашена!'
    form = LoginForm()
    regform = RegistrationForm()
    addform = AddForm()
    logoutform = LogoutForm()
    addform.brand.choices = [(
        brand.id, brand.name) for brand in Auto_brand.query.all()]

    addform.model.choices = [(
        model.id, model.name) for model in Auto_models.query.filter_by(
            brand_id=addform.brand.choices[0][0]).all()]

    return render_template('market/add.html', page_title=page_title,
                           form=form, regform=regform,
                           logoutform=logoutform, addform=addform)


@blueprint.route('/delete/auto_<id>', methods=['POST'])
def del_auto(id):
    auto = Auto.query.filter_by(id=id).first()
    auto.active = False
    db.session.commit()

    flash(f"Объявление {auto.name} успешно удалено!")
    return redirect(url_for('user.user_account', id=current_user.id))


@blueprint.route('/sell_auto/edit/<id>', methods=["GET", "POST"])
def edit_auto(id):
    page_title = 'Редактирование объявления'
    editform = EditForm()
    form = LoginForm()
    regform = RegistrationForm()
    logoutform = LogoutForm()
    auto = Auto.query.filter_by(id=id).first()
    if editform.validate_on_submit():
        auto.price = editform.price.data
        auto.description = editform.description.data
        auto.mileage = editform.mileage.data
        uploaded_files = request.files.getlist('url_picture')
        for file in uploaded_files:
            file.save(os.path.join(
                f'{current_app.static_folder}/uploaded', file.filename))
            new_auto_i = Images(
                auto_id=auto.id,
                url_picture=file.filename)
            db.session.add(new_auto_i)
        db.session.commit()
        flash(f"Объявление {auto.name} успешно отредактировано!")
        return redirect(url_for('market.auto_account', id=id))
    return render_template('market/edit.html', page_title=page_title,
                           logoutform=logoutform, editform=editform,
                           form=form, regform=regform, auto=auto)


@blueprint.route('/auto/<id>')
def brand(id):
    brands = Auto_brand.query.filter_by(id=id).all()
    brandArr = []
    modelArr = []
    for brand in brands:
        brandObj = {}
        brandObj['id'] = id
        brandObj['name'] = brand.name
        models = Auto_models.query.filter_by(brand_id=id).all()
        for model in models:
            modelObj = {}
            modelObj['id'] = model.id
            modelObj['name'] = model.name
            modelArr.append(modelObj)
            brandObj['models'] = modelArr
            brandArr.append(brandObj)
    return jsonify(brandObj)


@blueprint.route('/process_add', methods=['POST'])
def process_add():
    addform = AddForm()
    brand = Auto_brand.query.filter_by(id=addform.brand.data).first()
    model = Auto_models.query.filter_by(id=addform.model.data).first()
    new_auto = Auto(
        price=addform.price.data,
        description=addform.description.data,
        name=f'{brand.name} {model.name}, {addform.year.data}',
        user_id=current_user.id,
        brand_id=brand.id,
        model_id=model.id
        )

    db.session.add(new_auto)
    db.session.commit()
    new_auto_p = Params(
        auto_id=new_auto.id,
        holders=addform.holders.data,
        condition=addform.condition.data,
        steering_wheel=addform.steering_wheel.data,
        wheeldrive=addform.wheeldrive.data,
        color=addform.color.data,
        model=model.name,
        mileage=addform.mileage.data,
        brand=brand.name,
        year=addform.year.data,
        body_type=addform.body_type.data,
        type_engine=addform.type_engine.data,
        gear=addform.gear.data)

    uploaded_files = request.files.getlist('url_picture')
    for file in uploaded_files:
        file.save(os.path.join(
            f'{current_app.static_folder}/uploaded', file.filename))
        new_auto_i = Images(
            auto_id=new_auto.id,
            url_picture=file.filename
        )
        db.session.add(new_auto_i)
    db.session.commit()
    db.session.add(new_auto_p)
    db.session.commit()
    flash(f"Объявление {new_auto.name} успешно размещено!")
    return redirect(url_for('market.index'))


@blueprint.route('/sell_auto/<id>')
def auto_account(id):
    auto = Auto.query.filter_by(id=id).first()
    form = LoginForm()
    regform = RegistrationForm()
    logoutform = LogoutForm()
    delform = DeleteForm()
    msgform = MessageForm()
    if auto.active is True:
        params = Params.query.join(Auto).filter_by(id=id).first()
        all_params = {
            'Владельцев по ПТС': params.holders,
            'Поколение': params.generation,
            'Состояние': params.condition, 'Руль': params.steering_wheel,
            'Привод': params.wheeldrive,
            'Цвет': params.color, 'Объём двигателя': params.engine_capacity,
            'Модель': params.model,
            'Пробег': params.mileage, 'Марка': params.brand,
            'Год выпуска': params.year,
            'Тип кузова': params.body_type,
            'Тип двигателя': params.type_engine,
            'Коробка передач': params.gear, 'Мощность двигателя': params.power,
            'Количество дверей': params.doors,
            'VIN или номер кузова': params.vin,
            'Место осмотра': params.location, 'Комплектация': params.equipment,
            'Модификация': params.modification}
        title = f'Продажа {auto.name} на сайте "Не бита, не крашена!"'
        user = User.query.filter_by(id=auto.user_id).first()
        return render_template('market/auto.html', auto=auto,
                               page_title=title,
                               form=form, regform=regform,
                               logoutform=logoutform,
                               params=params, all_params=all_params,
                               user=user, delform=delform, msgform=msgform
                               )
    return render_template(
        'market/deleted.html',
        page_title='Объявление снято с продажи или удалено',
        form=form, logoutform=logoutform, delform=delform, regform=regform)


@blueprint.route('/find', methods=['GET', 'POST'])
def find():
    fform = FilterForm()
    if fform.validate_on_submit:
        full_auto_list = Auto.query.filter(
            Auto.price >= fform.price_1.data, Auto.price <= fform.price_2.data).all()
        page = request.args.get('page', 1, type=int)
        auto_list = Auto.query.filter(
            Auto.price >= fform.price_1.data, Auto.price <= fform.price_2.data).paginate(
                page, current_app.config['AUTO_PER_PAGE'], False)
        next_url = url_for('market.index', page=auto_list.next_num) \
            if auto_list.has_next else None
        prev_url = url_for('market.index', page=auto_list.prev_num) \
            if auto_list.has_prev else None
        page_title = 'Не бита, не крашена!'
        form = LoginForm()
        logoutform = LogoutForm()
        brands = Auto_brand.query.order_by(Auto_brand.id).all()
        count = {}
        for br in brands:
            auto = Auto.query.filter_by(brand_id=br.id).all()
            count[br.name] = len(auto)
        page = request.args.get('page', 1, type=int)
        full_auto_list = Auto.query.order_by(Auto.id).all()
        return render_template('market/index.html', page_title=page_title,
                               form=form,
                               logoutform=logoutform,
                               auto_list=auto_list.items,
                               next_url=next_url, prev_url=prev_url,
                               brands=brands, full_auto_list=full_auto_list,
                               count=count, fform=fform
                               )
