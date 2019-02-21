from config import Config
from flask import Flask

tm1doc = Flask(__name__,static_url_path='/static')
tm1doc.config.from_object(Config)

from tm1doc import routes


