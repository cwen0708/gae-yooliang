// jQuery paging plugin
// 分頁顯示元件
// Version 1.01 (08/14/2013)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2013 Qi-Liang Wen 啟良
(function(k,p,n){k.fn.paging=function(v,w){var t=this,s={setOptions:function(b){this.a=k.extend(this.a||{lapping:0,perpage:10,page:1,refresh:{interval:10,url:null},format:"",onFormat:function(){},onSelect:function(){return!0},onRefresh:function(){}},b||{});this.a.lapping|=0;this.a.perpage|=0;null!==this.a.page&&(this.a.page|=0);1>this.a.perpage&&(this.a.perpage=10);this.k&&p.clearInterval(this.k);this.a.refresh.url&&(this.k=p.setInterval(function(b){k.ajax({url:b.a.refresh.url,success:function(g){if("string"===typeof g)try{g=k.parseJSON(g)}catch(f){return}b.a.onRefresh(g)}})},1E3*this.a.refresh.interval,this));this.l=function(b){for(var g=0,f=0,h=1,d={e:[],h:0,g:0,b:5,d:3,j:0,m:0},a,l=/[*<>pq\[\]().-]|[nc]+!?/g,k={"[":"first","]":"last","<":"prev",">":"next",q:"left",p:"right","-":"fill",".":"leap"},e={};a=l.exec(b);){a=""+a;if(n===k[a])if("("===a)f=++g;else if(")"===a)f=0;else{if(h){if("*"===a){d.h=1;d.g=0}else{d.h=0;d.g="!"===a.charAt(a.length-1);d.b=a.length-d.g;if(!(d.d=1+a.indexOf("c")))d.d=1+d.b>>1}d.e[d.e.length]={f:"block",i:0,c:0};h=0}}else{d.e[d.e.length]={f:k[a],i:f,c:n===e[a]?e[a]=1:++e[a]};"q"===a?++d.m:"p"===a&&++d.j}}return d}(this.a.format);return this},setNumber:function(b){this.o=n===b||0>b?-1:b;return this},setPage:function(b){function q(b,a,c){c=""+b.onFormat.call(a,c);l=a.value?l+c.replace("<a",'<a data-page="'+a.value+'"'):l+c}if(n===b){if(b=this.a.page,null===b)return this}else if(this.a.page==b)return this;this.a.page=b|=0;var g=this.o,f=this.a,h,d,a,l,r=1,e=this.l,c,i,j,m,u=e.e.length,o=u;f.perpage<=f.lapping&&(f.lapping=f.perpage-1);m=g<=f.lapping?0:f.lapping|0;0>g?(a=g=-1,h=Math.max(1,b-e.d+1-m),d=h+e.b):(a=1+Math.ceil((g-f.perpage)/(f.perpage-m)),b=Math.max(1,Math.min(0>b?1+a+b:b,a)),e.h?(h=1,d=1+a,e.d=b,e.b=a):(h=Math.max(1,Math.min(b-e.d,a-e.b)+1),d=e.g?h+e.b:Math.min(h+e.b,1+a)));for(;o--;){i=0;j=e.e[o];switch(j.f){case"left":i=j.c<h;break;case"right":i=d<=a-e.j+j.c;break;case"first":i=e.d<b;break;case"last":i=e.b<e.d+a-b;break;case"prev":i=1<b;break;case"next":i=b<a}r|=i<<j.i}c={number:g,lapping:m,pages:a,perpage:f.perpage,page:b,slice:[(i=b*(f.perpage-m)+m)-f.perpage,Math.min(i,g)]};for(l="";++o<u;){j=e.e[o];i=r>>j.i&1;switch(j.f){case"block":for(;h<d;++h)c.value=h,c.pos=1+e.b-d+h,c.active=h<=a||0>g,c.first=1===h,c.last=h==a&&0<g,q(f,c,j.f);continue;case"left":c.value=j.c;c.active=j.c<h;break;case"right":c.value=a-e.j+j.c;c.active=d<=c.value;break;case"first":c.value=1;c.active=i&&1<b;break;case"prev":c.value=Math.max(1,b-1);c.active=i&&1<b;break;case"last":(c.active=0>g)?c.value=1+b:(c.value=a,c.active=i&&b<a);break;case"next":(c.active=0>g)?c.value=1+b:(c.value=Math.min(1+b,a),c.active=i&&b<a);break;case"leap":case"fill":c.pos=j.c;c.active=i;q(f,c,j.f);continue}c.pos=j.c;c.last=c.first=n;q(f,c,j.f)}t.length&&(k("a",t.html(l)).click(function(a){a.preventDefault();a=this;do if("a"===a.nodeName.toLowerCase())break;while(a=a.parentNode);s.setPage(k(a).data("page"));if(s.n)p.location=a.href}),this.n=f.onSelect.call({number:g,lapping:m,pages:a,slice:c.slice},b));return this}};return s.setNumber(v).setOptions(w).setPage()}})(jQuery,this);

