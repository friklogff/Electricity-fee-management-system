# models.py:
from config import *



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
    IsDeleted = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.UserID


    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))




class ElectricMeter(db.Model):
    __tablename__ = 'ElectricMeter'

    MeterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False)
    ElecType = db.Column(db.String(50), nullable=False)


class ElectricityUsage(db.Model):
    __tablename__ = 'ElectricityUsage'
    UsageID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False)
    MeterID = db.Column(db.Integer, db.ForeignKey('ElectricMeter.MeterID', ondelete='NO ACTION'), nullable=False)
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
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'), nullable=False)
    MeterID = db.Column(db.Integer, db.ForeignKey('ElectricMeter.MeterID', ondelete='NO ACTION'), nullable=False)
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
    BillID = db.Column(db.Integer, db.ForeignKey('ElectricityBill.BillID', ondelete='CASCADE'), nullable=False)
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


