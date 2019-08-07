$(function () {
    $('body')
    // 获取验证码
        .on('click', '.j-getCode', function (e) {
            var phone = $("#phone").val();
            if (phone == '') {
                layer.msg('请输入手机号', {icon: 5});
                return false;
            }
            var param = /^1[123456789]\d{9}$/;
            if (!param.test(phone) && $("#nation").val() == '86') {

                layer.msg('手机号不合法，请重新输入', {icon: 5});
                return false;
            }
//          var runTime = 60;
//          $('.j-getCode').attr('disabled', 'disabled');
//          $('.j-getCode').addClass('btn-default-disabled');
//          $('.j-getCode').val('验证码(' + runTime + 's)');
//          var interval = setInterval(function () {
//              runTime--;
//              $('.j-getCode').val('验证码(' + runTime + 's)');
//              if (runTime == 0) {
//                  $('.j-getCode').val('验证码');
//                  $('.j-getCode').removeAttr('disabled');
//                  $('.j-getCode').removeClass('btn-default-disabled');
//                  clearInterval(interval);
//              }
//          }, 1000);
//          $.ajax({
//              cache: true,
//              type: "POST",
//              url: "/tutorzzz/tutor/getPhoneCode",
//              data: {phone: phone,nation:$("#nation").val()},// 你的formid
//              async: false,
//              error: function (request) {
//                  layer.alert("Connection error");
//              },
//              success: function (data) {
//                  if (data.code == 0) {
//                      layer.msg('验证码发送成功', {icon: 1});
//
//                  } else {
//                      layer.msg(data.msg, {icon: 5});
//                  }
//
//              }
//          });
//          return false;
        });


    $("#registerId").on('click', function () {
        var username = $("#username").val().trim();
        /*  if (username == '') {
              layer.msg('请输入用户名', {icon: 5});
              return false;
          }
          var param = /^[A-Za-z0-9]{6,18}$/;
          if (!param.test(username)) {
              layer.msg('用户名不合法(数字字母，长度6-18位),请重新输入', {icon: 5});
              return false;
          }*/
        var password = $("#password").val().trim();
        if (password == '') {
            layer.msg('请输入密码', {icon: 5});
            return false;
        }
        param = /^[A-Za-z0-9]{6,18}$/;
        if (!param.test(password)) {
            layer.msg('密码不合法(数字字母,长度不能小于6位),请重新输入', {icon: 5});
            return false;
        }
        var cpassword = $("#cpass").val().trim();
        if (cpassword != password) {
            layer.msg('密码不一致', {icon: 5});
            return false;
        }

        var realName = $("#realName").val().trim();
        if (realName == '') {
            layer.msg('请输入姓名', {icon: 5});
            return false;
        }
        var school = $("#school").val().trim();
        if (school == '') {
            layer.msg('请输入学校', {icon: 5});
            return false;
        }
        var company = $("#company").val().trim();
        var wxId = $("#wxId").val().trim();
        if (wxId == '') {
            layer.msg('请输入微信号', {icon: 5});
            return false;
        }
        var research = $("#research").val().trim();
        if (research == '') {
            layer.msg('请输入研究方向', {icon: 5});
            return false;
        }
        var phone = $("#phone").val();
        if (phone == '') {
            layer.msg('请输入手机号', {icon: 5});
            return false;
        }
        param = /^1[123456789]\d{9}$/;
        if (!param.test(phone) && $("#nation").val() == '86') {
            // globalTip({'msg':'手机号不合法，请重新输入','setTime':3});
            layer.msg('手机号不合法，请重新输入', {icon: 5});
            return false;
        }
//      var code = $("#code").val();
//      if (code == '') {
//          layer.msg('请输入验证码', {icon: 5});
//          return false;
//      }
        var inviter = $("#inviter").val();

        var jsonData = {
            username: username,
            password: password,
            workStatus: $("#workStatus").val(),
            realName: realName,
            school: school,
            company: company,
            QQId: QQId,
            research: research,
            education: $("#education").val(),
            phone: phone,
            inviteCode: inviter,
//          code: code,
            nation:$("#nation").val()

        };
        $.ajax({
            cache: true,
            type: "POST",
            url: "/user/register",
            data: jsonData,// 你的formid
            async: false,
            error: function (request) {
                layer.alert("Connection error");
            },
            success: function (data) {
                if (data.code == 0) {
                    /* layer.confirm('提交成功，请耐心等待审核.', {icon: 1, btn: ['确定']}, function () {
                         window.location.href = '/login';
                     });*/
                    layer.open({
                        title: '温馨提示'
                        , content: '<h4>资料提交成功，请扫描微信二维码添加派单员微信号进行审核</h4>' +
                        '<div style="text-align: center"><img style="width: 197px;height: 197px;" src="/pic/KID.jpg" ></div>',
                        yes: function (index, layero) {
                            parent.layer.close(index);
                            window.location.href = '/login';
                        }
                    });
                } else {
                    layer.msg(data.msg, {icon: 5});
                }

            }
        });
    });
})
