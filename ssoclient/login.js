function login_to_sso(){
        var  user_name = $('#email').val();
        var  user_passwd = $('#password').val();
        var sid = '';

       var data = {
           'user_name': user_name,
           'user_passwd': user_passwd,
           'csrfmiddlewaretoken': '{{ csrf_token }}'
       }

            $.ajax(
                {
                    url:'/shop/deal_sso/',
                    type:'POST',
                    data:data,
                    async:false,
                    success:function (data) {
                        window.location.href = 'http://127.0.0.1:8000/sso_temp?token=' + data.token + '&callback='+'http://10.10.14.182:80/shop/shop_login/callback';

                    },
                    error:function (err) {

                    }
                })


            }