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
(function($){$.fn.ScaleImg=function(settings){settings=jQuery.extend({width:0,height:0},settings);return this.each(function(){$(this).css("position","relative").css("vertical-align","text-top");var par=$(this).parent().get(0).tagName;if(par=="A"){if($(this).parent().css('display')!="block"){$par=$(this).parent().parent()}else{$par=$(this).parent()}}else{$par=$(this).parent()}$par.css("vertical-align","text-top").css("text-align","left");var h=$par.height();var w=$par.width();$.fn.ScaleImg.Run($(this),w,h);try{$(this).load(function(){$.fn.ScaleImg.Run($(this),w,h)})}catch(e){}$(this).removeClass("resize")})};$.fn.ScaleImg.Run=function($this,parentWidth,parentHeight){var src=$this.attr("src");var img=new Image();img.src=src;var w=0;var h=0;var _doScaling=function(){if(img.width>0&&img.height>0){if(img.width/img.height>=parentWidth/parentHeight){if(img.width>parentWidth){w=parentWidth;h=(img.height*parentWidth)/img.width}else{w=img.width;h=img.height}}else{if(img.height>parentHeight){w=(img.width*parentHeight)/img.height;h=parentHeight}else{w=img.width;h=img.height}}}$this.width(w);$this.height(h)};_doScaling();var loading=$("<span>Loading..</span>");$this.hide();$this.after(loading);loading.remove();$this.show();var objHeight=$this.height();var objWidth=$this.width();if(objWidth>parentWidth){$this.css("left",(objWidth-parentWidth)/2)}else{$this.css("left",(parentWidth-objWidth)/2)}if(objHeight>parentHeight){$this.css("top",(objHeight-parentHeight)/2)}else{$this.css("top",(parentHeight-objHeight)/2)}}})(jQuery);

