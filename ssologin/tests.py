from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time


def genTokenSeq(name, passwd, address, expires=300):
    '''
    加密数据为jwt字符串
    :param name: 用户名
    :param passwd: 用户密码
    :param address: 服务器地址
    :param expires: 过期时间，默认5分钟，单位：秒
    :return: 返回字节流字符串
    salt:随机字符串，默认不可变，更改需要与服务器沟通
    secret_key:秘钥，默认不可变，更改需要与服务器沟通
    '''
    s = Serializer(
        salt='16fcf475-5180-4916-83c1-5ff79616eaa9',
        secret_key='4180da82-0c83-4d66-ab14-e2793573ecaa',
        expires_in=expires
    )
    timestamp = time.time()
    json_str = {
         'user_name': name,
         'user_passwd': passwd,
         'user_address': address,
         'timeout': expires,
         'iat': timestamp
    }

    return s.dumps(json_str)


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature, BadData


def tokenAuth(token):
    '''
    解码jwt数据
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

    return [user_name, user_passwd, user_address, msg]


if __name__ == '__main__':

    s = genTokenSeq('xx','m',120)
    print(s.decode('utf-8'))
    t = s.decode('utf-8')
    s = tokenAuth(t)
    print(s)
    # print(uuid.uuid4())
# eyJhbGciOiJIUzUxMiIsImV4cCI6MTU3MzcxMTU3NSwiaWF0IjoxNTczNzExMjc1fQ.eyJ0aW1lb3V0IjozMDAsImlhdCI6MTU3MzcxMTI3NS42NzQxNTkzLCJ1c2VyX2FkZHJlc3MiOjEyMCwidXNlcl9wYXNzd2QiOiJtIiwidXNlcl9uYW1lIjoieHgifQ.arsgSYHZlJ2-c4-ENZ9-vwsSfaAiA2xHD05AaZBO_xK62M-y75RXTc06-Ro5TdNvClG4J6xmuNrqtIL3IQQCjA
# eyJpYXQiOjE1NzM3MTEyOTEsImV4cCI6MTU3MzcxMTU5MSwiYWxnIjoiSFM1MTIifQ.eyJ1c2VyX25hbWUiOiJ4eCIsImlhdCI6MTU3MzcxMTI5MS43MDAwNzYsInVzZXJfcGFzc3dkIjoibSIsInVzZXJfYWRkcmVzcyI6MTIwLCJ0aW1lb3V0IjozMDB9.ELUjsZn2y6KwGior4Fd_BowD5kZDph0PxN1qs_fENnSN3GPYzIKWPoTYoH-v4L8qVOsmx2b9CIzKVkuqhhDdsQ
