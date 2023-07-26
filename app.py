from datetime import datetime

from sqlalchemy.exc import OperationalError

from apis import *


# 4.
# 电费账单模块:
# - 电费账单生成接口: 调用usp_generate_bill存储过程, 生成电费账单。
# - 电费账单查询接口: 返回电费账单。
# - 滞纳金计算接口: 调用usp_calc_latefee存储过程, 计算滞纳金。
# - 电费账单生成接口:
# python


# 调用usp_generate_bill存储过程,生成电费账单
@app.route('/bills/generate', methods=['POST'])
@admin_required()
def generate_bill():
    # 获取参数
    year = request.json.get('year')
    month = request.json.get('month')
    # 校验参数
    if not year or not month:
        abort(400, description='The year and month are required!')
    # 调用存储过程生成账单
    db.session.execute(text(f'EXEC usp_generate_bill @year = {year}, @month = {month}'))
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='生成成功')


# - 电费账单查询接口:
# python


# 返回电费账单
@app.route('/bills')
@jwt_required()
def query_bill():
    # 获取参数
    user_id = get_jwt_identity()
    # 查询账单
    bills = ElectricityBill.query.filter_by(PaidStatus='Unpaid', UserID=user_id).all()
    result = ElectricityBillSchema(many=True).dump(bills)
    # 返回账单
    return jsonify(errno=RET.OK, errmsg='成功', data=result)

    # # 额外返回每个账单的BillID
    # for bill in result:
    #     bill['bill_id'] = bill.pop('BillID')
    #     print(bill['bill_id'])
    # return jsonify(errno=RET.OK, errmsg='OK', data=result)


# - 滞纳金计算接口:
# python


# # 调用usp_calc_latefee存储过程,计算滞纳金
# @app.route('/bills/latefee', methods=['POST'])
# @admin_or_charger_required()
# def calculate_latefee():
#     # 获取参数
#     bill_id = request.json.get('billid')
#     # 调用存储过程计算滞纳金
#     db.session.execute('CALL usp_calc_latefee(:bill_id)', {'bill_id': bill_id})
#     db.session.commit()
#     # 返回成功
#     return jsonify(errno=RET.OK, errmsg='计算成功')


# 5.
# 支付模块:
# - 支付接口: 插入Payment表, 调用trg_update_billstatus触发器更新账单, 调用usp_update_balance存储过程更新账户。
# - 支付记录查询接口: 返回支付记录。
#
# - 支付接口:
# python

# @app.route('/clerk/charge', methods=['POST'])
# # @admin_or_charger_required()
# def charge_bill():
#     # 收费员选择账单并输入实收金额
#     bill_id = request.json.get('bill_id')
#     paid_fee = request.json.get('paid_fee')
#     try:
#         db.session.execute(text(f'EXEC usp_manual_charge @BillID = {bill_id}, @PaidFee = {paid_fee}'))
#         db.session.commit()
#     except IntegrityError as e:
#         db.session.rollback()
#         return jsonify(errno=RET.DATAERR, errmsg='支付记录已存在')
#     except OperationalError as e:
#         db.session.rollback()
#         return jsonify(errno=RET.DBERR, errmsg='数据库异常')
#     return jsonify(errno=RET.OK, errmsg='收费成功')
# 插入Payment表,调用相关触发器和存储过程
@app.route('/payments', methods=['POST'])
@jwt_required()
def make_payment():
    bill_id = request.json.get('bill_id')
    paid_fee = request.json.get('paid_fee')
    try:
        db.session.execute(text(f'EXEC usp_manual_charge @BillID = {bill_id}, @PaidFee = {paid_fee}'))
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(errno=RET.DATAERR, errmsg='支付记录已存在')
    except OperationalError as e:
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    return jsonify(errno=RET.OK, errmsg='收费成功')
    # # 获取参数
    # bill_id = request.json.get('billid')
    # paid_fee = request.json.get('paid_fee')
    # # 插入支付记录
    # bill = ElectricityBill.query.get(bill_id)
    # # 支付相关逻辑...
    # pay_no = '#1234'  # 支付流水号
    # pay_time = datetime.now()  # 支付时间
    # pay_amount = paid_fee  # 支付金额
    #
    # # 写入Payment表
    # payment = Payment(PayNo=pay_no, PayTime=pay_time, PayAmount=pay_amount, BillID=bill_id)
    # db.session.add(payment)
    # db.session.add()
    #
    # bill.PaidStatus = 'Paid'
    # db.session.commit()
    # # 返回支付记录ID
    # return jsonify(errno=RET.OK, errmsg='支付成功')


