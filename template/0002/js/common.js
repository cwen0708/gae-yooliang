var isHover = true;
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

// 建立聯絡頁面的地圖
function build_contact_map() {
    var map;
    var TILE_SIZE = 250;
    var chicago = new google.maps.LatLng(22.995948, 120.219483);

    function bound(value, opt_min, opt_max) {
        if (opt_min != null) value = Math.max(value, opt_min);
        if (opt_max != null) value = Math.min(value, opt_max);
        return value;
    }

    function degreesToRadians(deg) {
        return deg * (Math.PI / 180);
    }

    function radiansToDegrees(rad) {
        return rad / (Math.PI / 180);
    }

    /** @constructor */
    function MercatorProjection() {
        this.pixelOrigin_ = new google.maps.Point(TILE_SIZE / 2,
            TILE_SIZE / 2);
        this.pixelsPerLonDegree_ = TILE_SIZE / 360;
        this.pixelsPerLonRadian_ = TILE_SIZE / (2 * Math.PI);
    }

    MercatorProjection.prototype.fromLatLngToPoint = function (latLng, opt_point) {
        var me = this;
        var point = opt_point || new google.maps.Point(0, 0);
        var origin = me.pixelOrigin_;

        point.x = origin.x + latLng.lng() * me.pixelsPerLonDegree_;

        // Truncating to 0.9999 effectively limits latitude to 89.189. This is
        // about a third of a tile past the edge of the world tile.
        var siny = bound(Math.sin(degreesToRadians(latLng.lat())), -0.9999,
            0.9999);
        point.y = origin.y + 0.5 * Math.log((1 + siny) / (1 - siny)) * -me.pixelsPerLonRadian_;
        return point;
    };

    MercatorProjection.prototype.fromPointToLatLng = function (point) {
        var me = this;
        var origin = me.pixelOrigin_;
        var lng = (point.x - origin.x) / me.pixelsPerLonDegree_;
        var latRadians = (point.y - origin.y) / -me.pixelsPerLonRadian_;
        var lat = radiansToDegrees(2 * Math.atan(Math.exp(latRadians)) -
            Math.PI / 2);
        return new google.maps.LatLng(lat, lng);
    };

    function createInfoWindowContent() {
        var numTiles = 1 << map.getZoom();
        var projection = new MercatorProjection();
        var worldCoordinate = projection.fromLatLngToPoint(chicago);
        var pixelCoordinate = new google.maps.Point(
            worldCoordinate.x * numTiles,
            worldCoordinate.y * numTiles);
        var tileCoordinate = new google.maps.Point(
            Math.floor(pixelCoordinate.x / TILE_SIZE),
            Math.floor(pixelCoordinate.y / TILE_SIZE));

        return [
            '牧陽能控有限公司',
            $(".com_address").text(),
            $(".com_tel").text()
        ].join('<br>');
    }

    function initialize() {
        var mapOptions = {
            zoom: 14,
            center: chicago,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

        var coordInfoWindow = new google.maps.InfoWindow();
        coordInfoWindow.setContent(createInfoWindowContent());
        coordInfoWindow.setPosition(chicago);
        coordInfoWindow.open(map);

        google.maps.event.addListener(map, 'zoom_changed', function () {
            coordInfoWindow.setContent(createInfoWindowContent());
            coordInfoWindow.open(map);
        });

    }
    google.maps.event.addDomListener(window, 'load', initialize);
}

function rf_data() {
    var yesterday_kwh = parseFloat($("#kws").data("yesterday-kwh"));
    var yesterday_kwh_total = parseFloat($("#kws").data("yesterday-total-kwh"));
    var co2kg = parseFloat($("#co2").data("co2kg"));
    var price = parseFloat($("#seb").data("price"));

    var d = new Date();
    var total_second = (d.getHours() * 3600) + (d.getMinutes() * 60) + d.getSeconds();
    var pre_second_kwh = (yesterday_kwh / 12 / 60 / 60);
    var now_kwh = Math.ceil((yesterday_kwh_total + (total_second * pre_second_kwh)) * 100) / 100;
    if (d.getHours() < 6 || d.getHours() > 19) {
        now_kwh = yesterday_kwh_total;
    }
    if (d.getHours() > 19) {
        now_kwh = yesterday_kwh + yesterday_kwh_total;
    }
    $("#kws").text(number_1000(now_kwh));
    var now_co2 = Math.ceil((now_kwh * co2kg) * 100) / 100;
    $("#co2").text(number_1000(now_co2));
    var now_price = Math.ceil((now_kwh * price) * 100) / 100;
    $("#seb").text(number_1000(now_price));
    setTimeout(rf_data, 1000);
}
function number_1000(n) {
    n += "";
    var arr = n.split(".");
    var re = /(\d{1,3})(?=(\d{3})+$)/g;
    return arr[0].replace(re, "$1,") + (arr.length == 2 ? "" : "");
}

$(function () {
    $("#login_but").click(function () {
        json("/user_login", $("#user_login").serialize(), function (data) {
            if (data.info == "done") {
                location.href = "/monitor.html";
            } else {
                alert(data.info);
            }
        }, function (data) {
            if (data.info == "done") {
                location.href = "/monitor.html";
            } else {
                alert(data.info);
            }
        });
    });
    $('#user_id').keydown(function (event) {
        if (event.which == 13) {
            $("#ulaitem0z6z0").click();
        }
    });
    $('#user_pw').keydown(function (event) {
        if (event.which == 13) {
            $("#ulaitem0z6z0").click();
        }
    });

    //是否可以改變
    var can_change = true;

    function go_prev() {
        can_change = false;
        //取得最後一個 li
        var $last = $('.news_marquee ul li').last();
        //建立復制體
        var $copy = $last.clone();
        //隱藏復制體
        $copy.hide();
        //加到 ul 裡面的前面
        $copy.prependTo($('.news_marquee ul'));

        //花 1000 毫秒顯示出來
        $copy.slideDown(500, function () {
            //把最後一個移除
            $last.remove();
            can_change = true;
        });

    }

    function go_next() {
        can_change = false;
        //取得第一個 li
        var $first = $('.news_marquee ul li').first();
        //建立復制體
        var $copy = $first.clone();

        //向上移動，並刪除
        $first.slideUp(500, function () {
            $first.remove();
            can_change = true;
        });
        //加到 ul 裡面的最後面
        $copy.appendTo($('.news_marquee ul'));
    }

    //run();
    //setTimeout(run, 1000); // 只 run 1次
    //setInterval(run, 3000); // 不斷執行

    $("#next").click(function () {
        if (can_change == true) {
            go_next();
        }
    });

    $("#prev").click(function () {
        if (can_change == true) {
            go_prev();
        }
    });
    var $block = $('#abgne_fade_pic'),
        $ad = $block.find('.ad'),
        showIndex = 0,			// 預設要先顯示那一張
        fadeOutSpeed = 2000,	// 淡出的速度
        fadeInSpeed = 3000,		// 淡入的速度
        defaultZ = 10;			// 預設的 z-index

    // 先把其它圖片的變成透明
    $ad.css({
        opacity: 0,
        zIndex: defaultZ - 1
    }).eq(showIndex).css({
            opacity: 1,
            zIndex: defaultZ
        });

    // 組出右下的按鈕
    var str = '';
    for (var i = 0; i < $ad.length; i++) {
        str += '<a href="#">' + (i + 1) + '</a>';
    }
    var $controlA = $('#abgne_fade_pic').append($('<div class="control">' + str + '</div>').css('zIndex', defaultZ + 1)).find('.control a');
    $(".top_menu_button_7").click(function () {
        $(this).toggleClass('active');
    });
    // 當按鈕被點選時
    // 若要變成滑鼠滑入來切換時, 可以把 click 換成 mouseover
    $controlA.click(function () {
        // 取得目前點擊的號碼
        showIndex = $(this).text() * 1 - 1;

        // 顯示相對應的區域並把其它區域變成透明
        $ad.eq(showIndex).stop().fadeTo(fadeInSpeed, 1).css('zIndex', defaultZ).siblings('a').stop().fadeTo(fadeOutSpeed, 0).css('zIndex', defaultZ - 1);
        // 讓 a 加上 .on
        $(this).addClass('on').siblings().removeClass('on');

        return false;
    }).focus(function () {
            $(this).blur();
        }).eq(showIndex).addClass('on');

    $ad.hover(function () {
        isHover = true;
        // 停止計時器
        clearTimeout(timer);
    }, function () {
        isHover = false;
        // 啟動計時器
        timer = setTimeout(autoClick, 3100);
    })

    // 自動點擊下一個
    function autoClick() {
        if (isHover) return;
        showIndex = (showIndex + 1) % $controlA.length;
        $controlA.eq(showIndex).click();
    }

    $(window).resize(function () {
        var left = $(".top_tel").position().left + 20;
        $("#corporate_contributions_info").css("left", left + "px");
        var top = 102;
        $("#corporate_contributions_info").css("top", top + "px");
    });
    $(window).resize();
    $("#corporate_contributions_info").mouseenter(function () {
        $(this).stop().animate({
            height: "160px"
        });
    }).mouseleave(function () {
            $(this).stop().animate({
                height: "40px"
            });
        });
    // 啟動計時器
    timer = setTimeout(autoClick, 3100);
    timer02 = setTimeout(rf_data, 10);
    //產品輪播
    $('.jcarousel').jcarousel();
    //產品輪播-放大圖片
    $('.jcarousel img').click(function () {
        $('.bPic > img:last').attr('src', $(this).attr('img_src')).ScaleImg();
    }).css('cursor', 'pointer').first().click();

    $(".map-canvas-contact").each(function () {
        build_contact_map();
    });

    $("#contact_button_prev").click(function(){
        window.history.back();
    });
    $("#contact_button_next").click(function(){
        $(".error").hide();
        var url = window.location.href;
        var next_url = $(this).data("next_url");
        json(url, $("form").serialize(), function(data){
            for (var key in data) {
                if (key != "done")
                {
                    $("#info_" + key).html("&nbsp;*&nbsp;" + data[key]).prev().hide().delay(1200).next().slideDown();
                }
            }
            if (typeof(data.done) != "undefined") {
                window.location.href = data.next;
            }
            setTimeout('$(".error").slideUp();', 5000);
            setTimeout('$(".help").slideDown();', 5500);
        },function(data){

        });
    });

    //圖片依外框縮放
    $("img").one('load',function () {
        if ($(this).hasClass("scale")) {
            $(this).ScaleImg();
        };
    }).each(function () {
        if (this.complete) $(this).load();
    });
    //換圖
    jQuery('.img_change').mouseover(function () {
        $(this).attr("src", $(this).attr("src").replace("_out", "_over"));
    }).mouseout(function () {
        $(this).attr("src", $(this).attr("src").replace("_over", "_out"));
    });
    //填寫訂單訊息
    $("#go_step03").click(function() {
        $(".error").hide();
        var $form = $("form#step02");
        json($form.attr("action"), $form.serialize(), function(data) {
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
        }, function(data) {
            for (var key in data) {
                $("#info_" + key).html("&nbsp;*&nbsp;" + data[key]).slideDown();
            }
            if (data.done != undefined) {
                $("#d_form").slideUp();
            }
        });
    });

    //填寫訂單訊息
    $("#go_step04").click(function() {
        $(".error").hide();
        var $form = $("form#step03");
        json($form.attr("action"), $form.serialize(), function(data) {
            if (data.done != undefined) {
                window.location.href = $form.data("step04");;
            }
        }, function(data) {
            if (data.done != undefined) {
                window.location.href = $form.data("step04");;
            }
        });
    });
});
