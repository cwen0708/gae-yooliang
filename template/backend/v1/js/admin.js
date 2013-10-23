var editor_list = [];
var g_editor = null;

$(function(){
    try {
        google.load('picker', '1', { "callback": google_picker_after_load, 'language': 'zh-TW' });
    } catch(e) {

    }
    $(".btn-set-enable").live('click',function(){
        $(this).addClass("btn-success").next().removeClass("btn-danger");
    });
    $(".btn-set-disable").live('click',function(){
        $(this).addClass("btn-danger").prev().removeClass("btn-success");
    });
    $("#progress-box").remove();
});

gs.interact.afterLoad(function(){
    $("#uiContentTop").html("");
    $("#uiContentFooter").html("");
    var top_bar = $(".list-top-bar");
    $(".list-top-bar").remove();
    $("#uiContentTop").append(top_bar);
    var pagination = $(".pagination");
    $(".pagination").remove();
    pagination.removeClass("span9");
    $("#uiTopBar").append("<span id='page_title'></span>");
    if ($("body").data("sub_page_name") != undefined){
        $("#page_title").data("lang", $("body").data("sub_page_name"));
    }
    if (pagination != undefined){
        $("#uiTopBar").append(pagination);
    }
    var h1 = $("h1");
    $("h1").remove();
    if (h1.text() != undefined && h1.text() != ""){
        $("#page_title").data("lang", h1.text());
    }

    var manager_dir = $(".data-list").data("manager-dir");
    $(".data-list tbody").sortable({
        opacity: 0.6,
        //拖曳時透明
        cursor: 'move',
        //游標設定
        axis:'y',
        //只能垂直拖曳
        update : function () {
            var last_page_record = "";
            var $sort = $('.data-list tbody');
            $sort.find("tr").each(function() {
                if ($(this).data("id") != undefined) {
                    last_page_record += "rec[]=" + $(this).data("id") + "&";
                }
            });
            gs.ajax.json("/admin/record/sort.json", last_page_record + $sort.sortable('serialize') + "&t=" + manager_dir, function (data) {
                //pass
            }, function (data) {
                return false;
            });
        }
    });
    $(".data-row").each(function(){
        $(this).find(".btn-edit-page").data("page-url", "/admin/" + manager_dir.toLowerCase() + "/edit.html?id=" + $(this).data("id"));
        $(this).find(".btn-set-enable").data("json-url", "/admin/record/enable.json?id=" + $(this).data("id") + "&t=" + manager_dir);
        $(this).find(".btn-set-disable").data("json-url", "/admin/record/disable.json?id=" + $(this).data("id") + "&t=" + manager_dir);
        $(this).find(".btn-delete").data("json-url", "/admin/record/delete.json?id=" + $(this).data("id") + "&t=" + manager_dir);
    });
    $(".btn-set-enable.active").addClass("btn-success").next().removeClass("btn-danger");
    $(".btn-set-disable.active").addClass("btn-danger").prev().removeClass("btn-success");
    $(".btn-remove-image").live("click",function(){$(this).parent().remove();});
    hook_editor();
    build_pager();
    $(".record_already_delete").each(function(){
        try {
            set_show_already_delete($(this).data("id"));
        } catch(e) {
        }
    });
    gs.ui.refresh();
    if (gs.debug == true)
    {
        $("input").each(function(){
            if ($(this).val() == "")
            {
                $(this).val($(this).attr("name"));
            }
        });
        $("textarea").each(function(){
            if ($(this).val() == "")
            {
                $(this).val($(this).attr("name"));
            }
        });
    }
    $("img").one('load', function () {
        if ($(this).hasClass("scale")) {
            $(this).ScaleImg();
        };
    }).each(function () {
        if (this.complete) $(this).load();
    });
});