# 6.收费员手工收费,
# 在当前的系统设计中,收费员的作用似乎没有很好地体现出来。ChargeInfo 表最初也是为了记录收费员的收费信息而设计的。
# 那么,如何更好地发挥收费员的作用,并结合 ChargeInfo 表来丰富系统功能?
# 我们可以这么考虑:
# 1. 收费权限:系统中区分管理员和收费员两个角色。管理员具有全部权限,收费员只能进行收费操作(写入ChargeInfo表)。这样可以限制收费员的权限,保证系统安全。
# 2. 只有收费员可以写入ChargeInfo表,进行手工收费。管理员无权操作该表。这样ChargeInfo表中存储的信息就是收费员的收费记录。
# 3. 收费员登录系统后,只能看到用于收费的界面。此界面读取ElectricityBill表中当月未付费账单,收费员选择其中需收费的账单,输入实收金额后,系统自动写入ChargeInfo表,同时更新Bill表付费状态。
# 4. 统计各收费员的收费总额与明细。通过收费信息ChargeInfo表,系统可以定期统计每个收费员当月的收费金额,以此评价收费员的工作绩效。
# 5. 收费异常检测。系统可以对比每个账单的计费金额与实收金额,检查各收费员的收费信息,发现任何异常情况(少收费或漏收)及时提醒,以确保收费的准确性。


@app.route('/clerk/unpaid_bills')
# @admin_or_charger_required()  # 自定义装饰器检查收费员权限
def get_unpaid_bills():
    # 获取待收费账单
    bills = ElectricityBill.query.filter_by(PaidStatus='Unpaid').all()
    result = ElectricityBillSchema(many=True).dump(bills)
    return jsonify(errno=RET.OK, errmsg='成功', data=result)


# /clerk/charge接口:
# python
# @app.route('/clerk/charge', methods=['POST'])
# # @admin_or_charger_required()
# def charge_bill():
#     # 收费员选择账单并输入实收金额
#     bill_id = request.json.get('bill_id')
#     paid_fee = request.json.get('paid_fee')
#     db.session.execute(text(f'EXEC usp_manual_charge @BillID = {bill_id}, @PaidFee = {paid_fee}'))
#
#     # 执行存储过程完成收费操作
#     db.session.commit()
#
#     return jsonify(errno=RET.OK, errmsg='收费成功')
@app.route('/clerk/charge', methods=['POST'])
# @admin_or_charger_required()
def charge_bill():
    # 收费员选择账单并输入实收金额
    bill_id = request.json.get('bill_id')
    paid_fee = request.json.get('paid_fee')
    try:
        db.session.execute(text(f'EXEC usp_manual_charge @BillID = {bill_id}, @PaidFee = {paid_fee}'))
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify(errno=RET.DATAERR, errmsg='支付记录已存在')
    except OperationalError as e:
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    return jsonify(errno=RET.OK, errmsg='收费成功')


