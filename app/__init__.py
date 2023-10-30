from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary

app = Flask(__name__)
app.secret_key = '@#$%^^%$562536267%$%7*(9*&^5%&}}}}76%^^^'
app.config['SQLALCHEMY_DATABASE_URI'] = str.format('mysql+pymysql://root:{}@localhost/labsaledb?charset=utf8mb4',
                                                   'Omc6789#')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app=app)

cloud_dict = {
    "cloud_name": "dad8ejn0r",
    "api_key": "916986197549325",
    "api_secret": "8ZDd8GQafg9rc9_h5UrIBt0SZ4Q"
}

cloudinary.config(
    cloud_name=cloud_dict["cloud_name"],
    api_key=cloud_dict["api_key"],
    api_secret=cloud_dict["api_secret"]
)
