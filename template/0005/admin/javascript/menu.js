
gs.menu.list["main"] = [
    '<li class="menu"><a href="/admin/welcome.html" id="backend-logo"></li>',
    '<li class="menu"><a href="/admin/product/list.html"><i class="icon-th-list icon-white"></i><br /><span data-lang="銷售"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=1"><i class="icon-ok-circle icon-white"></i><br /><span data-lang="訂單"></span></a></li>',
    '<li class="menu"><a href="/admin/member/list.html"><i class="icon-user icon-white"></i><br /><span data-lang="客戶"></span></a></li>',
    '<li class="menu"><a href="/admin/news/list.html"><i class="icon-file icon-white"></i><br /><span data-lang="內容"></span></a></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><i class="icon-cog icon-white"></i><br /><span data-lang="setting"></span></a></li>'
];
gs.menu.list["/admin/welcome.html"] = [
    '<li class="nav-header menu hide"><a href="/admin/welcome.html"><span data-lang="歡迎"></span></a></li>',
    '<li class="menu"></li>',
    '<li class="nav-header"><span data-lang="快捷選單"></span></li>',
    '<li class="menu"><a href="/admin/product/create.html"><span data-lang="新增產品"></span></a></li>',
    '<li class="menu"><a href="/admin/partners/list.html"><span data-lang="合作廠商"></span></a></li>',
    '<li class="menu"><a href="/admin/partners/list.html"><span data-lang="合作廠商"></span></a></li>'
];
gs.menu.list["/admin/product/list.html"] = [
    '<li class="nav-header"><span data-lang="產品"></span></li>',
    '<li class="menu"><a href="/admin/productcategory/list.html"><span data-lang="產品分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/productcategory/list.html"><a href="/admin/productcategory/create.html"><span data-lang="新增產品分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/productcategory/list.html"><a href="/admin/productcategory/edit.html"><span data-lang="編輯產品分類"></span></a></li>',
    '<li class="menu"><a href="/admin/product/list.html"><span data-lang="產品"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/product/list.html"><a href="/admin/product/create.html"><span data-lang="新增產品"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/product/list.html"><a href="/admin/product/edit.html"><span data-lang="編輯產品"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="付款"></span></li>',
    '<li class="menu"><a href="/admin/freighttype/list.html"><span data-lang="付款方式"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/freighttype/list.html"><a href="/admin/freighttype/create.html"><span data-lang="新增付款方式"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/freighttype/list.html"><a href="/admin/freighttype/edit.html"><span data-lang="編輯付款方式"></span></a></li>',
    '<li class="menu"><a href="/admin/freight/list.html"><span data-lang="運費"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/freight/list.html"><a href="/admin/freight/create.html"><span data-lang="新增運費"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/freight/list.html"><a href="/admin/freight/edit.html"><span data-lang="編輯運費"></span></a></li>',
    '<li class="menu"><a href="/admin/freight/full_list.html"><span data-lang="列表"></span></a></li>',
];
gs.menu.list["/admin/orderinfo/list.html?order_status=1"] = [
    '<li class="nav-header"><span data-lang="依訂單狀態"></span></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=1"><span data-lang="新訂單"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=2"><span data-lang="處理中"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=3"><span data-lang="已完成"></span></a></li>',
    '<li class="nav-header"><span data-lang="依付款情況"></span></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?pay_status=0"><span data-lang="未確認"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?pay_status=1"><span data-lang="待付款"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?pay_status=2"><span data-lang="對帳中"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?pay_status=3"><span data-lang="已收款"></span></a></li>',
    '<li class="nav-header"><span data-lang="依寄送情況"></span></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?send_status=0"><span data-lang="未確認"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?send_status=1"><span data-lang="備貨中"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?send_status=2"><span data-lang="補貨中"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?send_status=3"><span data-lang="已發貨"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?send_status=4"><span data-lang="已到貨"></span></a></li>',
];
gs.menu.list["/admin/news/list.html"] = [
    '<li class="nav-header"><span data-lang="內容"></span></li>',
    '<li class="menu"><a href="/admin/webpage/list.html"><span data-lang="網站頁面"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webpage/list.html"><a href="/admin/webpage/create.html"><span data-lang="新增網站頁面"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webpage/list.html"><a href="/admin/webpage/edit.html"><span data-lang="編輯網站頁面"></span></a></li>',
    '<li class="menu"><a href="/admin/aboutus/list.html"><span data-lang="關於我們"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/aboutus/list.html"><a href="/admin/aboutus/create.html"><span data-lang="新增關於我們"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/aboutus/list.html"><a href="/admin/aboutus/edit.html"><span data-lang="編輯關於我們"></span></a></li>',
    '<li class="nav-header"><span data-lang="輪撥圖"></span></li>',
    '<li class="menu"><a href="/admin/banner/list.html"><span data-lang="首頁輪撥圖"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/banner/list.html"><a href="/admin/banner/create.html"><span data-lang="新增首頁輪撥圖"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/banner/list.html"><a href="/admin/banner/edit.html"><span data-lang="編輯首頁輪撥圖"></span></a></li>',
    '<li class="menu"><a href="/admin/banner2/list.html"><span data-lang="內頁輪撥圖"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/banner2/list.html"><a href="/admin/banner2/create.html"><span data-lang="新增內頁輪撥圖"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/banner2/list.html"><a href="/admin/banner2/edit.html"><span data-lang="編輯內頁輪撥圖"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="最新消息"></span></li>',
    '<li class="menu"><a href="/admin/newscategory/list.html"><span data-lang="最新消息分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/newscategory/list.html"><a href="/admin/newscategory/create.html"><span data-lang="新增最新消息分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/newscategory/list.html"><a href="/admin/newscategory/edit.html"><span data-lang="編輯最新消息分類"></span></a></li>',
    '<li class="menu"><a href="/admin/news/list.html"><span data-lang="最新消息"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/news/list.html"><a href="/admin/news/create.html"><span data-lang="新增最新消息"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/news/list.html"><a href="/admin/news/edit.html"><span data-lang="編輯最新消息"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="問與答"></span></li>',
    '<li class="menu"><a href="/admin/faqcategory/list.html"><span data-lang="問與答分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faqcategory/list.html"><a href="/admin/faqcategory/create.html"><span data-lang="新增問與答分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faqcategory/list.html"><a href="/admin/faqcategory/edit.html"><span data-lang="編輯問與答分類"></span></a></li>',
    '<li class="menu"><a href="/admin/faq/list.html"><span data-lang="問與答"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faq/list.html"><a href="/admin/faq/create.html"><span data-lang="新增問與答"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faq/list.html"><a href="/admin/faq/edit.html"><span data-lang="編輯問與答"></span></a></li>'
];
gs.menu.list["/admin/member/list.html"] = [
    '<li class="nav-header"><span data-lang="會員資料"></span></li>',
    '<li class="menu"><a href="/admin/member/list.html"><span data-lang="會員資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/member/list.html"><a href="/admin/member/create.html"><span data-lang="新增會員資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/member/list.html"><a href="/admin/member/edit.html"><span data-lang="編輯會員資料"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="contact_us"></span></li>',
    '<li class="menu"><a href="/admin/guestbook/list.html"><span data-lang="guestbook_list"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/guestbook/list.html"><a href="/admin/guestbook/create.html"><span data-lang="--留言內容"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/guestbook/list.html"><a href="/admin/guestbook/edit.html"><span data-lang="查看留言內容"></span></a></li>',
];
gs.menu.list["/admin/administrator/list.html"] = [
    '<li class="nav-header"><span data-lang="網站設定"></span></li>',
    '<li class="menu"><a href="/admin/websetting/list.html"><span data-lang="網站設定"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/websetting/list.html"><a href="/admin/websetting/create.html"><span data-lang="新增網站設定"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/websetting/list.html"><a href="/admin/websetting/edit.html"><span data-lang="編輯網站設定"></span></a></li>',
    '<li class="menu"><a href="/admin/webimage/list.html"><span data-lang="網站圖片"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webimage/list.html"><a href="/admin/webimage/create.html"><span data-lang="新增網站圖片"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webimage/list.html"><a href="/admin/webimage/edit.html"><span data-lang="編輯網站圖片"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="permissions_manage"></span></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><span data-lang="administrator_setting"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/administrator/list.html"><a href="/admin/administrator/create.html"><span data-lang="新增管理員"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/administrator/list.html"><a href="/admin/administrator/edit.html"><span data-lang="編輯管理員"></span></a></li>',
    '<li class="divider"></li>'
    /*
    '<li class="nav-header"><span data-lang="language_setting"></span></li>',
    '<li class="lang"><a href="#"><span data-lang="language_zhtw"></span></a></li>',
    '<li class="lang"><a href="#"><span data-lang="language_zhcn"></span></a></li>',
    '<li class="lang"><a href="#"><span data-lang="language_enus"></span></a></li>',
    '<li class="divider"></li>'
    */
];