gs.interact.afterJson(function(data){
    if (data.action == null) { return; }
    if (data.action == "message") {
        art.dialog({
            title: gs.lang.getLocalization(data.info),
            content: gs.lang.getLocalization(data.content),
            time: 2,
            lock: true,
            drag: false,
            resize: false,
            fixed: true,
            follow: document.getElementById('btn2'),
            ok: function(){
                var list = art.dialog.list;
                for (var i in list) {
                    list[i].close();
                };
                gs.interact.reload();
                return false;
            }
        });
    }
    if (data.action == "delete"){
        set_show_already_delete(data.record.toString());
    }
    if (data.action == "recovery"){
        $(".data-row").each(function(){
           if ($(this).data("id") == data.record.toString()) {
               var tds = $(this).find("td");
               for(var i = 0;i<tds.length;i++)
               {
                   var r = tds.eq(i);
                   r.html(r.data("recovery-string"));
               }
                var manager_dir = $(".data-list").data("manager-dir");
                $(this).find(".btn-edit-page").data("page-url", "/admin/" + manager_dir.toLowerCase() + "/edit.html?id=" + $(this).data("id"));
                $(this).find(".btn-set-enable").data("json-url", "/admin/record/enable.json?id=" + $(this).data("id") + "&t=" + manager_dir);
                $(this).find(".btn-set-disable").data("json-url", "/admin/record/disable.json?id=" + $(this).data("id") + "&t=" + manager_dir);
                $(this).find(".btn-delete").data("json-url", "/admin/record/delete.json?id=" + $(this).data("id") + "&t=" + manager_dir);
               gs.ui.refresh();
           }
        });
    }
    if (data.action == "refresh"){
        gs.interact.reload();
    }
    if (data.action == "real_delete"){
        gs.interact.reload();
    }
});

gs.interact.beforeSubmit(function(){
    $('.editor').each(function () {
        var $textarea = $(this);
        if ($textarea.attr('id') != undefined){
            $textarea.val(CKEDITOR.instances[$textarea.attr('id')].getData());
        }
    });
});

gs.interact.afterSubmit(function(data){
    debugger;
    art.dialog({
        title: gs.lang.getLocalization(data.info),
        content: gs.lang.getLocalization(data.content),
        time: 2,
        lock: true,
        drag: false,
        resize: false,
        fixed: true,
        follow: document.getElementById('btn2'),
        ok: function(){
            var list = art.dialog.list;
            for (var i in list) {
                list[i].close();
            };
            return false;
        }
    });
});

function set_show_already_delete(id) {
    $("tr").each(function(){
        if ($(this).data("id") == id) {
            var length = $(this).find("td").length - 2;
            var tds = $(this).find("td");
            for(var i = 0;i<tds.length;i++)
            {
                var r = tds.eq(i);
                r.data("recovery-string",r.html());
                r.html("<br />");
            }
            tds.eq(0).html('#');
            var text_flag = true;
            $(this).find("td").each(function(){
                if ($(this).width() > 50 && text_flag == true){
                    $(this).html('<spna data-lang="already_delete"></span>');
                    text_flag = false;
                }
            });
            var data_list = $(".data-list");
            var real_delete_url = "/admin/record/real_delete.json?id=" + id + "&t=" + data_list.data("manager-dir");
            var recovery_url = "/admin/record/recovery.json?id=" + id + "&t=" + data_list.data("manager-dir");
            tds.eq(-2).html('<button type="button" class="btn" data-lang="real_delete" data-json-url="' + real_delete_url + '"></button>');
            tds.eq(-1).html('<button type="button" class="btn" data-lang="recovery" data-json-url="' + recovery_url + '"></button>');
            gs.ui.refresh();
        }
    });
}

