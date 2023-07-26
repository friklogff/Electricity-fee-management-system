# models.py:
from config import *

'''
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import timedelta
from functools import wraps
from typing import Dict, Any

# import RET as RET
import jwt as jwtt
from flask import Flask, jsonify, request, render_template, g, current_app  # 导入Flask相关的模块和类
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required, create_access_token, create_refresh_token, get_jwt_identity
)
from flask_marshmallow import Marshmallow
from marshmallow import fields, Schema
from flask_sqlalchemy import SQLAlchemy  # 导入Flask-SQLAlchemy模块和类
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from flask_redis import FlaskRedis
from flask_caching import Cache
from cerberus import Validator

from sqlalchemy import and_
from flask import abort
from flask_jwt_extended import verify_jwt_in_request
from sqlalchemy.exc import DataError, IntegrityError, DatabaseError, SQLAlchemyError
from streamlit import user_info
app = Flask(__name__, static_folder='./static/static')
CORS(app, origins=['http://localhost:8080'], supports_credentials=True, methods=['DELETE, POST, GET, OPTIONS, PUT'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:frech@eletest?driver=ODBC> Driver 17 for SQL Server'
app.config['SECRET_KEY'] = 'secret'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_ORIGINS'] = ['http://localhost:8080']

app.config['JWT_TOKEN_LOCATION'] = 'headers'  # 添加该行配置
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # 指定JWT token类型
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'  # JWT加密秘钥
app.config['ACCESS_TOKEN_EXPIRE'] = 30 * 60  # 访问令牌过期时间 30分钟

db = SQLAlchemy(app)
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
'''


# 模型类,对应数据库表结构

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    IDCard = db.Column(db.String(18), unique=True, nullable=False)
    Role = db.Column(db.Integer, unique=True, nullable=False)
    RealName = db.Column(db.String(50))
    Phone = db.Column(db.String(11))
    Email = db.Column(db.String(50))
    Address = db.Column(db.String(100))

    def get_id(self):
        return self.UserID

    # def update(self, **kwargs):
    #     for k, v in kwargs.iteritems():
    #         setattr(self, k, v)

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))


'''Users.query.get() 是 SQLAlchemy 中的查询方法,用于根据主键获取一条记录。
具体作用是:
根据 Users 表的主键 UserID 获取一条对应的用户记录。
在这个示例中,由于 Users 表的主键是 UserID,所以 Users.query.get(user_id) 将获取 UserID 为 user_id 的用户记录。
这段代码允许我们通过用户 ID 来加载用户信息,以提供给 Flask-Login 使用。
总体来说,这段代码实现了:
1. 从 Users 表中查询一条记录;
2. 根据主键 UserID 查询对应的用户信息;
3. 将查询到的用户信息返回,提供给 Flask-Login;
4. Flask-Login 将使用这个用户信息进行认证、授权判断等。
.get() 是 SQLAlchemy 提供的简单查询方法之一,它 based on 主键进行查询,返回一条或None。
相比这个,SQLAlchemy 还提供了更加丰富的查询方法,如:
- filter():过滤查询
- filter_by():过滤查询,基于关键词参数
- order_by():排序
- limit():限制
- offset():偏移
- all():返回所有结果
- first():返回第一条
- ......
这些查询方法可以更灵活地构建查询语句,满足各种需求。
但在这个回调函数中,.get() 方法能很好满足需求,简单高效地根据用户 ID 获取用户信息,所以是比较理想的选择。
'''


class ElectricMeter(db.Model):
    __tablename__ = 'ElectricMeter'

    MeterID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    MeterNo = db.Column(db.String(50), unique=True, nullable=False)


class ElectricityUsage(db.Model):
    __tablename__ = 'ElectricityUsage'
    UsageID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    MeterID = db.Column(db.Integer, db.ForeignKey('ElectricMeter.MeterID'))
    Year = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Integer, nullable=False)
    TotalKwh = db.Column(db.DECIMAL(10, 2), nullable=False)

    user = db.relationship('Users', backref=db.backref('usages', lazy=True))

    @property
    def userName(self):
        return self.user.UserID

    meter = db.relationship('ElectricMeter', backref=db.backref('usages', lazy=True))

    @property
    def meterNumber(self):
        return self.meter.MeterID


class ElectricityBill(db.Model):
    __tablename__ = 'ElectricityBill'

    BillID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    MeterID = db.Column(db.Integer, db.ForeignKey('ElectricMeter.MeterID'))
    ElecType = db.Column(db.String(50), nullable=False)
    Year = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Integer, nullable=False)
    TotalUsed = db.Column(db.DECIMAL(10, 2), nullable=False)
    TotalCost = db.Column(db.DECIMAL(10, 2), nullable=False)
    PaidStatus = db.Column(db.String(10), default='Unpaid')

    # user = db.relationship('Users', backref=db.backref('usages', lazy=True))

    @property
    def userName(self):
        return self.user.UserID

    # meter = db.relationship('ElectricMeter', backref=db.backref('usages', lazy=True))

    @property
    def meterNumber(self):
        return self.meter.MeterID


