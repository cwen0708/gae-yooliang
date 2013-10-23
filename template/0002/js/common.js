var isHover = true;

// 用 json 取得頁面
function json(b, c, e, a) { $.ajax({ url: b, type: "POST", dataType: "json", data: c, async: !1, success: function (a) { e(a) }, error: function (b, c, d) { void 0 == a ? show_message(d.message) : a(d.message) } }) };

// 用 ajax 取得頁面
function ajax(url, data, successCallback, errorCallback) {
    $.ajax({
        url: url,
        type: "GET",
        data: data,
        async: true,
        success: function (responseText) {
            successCallback(responseText);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            if (errorCallback) {
                errorCallback(xhr.responseText);
            } else {
                window.alert(thrownError.message);
            }
        }
    });
};
function rf_data(){
    var yesterday_kwh = parseFloat($("#kws").data("yesterday-kwh"));
    var yesterday_kwh_total = parseFloat($("#kws").data("yesterday-total-kwh"));
    var co2kg = parseFloat($("#co2").data("co2kg"));
    var price = parseFloat($("#seb").data("price"));

    var d = new Date();
    var total_second = (d.getHours() * 3600) + (d.getMinutes() * 60) + d.getSeconds();
    var pre_second_kwh = (yesterday_kwh/12/60/60);
    var now_kwh = Math.ceil((yesterday_kwh_total + (total_second * pre_second_kwh))*100)/100;
    if (d.getHours() < 6 || d.getHours() > 19){
        now_kwh = yesterday_kwh_total;
    }
    if (d.getHours() > 19){
        now_kwh = yesterday_kwh + yesterday_kwh_total;
    }
    $("#kws").text(number_1000(now_kwh));
    var now_co2 = Math.ceil((now_kwh * co2kg)*100)/100;
    $("#co2").text(number_1000(now_co2));
    var now_price = Math.ceil((now_kwh * price)*100)/100;
    $("#seb").text(number_1000(now_price));
    setTimeout(rf_data, 1000);
}
function number_1000(n) {
    n += "";
    var arr = n.split(".");
    var re = /(\d{1,3})(?=(\d{3})+$)/g;
    return arr[0].replace(re,"$1,") + (arr.length == 2 ? "" : "");
}

$(function() {
    $("#login_but").click(function(){
        json("/user_login", $("#user_login").serialize(),function(data){
            if (data.info == "done") {
                location.href = "/monitor.html";
            }else{
                alert(data.info);
            }
        },function(data){
            if (data.info == "done") {
                location.href = "/monitor.html";
            }else{
                alert(data.info);
            }
        });
    });
    $('#user_id').keydown(function(event) {
        if (event.which == 13) {
            $("#ulaitem0z6z0").click();
        }
    });
    $('#user_pw').keydown(function(event) {
        if (event.which == 13) {
            $("#ulaitem0z6z0").click();
        }
    });

    //是否可以改變
    var can_change = true;
    function go_prev(){
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
            $copy.slideDown(500,function(){
                //把最後一個移除
                $last.remove();
                can_change = true;
            });

    }

    function go_next(){
            can_change = false;
            //取得第一個 li
            var $first = $('.news_marquee ul li').first();
            //建立復制體
            var $copy = $first.clone();

            //向上移動，並刪除
            $first.slideUp(500,function(){
                $first.remove();
                can_change = true;
            });
            //加到 ul 裡面的最後面
            $copy.appendTo($('.news_marquee ul'));
    }

    //run();
    //setTimeout(run, 1000); // 只 run 1次
    //setInterval(run, 3000); // 不斷執行

    $("#next").click(function(){
        if (can_change == true)
        {
            go_next();
        }
    });

    $("#prev").click(function(){
        if (can_change == true)
        {
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
	for(var i=0;i<$ad.length;i++){
		str += '<a href="#">' + (i + 1) + '</a>';
	}
	var $controlA = $('#abgne_fade_pic').append($('<div class="control">' + str + '</div>').css('zIndex', defaultZ + 1)).find('.control a');
    $(".top_menu_button_7").click(function(){
       $(this).toggleClass('active');
    });
	// 當按鈕被點選時
	// 若要變成滑鼠滑入來切換時, 可以把 click 換成 mouseover
	$controlA.click(function(){
		// 取得目前點擊的號碼
		showIndex = $(this).text() * 1 - 1;
 
		// 顯示相對應的區域並把其它區域變成透明
		$ad.eq(showIndex).stop().fadeTo(fadeInSpeed, 1).css('zIndex', defaultZ).siblings('a').stop().fadeTo(fadeOutSpeed, 0).css('zIndex', defaultZ - 1);
		// 讓 a 加上 .on
		$(this).addClass('on').siblings().removeClass('on');
 
		return false;
	}).focus(function(){
		$(this).blur();
	}).eq(showIndex).addClass('on');

	$ad.hover(function(){
		isHover = true;
		// 停止計時器
		clearTimeout(timer);
	}, function(){
		isHover = false;
		// 啟動計時器
		timer = setTimeout(autoClick, 3100);
	})

	// 自動點擊下一個
	function autoClick(){
		if(isHover) return;
		showIndex = (showIndex + 1) % $controlA.length;
		$controlA.eq(showIndex).click();
	}

    $(window).resize(function(){
        var left = $(".top_tel").position().left + 20;
        $("#corporate_contributions_info").css("left", left + "px");
        var top = 102;
        $("#corporate_contributions_info").css("top", top + "px");
    });
    $(window).resize();
    $("#corporate_contributions_info").mouseenter(function(){
        $(this).stop().animate({
            height: "160px"
        });
    }).mouseleave(function(){
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
    $('.jcarousel img').click(function() {
        $('.bPic > img:last').attr('src', $(this).attr('img_src')).ScaleImg();
    }).css('cursor', 'pointer').first().click();
});
