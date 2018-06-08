(function ($) {
    $.fn.imgUploader = function (action, params) {
        if (typeof  action == "string") {
            return $.fn.imgUploader.methods[action](this, params)
        }

        var _param = arguments[ arguments.length - 1];

        return this.each(function (index, dom) {
            var newParam = $.extend({}, $.fn.imgUploader.defaults, _param || {})
            // 把参数拼装后，存入本地；允许组件参数升级
            $(dom).data('options', newParam)

            initHtml($(dom));
            bindEvent($(dom));
        })
    };

    $.fn.imgUploader.defaults = {

    };

    $.fn.imgUploader.methods = {
        open: function () {

        },
        close: function () {

        },
        _clear: function () {

        },
        onFinish: function () {

        }

    };


    function initHtml(jq) {
        var options = $(jq).data("options")
        var htmlStr = [
            '<div class="ss-uploader-frame">',
                '<div>',
                '</div>',
            '</div>'
        ]
    }

    function bindEvent(jq) {

    }

    function showUploader() {

    }
    function closeUploader() {

    }


})(window.jQuery);