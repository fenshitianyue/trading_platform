$(function () {
    var tab = 'account_number';

    $('#num').keyup(function (event) {
        $('.tel-warn').addClass('hide');
        checkBtn();
    });

    $('#pass').keyup(function (event) {
        $('.tel-warn').addClass('hide');
        checkBtn();
    });

    $('#veri').keyup(function (event) {
        $('.tel-warn').addClass('hide');
        checkBtn();
    });

    $('#num2').keyup(function (event) {
        $('.tel-warn').addClass('hide');
        checkBtn();
    });

    $('#veri-code').keyup(function (event) {
        $('.tel-warn').addClass('hide');
        checkBtn();
    });

    // 按钮是否可点击
    function checkBtn() {
        $(".log-btn").off('click');
        var inp = $.trim($('#num').val());
        var pass = $.trim($('#pass').val());
        if (inp != '' && pass != '') {
            if (!$('.code').hasClass('hide')) {
                code = $.trim($('#veri').val());
                if (code == '') {
                    $(".log-btn").addClass("off");
                } else {
                    $(".log-btn").removeClass("off");
                    sendBtn();
                }
            } else {
                $(".log-btn").removeClass("off");
                sendBtn();
            }
        } else {
            $(".log-btn").addClass("off");
        }
    }

    function checkAccount(username) {
        if (username == '') {
            $('.num-err').removeClass('hide').find("em").text('请输入账户');
            return false;
        } else {
            $('.num-err').addClass('hide');
            return true;
        }
    }

    function checkPass(pass) {
        if (pass == '') {
            $('.pass-err').removeClass('hide').text('请输入密码');
            return false;
        } else {
            $('.pass-err').addClass('hide');
            return true;
        }
    }

    function checkCode(code) {
        if (code == '') {
            // $('.tel-warn').removeClass('hide').text('请输入验证码');
            return false;
        } else {
            // $('.tel-warn').addClass('hide');
            return true;
        }
    }

    function checkPhone(phone) {
        var status = true;
        if (phone == '') {
            $('.num2-err').removeClass('hide').find("em").text('请输入手机号');
            return false;
        }
        var param = /^1[34578]\d{9}$/;
        if (!param.test(phone)) {
            // globalTip({'msg':'手机号不合法，请重新输入','setTime':3});
            $('.num2-err').removeClass('hide');
            $('.num2-err').text('手机号不合法，请重新输入');
            return false;
        }
        $.ajax({
            url: '/checkPhone',
            type: 'post',
            dataType: 'json',
            async: false,
            data: {phone: phone, type: "login"},
            success: function (data) {
                if (data.code == '0') {
                    $('.num2-err').addClass('hide');
                    // console.log('aa');
                    // return true;
                } else {
                    $('.num2-err').removeClass('hide').text(data.msg);
                    // console.log('bb');
                    status = false;
                    // return false;
                }
            },
            error: function () {
                status = false;
                // return false;
            }
        });
        return status;
    }

    function checkPhoneCode(pCode) {
        if (pCode == '') {
            $('.error').removeClass('hide').text('请输入验证码');
            return false;
        } else {
            $('.error').addClass('hide');
            return true;
        }
    }

    // 登录点击事件
    function sendBtn() {
        $(".log-btn").click(function () {
            // var type = 'phone';
            var inp = $.trim($('#num').val());
            var pass = $.trim($('#pass').val());
            var params = {};
            params.username = inp;
            params.password = pass;
            if (checkAccount(inp) && checkPass(pass)) {
                if (!$('.code').hasClass('hide')) {
                    code = $.trim($('#veri').val());
                    if (!checkCode(code)) {
                        return false;
                    }
                    params.code = code;
                }

                $.ajax({
                    type: "POST",
                    url: "/user/login",
                    data: params,
                    success: function (r) { //这里要给参数r加上用户名接口，并且用ajax发送给main
                        if (r.code == 0) {
                        	$.ajax({
                        		type:"POST",
                        		async:false,
                        		
                        	})
                            parent.location.href = '/main';
                        } else {
                            layer.msg(r.msg);
                        }
                    }
                });
            } else {
                return false;
            }
        });
    }

    // 登录的回车事件
    $(window).keydown(function (event) {
        if (event.keyCode == 13) {
            $('.log-btn').trigger('click');
        }
    });


    $(".form-data").delegate(".send", "click", function () {
        var phone = $.trim($('#num2').val());
        if (checkPhone(phone)) {
            $.ajax({
                url: '/getcode',
                type: 'post',
                dataType: 'json',
                async: true,
                data: {phone: phone, type: "login"},
                success: function (data) {
                    if (data.code == '0') {

                    } else {

                    }
                },
                error: function () {

                }
            });
            var oTime = $(".form-data .time"),
                oSend = $(".form-data .send"),
                num = parseInt(oTime.text()),
                oEm = $(".form-data .time em");
            $(this).hide();
            oTime.removeClass("hide");
            var timer = setInterval(function () {
                var num2 = num -= 1;
                oEm.text(num2);
                if (num2 == 0) {
                    clearInterval(timer);
                    oSend.text("重新发送验证码");
                    oSend.show();
                    oEm.text("120");
                    oTime.addClass("hide");
                }
            }, 1000);
        }
    });

    var refreshCode = function () {
        $.ajax({
            url: '/admin/getCaptcha',
            type: 'GET',
            async: true,
            data: {},
            success: function (data) {
                $("#code_img").attr('src', data);
            },
            error: function () {
                status = false;
                // return false;
            }
        });
    }
    $("#code_img").on('click', function () {
        refreshCode();
    })

    refreshCode();

});