# @app.route('/clerk/charge', methods=['POST'])
# @admin_or_charger_required()  # 自定义装饰器检查收费员权限
# def charge_bill():
#
#     # 收费员选择账单并输入实收金额
#     bill_id = request.json.get('bill_id')
#     paid_fee = request.json.get('paid_fee')
#     # 查询账单信息
#     bill = ElectricityBill.filter_by(BillID=bill_id).first()
#
#     # 插入ChargeInfo表
#     charge_info = {
#         'BillID': bill.BillID,
#         'ChargeDate': datetime.now(),
#         'PaidFee': paid_fee
#     }
#     charge = ChargeInfo(**charge_info)
#     db.session.add(charge)
#
#     # 生成支付信息,插入Payment表
#     pay_no = '#1234'  # 支付流水号
#     pay_time = datetime.now()  # 支付时间
#     pay_amount = paid_fee  # 支付金额
#
#     payment = Payment(PayNo=pay_no, PayTime=pay_time, PayAmount=pay_amount, BillID=bill.BillID)
#     db.session.add(payment)
#
#     # 更新账单付费状态
#     bill.PaidStatus = 'Paid'
#     db.session.commit()
#
#     return jsonify(errno=RET.OK, errmsg='收费成功')


# - 支付记录查询接口:
# python


# 返回支付记录
@app.route('/payments')
@admin_or_charger_required()
def query_payment():
    # 获取参数
    bill_id = request.args.get('billid')
    # 查询支付记录
    payment_list = []
    if bill_id:
        payment_list = Payment.query.filter(Payment.bill_id == bill_id).all()
    else:
        payment_list = Payment.query.all()
    # 返回支付记录
    return jsonify(errno=RET.OK, errmsg='OK', data=[payment.to_dict() for payment in payment_list])


# 根据现有接口, 我对软硬删除接口的设计方案如下:
# 1.
# 软删除接口
# - 用户软删除接口
# python


@app.route('/users/soft_delete', methods=['POST'])
# @admin_required()  # 管理员权限
def soft_delete_user():
    user_id = request.json.get('user_id')
    print(user_id)
    user = Users.query.get(user_id)
    print(user.IsDeleted)
    user.IsDeleted = True
    print(user.IsDeleted)
    db.session.commit()
    print(user.IsDeleted)
    return jsonify(errno=RET.OK, errmsg='用户软删除成功')


# @app.route('/profile/update', methods=['PUT'])
# @jwt_required()
# def update_profile():
#     u_id = get_jwt_identity()
#     user_data = request.get_json()
#     user = Users.query.get(u_id)
#     user.RealName = user_data['RealName']
#     user.Phone = user_data['Phone']
#     user.Email = user_data['Email']
#     user.Address = user_data['Address']
#     db.session.commit()
#     result = UsersSchema().dump(user)
#     return jsonify(result)
# - 其他模型(如ElectricMeter、ElectricityBill等)的软删除接口类似, 设置对应模型的IsDeleted属性为True即可。
# 2.
# 硬删除接口
# - 用户硬删除接口
# python


@app.route('/users/hard_delete', methods=['DELETE'])
# @admin_required()  # 管理员权限
def hard_delete_user():
    user_id = request.json.get('user_id')
    user = Users.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(errno=RET.OK, errmsg='用户硬删除成功')


# - 其他模型的硬删除接口也类似, 直接调用db.session.delete()
# 删除对应数据即可。
# 3.
# 查询接口判断IsDeleted参数返回正常数据或软删除数据
# - 用户查询接口
# python


@app.route('/all_users')
@admin_required()  # 管理员权限
def query_users():
    users = Users.query.filter_by(IsDeleted=False).all()  # 查询未删除用户
    if request.args.get('with_deleted'):
        users = Users.query.all()  # 参数with_deleted=1时查询全部用户包括软删除
    result = UsersSchema(many=True).dump(users)
    return jsonify(result)


