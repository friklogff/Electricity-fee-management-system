from sqlalchemy import text

from schemas import *


# 定义全局常量
class RET:
    OK = 0  # 成功
    DBERR = 1  # 数据库查询错误
    NODATA = 2  # 无数据
    DATAEXIST = 3  # 数据已存在
    DATAERR = 4  # 数据错误
    PARAMERR = 5  # 参数错误
    USERERR = 6  # 用户错误
    ROLEERR = 7  # 角色错误
    PWDERR = 8  # 密码错误
    REQERR = 9  # 请求错误
    EXCEPTION = 10  # 系统异常

    errmsg = {
        DBERR: "数据库异常",
        NODATA: "无数据",
        DATAEXIST: "数据已存在",
        DATAERR: "数据错误",
        PARAMERR: "参数错误",
        USERERR: "用户错误",
        ROLEERR: "角色错误",
        PWDERR: "密码错误",
        REQERR: "请求错误",
        EXCEPTION: "系统异常"
    }


# ---------------使用自定义装饰器在执行视图函数前判断用户角色并控制权限------------------------------------------------
# JWT认证回调函数
# @jwt.user_lookup_loader
# def authenticate(username, password):
#     user = Users.query.filter_by(Username=username).first()
#     if user and user.password == password:
#         return user
#

# # JWT解码回调函数,设置当前用户
# def identity(payload):
#     user_id = payload['identity']
#     user = cache.get(user_info_key.format(user_id))
#     if not user:
#         user = Users.query.filter_by(UserID=user_id).first()
#         cache.set(user_info_key.format(user_id), user)
#     g.current_user = user
#     return user
#
# # 判断当前用户角色,返回对应角色代码
# def get_user_role():
#     return g.current_user.Role

# JWT解码回调函数
# def identity(user_id, payload):
#     user = cache.get(user_info_key.format(user_id))
#     if not user:
#         user = Users.query.filter_by(UserID=user_id).first()
#         cache.set(user_info_key.format(user_id), user)
#     return user


# 验证管理员权限装饰器
# 管理员权限装饰器
# # 获取登录用户角色
# role = get_jwt_claims(request.access_token)['privilege']
# 这两行代码的作用是:
# 1. 获取请求头中的 Authorization,并提取出令牌部分(token)
# 2. 使用 PyJWT 解析令牌,获取 payload 部分的内容
# 具体解释如下:
# token = request.headers.get('Authorization').split(' ')[1]
# - request.headers.get('Authorization') 获取请求头中的 Authorization 字段
# - .split(' ')[1] 把 Authorization 的值按空格分割,取第二部分,就是我们的令牌 token
# claims = jwtt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
# - jwtt.decode() 使用 PyJWT 解析令牌
# - token 是上一步获取的令牌值
# - app.config['SECRET_KEY'] 是我们设置的密钥,需要在Flask配置中设置,如:
# python
# SECRET_KEY = 'mysecretkey'
# - algorithms=['HS256'] 指定我们使用的算法是 HS256,需要与签发令牌的算法一致
# - 解析成功后,会返回令牌的 payload,我们可以从中获取自定义的声明等信息,这里命名为 claims
# 所以,要使用这两行代码,我们需要:
# 1. 在 Flask 配置中设置 SECRET_KEY,作为签名校验的密钥
# 2. 令牌需要使用 HS256 算法签发(此例中我们使用的算法)
# 3. 我们可以在 payload 中设置自定义声明,如用户角色等信息
# 这两行代码最主要的作用就是从请求中获取令牌,并解析校验,获取 payload 信息用于后续的权限认证等逻辑。


def admin_required():
    import jwt as jwtt
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get('Authorization').split(' ')[1]
                print(token)
            except:
                return jsonify(errno=RET.ROLEERR, errmsg='token error'), 401
            try:
                claims = jwtt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                print(claims)
            except:
                return jsonify(errno=RET.ROLEERR, errmsg='claims error'), 401

            role = claims['privilege']
            if role != 0:  # ROLE = {0: '管理员'}
                return jsonify(errno=RET.ROLEERR, errmsg='用户权限不足'), 401
            try:
                return fn(*args, **kwargs)
            except DatabaseError:
                return '数据库异常,请稍后再试。', 500

        return wrapper

    return decorator


