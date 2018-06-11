(function ($) {
    $.fn.albumCreator = function (action, params) {
        
    };

    // 在点击按钮的时候发出请求，
    $.fn.albumCreator.defaults = {
        onConfirm: function () {
            // 提交时，修改 update create
        },
        onCancel: function () {
            // 关闭弹窗
        },
    };
    
    $.fn.albumCreator.methods = {
        setContent: function(jq, data) {

        },
        open: function (jq) {
            
        },
        close: function (jq) {
            
        },
        clear: function (jq) {
            
        }
    }
    
    function initHtml(jq) {
        var options = $(jq).data("options");
        var htmlStr = [
            '<div class="ss-albumDetail-frame" id="_albumDetail">',
                '<div class="modal ss-albumDetail-modal" tabindex="-1" role="dialog">',
                    '<div class="modal-dialog" role="document">',
                        '<div class="modal-content">',
                            '<div class="modal-header">' ,
                                '<h5 class="modal-title">相册详情</h5>' ,
                                '<button type="button" class="close" id="_albumClose" data-dismiss="modal" aria-label="Close">',
                                    '<span aria-hidden="true">&times;</span>',
                                '</button>',
                            '</div>',
                            '<div class="modal-body">',
                                '<form onsubmit="return false" id="_albumForm">',
                                    '<div class="form-group">',
                                        '<label for="albumTitle">Email address</label>',
                                        '<input type="text" name="title" class="form-control" id="albumTitle" placeholder="请输入相册标题">',
                                    '</div>',
                                    '<div class="form-group">',
                                        '<label for="albumTagId">Example multiple select</label>',
                                        '<select class="form-control" name="tagId" id="albumTagId">',
                                            '<option>1</option>',
                                        '</select>',
                                    '</div>',
                                    '<div class="form-group">',
                                        '<label for="albumRemark">Example textarea</label>',
                                        '<textarea name="remark" class="form-control" id="albumRemark" rows="3" />',
                                    '</div>',
                                '</form>',
                            '</div>',
                            '<div class="modal-footer">',
                                '<button type="button" id="_albumConfirm" class="btn btn-primary">保存</button>',
                                '<button type="button" id="_albumCancel" class="btn btn-default" data-dismiss="modal">取消</button>',
                            '</div>',
                        '</div>',
                    '</div>',
                '</div>',
            '</div>'
        ]
    }

})(window.jQuery)