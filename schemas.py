# schemas.py:
from flask_marshmallow import Marshmallow
from newmodels import *

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import jsonify
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        sqla_session = db.session


class ElectricMeterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElectricMeter
        sqla_session = db.session


class ElectricityUsageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElectricityUsage
        sqla_session = db.session
    UserID = fields.Str()
    MeterID = fields.Str()

class ElectricityBillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElectricityBill
        sqla_session = db.session
    UserID = fields.Str()
    MeterID = fields.Str()


class ChargeInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChargeInfo
        sqla_session = db.session
    BillID = fields.Str()


class ChargeStandardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChargeStandard
        sqla_session = db.session


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        sqla_session = db.session
    BillID = fields.Str()


class SystemLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SystemLog
        sqla_session = db.session