// 建立分頁
var last_pager_c = 0;
function build_pager() {
    $(".pagination").each(function(){
        var page_all = parseInt($(this).data("page-all"));
        var page_now = parseInt($(this).data("page-now"));
        if (isNaN(page_all) == false && isNaN(page_now) == false)
        {
            var ul = $(this).find("ul").eq(0);
            for(var i=page_all;i>0;i--)
            {
                ul.prepend('<li><a href="#">' + i + '</a></li>');
            }
            last_pager_c = page_now;
            $(this).html('<ul></ul>');
            $(this).find("ul").paging(page_all, {
                format: "[nnnnnnnncn - <  > ]",
                perpage: 1,
                lapping: 0,
                page: page_now,
                onSelect: function (page) {
                    var temp_last_page = replace_url_param(gs.interact.getLastUrl(), "page", page);
                    if (last_pager_c != page) {
                        gs.interact.load(temp_last_page,true);
                    }
                },
                onFormat: function (type) {
                    switch (type) {
                        case 'block':
                            if (!this.active)
                                return '<li class="active"><a href="#">' + this.value + '</a></li>' + this.value + '</span> ';
                            else if (this.value != this.page)
                                return '<li><a href="#' + this.value + '">' + this.value + '</a></li>';
                            return '<li class="disabled"><a href="#' + this.value + '">' + this.value + '</a></li>';
                        case 'next':
                            if (this.active)
                                return '<li><a href="#">></a></li>';
                            return '<li><a href="#">></a></li>';
                        case 'prev':
                            if (this.active)
                                return '<li><a href="#"><</a></li>';
                            return '<li><a href="#"><</a></li>';
                        case 'first':
                            if (this.active)
                                return '';
                            return '';
                        case 'last':
                            if (this.active)
                                return '';
                            return '';
                        case "leap":
                            if (this.active)
                                return '<li class="disabled"><a href="#">...</a></li>';
                            return '';
                        case 'fill':
                            if (this.active)
                                return "";
                            return "";
                    }
                }
            });
        }

    });
}

// 替換 # 後面參數的值
function replace_url_param(url, name, newvalue) {
    url = url.replace("#/", "");
    var old = "";
    var m = url.substring(0, url.indexOf("?"));              //?前的文字
    var s = url.substring(url.indexOf("?"), url.length);     //?後的文字
    var j = 0;
    if (url.indexOf("?") >= 0) {
        var i = s.indexOf(name + "=");
        if (i >= 0) {
            j = s.indexOf("&", i);
            if (j >= 0) {
                old = s.substring(i + name.length + 1, j);
                s = url.replace(name + "=" + old, name + "=" + newvalue);
            } else {
                old = s.substring(i + name.length + 1, s.length);
                s = url.replace(name + "=" + old, name + "=" + newvalue);
            }
        } else {
            s = url + "&" + name + "=" + newvalue;
        }
    } else {
        s = url + "?" + name + "=" + newvalue;
    }
    return s;
}
var gp_last_editor = null;
function google_picker_after_load(){

}
function google_picker_before_editor_select() {
    var picker = new google.picker.PickerBuilder().
        addViewGroup(
            new google.picker.ViewGroup(google.picker.ViewId.PHOTOS).
                addView(google.picker.ViewId.PHOTO_ALBUMS).
                addView(google.picker.ViewId.PHOTOS).
                addView(google.picker.ViewId.PHOTO_UPLOAD)).
        setCallback(google_picker_after_editor_select).
        build();
    picker.setVisible(true);
}
function google_picker_after_editor_select(data) {
    if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
        var url = 'nothing';
        var doc = data[google.picker.Response.DOCUMENTS][0];
        url = doc[google.picker.Document.EMBEDDABLE_URL] || doc[google.picker.Document.URL];
        var doc2 = doc[google.picker.Document.THUMBNAILS];
        var thumbnail = doc2[0];
        url = thumbnail[google.picker.Thumbnail.URL];
        url = url.replace('/s32-c/','/w1000/');
        url = url.replace('https://','http://');
        var c = doc[google.picker.Document.URL];
        if (url == "nothing")
        {
            gs.alert.error("取得圖片時發生錯誤了");
        }else{
            gp_last_editor.insertHtml( '<img src="' + url + '">' );
        }
    }
}
// Create and render a Picker object for selecting documents
function createImagePicker() {
    var picker = new google.picker.PickerBuilder().
        addViewGroup(
            new google.picker.ViewGroup(google.picker.ViewId.DOCS).
                addView(google.picker.ViewId.FOLDERS).
                addView(google.picker.ViewId.IMAGE_SEARCH).
                addView(google.picker.ViewId.RECENTLY_PICKED).
                addView(google.picker.ViewId.DOCS_IMAGES)
        ).
        addViewGroup(
            new google.picker.ViewGroup(google.picker.ViewId.PHOTOS).
                addView(google.picker.ViewId.PHOTO_ALBUMS).
                addView(google.picker.ViewId.PHOTOS).
                addView(google.picker.ViewId.PHOTO_UPLOAD)).
        setCallback(pickerImageCallback).
        build();
    picker.setVisible(true);
}

