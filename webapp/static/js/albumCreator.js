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
                    '</div>',
                '</div>',
            '</div>'
        ]
    }

})(window.jQuery)