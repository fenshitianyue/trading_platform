var black_status = 0;
var jsonData = null;
var searchFlag = 0;
var cols = [
    {
        field: 'realName', align: 'center',
        title: '姓名', sortable: true
    },
    {
        field: 'createTime', align: 'center',
        title: '注册时间', sortable: true
    },
  
];

$(function () {

    load();
});

function load() {
    $('#exampleTable')
        .bootstrapTable(
            {
                method: 'post', // 服务器数据的请求方式 get or post
                url: "/myInvite", // 服务器数据的加载地址
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
                sortName: "createTime",
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


