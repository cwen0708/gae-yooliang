jQuery(document).ready(function() {
	// 文字欄位內的提示文字_新版2012.07.31
	_hint = jQuery('.search').find('form').bind('submit', function() {
		/* 觸發清除訊息事件 */
		jQuery(this).find('input[title]').trigger('clear');
	}).end().delegate('input[title]', 'clear', function() {
		/* 清除預設訊息 */
		if (this.value == this.title && !jQuery(this).is('.pwd')) this.value = '';
	}).delegate('input[title]', 'focus', function() {
		/* 觸發焦點事件 */
		var input = jQuery(this);
		if (input.is('.pwd'))
		{
			if (this.type == 'text')
			{
				/* 密碼欄位 */
				var tmp = input.hide().prev().show();
		 
				/* For 笨 IE 延遲觸發焦點*/
				setTimeout(function() {
					tmp.trigger('focus');
				}, 5);
			}
		}
		else input.trigger('clear');
	}).delegate('input[title]', 'blur', function() {
		/* 觸發離開事件 */
		if (this.value == '' || this.value == this.title)
		{
			if (this.type == 'password') jQuery(this).hide().next().show();
			else this.value = this.title;
		}
	}).delegate('input[title]', 'init', function() {
		if (this.type == 'password') jQuery(this).parent().append('<input type="text" value="' +this.title+ '" title="" class="' +this.className+ '" />');
	}).find('input').trigger('init').trigger('blur');
	
	/* banner */
	$('#slides').slides({
				preload: true,
				preloadImage: 'images/loading.gif',
				play: 5000,
				pause: 2500,
				hoverPause: true,
			});
			
	/* 小圖換大圖 */
	$('.sPic img').each(function (index, domEle) {
		$(domEle).click(
			function() {
				/* 更換 bigPic 的圖片路徑 */
				var bigPic = $('.bPic > img:last');  /* 針對區塊下的最後一張圖 */
				/* var bigPic = $jQuery('.bigPic > span > img');  // 另一種區隔方法，大圖加標籤區隔 */
				var img_src = $(this).attr('img_src');  /* 更換bigPic的圖片路徑 */
				bigPic.attr('src', img_src);
			},
			function () {
			}
		);
	}).css('cursor', 'pointer');
	
	/* 小圖輪撥 */
        var sPicList_width = $(".sPic").length * 97;
        $('.sPicList').css('width',sPicList_width);
        var jcarousel_move_speed = 500;                                                 //移動速度
        var jcarousel_item_width = 97;                                                //項目的寬度
        var jcarousel_list_can_move = true;                                             //是否可以移動
        var jcarousel_list_width = jcarousel_item_width - ($(".sPicList .sPic").length * 97);   //整體寬度

        $('#next').click(function () {
            var next_stop = (sPicList_width - $("#jcarousel").width()) * -1 + jcarousel_item_width;
            if ($(".sPicList").position().left >= next_stop && jcarousel_list_can_move) {
                jcarousel_list_can_move = false;
                $('.sPicList').stop().animate({left: '-=' + jcarousel_item_width}, jcarousel_move_speed, 'linear', function () {
                    jcarousel_list_can_move = true;
                });
            }
        }).css('cursor', 'pointer');
        
        $('#prev').click(function () {
            if ($(".sPicList").position().left < 0 && jcarousel_list_can_move) {
                jcarousel_list_can_move = false;
                $('.sPicList').animate({left: '+=' + jcarousel_item_width}, jcarousel_move_speed, 'linear', function () {
                    jcarousel_list_can_move = true;
                });
            }
        }).css('cursor', 'pointer');
		
		/* faq */
		var sBlock = $('#slideDownUp'),
	list   = sBlock.find('div.pAnswer');
	sBlock.delegate('div.pQuestion', 'click', function() {
			var aObj = $(this).next();
      if (aObj.is()) {
        aObj.slideUp('600');
      }
      else {
        list.hide();
        aObj.slideDown('600');
      }
			
		}).find('div.pQuestion').first().trigger('click'); //.first().click(); 預設第一個打開,如果不要則拿掉
		
})


			
/* rightFloat */
    $(window).load(function(){
		var $win = $(window),
			$ad = $('#rightFloat').css('opacity', 0).show(),	// 讓廣告區塊變透明且顯示出來
            ml = parseInt($("#main").css("margin-left").replace("px","")),
            left = ml + $("#main").width() + 28;
			_width = $ad.width(),
			_height = $ad.height(),
			_diffY = 50, _diffX = 30,	// 距離右及上方邊距
			_moveSpeed = 800;	// 移動的速度

		// 先把 #abgne_float_ad 移動到定點
		$ad.css({
			top: _diffY,	// 往上
			left: left,
			opacity: 1
		});

		// 幫網頁加上 scroll 及 resize 事件
		$win.bind('scroll resize', function(){
			var $this = $(this);

            var ml = parseInt($("#main").css("margin-left").replace("px",""));
            var left = ml + $("#main").width() + 28;
            if ($(window).width() < left){
                left = $(window).width() - $('#rightFloat').width();
            }
			// 控制 #abgne_float_ad 的移動
			$ad.stop().animate({
				top: $this.scrollTop() + _diffY,	// 往上
				left: left
			}, _moveSpeed);
		}).scroll();	// 觸發一次 scroll()
	});