// yooliang general function
// 侑良通用函式
// Version 1.03 (08/18/2012)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2012 Qi-Liang Wen 啟良
function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:!1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?show_message(d.message):errorCallback(d.message)}})};
function ajax(url,data,successCallback,errorCallback){$.ajax({url:url,type:"GET",cache: false,data:data,async:true,success:function(responseText){successCallback(responseText)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};
function html2text(){$(".html_2_text").each(function(){var text=$(this).text();var length=0;if($(this).data("word-count")!=undefined){try{length=parseInt($(this).data("word-count"))}catch(e){}}if(length>0){$(this).text(text.substring(0,length))}$(this).show()})}
function yooliang_replace_url_param(url,name,newvalue){url=url.replace("#/","");var old="";var m=url.substring(0,url.indexOf("?"));var s=url.substring(url.indexOf("?"),url.length);var j=0;if(url.indexOf("?")>=0){var i=s.indexOf(name+"=");if(i>=0){j=s.indexOf("&",i);if(j>=0){old=s.substring(i+name.length+1,j);s=url.replace(name+"="+old,name+"="+newvalue)}else{old=s.substring(i+name.length+1,s.length);s=url.replace(name+"="+old,name+"="+newvalue)}}else{s=url+"&"+name+"="+newvalue}}else{s=url+"?"+name+"="+newvalue}return s};
function build_pager() {
    //建立分頁
    $(".pagination").each(function () {
        var page_url = $(this).data("page-url");
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
                        var url = yooliang_replace_url_param(page_url, "isAjax", 'true');
                        url = yooliang_replace_url_param(url, "page", page);
                        $.address.value(url);
                        return false;
                    }
                },
                onFormat: function (type) {
                    switch (type) {
                        case 'block':
                            if (!this.active)
                                return '<a href="' + page_url + '?page=' + this.value + '">' + this.value + '</a>';
                            else if (this.value != this.page)
                                return '<a href="' + page_url + '?page=' + this.value + '">' + this.value + '</a>';
                            return '<span class="current">' + this.value + '</span>';
                        case 'prev':
                            if (this.active)
                                return '';
                            return '';
                        case 'next':
                            if (this.active)
                                return '';
                            return '';
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
function after_page_load(){
    html2text();
    build_pager();
    $(window).resize();
		//換圖
	$(".caseSPic div").css('cursor', 'pointer').mouseover(function(){
		$(this).css('border', '5px solid #fcc800');
    }).mouseout(function(){
		$(this).css('border', '5px solid #fff');
    });
    $(".resize").ScaleImg();
}

var first_load = true;
$(function () {
    jQuery('.img_change').mouseover(function () {
        $(this).attr("src", $(this).attr("src").replace("_out", "_over"));
    }).mouseout(function () {
        $(this).attr("src", $(this).attr("src").replace("_over", "_out"));
    });

    //背景圖
    $("#wrapper .bgImg").css("display", "none");
    var src_url = $("#wrapper .bgImg").attr("src");
    $("#wrapper").hide().css("background-image", "url(" + src_url + ")").fadeIn(1500);

	//con
	$(".con").css('opacity', 0).delay( 500 ).animate({opacity: 1,right: "50%"},4500);

    $(".bPicView img").ScaleImg();
    //slogan
    $(".slogan").css('opacity', 0).delay(2000).animate({opacity: 1, left: "4%"}, 2500);

    $(".goodsList a").hide();
    $(".goodsList .delay5").delay(500).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay10").delay(1000).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay15").delay(1500).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay20").delay(2000).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay25").delay(2500).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay30").delay(3000).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay35").delay(3500).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay40").delay(4000).fadeIn(2500).css("background-color","#fff");
    $(".goodsList .delay45").delay(4500).fadeIn(2500).css("background-color","#fff");
    $(".goodsList").css('opacity', .8);
    $(".goodsList").mouseover(function () {
        $(this).css('opacity', 1);
    }).mouseout(function () {
        $(this).css('opacity', .8);
    });


    $(window).resize(function(){
        //高
        var windowHeight = $(window).height();
        var menuBtn = $('.menuBtn').height();
        var menuBtnH = (windowHeight - menuBtn) / 2;
        $('.menuBtn').css('margin-top',menuBtnH);

        var windowWidth = $(window).width();
        var leftMenu = $('#left').width();
        var vBoxW = windowWidth - leftMenu;
        var conW = (windowWidth - leftMenu) * 0.8;
        var conWMR = conW / 2;
        var viewW = conW - 520;
        $('#verticalBox').css({'width':vBoxW, 'height':windowHeight});
        $('.con').css({'width':conW, 'margin-right':(-conWMR)});
        $('.caseViewInfo').css('width' ,viewW);

        var windowWidth = $(window).width();
        var leftMenu = $('#left').width();
        var vBoxW = windowWidth - leftMenu;
        var conW = (windowWidth - leftMenu) * 0.8;
        var conWMR = conW / 2;
        var listW = conW - 220;
        $('#verticalBox').css({'width':vBoxW, 'height':windowHeight});
        $('.con').css({'width':conW, 'margin-right':(-conWMR)});
        $('.caseListInfo').css('width' ,listW);
    });
    $(window).resize();

    //左側選單
    $('.menuBtn').click(function () {
        var leftMenu = $('#left').width();
        if (leftMenu == 196) {
            $(this).css('background-image', 'url(images/menubtnOver.png)');
            $('#left').stop().animate({width: 24}, 600, "easeOutBounce");
            $('.menuBox').hide();
            $('#iFooter').css('z-index', '100');
            $('.footerLogo').fadeIn(400);
        } else {
            $(this).css('background-image', 'url(images/menubtnOut.png)');
            $('#left').stop().animate({width: 196}, 600, "easeOutBounce");
            $('.menuBox').delay(600).fadeIn(400);
            $('#iFooter').css('z-index', '98');
            $('.footerLogo').fadeOut(400);
            $('.footerRight').css('width', footerRWidth);
        }
    }).css('cursor', 'pointer');

    try{
        var init = true,
            state = window.history.pushState !== undefined;

        $.address.state('/').init(function(event) {
            // Initializes the plugin
            $('.menu a').address();
            $('#verticalBox a').address();
        }).change(function(event) {
            var value = $.address.state().replace(/^\/$/, '') + event.value;

            if (state && init) {
                init = false;
            } else {
                if (first_load){
                    first_load = false;
                }else{
                    $(".con").fadeOut(function(){
                        ajax(value, "isAjax=true", function(data){
                            $(".con").remove();
                            $("#verticalBox").html(data);
                            after_page_load();
                            $(".con").css('right', "50%").fadeIn();
                        }, function(data){

                        });
                    });
                }
                return false;
            }
        });
        if (!state) {
            // Hides the page during initialization
            document.write('<style type="text/css"> .con { display: none; } </style>');
        }
    } catch (e) {}

    $(document).on("click", ".caseSPic div", function(){
        /* 更換 bigPic 的圖片路徑 */
        var bigPic = $('.bPicView img');  /* 針對區塊下的最後一張圖 */
        /* var bigPic = $jQuery('.bigPic > span > img');  // 另一種區隔方法，大圖加標籤區隔 */
        var img_src = $(this).find("img").attr('src');  /* 更換bigPic的圖片路徑 */
        bigPic.attr('src', img_src);
        $(".resize").ScaleImg();
    });
    after_page_load();
});