def admin_or_charger_required():
    import jwt as jwtt
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get('Authorization').split(' ')[1]
                print(token)
            except:
                return jsonify(errno=RET.ROLEERR, errmsg='token error'), 401
            try:
                claims = jwtt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                print(claims)
            except:
                return jsonify(errno=RET.ROLEERR, errmsg='claims error'), 401

            role = claims['privilege']
            if role != 1:  # ROLE = {0: '管理员'}
                return jsonify(errno=RET.ROLEERR, errmsg='用户权限不足'), 401
            try:
                return fn(*args, **kwargs)
            except DatabaseError:
                return '数据库异常,请稍后再试。', 500

        return wrapper

    return decorator
# def admin_or_charger_required():
#     import jwt as jwtt
#     def decorator(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             try:
#                 token = request.headers.get('Authorization').split(' ')[1]
#                 print(token)
#             except:
#                 return jsonify(errno=RET.ROLEERR, errmsg='token error'), 401
#             try:
#                 claims = jwtt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#                 print(claims)
#             except:
#                 return jsonify(errno=RET.ROLEERR, errmsg='claims error'), 401
#
#             role = claims['privilege']
#             print(role, "hi")
#
#             if role != 1:
#                 return jsonify(errno=RET.ROLEERR, errmsg='用户权限不足'), 401
#             try:
#                 return fn(*args, **kwargs)
#             except DatabaseError:
#                 return '数据库异常,请稍后再试。', 500
#
#         return wrapper
#
#     return decorator


# 验证用户本人权限装饰器
# access_token = request.headers.get('Authorization')
# """从请求头获取access_token"""
# token_id = decode_auth_token(access_token)
# """解密access_token获取其中的用户ID"""