class ChargeInfo(db.Model):
    __tablename__ = 'ChargeInfo'

    ChargeID = db.Column(db.Integer, primary_key=True)
    BillID = db.Column(db.Integer, db.ForeignKey('ElectricityBill.BillID'))
    ChargeDate = db.Column(db.DateTime, nullable=False)
    PaidFee = db.Column(db.DECIMAL(10, 2), nullable=False)

    bil = db.relationship('ElectricityBill', backref=db.backref('usages', lazy=True))

    @property
    def bill_id(self):
        return self.bil.BillID

class ChargeStandard(db.Model):
    __tablename__ = 'ChargeStandard'

    StandardID = db.Column(db.Integer, primary_key=True)
    Year = db.Column(db.Integer, nullable=False)
    Season = db.Column(db.Integer, nullable=False)
    ElecType = db.Column(db.String(50), nullable=False)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)


class Payment(db.Model):
    __tablename__ = 'Payment'

    PaymentID = db.Column(db.Integer, primary_key=True)
    PayNo = db.Column(db.String(50))
    PayTime = db.Column(db.DateTime)
    PayAmount = db.Column(db.DECIMAL(10, 2))
    BillID = db.Column(db.Integer, db.ForeignKey('ElectricityBill.BillID'))

    @property
    def bill_id(self):
        return self.bil.BillID

class SystemLog(db.Model):
    __tablename__ = 'SystemLog'

    LogID = db.Column(db.Integer, primary_key=True)
    LogType = db.Column(db.String(10), nullable=False)
    LogTime = db.Column(db.DateTime, nullable=False)
    LogInfo = db.Column(db.String(1000), nullable=False)