// jQuery image resize plugin
// 圖片縮放顯示
// Version 1.03 (07/09/2012)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2012 Qi-Liang Wen 啟良
(function($){$.fn.ScaleImg=function(settings){settings=jQuery.extend({width:0,height:0},settings);return this.each(function(){$(this).css("position","relative").css("vertical-align","text-top");var par=$(this).parent().get(0).tagName;if(par=="A"){if($(this).parent().css('display')!="block"){$par=$(this).parent().parent()}else{$par=$(this).parent()}}else{$par=$(this).parent()}$par.css("vertical-align","text-top").css("text-align","left");var h=$par.height();var w=$par.width();$.fn.ScaleImg.Run($(this),w,h);try{$(this).load(function(){$.fn.ScaleImg.Run($(this),w,h)})}catch(e){}})};$.fn.ScaleImg.Run=function($this,parentWidth,parentHeight){var src=$this.attr("src");var img=new Image();img.src=src;var w=0;var h=0;var _doScaling=function(){if(img.width>0&&img.height>0){if(img.width/img.height>=parentWidth/parentHeight){if(img.width>parentWidth){w=parentWidth;h=(img.height*parentWidth)/img.width}else{w=img.width;h=img.height}}else{if(img.height>parentHeight){w=(img.width*parentHeight)/img.height;h=parentHeight}else{w=img.width;h=img.height}}}$this.width(w);$this.height(h)};_doScaling();var loading=$("<span>Loading..</span>");$this.hide();$this.after(loading);loading.remove();$this.show();var objHeight=$this.height();var objWidth=$this.width();if(objWidth>parentWidth){$this.css("left",(objWidth-parentWidth)/2)}else{$this.css("left",(parentWidth-objWidth)/2)}if(objHeight>parentHeight){$this.css("top",(objHeight-parentHeight)/2)}else{$this.css("top",(parentHeight-objHeight)/2)}}})(jQuery);

