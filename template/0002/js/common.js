var isHover = true;

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

// 用 json 取得頁面
function json(b, c, e, a) {
    $.ajax({ url: b, type: "POST", dataType: "json", data: c, async: !1, success: function (a) {
        e(a)
    }, error: function (b, c, d) {
        void 0 == a ? show_message(d.message) : a(d.message)
    } })
};

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
});
