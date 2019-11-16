from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import time
import hashlib

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

    return s.dumps(json_str).decode('utf-8')


def shop_login(request):

    return render(request,'shop/shop_login.html',locals())


def md5(data):
    res = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    return res


def deal_sso(request):
    message = {
        'token': '',
    }
    if request.method == 'POST':
        user_name = request.POST.get('user_name', '')
        user_passwd = request.POST.get('user_passwd', '')
        token = genTokenSeq(user_name, user_passwd, 'kechuangdata')
        message['token'] = token
        print(message)
    return JsonResponse(message)


def sso_callback(request):
    code = request.GET.get('code').strip()
    print(type(code),code)
    if code == '302' or code == '400':
        token = request.GET.get('token')
        res = HttpResponseRedirect('/shop/')
        res.set_cookie('token', token)
    elif code == '401' or code == '403' or code == '404':
        res = HttpResponseRedirect('/shop/shop_login/')
    else:
        print(code)
        res = HttpResponseRedirect('/shop/shop_register/')

    return res
