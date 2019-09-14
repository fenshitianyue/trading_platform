var prefix = '/orders';
var searchFlag = 0;
var cols = [
    {
        field: 'id',
        title: '订单编号', sortable: true
    },
    {
        field: 'title',
        title: '标题', sortable: true
    },
    {
        field: 'publishTime',
        title: '发布时间', sortable: true
    },
    {
        field: 'dueTime',
        title: '交付时间', sortable: true,
        formatter: function (value, row, index) {
            return '<span style="color:red;"><strong>' + value + '</strong></span>';
        }
    },

    {
        field: 'orderTag',
        title: '开发语言', sortable: true
    },
    {
        field: 'requireType',
        title: '需求类型', sortable: true
    },
    {
        field: 'devPrice',
        title: '开发价格', sortable: true,
        formatter: function (value, row, index) {
            return '<span style="color:red;"><strong>&yen' + value + '</strong></span>';
        }
    },
    {
        field: 'docFilePath',
        title: '需求文档', sortable: true,
        formatter: function (value, row, index) {
            if (value == '' || value == null) {
                return '无';
            }
            return '<a href="' + value + '" class="btn btn-primary btn-sm" target="_blank">需求文档</a>';

        }
    },
    {
        field: 'allFilePath',
        title: '附件', sortable: true,
        formatter: function (value, row, index) {
            if (value == '' || value == null) {
                return '无';
            }
            return '<a href="' + value + '" class="btn btn-primary btn-sm">附件</a>';
        }
    },
    {
        title: '操作',
        field: 'id',
        align: 'center',
        formatter: function (value, row, index) {
            if (row.billStatus == 0) {
                if (row.isBillable == 1) {
                    return '<a class="btn btn-primary btn-sm " href="#" mce_href="#" title="申请结算" onclick="settleOrder(\''
                        + row.id
                        + '\')"><i class="fa fa-diamond"></i></a> ';
                }
                if (row.isBillable == 0) {
                    {
                        return '<a class="btn btn-primary btn-sm" disabled="disabled" href="#" mce_href="#" title="等待售后完成"><i class="fa fa-diamond"></i></a> ';
                    }
                }
            } else {
                return '<span style="color:green"><strong>已申请</strong></span>';
            }
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
                url: prefix + "/finishOrders", // 服务器数据的加载地址
                showRefresh: true,
                showToggle: true,
                showColumns: true,
                iconSize: 'outline',
                toolbar: '#exampleToolbar',
                striped: true, // 设置为true会有隔行变色效果
                dataType: "json", // 服务器返回的数据类型
                pagination: true, // 设置为true会在底部显示分页条
                singleSelect: false, // 设置为true将禁止多选
                // //发送到服务器的数据编码类型
                contentType: "application/json",
                pageSize: 10, // 如果设置了分页，每页数据条数
                pageNumber: 1, // 如果设置了分布，首页页码
                //search : true, // 是否显示搜索框
                showColumns: false, // 是否显示内容下拉框（选择显示的列）
                sidePagination: "server", // 设置在哪里进行分页，可选值为"client" 或者 "server"
                queryParamsType: "",
                // //设置为limit则会发送符合RESTFull格式的参数
                sortOrder: "desc", //排序方式
                sortName: "id",
                queryParams: initParams,
                // //请求服务器数据时，你可以通过重写参数的方式添加一些额外的参数，例如 toolbar 中的参数 如果
                // queryParamsType = 'limit' ,返回参数必须包含
                // limit, offset, search, sort, order 否则, 需要包含:
                // pageSize, pageNumber, searchText, sortName,
                // sortOrder.
                // 返回false将会终止请求
                responseHandler: function (res) {
                    return {
                        "total": res.total,//总数
                        "rows": res.data   //数据
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

    var jsonData = { //说明：传入后台的参数包括offset开始索引，limit步长，sort排序列，order：desc或者,以及所有列的键值对
        pageNumber: params.pageNumber,
        pageSize: params.pageSize,
        sortField: params.sortName,
        order: params.sortOrder,

    };
    if ($("#condition_id").val() != '-1' && $("#searchName").val().trim() != '' && searchFlag == 1) {
        jsonData[$("#condition_id").val()] = $("#searchName").val().trim();
    }
    return jsonData;
}

function settleOrder(id) {

    layer.open({
        type: 2,
        title: '申请订单' + id + '结算',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['70%', '80%'],
        content: "/settleRecord/settle/" + id
    });
}
