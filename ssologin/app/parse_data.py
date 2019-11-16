import hashlib
import pymysql
from app import r


def md5(data):
    '''
    md5加密
    :param data: 需要加密的数据
    :return: 返回加密后的数据
    '''
    res = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    return res


def connect_mysql(db, user_name,ip,port,passwd):
    '''
    连接数据库
    :param db: 数据库名字
    :param user_name: 用户名
    :param ip: 数据库ip，
    :param port: 端口号
    :param passwd: 用户密码
    :return: 返回用户名
    '''
    if ip:
        connect = pymysql.connect(ip, 'root', passwd, db, charset='utf8', port=int(port))
    else:
        connect = pymysql.connect('127.0.0.1', 'root', '7890', db, charset='utf8', port=33060)
    cursor = connect.cursor()
    print('连接mysql成功')
    sql = "select user_passwd from userinfo where user_name='%s'"%str(user_name)
    cursor.execute(sql)
    res = cursor.fetchone()
    cursor.close()
    connect.close()
    return res[0]


def parse_token(res):
    '''
    验证密码
    :param res:解析后的令牌数据
    :return: 返回登录状态
    '''
    message = {
        'code': '401'
    }
    user_name = res[0]
    if user_name:
        password = res[1]
        dbt = res[2]
        db_list = dbt.split(':')
        print(db_list)
        if len(db_list) > 1:
            ip = db_list[0]
            port = db_list[1]
            passwd = db_list[2]
            db = db_list[3]

        else:
            db = db_list[0]
            ip = None
            port = None
            passwd = None
        try:
            passwd = connect_mysql(db, user_name, ip=ip, port=port, passwd=passwd)
        except:
            message['code'] = '402'
            return message
        else:
            if password == passwd:
                message['code'] = '400'
                ti = int(res[3])
                if ti > 3600:
                    ti = 3600
                r.set(md5(user_name), 'true', ex=ti)
            else:
                message['code'] = '403'

    return message