//var prefix = "/ITKIM/tutor";
var black_status = 0;
var jsonData = null;
var searchFlag = 0;
var cols = [
    {
        field: 'id', align: 'center',
        title: '编号', sortable: true
    },
    {
        field: 'subTutor', align: 'center',
        title: '姓名', sortable: true
    },
    {
        field: 'finishTime', align: 'center',
        title: '完成时间', sortable: true
    },
    {
        field: 'rewardFee', align: 'center',
        title: '奖励金额', sortable: true
    },
    {
        title: '操作',
        field: 'id',
        align: 'center',
        formatter: function (value, row, index) {
            if (row.status == 0) {
                return '<a class="btn btn-primary btn-sm " href="#" mce_href="#" title="申请结算" onclick="settleReward(\''
                    + row.id
                    + '\')"><i class="fa fa-diamond"></i></a> ';
            }
            if (row.status == 1) {
                return '<span style="color:orange"><strong>申请中</strong></span>';
            }
            if (row.status == 2) {
                return '<span style="color:green"><strong>已申请</strong></span>';
            }
            return '无';
        }
    }
];

$(function () {

    load();
});

function load() {
    $('#exampleTable')
        .bootstrapTable(
            {
                method: 'post', // 服务器数据的请求方式 get or post
                //url: prefix + "/myReward", // 服务器数据的加载地址
                url: "/myReward", // 服务器数据的加载地址
                showRefresh: true,
                showToggle: true,
                showColumns: true,
                iconSize: 'outline',
                toolbar: '#exampleToolbar',
                striped: true, // 设置为true会有隔行变色效果
                dataType: "json", // 服务器返回的数据类型
                pagination: true, // 设置为true会在底部显示分页条
                singleSelect: false, // 设置为true将禁止多选
                // contentType : "application/x-www-form-urlencoded",
                // //发送到服务器的数据编码类型
                pageSize: 10, // 如果设置了分页，每页数据条数
                pageNumber: 1, // 如果设置了分布，首页页码
                //search : true, // 是否显示搜索框
                showColumns: false, // 是否显示内容下拉框（选择显示的列）
                sidePagination: "server", // 设置在哪里进行分页，可选值为"client" 或者 "server"
                queryParamsType: "",
                // //设置为limit则会发送符合RESTFull格式的参数
                sortOrder: "asc", //排序方式
                sortName: "finishTime",
                queryParams: initParams,
                // //请求服务器数据时，你可以通过重写参数的方式添加一些额外的参数，例如 toolbar 中的参数 如果
                // queryParamsType = 'limit' ,返回参数必须包含
                // limit, offset, search, sort, order 否则, 需要包含:
                // pageSize, pageNumber, searchText, sortName,
                // sortOrder.
                // 返回false将会终止请求
                responseHandler: function (res) {
                    return {
                        "total": res.data.total,//总数
                        "rows": res.data.data   //数据
                    };
                },
                columns: cols
            });
}

function reLoad() {
    $('#exampleTable').bootstrapTable('refresh');
}

function search() {
    var optionData = {pageNumber: 1}
    if (review_status != '') {
        optionData.reviewStatus = review_status;
    }
    if ($("#condition_id").val() != '-1' && $("#searchName").val().trim() != '') {
        optionData[$("#condition_id").val()] = $("#searchName").val().trim();
        searchFlag = 1;
    } else {
        searchFlag = 0;
    }

    $("#exampleTable").bootstrapTable("refreshOptions", optionData);
    reLoad();
}

function initParams(params) {
    jsonData = { //说明：传入后台的参数包括offset开始索引，limit步长，sort排序列，order：desc或者,以及所有列的键值对
        pageNumber: params.pageNumber,
        pageSize: params.pageSize,
        sortField: params.sortName,
        order: params.sortOrder
    };
    if ($("#condition_id").val() != '-1' && $("#searchName").val().trim() != '' && searchFlag == 1) {
        jsonData[$("#condition_id").val()] = $("#searchName").val().trim();
    }

    return jsonData;
}


function settleReward(id) {

    layer.open({
        type: 2,
        title: '申请奖励' + id + '结算',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['70%', '80%'],
        content: "/ITKIM/settleRecord/settleReward/" + id
    });
}

function batchSettleReward(id) {



    $.ajax({
        cache: true,
        type: "POST",
        url: "/ITKIM/settleRecord/checkBatchSettleReward",
        data: {},// 你的formid
        async: false,
        error: function (request) {
            parent.layer.alert("Connection error");
        },
        success: function (data) {
            if (data.code == 0) {
                var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
                parent.layer.close(index);

                layer.confirm("确认要结算所有奖励吗?", {
                    btn: ['确定', '取消']
                    // 按钮
                }, function (index, layero){
                    layer.close(index); //如果设定了yes回调，需进行手工关闭
                    layer.open({
                        type: 2,
                        title: '申请所有奖励',
                        maxmin: true,
                        shadeClose: false, // 点击遮罩关闭层
                        area: ['70%', '80%'],
                        content: "/ITKIM/settleRecord/batchSettleReward"
                    });
                }, function () {

                });

            } else {
                parent.layer.alert(data.msg)
            }

        }
    });



}