def user_required(fn):
    """登录用户校验装饰器"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        """装饰器内层函数"""
        jwt_id = get_jwt_identity()
        if not jwt_id:
            return jsonify(errno=RET.AUTHERR, errmsg='未登录')

        user_id = current_user.get_id()
        """获取当前登录用户ID"""
        """使用flask_jwt_extended从JWT token中解析出user_id"""
        # 如果两个ID不一致,返回未授权错误
        if user_id != jwt_id:
            return jsonify(errno=RET.AUTHERR, errmsg='未授权访问')

        return fn(*args, **kwargs)

    return wrapper


# 获取当前登录用户


# ---------------使用自定义装饰器在执行视图函数前判断用户角色并控制权限------------------------------------------------


# return jsonify({'msg': 'User created'})
# - 用户信息更新接口:
# python

# # 用户修改用户接口
# @app.route('/user/<int:id>', methods=['PUT'])
# @admin_required
# def update_user(id):
#     user_data = request.get_json()
#     user = Users.query.get(id)
#     user.password = user_data['password']
#     user.Username = user_data['name']
#     db.session.commit()
#     result = UsersSchema().dump(user)
#     return jsonify(result)
#     # return {'message': 'User updated successfully.'}, 200
# # 更新Users表
# @app.route('/profile/<int:user_id>', methods=['PUT'])
# @user_required
# def update_profile(user_id):
#     # 获取参数
#     username = request.json.get('username')
#     realname = request.json.get('realname')
#     idcard = request.json.get('idcard')
#     phone = request.json.get('phone')
#     email = request.json.get('email')
#     address = request.json.get('address')
#
#     # 检查参数是否完整
#     if not all([username, realname, idcard, email, address]):
#         return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
#
#     # 验证用户名
#     if not re.match(r'^[A-Za-z0-9_]{5,50}$', username):
#         return jsonify(errno=RET.PARAMERR, errmsg='用户名格式错误')
#
#     # 验证身份证号码
#     if not re.match(r'^\d{6}(18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|[xX])$', idcard):
#         return jsonify(errno=RET.PARAMERR, errmsg='身份证号码格式错误')
#
#     # 验证邮箱
#     if not re.match(r'^[\w-]+(.[a-z\d\-]+)*@([a-z\d\-]+(.[a-z\d\-]+)*){2,4}$', email):
#         return jsonify(errno=RET.PARAMERR, errmsg='邮箱格式错误')
#
#     # 查询用户名是否已存在
#     user = Users.query.filter(Users.username==username).first()
#     if user and user.id != user_id:
#         return jsonify(errno=RET.DATAEXIST, errmsg='用户名已存在')
#
#     # 查询身份证号码是否已存在
#     user = Users.query.filter(Users.idcard==idcard).first()
#     if user and user.id != user_id:
#         return jsonify(errno=RET.DATAEXIST, errmsg='身份证号码已存在')
#
#     # 更新用户信息
#     Users.query.filter(Users.id==user_id).update({
#         "username": username,
#         "realname": realname,
#         "idcard": idcard,
#         "phone": phone,
#         "email": email,
#         "address": address
#     })
#     db.session.commit()
#
#     # 获取完整用户信息
#     user = Users.query.get(user_id)
#     return jsonify(errno=RET.OK, errmsg='更新成功', data=user.to_dict())
# 接口设计
# 1.
# 用户模块:
# - 用户注册接口: 插入Users表。
# - 用户登录接口: 验证登录, 返回token。
# - 用户信息获取接口: 返回用户信息。
# - 用户信息更新接口: 更新Users表。
# - 用户注册接口:
# python


# python


# 管理员注册接口
@app.route('/admin/register', methods=['POST'])
# @admin_required()
def admin_register():
    username = request.json.get('Username')
    password = request.json.get('Password')
    idcard = request.json.get('IDCard')
    role = request.json.get('Role')  # 新增角色类型
    print(username, password, idcard, role)
    # 校验输入
    # if not all([username, password, idcard, role]):
    #     return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    if not username or not password:
        return jsonify({'msg': 'Missing Username or Password'}), 401
    if Users.query.filter(Users.Username == username).first() or \
            Users.query.filter(Users.IDCard == idcard).first():
        return jsonify(errno=RET.DATAEXIST, errmsg='用户名或身份证号已存在')
    # 加密密码
    hash_pw = generate_password_hash(password)
    # 添加用户
    user = Users(Username=username, Password=hash_pw, Role=role, IDCard=idcard)

    # 事务添加用户
    try:
        db.session.execute(text("ALTER TABLE Users DISABLE TRIGGER tr_create_user_electric_meter"))
        db.session.add(user)
        db.session.commit()
    except DataError as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常: {}'.format(e))
    except DatabaseError as e:
        error = e.orig.args  # 使用DatabaseError的orig属性
        current_app.logger.error(error)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常: {}'.format(error))

    # 生成访问令牌,将角色信息存入Payload
    # 生成访问和刷新token
    access_token = create_access_token(identity=user.UserID, additional_claims={'privilege': user.Role},
                                       expires_delta=timedelta(minutes=30))
    # 生成刷新令牌
    refresh_token = create_refresh_token(identity=user.UserID, expires_delta=timedelta(days=7))
    result = {'access_token': access_token, 'refresh_token': refresh_token}
    current_app.logger.info('用户 {} 注册成功'.format(user.Username))
    return jsonify(errno=RET.OK, errmsg='注册成功', data=result)


# 插入Users表,返回用户ID和token
# 用户注册接口
# python
@app.route('/users/register', methods=['POST'])
def create_user():
    username = request.json.get('Username')
    password = request.json.get('Password')
    idcard = request.json.get('IDCard')

    if not all([username, password, idcard]):
        return jsonify(errno=4001, errmsg='参数不完整')
    if Users.query.filter(Users.Username == username).first():
        return jsonify(errno=3001, errmsg='用户名已存在')
    if Users.query.filter(Users.IDCard == idcard).first():
        return jsonify(errno=3002, errmsg='身份证号已存在')
    role = 2  # 默认role从3开始
    # 判断role是否唯一
    while Users.query.filter_by(Role=role).first():
        role += 1  # 如果角色存在,递增role值
        # 校验输入
        # 加密密码
    hash_pw = generate_password_hash(password)
    # 添加用户
    user = Users(Username=username, Password=hash_pw, Role=role, IDCard=idcard)

    try:
        # 添加用户并提交
        db.session.add(user)
        # 在插入用户前禁用触发器
        db.session.execute(text("ALTER TABLE Users DISABLE TRIGGER tr_create_user_electric_meter"))
        db.session.commit()

        # 获取刚刚插入的用户的 UserID
        inserted_user = Users.query.filter_by(Username=username).first()

        if inserted_user:
            # 添加电表记录并提交
            electric_meter = ElectricMeter(UserID=inserted_user.UserID)
            db.session.add(electric_meter)
            db.session.commit()

        # 在插入用户后启用触发器
        db.session.execute(text("ALTER TABLE Users ENABLE TRIGGER tr_create_user_electric_meter"))
        db.session.commit()

        return jsonify(status='success', msg='用户注册成功')
    except Exception as e:
        db.session.rollback()
        return jsonify(status='error', msg='用户注册失败：{}'.format(str(e)))

    # try:
    #     db.session.add(user)
    #     db.session.commit()
    # except DataError as e:
    #     return jsonify(errno=4001, errmsg='数据库异常: {}'.format(e))
    #
    # return jsonify(errno=0, errmsg='注册成功',
    #                data={'username': username})

    # # 校验输入
    # if not all([username, password, idcard]):
    #     return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # if not username or not password:
    #     return jsonify({'msg': 'Missing Username or Password'}), 401
    # if Users.query.filter(Users.Username == username).first() or \
    #         Users.query.filter(Users.IDCard == idcard).first():
    #     return jsonify(errno=RET.DATAEXIST, errmsg='用户名或身份证号已存在')
    # # 加密密码
    # hash_pw = generate_password_hash(password)
    # # 添加用户
    # user = Users(Username=username, Password=hash_pw, Role=role, IDCard=idcard)
    #
    # # 事务添加用户
    # try:
    #     db.session.add(user)
    #     db.session.commit()
    # except DataError as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='数据库异常: {}'.format(e))
    # except DatabaseError as e:
    #     error = e.orig.args  # 使用DatabaseError的orig属性
    #     current_app.logger.error(error)
    #     return jsonify(errno=RET.DBERR, errmsg='数据库异常: {}'.format(error))
    # result = '用户 {} 注册成功'.format(user.Username)
    # current_app.logger.info(result)
    # return jsonify(errno=RET.OK, errmsg='注册成功', data=result)

    # # 生成访问令牌,将角色信息存入Payload
    # # 生成访问和刷新token
    # access_token = create_access_token(identity=user.UserID, additional_claims={'privilege': user.Role},
    #                                    expires_delta=timedelta(minutes=30))
    # # 生成刷新令牌
    # refresh_token = create_refresh_token(identity=user.UserID, expires_delta=timedelta(days=7))
    # result = {'access_token': access_token, 'refresh_token': refresh_token}





# 验证登录,返回token
# 登录接口
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # JSON 校验
    username = request.json.get('Username', None)  # 获取请求中的用户名
    password = request.json.get('Password', None)  # 获取请求中的密码

    user = Users.query.filter_by(Username=username).first()
    print(username, password)
    # 登录校验
    if not user or not check_password_hash(user.Password, password):
        print('用户名或密码错误')
        return jsonify(errno=RET.DATAERR, errmsg='用户名或密码错误')

    # 访问令牌黑名单校验
    if cache.get(access_token_blacklist_key.format(user.UserID)):
        # 清除用户登录信息缓存
        cache.delete(user_info_key.format(user.UserID))
        # 设置登录Session过期
        session.pop(user.UserID, None)

    if user and check_password_hash(user.Password, password):
        login_user(user)
        # 生成访问和刷新token
        access_token = create_access_token(identity=user.UserID, additional_claims={'privilege': user.Role},
                                           expires_delta=timedelta(minutes=30))
        # 生成刷新令牌
        refresh_token = create_refresh_token(identity=user.UserID, expires_delta=timedelta(days=7))
        # 存储用户登录信息至缓存
        cache.set(user_info_key.format(user.UserID), user, timeout=30 * 24 * 60 * 60)
        print('登陆成功')

        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401


@app.route('/logout', methods=['POST'])
@jwt_required()
# @user_required    # user_id = current_user.get_id()
def logout():
    """用户登出"""
    user_id = get_jwt_identity()

    # 校验是否在黑名单中,如果在,则表示已经退出,直接返回
    if cache.get(access_token_blacklist_key.format(user_id)):
        return jsonify(errno=RET.OK, errmsg='已登出')
    # 如果不在,则退出登录
    # 删除用户登录缓存中的信息
    cache.delete(user_info_key.format(user_id))
    # 设置登录session过期
    session.pop(user_id, None)
    # 清空访问令牌缓存
    cache.delete(access_token_blacklist_key.format(user_id))
    # 记录日志
    current_app.logger.info('用户 {} 登出'.format(user_id))
    # 将access token加入黑名单
    cache.set(access_token_blacklist_key.format(user_id), 1, timeout=60)
    # 返回成功信息
    logout_user()
    return jsonify(errno=RET.OK, errmsg='退出成功')


# # - 用户信息获取接口:
# @app.route('/profile')
# @jwt_required()
# def get_user_profile():
#     # u_id = current_user.get_id()
#     u_id = get_jwt_identity()
#     print(u_id)
#
#     user = Users.query.filter(Users.UserID == u_id).first()
#     users_schema = UsersSchema()
#     users_data = users_schema.dump(user)
#     current_app.logger.info('用户 %s 访问个人信息接口', u_id)
#     return jsonify(users_data)


# conn = db.engine.raw_connection()  # 获取原生数据库连接
#
# cursor = conn.cursor()
# cursor.callproc('usp_GetUserInfo', [user_id])
# result = cursor.fetchall()
#
# cursor.close()
# result = db.session.execute('CALL usp_GetUserInfo', user_id)  # 执行存储过程

# return render_template('user_info.html', result=result)
# user_profile = result.fetchone()
# return jsonify(user_profile._asdict())
# print(u_id, result)
#

# user = result.first()
# info = {
#     'UserID': user .UserID,
#     'Username': user .Username,
#     'RealName': user .RealName,
#     'Phone': user .Phone,
#     'Email': user .Email,
#     'MeterID': user .MeterID,
#     'ElecType': user .ElecType
# }
# current_app.logger.debug(result)
# print(info)
# return jsonify(info)
# return 0

# try:
# user_data = request.get_json()
# username= user_data['Username'],
# real_name=user_data['RealName'],
# phone = user_data['Phone'],
# email = user_data['Email'],
# elec_type = user_data['ElecType']

@app.route('/profile')
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()

    current_app.logger.debug('用户 %s 访问个人信息接口', user_id)
    result = db.session.execute(text(f'EXEC usp_GetUserInfo @user_id = {user_id}'))

    data = []
    for row in result:
        # 直接转为字典,不需要排序
        d = {col: val for col, val in zip(result.keys(), row)}
        data.append(d)

    db.session.commit()
    return jsonify(data)


@app.route('/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    u_id = get_jwt_identity()
    data = request.get_json()

    username = data.get('Username')
    real_name = data.get('RealName')
    phone = data.get('Phone')
    email = data.get('Email')
    elec_type = data.get('ElecType')
    address = data.get('Address')
    sql = f'EXEC usp_UpdateUserElecInfo @UserID = {u_id}'

    if username is not None:
        sql = sql + f", @Username = '{username}'"
    if real_name is not None:
        sql = sql + f", @RealName = '{real_name}'"
    if phone is not None:
        sql = sql + f", @Phone = '{phone}'"
    if email is not None:
        sql = sql + f", @Email = '{email}'"
    if address is not None:
        sql = sql + f", @Address = '{address}'"
    if elec_type is not None:
        sql = sql + f", @ElecType = '{elec_type}'"
    db.session.execute(text(sql))

    db.session.commit()  # 手动提交事务

    user = Users.query.get(u_id)
    users_data = UsersSchema().dump(user)
    return jsonify(users_data)


#
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


#     """更新个人信息"""
#     u_id = current_user.get_id()
#     # 查询要更新的user
#     # 获取参数并校验
#     user = Users.query.filter(Users.UserID == u_id).first()
#     if not user:
#         return jsonify(errno=RET.NODATA, errmsg='用户不存在')
#     # 只接收需要更新的字段
#     update_data = request.json
#     # 校验唯一性
#     if Users.query.filter(Users.Username == update_data.get('Username')).first():
#         return jsonify(errno=RET.DATAERR, errmsg='用户名已存在')
#     if Users.query.filter(Users.IDCard == update_data.get('IDCard')).first():
#         return jsonify(errno=RET.DATAERR, errmsg='身份证号码已存在')
#         # 校验邮箱格式
#     # if update_data.get('email') and not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', update_data.get('email')):
#     #     return jsonify(errno=RET.DATAERR, errmsg='邮箱格式错误')
#     # 开启事务
#     try:
#         # 更新用户信息
#         user = UsersSchema().load(update_data, instance=user, partial=True)
#         db.session.begin_nested()
#         # db.session.add(user)
#         db.session.commit()
#         current_app.logger.info('用户 {} 更新信息成功'.format(u_id))
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg='数据库异常')
#
#
#     db.session.commit()
#     # 序列化返回
#     user_data = UsersSchema().dump(user)
#     return jsonify(errno=RET.OK, errmsg='更新成功', data=user_data)


# 2.
# 电表模块:
# - 电表添加接口:
# python
# 插入ElectricMeter表
@app.route('/meters', methods=['POST'])
@admin_or_charger_required()
def add_meter():
    # 获取参数
    meterno = request.json.get('meterno')
    # 保存电表信息
    meter = ElectricMeter(meterno=meterno)
    db.session.add(meter)
    db.session.commit()
    # 返回电表ID
    return jsonify(errno=RET.OK, errmsg='添加成功', data={'meterid': meter.MeterID})


# - 电表信息获取接口:
# python


# 返回电表信息
@app.route('/meters/<int:meter_id>')
@jwt_required()
@admin_required()
def get_meter(meter_id):
    # 获取电表信息
    meter = ElectricMeter.query.filter(ElectricMeter.MeterID == meter_id).first()
    print(meter)
    electric_meter_schema = ElectricMeterSchema()
    electric_meter_data = electric_meter_schema.dump(meter)
    return jsonify(errno=RET.OK, errmsg='OK', data=electric_meter_data)


# - 电表信息更新接口:
# python


# 更新ElectricMeter表
@app.route('/meters/<int:meter_id>', methods=['PUT'])
@admin_or_charger_required()
def update_meter(meter_id):
    # 获取参数
    meterno = request.json.get('meterno')
    # 更新电表信息
    ElectricMeter.query.filter(ElectricMeter.id == meter_id).update({"meterno": meterno})
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='更新成功')


# 3.
# 用电记录模块:
# - 用电记录添加接口: 插入ElectricityUsage表。
# - 用电记录查询接口: 返回用电记录。
# - 用电记录导入接口: 调用usp_import_electricityusage存储过程, 导入用电记录。
# - 用电记录归档任务: 每月1日调用usp_archive_usage存储过程, 归档上月用电记录。
# - 用电记录添加接口:
# python


# 插入ElectricityUsage表
@app.route('/usage', methods=['POST'])
@admin_or_charger_required()
def add_usage():
    # 获取参数
    meter_id = request.json.get('meterid')
    usetime = request.json.get('usetime')
    usedkilowatt = request.json.get('usedkilowatt')
    # 保存用电记录
    usage = ElectricityUsage(meter_id=meter_id, usetime=usetime, usedkilowatt=usedkilowatt)
    db.session.add(usage)
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='添加成功')


# - 用电记录查询接口:
# python


# 返回用电记录
@app.route('/electricity_usage')
@admin_or_charger_required()
def query_electricity_usage():
    usage = ElectricityUsage.query.all()
    result = ElectricityUsageSchema(many=True).dump(usage)
    return jsonify(result)

    # 获取参数
    # user_id = request.args.get('user_id')
    # start_time = request.args.get('start_time')
    # end_time = request.args.get('end_time')
    # # 参数校验
    # if start_time and end_time and start_time > end_time:
    #     return jsonify(errno=RET.PARAMERR, errmsg='start_time不能大于end_time')
    # # 查询用电记录
    # usage_list = []
    # if user_id:
    #     usage_list = ElectricityUsage.query.filter(ElectricityUsage.UserID == user_id).all()
    # if start_time and end_time:
    #     usage_list = ElectricityUsage.query.filter(
    #         ElectricityUsage.year.between(int(start_time), int(end_time)) &
    #         ElectricityUsage.month.between(int(start_time), int(end_time))
    #     ).all()
    # if not usage_list:
    #     return jsonify(errno=RET.NODATA, errmsg='无数据')
    # # 返回用电记录
    # return jsonify(
    #     errno=RET.OK,
    #     errmsg='OK',
    #     usage_records=[u.to_dict() for u in usage_list]
    # )


# - 用电记录导入接口:
# python


# 调用usp_import_electricityusage存储过程,导入用电记录
@app.route('/usage/import', methods=['POST'])
@admin_or_charger_required()
def import_usage():
    # 获取文件
    file = request.files.get('file')
    # 调用存储过程导入数据
    db.session.execute('CALL usp_import_electricityusage(:fileobj)', {'fileobj': file.stream})
    db.session.commit()
    # 返回成功
    return jsonify(errno=RET.OK, errmsg='导入成功')


# - 用电记录归档任务:
# python


# 每月1日调用usp_archive_usage存储过程,归档上月用电记录
@app.cli.command()
def archive_usage():
    # 调用存储过程归档上月用电记录
    print('归档上月用电记录...')
    db.session.execute('CALL usp_archive_usage()')
    db.session.commit()
    print('归档完成!')
