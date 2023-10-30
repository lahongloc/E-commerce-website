from flask_sqlalchemy import SQLAlchemy

from app import app
from flask import render_template, request, redirect, url_for
import utils
import math
import cloudinary.uploader
from app import cloud_dict
import requests


@app.route('/')
def home():
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    page = request.args.get('page', 1)
    count_products = utils.count_products()

    products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))

    return render_template('index.html',
                           products=products,
                           page_number=math.ceil(count_products / app.config['PAGE_SIZE']))


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories()
    }


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        email = request.form.get('email')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = 'Mat khau xac nhan khong khop!'
        except Exception as ex:
            err_msg = ex.args[0] if len(ex.args) > 0 else None
            if err_msg.find("1062") >= 0:
                err_msg = "Da ton tai username nay trong he thong!"
            db.session.rollback()
            return render_template('register.html', err_msg=err_msg)

    return render_template('register.html', err_msg=err_msg)


@app.route('/products')
def products_list():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')

    products = utils.load_products(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('products.html', products=products)


@app.route('/products/<product_id>')
def product_details(product_id):
    products = utils.load_products()
    current_product = {}
    for p in products:
        if p['id'] == int(product_id):
            current_product = p
            break

    return render_template('details.html', current_product=current_product)


if __name__ == '__main__':
    from app.admin import *

    app.run(debug=True)
