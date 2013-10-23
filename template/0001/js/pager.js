$(function () {
    var $block = $('#abgne_fade_pic'),
        $ad = $block.find('.ad'),
        showIndex = 0,			// 預設要先顯示那一張
        fadeOutSpeed = 1000,	// 淡出的速度
        fadeInSpeed = 1000,		// 淡入的速度
        defaultZ = 10,			// 預設的 z-index
        isHover = false,
        timer, speed = 5000;	// 計時器及輪播切換的速度

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
    // 當按鈕被點選時
    // 若要變成滑鼠滑入來切換時, 可以把 click 換成 mouseover
    $controlA.click(function () {
        // 取得目前點擊的號碼
        showIndex = $(this).text() * 1 - 1;

        // 顯示相對應的區域並把其它區域變成透明
        $ad.eq(showIndex).stop().fadeTo(fadeInSpeed, 1,function () {
            if (!isHover) {
                clearTimeout(timer);
                // 啟動計時器
                timer = setTimeout(autoClick, speed + fadeInSpeed);
            }
        }).css('zIndex', defaultZ).siblings('a').stop().fadeTo(fadeOutSpeed, 0).css('zIndex', defaultZ - 1);
        // 讓 a 加上 .on
        $(this).addClass('on').siblings().removeClass('on');

        return false;
    }).focus(function () {
            $(this).blur();
        }).eq(showIndex).addClass('on');

    $block.hover(function () {
        isHover = true;
        // 停止計時器
        clearTimeout(timer);
    }, function () {
        isHover = false;
        // 啟動計時器
        timer = setTimeout(autoClick, speed);
    })

    // 自動點擊下一個
    function autoClick() {
        if (isHover) return;
        showIndex = (showIndex + 1) % $controlA.length;
        $controlA.eq(showIndex).click();
    }

    // 啟動計時器
    timer = setTimeout(autoClick, speed);
    setInterval(a, 100);

     jQuery('.img_change').mouseover(function () {
        $(this).attr("src", $(this).attr("src").replace("_out", "_over"));
    }).mouseout(function () {
        $(this).attr("src", $(this).attr("src").replace("_over", "_out"));
    });
});

function a() {
    var j = parseFloat($("#st").text()) + 0.100;
    $("#st").text(j)
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
};

