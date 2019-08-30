var prefix = "/notice"
$(function () {
    load();
});

function load() {
    $('#exampleTable')
        .bootstrapTable(
            {
                method: 'post', // 服务器数据的请求方式 get or post
                url: prefix + "/list", // 服务器数据的加载地址
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
                pageSize: 10, // 如果设置了分页，每页数据条数
                pageNumber: 1, // 如果设置了分布，首页页码
                //search : true, // 是否显示搜索框
                showColumns: false, // 是否显示内容下拉框（选择显示的列）
                sidePagination: "server", // 设置在哪里进行分页，可选值为"client" 或者 "server"
                queryParamsType: "",
                // //设置为limit则会发送符合RESTFull格式的参数
                sortOrder: "desc", //排序方式
                sortName: "createTime",
                queryParams: function (params) {
                    return {
                        pageNumber: params.pageNumber,
                        pageSize: params.pageSize,
                        sortField: params.sortName,
                        order: params.sortOrder
                    };
                },
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
                columns: [
                    {
                        field: 'title', sortable: true,
                        title: '标题',
                        formatter: function (value, row, index) {
                            if (row.status == 0) {
                                return '<span style="color: red">*</span>' + value;
                            }
                            return value;
                        }
                    },
                    {
                        field: 'content', sortable: true,
                        title: '内容'
                    },

                    {
                        field: 'status',
                        title: '阅读状态', sortable: true,
                        formatter: function (value, row, index) {
                            if (value == 0) {
                                return '未阅读';

                            } else {
                                return '已阅读';
                            }
                        }
                    },
                    {
                        field: 'createTime', sortable: true,
                        title: '通知时间'
                    },
                    {
                        title: '操作',
                        field: 'id',
                        align: 'center',
                        formatter: function (value, row, index) {

                            var d = '<a class="btn btn-primary btn-sm " href="#" title="查看通知"  mce_href="#" ' +
                                'onclick="view(\'' + row.id + '\',\'' + row.title + '\',\'' + row.content + '\',\'' + row.status + '\')"><i class="fa fa-envelope-open-o"></i></a> ';
                            return d;
                        }
                    }]
            });
}

function reLoad() {
    $('#exampleTable').bootstrapTable('refresh');
}

function view(id, title, content, status) {
    layer.open({
        title: title,
        content: content,
        yes: function (index, layero) {
            if (status == 1) {
                layer.close(index);
            } else {
                $.ajax({
                    cache: false,
                    type: "POST",
                    url: prefix + '/read/' + id,
                    data: {},
                    error: function (request) {
                        parent.layer.alert("Connection error");
                    },
                    success: function (data) {
                        if (data.code == 0) {
                            reLoad();
                        }
                        layer.close(index); //如果设定了yes回调，需进行手工关闭

                    }
                });
            }


        }
    });
}
