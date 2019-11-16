get_cookie()
    function get_cookie() {
        var token = '';
        var cook=document.cookie.split(";");
        console.log(cook)
        for (var i in cook){
            var key = cook[i].split('=')[0]
            if(key == 'token'){
                token = cook[i].split('=')[1];
                break;
            }
            else {
                token = Math.random().toString().split('.')[1]
            }
        }
        if (token){
            window.location.href = 'http://127.0.0.1:8000/sso_temp?token=' + token + '&callback='+'http://10.10.14.182:80/shop/shop_login/callback';
        }
        else {
            window.location.href = 'http://127.0.0.1:8000/sso_temp?callback='+'http://10.10.14.182:80/shop/shop_login/callback';
        }
    }