$(function(){
    $(".pagination").each(function(){
        var page_all = parseInt($(this).data("page-all"));
        var page_now = parseInt($(this).data("page-now"));
        if (isNaN(page_all) == false && isNaN(page_now) == false)
        {
            $(this).paging(page_all, {
                format: "[< nnnnnncnnnnnn >]",
                perpage: 1,
                lapping: 2,
                page: page_now,
                onSelect: function (page) {
                    var temp_last_page = replace_url_param(location.href, "page", page);
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
});

/*
 jQuery paging plugin v1.1.0
 http://www.xarg.org/2011/09/jquery-pagination-revised/

 Copyright (c) 2011, Robert Eisele (robert@xarg.org)
 Dual licensed under the MIT or GPL Version 2 licenses.
*/
(function(k,p,n){k.fn.paging=function(v,w){var t=this,s={setOptions:function(b){this.a=k.extend(this.a||{lapping:0,perpage:10,page:1,refresh:{interval:10,url:null},format:"",onFormat:function(){},onSelect:function(){return!0},onRefresh:function(){}},b||{});this.a.lapping|=0;this.a.perpage|=0;null!==this.a.page&&(this.a.page|=0);1>this.a.perpage&&(this.a.perpage=10);this.k&&p.clearInterval(this.k);this.a.refresh.url&&(this.k=p.setInterval(function(b){k.ajax({url:b.a.refresh.url,success:function(g){if("string"===typeof g)try{g=
k.parseJSON(g)}catch(f){return}b.a.onRefresh(g)}})},1E3*this.a.refresh.interval,this));this.l=function(b){for(var g=0,f=0,h=1,d={e:[],h:0,g:0,b:5,d:3,j:0,m:0},a,l=/[*<>pq\[\]().-]|[nc]+!?/g,k={"[":"first","]":"last","<":"prev",">":"next",q:"left",p:"right","-":"fill",".":"leap"},e={};a=l.exec(b);){a=""+a;if(n===k[a])if("("===a)f=++g;else if(")"===a)f=0;else{if(h){if("*"===a){d.h=1;d.g=0}else{d.h=0;d.g="!"===a.charAt(a.length-1);d.b=a.length-d.g;if(!(d.d=1+a.indexOf("c")))d.d=1+d.b>>1}d.e[d.e.length]=
{f:"block",i:0,c:0};h=0}}else{d.e[d.e.length]={f:k[a],i:f,c:n===e[a]?e[a]=1:++e[a]};"q"===a?++d.m:"p"===a&&++d.j}}return d}(this.a.format);return this},setNumber:function(b){this.o=n===b||0>b?-1:b;return this},setPage:function(b){function q(b,a,c){c=""+b.onFormat.call(a,c);l=a.value?l+c.replace("<a",'<a data-page="'+a.value+'"'):l+c}if(n===b){if(b=this.a.page,null===b)return this}else if(this.a.page==b)return this;this.a.page=b|=0;var g=this.o,f=this.a,h,d,a,l,r=1,e=this.l,c,i,j,m,u=e.e.length,o=
u;f.perpage<=f.lapping&&(f.lapping=f.perpage-1);m=g<=f.lapping?0:f.lapping|0;0>g?(a=g=-1,h=Math.max(1,b-e.d+1-m),d=h+e.b):(a=1+Math.ceil((g-f.perpage)/(f.perpage-m)),b=Math.max(1,Math.min(0>b?1+a+b:b,a)),e.h?(h=1,d=1+a,e.d=b,e.b=a):(h=Math.max(1,Math.min(b-e.d,a-e.b)+1),d=e.g?h+e.b:Math.min(h+e.b,1+a)));for(;o--;){i=0;j=e.e[o];switch(j.f){case "left":i=j.c<h;break;case "right":i=d<=a-e.j+j.c;break;case "first":i=e.d<b;break;case "last":i=e.b<e.d+a-b;break;case "prev":i=1<b;break;case "next":i=b<a}r|=
i<<j.i}c={number:g,lapping:m,pages:a,perpage:f.perpage,page:b,slice:[(i=b*(f.perpage-m)+m)-f.perpage,Math.min(i,g)]};for(l="";++o<u;){j=e.e[o];i=r>>j.i&1;switch(j.f){case "block":for(;h<d;++h)c.value=h,c.pos=1+e.b-d+h,c.active=h<=a||0>g,c.first=1===h,c.last=h==a&&0<g,q(f,c,j.f);continue;case "left":c.value=j.c;c.active=j.c<h;break;case "right":c.value=a-e.j+j.c;c.active=d<=c.value;break;case "first":c.value=1;c.active=i&&1<b;break;case "prev":c.value=Math.max(1,b-1);c.active=i&&1<b;break;case "last":(c.active=
0>g)?c.value=1+b:(c.value=a,c.active=i&&b<a);break;case "next":(c.active=0>g)?c.value=1+b:(c.value=Math.min(1+b,a),c.active=i&&b<a);break;case "leap":case "fill":c.pos=j.c;c.active=i;q(f,c,j.f);continue}c.pos=j.c;c.last=c.first=n;q(f,c,j.f)}t.length&&(k("a",t.html(l)).click(function(a){a.preventDefault();a=this;do if("a"===a.nodeName.toLowerCase())break;while(a=a.parentNode);s.setPage(k(a).data("page"));if(s.n)p.location=a.href}),this.n=f.onSelect.call({number:g,lapping:m,pages:a,slice:c.slice},b));
return this}};return s.setNumber(v).setOptions(w).setPage()}})(jQuery,this);
