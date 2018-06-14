(function ($) {
    $.fn.albumCreator = function (action, params) {
        if (typeof  action == "string") {
            return $.fn.albumCreator.methods[action](this, params)
        }

        var _param = arguments[ arguments.length - 1];

        return this.each(function (index, dom) {
            var newParam = $.extend({}, $.fn.albumCreator.defaults, _param || {});
            // 把参数拼装后，存入本地；允许组件参数升级
            $(dom).data('options', newParam)
            initHtml($(dom));
            bindEvent($(dom));
        })
    };

    // 在点击按钮的时候发出请求，
    $.fn.albumCreator.defaults = {
        title: '',
        remark: '',
        tagId: 1,
        privacy: false,
        tagArr: [],
        onConfirm: function (res) {
            // 提交时，修改 update create

        },
        onCancel: function (res) {
            // 关闭弹窗
        },
    };
    
    $.fn.albumCreator.methods = {
        setContent: function(jq, data) {
            return jq.each(function (i, dom) {
                return setContent(dom, data)
            })
        },
        open: function (jq) {
            return jq.each(function (i, dom) {
                return showAlbumDetail(dom)
            })
        },
        close: function (jq) {
            return jq.each(function (i, dom) {
                return hideAlbumDetail(dom)
            })
        },
        clear: function (jq) {
            return jq.each(function (i, dom) {
                return clearAlbumDetail(dom)
            })
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
                                        '<label for="albumTitle">相册标题</label>',
                                        '<input type="text" name="title" value="' + options.title + '" class="form-control" id="albumTitle" placeholder="请输入相册标题">',
                                    '</div>',
                                    '<div class="form-group">',
                                        '<label for="albumTagId">关联类型</label>',
                                        '<select class="form-control" value="' + options.tagId + '" name="tagId" id="albumTagId">',
                                            '<option value="">请选择类型</option>',
                                            options.tagArr.map(function (tag) {
                                                if (tag.id === options.tagId ){
                                                    return '<option selected value="' + tag.id + '">' + tag.title + '</option>';
                                                }
                                                return '<option value="' + tag.id + '">' + tag.title + '</option>';
                                            }),
                                        '</select>',
                                    '</div>',
                                    '<div class="form-group">',
                                        '<div class="form-check">',
                                        (
                                            options.privacy ?
                                            '<input class="form-check-input" type="checkbox" id="privacyCheckbox" checked>'
                                            :
                                            '<input class="form-check-input" type="checkbox" id="privacyCheckbox">'
                                        ),
                                            '<label class="form-check-label" for="privacyCheckbox">是否公开</label>',
                                        '</div>',
                                    '</div>',
                                    '<div class="form-group">',
                                        '<label for="albumRemark">相册描述</label>',
                                        '<textarea name="remark" class="form-control" id="albumRemark" rows="3">' + options.remark + '</textarea>',
                                    '</div>',
                                '</form>',
                            '</div>',
                            '<div class="modal-footer">',
                                '<button type="button" id="_albumConfirm" class="btn btn-primary">保存</button>',
                                '<button type="button" id="_albumCancel" class="btn btn-default">取消</button>',
                            '</div>',
                        '</div>',
                    '</div>',
                '</div>',
            '</div>'
        ]
        $(jq).html(htmlStr.join(""))
    }

    function bindEvent(jq) {
        var options = $(jq).data("options");
        var $checkbox = $(jq).find('#privacyCheckbox');

        $(jq).find('#_albumConfirm').on('click', function () {
            var paramStr = $(jq).find('#_albumForm').serialize() +
                '&privacy=' + Number($checkbox[0].checked)
            return options.onConfirm(paramStr)
        })

        $(jq).find('#_albumCancel, #_albumClose').on('click', function () {
            $(jq).albumCreator('close')
        })
    }

    function setContent(jq, _data) {
        var options = $(jq).data("options");
        var newParam = $.extend({}, options, _data);
        $(jq).data('options', options);
        initHtml(jq)
        bindEvent(jq)
    }

    function showAlbumDetail(jq) {
        $(jq).find("#_albumDetail").show()
    }

    function hideAlbumDetail(jq) {
        $(jq).find("#_albumDetail").hide()
    }

    function clearAlbumDetail(jq) {
        $(jq).find("#_albumForm")[0].reset()
    }
})(window.jQuery)