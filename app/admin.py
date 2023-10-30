from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Category, Product

admin = Admin(app=app, name="E-Commerce Administration", template_mode='bootstrap4')


class ProductView(ModelView):
    column_display_all_relations = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_exclude_list = ['image', 'active', 'created_date']
    column_filters = ['name', 'price']
    column_list = ['name', 'description', 'price', 'category']


admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
