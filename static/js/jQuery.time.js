//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function () {
    // if(animating) return false;
    // animating = true;
    current_fs = $(this).parent();
    next_fs = $(this).parent().next();
    if (current_fs.attr('id') == 'fieldset1') {
        if ($("#msform").data('bootstrapValidator')) {
            $("#msform").data('bootstrapValidator').destroy();
            $('#msform').data('bootstrapValidator', null);
        }
        formValidator1();

    } else if (current_fs.attr('id') == 'fieldset2') {
        $("#msform").data('bootstrapValidator').destroy();
        $('#msform').data('bootstrapValidator', null);
        formValidator2();
    } else if (current_fs.attr('id') == 'fieldset3') {
        $("#msform").data('bootstrapValidator').destroy();
        $('#msform').data('bootstrapValidator', null);
        formValidator3();
    }
    if (current_fs.attr('id') == 'fieldset1') {
        $.ajax({
            cache: true,
            type: "POST",
            url: "/user/checkUsername",
            data: {username: $("#username").val()},// 你的formid
            async: false,
            error: function (request) {
                layer.alert("Connection error");
            },
            success: function (data) {
                if (data.valid) {
                    nextTab();
                } else {
                    layer.msg('用户名已存在', {icon: 5});
                }

            }
        });

    }else{
        nextTab();

    }

});

function nextTab() {
    var bootstrapValidator = $("#msform").data('bootstrapValidator');
    bootstrapValidator.validate();
    console.log(bootstrapValidator.getInvalidFields())
    if (!bootstrapValidator.isValid()) {
        return;
    } else { // 验证通过
        console.log("下一个")
        //activate next step on progressbar using the index of next_fs
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

        //show the next fieldset
        next_fs.show();
        //hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function (now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50) + "%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({'transform': 'scale(' + scale + ')'});
                next_fs.css({'left': left, 'opacity': opacity});
            },
            duration: 800,
            complete: function () {
                current_fs.hide();
                // animating = false;
            },
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });
    }
}

$(".previous").click(function () {
    if (animating) return false;
    animating = true;

    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

    //show the previous fieldset
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({opacity: 0}, {
        step: function (now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1 - now) * 50) + "%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({'left': left});
            previous_fs.css({'transform': 'scale(' + scale + ')', 'opacity': opacity});
        },
        duration: 800,
        complete: function () {
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

$(".submit").click(function () {
    return false;
})

function formValidator1() {
    $('#msform').bootstrapValidator({
        excluded: [":disabled"],
        message: 'This value is not valid',
        verbose: false,
        fields: {
            username: {
                validators: {
                    notEmpty: {
                        message: "请输入用户名"
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: '用户名必须6位以上'
                    },
                    regexp: {
                        regexp: /^[A-Za-z0-9]{6,18}$/,
                        message: '用户名只能是数字字母组合'
                    }
                }
            },
            // 密码验证
            password: {
                validators: {
                    notEmpty: {
                        message: "请输入密码"
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: '密码必须6位以上'
                    },
                    regexp: {
                        regexp: /^[A-Za-z0-9]{6,18}$/,
                        message: '密码不合法(数字字母,长度不能小于6位),请重新输入'
                    }
                }
            },
            //
            cpass: {
                validators: {
                    notEmpty: {
                        message: "请输入密码"
                    },
                    callback: {
                        message: '密码不一致',
                        callback: function (value, validator) {
                            if (value != $('#password').val().trim()) {
                                return false;
                            }
                            return true;
                        }
                    }
                }
            }
        }
    });
}

function formValidator2() {
    $('#msform').bootstrapValidator({
        excluded: [":disabled"],
        message: 'This value is not valid',
        verbose: false,
        fields: {
            // 姓名
            realName: {
                validators: {
                    notEmpty: {
                        message: "请输入姓名"
                    }
                }
            },
            // 学校
            school: {
                validators: {
                    notEmpty: {
                        message: "请输入学校"
                    }
                }
            },
            // 公司
//          company: {
//              validators: {
//                  notEmpty: {
//                      message: "请输入公司"
//                  }
//              }
//          },
            // 微信
            wxId: {
                validators: {
                    notEmpty: {
                        message: "请输入微信"
                    }
                }
            },
            // 研究方向
            research: {
                validators: {
                    notEmpty: {
                        message: "请输入研究方向"
                    }
                }
            }
        }
    });
}

function formValidator3() {
    $('#msform').bootstrapValidator({
        excluded: [":disabled"],
        message: 'This value is not valid',
        fields: {
            // 手机号
            phone: {
                validators: {
                    notEmpty: {
                        message: "请输入姓名"
                    }
                }
            },
            // 验证码
            code: {
                validators: {
                    notEmpty: {
                        message: "请输入验证码"
                    }
                }
            }
        }
    });
}