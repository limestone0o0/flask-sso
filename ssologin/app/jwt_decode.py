from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature, BadData


def tokenAuth(token):
    '''
    解码jwt令牌数据，secret_key随意更改，和客户端一样即可
    :param token: jwt字符串
    :return: 返回解密后的数据
    '''
    s = Serializer(
        secret_key='4180da82-0c83-4d66-ab14-e2793573ecaa',
        salt='16fcf475-5180-4916-83c1-5ff79616eaa9')
    try:
        data = s.loads(token)
    except SignatureExpired:
        msg = 'token expired'
        return [None, msg]
    except BadSignature as e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                # the token is tampered.
                msg = 'token tampered'
                return [None, msg]
        msg = 'badSignature of token'

        return [None, msg]
    except:
        msg = 'wrong token with unknown reason'
        return [None, msg]
    if ('user_name' not in data) or ('user_passwd' not in data) or ('user_address' not in data):
        msg = 'illegal payload inside'
        return [None, msg]
    msg = 'user(' + data['user_name'] + ') logged in by token.'

    user_name = data['user_name']
    user_passwd = data['user_passwd']
    user_address = data['user_address']
    timeout = data['timeout']

    return [user_name, user_passwd, user_address, timeout, msg]