# - 其他模型查询接口也类似, 根据请求参数判断是否返回软删除数据。
# 以上就是我对软硬删除接口以及查询判断IsDeleted的简单设计方案。软删除通过设置IsDeleted标记为True实现, 硬删除直接调用db.session.delete()
# 物理删除数据。查询接口通过判断请求参数with_deleted返回所有数据或仅未删除数据。
# 请指出该方案存在的不足或可以改进的地方。我也理解软硬删除涉及的业务逻辑较为复杂, 上述只是一个简单的思路, 实际实现还需要考虑许多边界情况, 我会努力学习和总结这方面的经验。
# 如果您还有其他问题, 请随时提出, 我很乐意讨论和学习。谢谢您的提问, 这对我学习Web开发和数据库设计都很有帮助。 （已编辑）
@app.route('/')
@cache.cached(timeout=5 * 60)
# @admin_required()
def index():
    """首页视图函数"""
    # 获取请求参数并校验
    v = Validator({
        'page': {'type': 'integer'},
        'size': {'type': 'integer'}
    })
    if not v.validate(request.args):
        return jsonify(errno=RET.PARAMERR, errmsg=v.errors)
    # 记录日志
    u_id = current_user.get_id()

    current_app.logger.info('用户 {} 访问首页'.format(u_id))

    # 使用g.user访问用户信息
    return render_template('index.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True)

'''






# 6.
# 日志模块:
# - 系统日志清理任务: 每日调用trg_cleanup_systemlog触发器, 清理超期系统日志。
# - 操作日志记录触发器: 在相关表上调用trg_record_systemlog触发器, 记录操作日志。
# - 系统日志清理任务:
# python


# 每日调用trg_cleanup_systemlog触发器,清理超期系统日志
@app.cli.command()
def cleanup_logs():
    # 调用触发器清理超期日志
    print('开始清理超期系统日志...')
    db.session.execute('CALL trg_cleanup_systemlog()')
    db.session.commit()
    print('清理完成!')


# - 操作日志记录触发器:
# 在相关表上已定义trg_record_systemlog触发器, 记录操作日志。
# 7.
# 备份模块:
# - 数据库备份接口: 调用usp_db_backup存储过程, 执行差异备份。
# - 数据库全备接口: 调用usp_db_fullybackup存储过程, 执行全备份。
# - 数据库日志备份接口: 调用usp_db_logbackup存储过程, 执行日志备份。
# - 数据库备份接口:
# python


# 调用usp_db_backup存储过程,执行差异备份
@app.route('/backup/diff')
@admin_required
def diff_backup():
    # 调用存储过程执行差异备份
    db.session.execute('CALL usp_db_backup()')
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='差异备份完成')


# - 数据库全备接口:
# python


# 调用usp_db_fullybackup存储过程,执行全备份
@app.route('/backup/full')
@admin_required
def full_backup():
    # 调用存储过程执行全备份
    db.session.execute('CALL usp_db_fullybackup()')
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='全备份完成')


# - 数据库日志备份接口:
# python


# 调用usp_db_logbackup存储过程,执行日志备份
@app.route('/backup/log')
@admin_required
def log_backup():
    # 调用存储过程执行日志备份
    db.session.execute('CALL usp_db_logbackup()')
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='日志备份完成')


# 8.
# 其他模块:
# - 数据字典接口:
# python


# 返回对应字典数据
@app.route('/dicts/<dict_code>')
def get_dict(dict_code):
    # 根据字典代码查询对应字典
    dict_list = Dict.query.filter(Dict.dict_code==dict_code).all()
    # 返回字典列表
    return jsonify(errno=RET.OK, errmsg='OK', data=[d.to_dict() for d in dict_list])


# - 管理任务接口:
# python


# 执行数据库维护任务如:数据库压缩、统计数据重算等
@app.cli.command()
@admin_required
def db_maint():
    # 执行数据库维护任务
    print('开始进行数据库维护...')
    db.session.execute('CALL usp_db_maint()')
    db.session.commit()
    print('数据库维护完成!')


# - 统计报表接口:
# python


# 生成各统计报表
@app.route('/reports')
@admin_or_charger_required
def gen_reports():
    # 生成各统计报表
    report_code = request.args.get('reportcode')
    # 根据报表代码查询对应报表存储过程
    if report_code == 'rpt_meter_usage':
        db.session.execute('CALL usp_gen_meter_usage_report()')
    elif report_code == 'rpt_bill_stat':
        db.session.execute('CALL usp_gen_bill_stat_report()')
    # 等等...
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='报表生成成功')
'''