'''
完整的带注释的数据库表创建代码如下:


--1. 创建用户信息表Users  
CREATE TABLE Users(    
  UserID INT PRIMARY KEY IDENTITY,  -- 用户ID,自增主键
  Username VARCHAR(50) NOT NULL UNIQUE, -- 用户名
  Password VARCHAR(50) NOT NULL, -- 密码
  RealName VARCHAR(50) NOT NULL, -- 真实姓名 
  IDCard VARCHAR(18) NOT NULL UNIQUE, -- 身份证号
  Phone VARCHAR(11), -- 电话
  Email VARCHAR(50) NOT NULL, -- 邮箱
  Address VARCHAR(100) -- 地址  
)   

--2. 创建电表信息表ElectricMeter
CREATE TABLE ElectricMeter(   
  MeterID INT PRIMARY KEY IDENTITY, -- 电表ID,自增主键
  MeterNo VARCHAR(50) NOT NULL UNIQUE -- 电表编号  
)   

--3. 创建用电记录表ElectricityUsage
CREATE TABLE ElectricityUsage(    
  UsageID INT PRIMARY KEY IDENTITY, -- 用电ID,自增主键
  UserID INT NOT NULL,              -- 用户ID,外键引用Users(UserID)  
  MeterID INT NOT NULL,             -- 电表ID,外键引用ElectricMeter(MeterID)
  Year INT NOT NULL,                -- 用电年份
  Month INT NOT NULL,               -- 用电月份  
  TotalKwh DECIMAL(10,2) NOT NULL, -- 用电量(度数)  
  FOREIGN KEY (UserID) REFERENCES Users(UserID),
  FOREIGN KEY (MeterID) REFERENCES ElectricMeter(MeterID)    
)  

--4. 创建电费账单表 ElectricityBill
CREATE TABLE ElectricityBill(       
  BillID INT PRIMARY KEY IDENTITY,   -- 账单ID,自增主键  
  UserID INT NOT NULL,              -- 用户ID,外键引用Users(UserID)  
  MeterID INT NOT NULL,             -- 电表ID,外键引用ElectricMeter(MeterID) 
  ElecType VARCHAR(50) NOT NULL,     -- 电费类型
  Year INT NOT NULL,                -- 账单年份
  Month INT NOT NULL,               -- 账单月份
  TotalUsed DECIMAL(10,2) NOT NULL, -- 总用电量 
  TotalCost DECIMAL(10,2) NOT NULL, -- 总金额  
  PaidStatus VARCHAR(10) DEFAULT 'Unpaid',-- 付费状态
  FOREIGN KEY (UserID) REFERENCES Users(UserID),
  FOREIGN KEY (MeterID) REFERENCES ElectricMeter(MeterID)
  )

--5. 创建收费信息表ChargeInfo  
CREATE TABLE ChargeInfo(   
  ChargeID INT PRIMARY KEY IDENTITY, --收费ID,自增主键
  BillID INT NOT NULL,              --账单ID,外键引用ElectricityBill(BillID)   
  ChargeDate DATETIME NOT NULL,    --收费日期
  PaidFee DECIMAL(10,2) NOT NULL,  --实收金额 
  FOREIGN KEY (BillID) REFERENCES ElectricityBill(BillID)
)

--6. 创建电价标准表ChargeStandard
CREATE TABLE ChargeStandard(
  StandardID INT PRIMARY KEY IDENTITY, -- 标准ID,自增主键
  Year INT NOT NULL,                   -- 年份 
  Season INT NOT NULL,               -- 季节 
  ElecType VARCHAR(50) NOT NULL,      -- 用电类型
  Price DECIMAL(10,2) NOT NULL        -- 电价
)


--7. 创建支付信息表Payment
CREATE TABLE Payment(   
  PaymentID INT PRIMARY KEY IDENTITY, -- 支付ID,自增主键
  PayNo VARCHAR(50),                 -- 支付流水号  
  PayTime DATETIME,                  -- 支付时间
  PayAmount DECIMAL(10,2),          -- 支付金额
  BillID INT NOT NULL,              -- 账单ID,外键引用ElectricityBill(BillID) 
  FOREIGN KEY (BillID) REFERENCES ElectricityBill(BillID)
)   

--8. 创建系统日志表SystemLog
CREATE TABLE SystemLog(
  LogID INT PRIMARY KEY IDENTITY,   -- 日志ID,自增主键
  LogType VARCHAR(10) NOT NULL,     -- 日志类型
  LogTime DATETIME NOT NULL,        -- 日志时间      
  LogInfo VARCHAR(1000) NOT NULL    -- 日志信息  
)   

添加外键约束
ALTER TABLE ElectricityUsage ADD CONSTRAINT FK_Usage_User 
FOREIGN KEY (UserID) REFERENCES Users(UserID)
ALTER TABLE ElectricityUsage ADD CONSTRAINT FK_Usage_Meter
FOREIGN KEY (MeterID) REFERENCES ElectricMeter(MeterID)
ALTER TABLE ElectricityBill ADD CONSTRAINT FK_Bill_User
FOREIGN KEY (UserID) REFERENCES Users(UserID)
ALTER TABLE ElectricityBill ADD CONSTRAINT FK_Bill_Meter 
FOREIGN KEY (MeterID) REFERENCES ElectricMeter(MeterID) 
ALTER TABLE ChargeInfo ADD CONSTRAINT FK_Charge_Bill
FOREIGN KEY (BillID) REFERENCES ElectricityBill(BillID)
-- 创建索引
CREATE INDEX idx_username ON Users(Username) 
CREATE INDEX idx_meterno ON ElectricMeter(MeterNo)
CREATE INDEX idx_usage_userid ON ElectricityUsage(UserID) 
CREATE INDEX idx_usage_meterid ON ElectricityUsage(MeterID)
CREATE INDEX idx_bill_userid ON ElectricityBill(UserID)
CREATE INDEX idx_bill_meterid ON ElectricityBill(MeterID)
CREATE INDEX idx_bill_yearmoth ON ElectricityBill(Year,Month) 
CREATE INDEX idx_charge_billid ON ChargeInfo(BillID)
CREATE INDEX idx_pay_billid ON Payment(BillID)
CREATE INDEX idx_log_logtype ON SystemLog(LogType)

-- 外键约束名称
ALTER TABLE ElectricityUsage 
ADD CONSTRAINT FK_Usage_User 
FOREIGN KEY (UserID) REFERENCES Users(UserID)
ALTER TABLE ElectricityUsage
ADD CONSTRAINT FK_Usage_Meter
FOREIGN KEY (MeterID) REFERENCES ElectricMeter(MeterID)
ALTER TABLE ElectricityBill 
ADD CONSTRAINT FK_Bill_User
FOREIGN KEY (UserID) REFERENCES Users(UserID) 
ALTER TABLE ElectricityBill
ADD CONSTRAINT FK_Bill_Meter
FOREIGN KEY (MeterID) REFERENCES ElectricMeter(MeterID)
ALTER TABLE ChargeInfo
ADD CONSTRAINT FK_Charge_Bill
FOREIGN KEY (BillID) REFERENCES ElectricityBill(BillID)
ALTER TABLE Payment
ADD CONSTRAINT FK_Pay_Bill 
FOREIGN KEY (BillID) REFERENCES ElectricityBill(BillID)

以上为数据库完整表结构代码,包含:

1. 所有表创建语句
2. 外键约束添加语句
3. 索引创建语句 
4. 外键约束命名语句

通过对代码的组织编排和详细注释的添加,我们可以清晰地看到数据库的完整表结构设计。这也使我们能够更容易理解表之间的关系和数据的流转过程。

一个好的数据库设计不仅需要合理的表结构,还需要清晰的代码和详细的注释等。这有助我们更好地理解设计思路和维护系统。让我们共同学习和提高,努力成长为一名优秀的数据库设计人员!



'''