// A simple callback implementation.
function pickerImageCallback(data) {
    if (data[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
        var url = 'nothing';
        var doc = data[google.picker.Response.DOCUMENTS][0];
        url = doc[google.picker.Document.EMBEDDABLE_URL] || doc[google.picker.Document.URL];
        var doc2 = doc[google.picker.Document.THUMBNAILS];
        var thumbnail = doc2[0];
        url = thumbnail[google.picker.Thumbnail.URL];
        url = url.replace('/s32-c/','/w1000/');
        url = url.replace('https://','http://');
        console.log(url);
        var c = doc[google.picker.Document.URL];

        if (url == "nothing")
        {
            gs.alert.error("取得圖片時發生錯誤了");
        }else{
            $(".google_image_picker_action").val(url).removeClass("google_image_picker_action");
        }
    }
}
// 載入編輯器
function hook_editor() {
    editor_list = [];
    $(".editor").each(function () {
        try {
            var editor = CKEDITOR.replace( $(this).attr("id"), {
                extraPlugins : 'gpimage',
                toolbar : 'Custom',
                font_names :'Arial/Arial; Helvetica; sans-serif;Comic Sans MS/Comic Sans MS; cursive;Courier New/Courier New; Courier; monospace;Georgia/Georgia; serif;Lucida Sans Unicode/Lucida Sans Unicode; Lucida Grande; sans-serif;Tahoma/Tahoma; Geneva; sans-serif;Times New Roman/Times New Roman; Times; serif;Trebuchet MS/Trebuchet MS; Helvetica; sans-serif;Verdana/Verdana; Geneva; sans-serif;細明體; 新細明體; 微軟正黑體; 微软雅黑; 標楷體; 宋体'
            });
        } catch (e) {
        }
    });
    $(".editor_image_upload").each(function () {
        var fix_val = $(this).find("input").val();
        fix_val = fix_val.replace('/s3000/','/w1000/');
        fix_val = fix_val.replace('/w1000/','/w1000/');
        fix_val = fix_val.replace('/w6000/','/w1000/');
        fix_val = fix_val.replace('/s6000/','/w1000/');
        fix_val = fix_val.replace('/s144/','/w1000/');
        $(this).find("input").val(fix_val);
        $(this).find(".btn").click(function () {
            try {
                var _this = $(this).parent();
                _this.find("input").addClass("google_image_picker_action");
                google.load('picker', '1', { "callback": createImagePicker, 'language': 'zh-TW' });
            } catch (e) {
            }
        });
        $(this).removeClass("editor_image_upload");
    });
    $(".editor_images_upload").each(function () {
        var fix_val = $(this).find("input").val();
        fix_val = fix_val.replace('/s3000/','/w1000/');
        fix_val = fix_val.replace('/w1000/','/w1000/');
        fix_val = fix_val.replace('/w6000/','/w1000/');
        fix_val = fix_val.replace('/s6000/','/w1000/');
        fix_val = fix_val.replace('/s144/','/w1000/');
        $(this).find("input").val(fix_val);
        $(this).find(".btn").click(function () {
            try {
                var _this = $(this).parent();
                var $imgs = $('<div class="input-append" style="width:100%;"><input class="span10" type="text" name="images"><button class="btn btn-remove-image" type="button" data-lang="image_remove" style="width:17.09401709401709%"></button></div>')
                $imgs.find("input").addClass("google_image_picker_action");
                $("#imgs").prepend($imgs);
                gs.ui.refresh();
                google.load('picker', '1', { "callback": createImagePicker, 'language': 'zh-TW' });

            } catch (e) {
            }
        });
        $(this).removeClass("editor_image_upload");
    });
    $(".editor_file_upload").each(function () {
        $(this).find(".btn").click(function () {
            var _this = $(this).parent();
            g_editor.loadPlugin('insertfile', function () {
                g_editor.plugin.fileDialog({
                    fileUrl: _this.find("input").val(),
                    clickFn: function (url, title) {
                        _this.find("input").val(url);
                        g_editor.hideDialog();
                    }
                });
            });
        });
        $(this).removeClass("editor_file_upload");
    });
}

/*
* jQuery image display plugin
* 圖片縮放顯示
* Version 1.03 (07/09/2012)
* @requires jQuery v1.4.2 or later
*
* Copyright (c) 2012 Qi-Liang Wen 啟良
*/
(function ($) {
    $.fn.ScaleImg = function (settings) {
        settings = jQuery.extend({
            width: 0,
            height: 0
        },
        settings);
        return this.each(function () {
            $(this).css("position", "relative").css("vertical-align", "text-top");
            var par = $(this).parent().get(0).tagName;
            if (par == "A") {
                if ($(this).parent().css('display') != "block") {
                    $par = $(this).parent().parent();
                } else {
                    $par = $(this).parent();
                }
            } else {
                $par = $(this).parent();
            }
            $par.css("vertical-align", "text-top").css("text-align", "left");
            var h = $par.height();  //外層容器高度
            var w = $par.width();     //外層容器寬度
            $.fn.ScaleImg.Run($(this), w, h);
            try {
                $(this).load(function () {
                    $.fn.ScaleImg.Run($(this), w, h);
                });
            } catch (e) {

            }
        });
    };
    $.fn.ScaleImg.Run = function ($this, parentWidth, parentHeight) {
        var src = $this.attr("src");
        var img = new Image();
        img.src = src;
        var w = 0;
        var h = 0;
        var _doScaling = function () {

            if (img.width > 0 && img.height > 0) {
                if (img.width / img.height >= parentWidth / parentHeight) {
                    if (img.width > parentWidth) {
                        w = parentWidth;
                        h = (img.height * parentWidth) / img.width;
                    }
                    else {
                        w = img.width;
                        h = img.height;
                    }
                }
                else {
                    if (img.height > parentHeight) {
                        w = (img.width * parentHeight) / img.height;
                        h = parentHeight;
                    }
                    else {
                        w = img.width;
                        h = img.height;
                    }
                }
            }
            $this.width(w);
            $this.height(h);
        };
        _doScaling();
        var loading = $("<span>Loading..</span>");
        $this.hide();
        $this.after(loading);
        loading.remove();
        $this.show();
        var objHeight = $this.height();  //圖片高
        var objWidth = $this.width();    //圖片寬

        if (objWidth > parentWidth) {
            $this.css("left", (objWidth - parentWidth) / 2);
        } else {
            $this.css("left", (parentWidth - objWidth) / 2);
        }
        if (objHeight > parentHeight) {
            $this.css("top", (objHeight - parentHeight) / 2);
        } else {
            $this.css("top", (parentHeight - objHeight) / 2);
        }
    }
})(jQuery);
