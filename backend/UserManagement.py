from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import db_info


# 连接数据库
def connect_db():
    conn = mysql.connector.connect(
        host=db_info.host,
        user=db_info.user, 
        password=db_info.password,
        database=db_info.database
    )
    return conn

# 查找数据库中是否有此用户
def get_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# password_hash = generate_password_hash('123')
# print(password_hash)


# 登录函数
def user_login(username, password):
    user = get_user_by_username(username)
    if user is None:
        return False
    if not check_password_hash(user['hashed_password'], password):
        return False
    return True


# 注册函数
def user_register(username, password, phone=None):
    if get_user_by_username(username):
        return {'success': False, 'message': '用户已存在，请登录'}
    
    # 加密加密加密
    hashed_password = generate_password_hash(password)

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, hashed_password, phone) VALUES (%s, %s, %s)",
            (username, hashed_password, phone)
        )
        conn.commit()
        conn.close()
        return {'success': True, 'message': '注册成功'}
    except mysql.connector.Error as e:
        return {'success': False, 'message': f'数据库错误: {e}'}
    

# 修改密码函数
def change_password(username, old_password, new_password):
    # 验证原密码是否正确
    if not user_login(username, old_password):
        return {'success': False, 'message': '原密码错误'}
    
    # 对新密码进行哈希加密
    hashed_new_password = generate_password_hash(new_password)
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET hashed_password = %s WHERE username = %s",
            (hashed_new_password, username)
        )
        conn.commit()
        conn.close()
        return {'success': True, 'message': '密码修改成功'}
    except mysql.connector.Error as e:
        return {'success': False, 'message': f'数据库错误: {e}'}

# 测试
# print(user_login('xwl', '123456'))