// yooliang general function
// 侑良通用函式
// Version 1.03 (08/18/2012)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2012 Qi-Liang Wen 啟良
function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:!1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_message(d.message):errorCallback(d.message)}})};
function ajax(url,data,successCallback,errorCallback){$.ajax({url:url,type:"GET",cache: false,data:data,async:true,success:function(responseText){successCallback(responseText)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};
function html2text(){$(".html_2_text").each(function(){var text=$(this).text();var length=0;if($(this).data("word-count")!=undefined){try{length=parseInt($(this).data("word-count"))}catch(e){}}if(length>0){$(this).text(text.substring(0,length))}$(this).show()})}
function yooliang_replace_url_param(url,name,newvalue){url=url.replace("#/","");var old="";var m=url.substring(0,url.indexOf("?"));var s=url.substring(url.indexOf("?"),url.length);var j=0;if(url.indexOf("?")>=0){var i=s.indexOf(name+"=");if(i>=0){j=s.indexOf("&",i);if(j>=0){old=s.substring(i+name.length+1,j);s=url.replace(name+"="+old,name+"="+newvalue)}else{old=s.substring(i+name.length+1,s.length);s=url.replace(name+"="+old,name+"="+newvalue)}}else{s=url+"&"+name+"="+newvalue}}else{s=url+"?"+name+"="+newvalue}return s};

$(function () {
    //將 html 轉為純文字
    html2text();
    //=================================================================================//
    //首頁-隱藏特定分隔線
    $(".iGoodsListBox .gLine").eq(2).hide();
    //問與答開合
    var sBlock = $('#slideDownUp'),
        list = sBlock.find('div.pAnswer');
    sBlock.delegate('div.pQuestion', 'click',function () {
        var aObj = $(this).next();
        if (aObj.is()) {
            aObj.slideUp('600');
        }
        else {
            list.hide();
            aObj.slideDown('600');
        }

    }).find('div.pQuestion').first().trigger('click'); //.first().click(); 預設第一個打開,如果不要則拿掉

    //合作廠商輪播-數量不足時填充項目
    $("#mycarousel").each(function () {
        if ($(this).find("li").length < 6) {
            var st = "";
            var ht = $(this).html();
            for (var i = 0; i < (7 - $(this).find("li").length); i++) {
                st += ht;
            }
            $(this).html(st);
        }
    }).find("li").show();
    //合作廠商輪播
    $('#mycarousel').jcarousel({auto: 0,wrap: 'last'});
    //產品列表-添加分隔線
    product_list_hr();
    //產品輪播
    $('.jcarousel').jcarousel();
    //產品輪播-放大圖片
    $('.jcarousel img').click(function () {
        $('.bPic > img:last').attr('src', $(this).attr('img_src')).ScaleImg();
    }).css('cursor', 'pointer').first().click();
    //橫幅輪播
    $(".ad img").hide();
    $("#abgne_fade_pic").each(function(){
        var $block = $(this),
            $ad = $block.find('.ad'),
            showIndex = 0,			// 預設要先顯示那一張
            fadeOutSpeed = 1000,	// 淡出的速度
            fadeInSpeed = 1000,		// 淡入的速度
            defaultZ = 10,			// 預設的 z-index
            isHover = false,        // 滑鼠是否停在上方
            timer, speed = 5000;	// 計時器及輪播切換的速度
        $ad.css({
            opacity: 0,
            zIndex: defaultZ - 1
        }).eq(showIndex).css({
            opacity: 1,
            zIndex: defaultZ
        });
        var str = '';
        for (var i = 0; i < $ad.length; i++) {
            str += '<a href="#">' + (i + 1) + '</a>';
        }
        var $controlA = $('#abgne_fade_num').append($('<div class="control">' + str + '</div>').css('zIndex', defaultZ + 1)).find('.control a');
        $(".control").each(function () {
            var l = $(this).find("a").length.toString();
            $(this).addClass("n" + l);
            var item = 0;
            $(this).find("a").each(function () {
                item++;
                $(this).addClass("item" + item.toString());
            });
        });
        $controlA.click(function () {
            showIndex = $(this).text() * 1 - 1;
            $ad.eq(showIndex).stop().fadeTo(fadeInSpeed, 1,function () {
                if (!isHover) {
                    clearTimeout(timer);
                    timer = setTimeout(autoClick, speed + fadeInSpeed);
                }
            }).css('zIndex', defaultZ).siblings('a').stop().fadeTo(fadeOutSpeed, 0).css('zIndex', defaultZ - 1);
            $(this).addClass('on').siblings().removeClass('on');

            return false;
        }).focus(function () {
                $(this).blur();
            }).eq(showIndex).addClass('on');

        $block.hover(function () {
            isHover = true;
            clearTimeout(timer);
        }, function () {
            isHover = false;
            timer = setTimeout(autoClick, speed);
        })
        function autoClick() {
            if (isHover) return;
            showIndex = (showIndex + 1) % $controlA.length;
            $controlA.eq(showIndex).click();
        }
        timer = setTimeout(autoClick, speed);
    });
    $(".ad img").show();
    $("#but_send_guestbook").click(function(){
        $(".error").hide();
        var $form = $("form#gurestbook");
        json($form.attr("action"), $form.serialize(), function (data) {
            for (var key in data) {
                $("#info_" + key).html("" + data[key]).slideDown().delay(5000).slideUp();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp().delay(5000).slideDown();
            }
        }, function (data) {
            for (var key in data) {
                $("#info_" + key).html("" + data[key]).slideDown().delay(5000).slideUp();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp().delay(5000).slideDown();
            }
        });
    });
    //更改密碼
    $("#but_pw_ch_send").click(function () {
        $(".error").hide();
        var $form = $("form#pw_ch");
        json($form.attr("action"), $form.serialize(), function (data) {
            for (var key in data) {
                $("#info_" + key).html("&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp();
            }
        }, function (data) {
            for (var key in data) {
                $("#info_" + key).html("&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp();
            }
        });
    });
    //更改密碼-清空
    $("#but_pw_ch_reset").click(function(){
        $("#old_pw").val("");
        $("#pw").val("");
        $("#pw2").val("");
    });

    //填寫訂單訊息
    $("#go_step03").click(function () {
        $(".error").hide();
        var $form = $("form#step02");
        json($form.attr("action"), $form.serialize(), function (data) {
            for (var key in data) {
                $("#info_" + key).html("<br/>&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                window.location.href = $form.data("step03");;
            }
            if (data.error != undefined) {
                alert(data.error);
            }

            setTimeout('$("#info_done").slideUp();', 5000);
        }, function (data) {
            for (var key in data) {
                $("#info_" + key).html("&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp();
            }
        });
    });

    //填寫訂單訊息
    $("#go_step04").click(function () {
        $(".error").hide();
        var $form = $("form#step03");
        json($form.attr("action"), $form.serialize(), function (data) {
            if (data.done != undefined) {
                window.location.href = $form.data("step04");;
            }
        }, function (data) {
            if (data.done != undefined) {
                window.location.href = $form.data("step04");;
            }
        });
    });

    //修改會員資料
    $("#but_info_send").click(function () {
        $(".error").hide();
        var $form = $("form#info");
        json($form.attr("action"), $form.serialize(), function (data) {
            for (var key in data) {
                $("#info_" + key).html("&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp();
            }
            setTimeout('$("#info_done").slideUp();', 5000);
        }, function (data) {
            for (var key in data) {
                $("#info_" + key).html("&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp();
            }
            setTimeout('$("#info_done").slideUp();', 5000);
        });
    });
    //加入會員
    $("#but_join_send").click(function () {
        if ($("#must_check").is(":checked")) {
            $(".error").hide();
            var $form = $("form#res");
            json($form.attr("action"), $form.serialize(), function (data) {
                for (var key in data) {
                    $("#info_" + key).html("&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;" + data[key]).slideDown();
                }
                if (data.done != undefined) {
                    $("#d_form").slideUp();
                }
            }, function (data) {
                for (var key in data) {
                    $("#info_" + key).html("&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;" + data[key]).slideDown();
                }
                if (data.done != undefined) {
                    $("#d_form").slideUp();
                }
            });
        } else {
            $("#info_must_check").html("&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;請先閱讀並同意條約規範");
        }
    });
    //加入會員-清空
    $("#but_join_reset").click(function(){
        $("#email").val("");
        $("#pw").val("");
        $("#pw2").val("");
    });
    //會員登入
    $("#but_login").click(function () {
        var $form = $("form#login");
        json($form.attr("action"), $form.serialize(), function (data) {
            if (data.info == "done"){
                location.reload();
            }else{
                for (var key in data) {
                    alert(data[key]);
                }
            }
        }, function (data) {
        });
    });
    //會員登出
    $("#but_logout").click(function () {
        json($(this).data("action"), null, function (data) {
            if (data.info == "done"){
                location.reload();
            }
        }, function (data) {
        });
    });

    //換圖
    jQuery('.img_change').mouseover(function () {
        $(this).attr("src", $(this).attr("src").replace("_out", "_over"));
    }).mouseout(function () {
        $(this).attr("src", $(this).attr("src").replace("_over", "_out"));
    });

    //分頁
    $(".pagination").each(function () {
        var page_all = parseInt($(this).data("page-all"));
        var page_now = parseInt($(this).data("page-now"));
        if (isNaN(page_all) == false && isNaN(page_now) == false) {
            $(this).paging(page_all, {
                format: "[< nnnnnncnnnnnn >]",
                perpage: 1,
                lapping: 2,
                page: page_now,
                onSelect: function (page) {
                    var temp_last_page = yooliang_replace_url_param(location.href, "page", page);
                    if (page_now != page) {
                        location.href = temp_last_page;
                    }
                },
                onFormat: function (type) {
                    switch (type) {
                        case 'block':
                            if (!this.active)
                                return '<a href="#">' + this.value + '</a>';
                            else if (this.value != this.page)
                                return '<a href="#' + this.value + '">' + this.value + '</a>';
                            return '<span class="current">' + this.value + '</span>';
                        case 'prev':
                            if (this.active)
                                return '<a href="#" title="上一頁"><img src="images/pre_out.gif" alt="上一頁" class="img_change" align="absmiddle" /></a>';
                            return '<a href="#" title="上一頁"><img src="images/pre_out.gif" alt="上一頁" class="img_change" align="absmiddle" /></a>';
                        case 'next':
                            if (this.active)
                                return '<a href="#" title="下一頁"><img src="images/next_out.gif" alt="下一頁" class="img_change" align="absmiddle" /></a>';
                            return '<a href="#" title="下一頁"><img src="images/next_out.gif" alt="下一頁" class="img_change" align="absmiddle" /></a>';
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
                                return '<a href="#">...</a>';
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

    //圖片依外框縮放
    $("img").one('load',function () {
        if ($(this).hasClass("scale")) {
            $(this).ScaleImg();
        };
    }).each(function () {
        if (this.complete) $(this).load();
    });
});
function product_list_hr(){
    var item_count = 0;                            // 一開始是第 0 個
    var item_length = $(".pGoodsList").length;  // 共有 n 個
    $(".pGoodsList").each(function () {
        item_count++;
        if (item_count % 4 == 0 || item_count == item_length) {
            $('<div class="clear"></div>').insertAfter(this);
        }
    });
}
function pager_for_guestbook(){
    //分頁-for留言版 ajax
    $(".pagination2").each(function () {
        var page_all = parseInt($(this).data("page-all"));
        var page_now = parseInt($(this).data("page-now"));
        if (isNaN(page_all) == false && isNaN(page_now) == false) {
            $(this).paging(page_all, {
                format: "[< nnnnnncnnnnnn >]",
                perpage: 1,
                lapping: 2,
                page: page_now,
                onSelect: function (page) {
                    if (page_now != page) {
                        load_guestbook_list(page);
                    }
                },
                onFormat: function (type) {
                    switch (type) {
                        case 'block':
                            if (!this.active)
                                return '<a href="#">' + this.value + '</a>';
                            else if (this.value != this.page)
                                return '<a href="#' + this.value + '">' + this.value + '</a>';
                            return '<span class="current">' + this.value + '</span>';
                        case 'prev':
                            if (this.active)
                                return '<a href="#" title="上一頁"><img src="images/pre_out.gif" alt="上一頁" class="img_change" align="absmiddle" /></a>';
                            return '<a href="#" title="上一頁"><img src="images/pre_out.gif" alt="上一頁" class="img_change" align="absmiddle" /></a>';
                        case 'next':
                            if (this.active)
                                return '<a href="#" title="下一頁"><img src="images/next_out.gif" alt="下一頁" class="img_change" align="absmiddle" /></a>';
                            return '<a href="#" title="下一頁"><img src="images/next_out.gif" alt="下一頁" class="img_change" align="absmiddle" /></a>';
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
                                return '<a href="#">...</a>';
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
function load_guestbook_list(page){
    if (page == undefined){
        page = 1;
    }
    var p = $("#parent_category").val();
    var s = $("#sub_category").val();
    var k = $("#keyword").val();
    var u = $("#guestbook_list_area").data("url");
    $("#guestbook_list_area").html('<div style="line-height: 500px; text-align: center;">載入中...</div>');
    ajax(u, "parent=" + p + "&category=" + s + "&keyword=" + k + "&page=" + page , function(data){
        $("#guestbook_list_area").html(data);
        product_list_hr();
        pager_for_guestbook();
    });
}
