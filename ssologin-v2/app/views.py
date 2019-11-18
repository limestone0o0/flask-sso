from flask import Response, request, jsonify, render_template
from manage import app
from app.models import *
from app.jwt_decode import tokenAuth
from app import r
from app.parse_data import md5, parse_token


@app.route('/', endpoint='index')
def index():

    return Response('success')


@app.route('/sso_temp', endpoint='sso_temp')
def sso_temp():
    token = request.args.get('token', '')
    callback = request.args.get('callback', '')

    return render_template('temp.html', **locals())


@app.route('/verify/', endpoint='verify', methods=['GET', 'POST'])
def verify():
    '''
    验证
    :return:返回验证代码
    '''
    message = {
        'code': '401',
        'msg': 'false'
    }
    token = request.form.get('token')
    if not token:
        token = request.cookies.get('token', '')
        if not token:
            return jsonify(message)

    res = tokenAuth(token)
    if res[0]:
        user_name = res[0]
        sid = r.get(md5(user_name))
        if sid and sid.decode('utf-8') == 'true':
            message['code'] = '302'
            message['token'] = token
            result = jsonify(message)
            result.set_cookie('token', token)
            return result

    message = parse_token(res)
    if message['code'] == '400':
        message['token'] = token
        result = jsonify(message)
        result.set_cookie('token', token)
        return result

    print(message)
    return jsonify(message)


@app.route('/server_register/', endpoint='registers', methods=['POST'])
def registers():
    '''
    注册服务器
    :return: 返回注册状态
    '''
    message = {
        'code': '406',
        'msg': '访问错误'
    }
    if request.method == 'POST':
        if request.data.get('user_token') and request.data.get('user_token') == 'xxmshuai':
            user_name = request.data.get('user_name', '')
            if user_name:
                u_data = User.query.filter_by(user_name=user_name)
                if not u_data:
                    u = User()
                    u.user_name = user_name
                    u.user_address = request.data.get('user_address')
                    u.user_token = 'xxmshuai'
                    db.session.add(u)
                    db.session.commit()
                    message['code'] = '200'
                    message['msg'] = '注册成功'
                    return jsonify(message)

                else:
                    message['code'] = '206'
                    message['msg'] = '已经注册过'
                    return jsonify(message)

    return jsonify(message)


