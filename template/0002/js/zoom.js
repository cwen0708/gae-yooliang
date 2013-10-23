/*
* jQuery image display plugin
* 圖片縮放顯示
* Version 1.03 (07/09/2012)
* @requires jQuery v1.4.2 or later
*
* Copyright (c) 2012 Qi-Liang Wen 啟良
*/
(function ($) {
    /*
    if(!(window.jQuery && window.jQuery.fn.jquery == '1.8.1'))
    {
     var element = document.createElement('script');
     element.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js');
     element.setAttribute('type', 'text/javascript');
     document.getElementsByTagName('head')[0].appendChild(element);
    }
    $(".jfk-checkbox-checkmark").click();
    */
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

$(document).ready(function () {
    $(".scale").hide();
    $(".scale").ScaleImg();
});
