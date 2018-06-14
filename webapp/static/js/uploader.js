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
        url: '/shangshanfan/picture/uploadImage',
        title: '上传图片',
        multiple: false,
        onSuccess: function () {
            console.log('设置成功回调')
        },
        onError: function () {
            console.log('设置失败回调')
        }
    };

    $.fn.imgUploader.methods = {
        open: function (jq) {
            return jq.each(function (i, dom) {
                return showUploader(dom)
            })
        },
        close: function (jq) {
            return jq.each(function (i, dom) {
                return closeUploader(dom)
            })
        },
        clear: function (jq) {
            return jq.each(function (i, dom) {
                return clearUploader(dom)
            })
        },

    };


    function initHtml(jq) {
        var options = $(jq).data("options");
        var htmlStr = [
            '<div class="ss-uploader-frame" id="_uploadFrame">',
                '<div class="modal ss-uploader-modal" tabindex="-1" role="dialog">',
                    '<div class="modal-dialog" role="document">',
                        '<div class="modal-content">',
                            '<div class="modal-header">' ,
                                '<h5 class="modal-title">' + options.title + '</h5>' ,
                                '<button type="button" class="close" id="_uploadClose" data-dismiss="modal" aria-label="Close">',
                                    '<span aria-hidden="true">&times;</span>',
                                '</button>',
                            '</div>',
                            '<div class="modal-body">',
                                '<form onsubmit="return false" id="_uploadForm">',
                                    '<div class="form-group">' ,
                                        (options.multiple ?
                                                '<input type="file" name="image" class="form-control-file" id="_uploadInput" multiple="multiple">'
                                                :
                                                '<input type="file" name="image" class="form-control-file" id="_uploadInput">'
                                        ),
                                    '</div>',
                                '</form>',
                            '</div>',
                        '</div>',
                    '</div>',
                '</div>',
            '</div>'
        ]
        $(jq).append(htmlStr.join(""))
    }

    function bindEvent(jq) {
        var options = $(jq).data("options");
        $(jq).find('#_uploadInput').on("change", function (e) {
            $("#_uploadForm").ajaxSubmit({
                url: options.url,
                type: 'post',
                dataType: 'json',
                success: function (res) {
                    if (!res.errno) {
                        options.onSuccess(res);
                    }
                },
                error: function (err) {
                    options.onError(err)
                }
            })
        })

        $(jq).find('#_uploadClose').on("click", function (e) {
            $(jq).imgUploader('close')
        })
    }

    function showUploader(jq) {
        $(jq).find("#_uploadFrame").show()
    }
    function closeUploader(jq) {
        $(jq).find("#_uploadFrame").hide()
    }
    function clearUploader(jq) {
        $(jq).find("#_uploadInput").val('')
    }

})(window.jQuery);