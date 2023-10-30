from app import app, db
from app.models import Category, Product, User
import hashlib


def load_categories():
    return Category.query.all()
    # return load_json(os.path.join(app.root_path, 'data/categories.json'))


def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=None):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if from_price:
        products = products.filter(Product.price.__ge__(from_price))
    if to_price:
        products = products.filter(Product.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()
    # products = load_json(os.path.join(app.root_path, 'data/products.json'))
    # if cate_id:
    #     products = [p for p in products if int(cate_id) == int(p['category_id'])]
    # if kw:
    #     products = [p for p in products if p['name'].lower().find(kw.lower()) >= 0]
    #
    # if from_price and to_price:
    #     products = [ p for p in products if float(from_price) <= p['price'] <= float(to_price)]
    # elif from_price:
    #     products = [p for p in products if float(from_price) <= p['price']]
    # elif to_price:
    #     products = [p for p in products if p['price'] <= float(to_price)]
    #
    # return products


def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()
