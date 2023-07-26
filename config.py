from flask_sqlalchemy import SQLAlchemy
import re
from datetime import timedelta
from functools import wraps
from typing import Dict, Any
# import RET as RET

from marshmallow import fields, Schema
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from cerberus import Validator

from sqlalchemy import and_
from flask import abort
from flask_jwt_extended import verify_jwt_in_request
from sqlalchemy.exc import DataError, IntegrityError, DatabaseError, SQLAlchemyError
from streamlit import user_info
# app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'  # JWT加密秘钥
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from flask import Flask, jsonify, request, render_template, g, current_app  # 导入Flask相关的模块和类
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required, create_access_token, create_refresh_token, get_jwt_identity
)

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy  # 导入Flask-SQLAlchemy模块和类
from flask_redis import FlaskRedis
from flask_caching import Cache

app = Flask(__name__, static_folder='./static/static')
CORS(app, origins=['http://localhost:8080'], supports_credentials=True, methods=['DELETE, POST, GET, OPTIONS, PUT'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:frech@ele_m?driver=ODBC> Driver 17 for SQL Server'
app.config['SECRET_KEY'] = 'secret'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_ORIGINS'] = ['http://localhost:8080']

app.config['JWT_TOKEN_LOCATION'] = 'headers'  # 添加该行配置
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # 指定JWT token类型
app.config['ACCESS_TOKEN_EXPIRE'] = 30 * 60  # 访问令牌过期时间 30分钟

db = SQLAlchemy(app)
# db = SQLAlchemy()
# db.init_app(app)
ma = Marshmallow(app)

jwt = JWTManager(app)

redis_store = FlaskRedis(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis',
                           'CACHE_REDIS_HOST': '127.0.0.1',
                           'CACHE_REDIS_PORT': 6379})  # 缓存初始化
# 访问令牌黑名单cache key
access_token_blacklist_key = 'access_token_blacklist_{}'

# 用户登录信息缓存KEY的格式
user_info_key = 'user_info_{}'

login_manager = LoginManager()
login_manager.init_app(app)