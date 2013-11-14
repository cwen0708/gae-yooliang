
gs.menu.list["main"] = [
    '<li class="menu"><a href="/admin/welcome.html" id="backend-logo"></li>',
    '<li class="menu"><a href="/admin/rawdata/list.html"><i class="icon-facetime-video icon-white"></i><br /><span data-lang="監控"></span></a></li>',
    '<li class="menu"><a href="/admin/product/list.html"><i class="icon-ok-circle icon-white"></i><br /><span data-lang="銷售"></span></a></li>',
    '<li class="menu"><a href="/admin/aboutus/list.html"><i class="icon-file icon-white"></i><br /><span data-lang="內容"></span></a></li>',
    '<li class="menu"><a href="/admin/customer/list.html"><i class="icon-th-list icon-white"></i><br /><span data-lang="客戶"></span></a></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><i class="icon-cog icon-white"></i><br /><span data-lang="setting"></span></a></li>'
];
gs.menu.list["/admin/welcome.html"] = [
    '<li class="nav-header menu hide"><a href="/admin/welcome.html"><span data-lang="歡迎"></span></a></li>',
    '<li class="menu"></li>',
    '<li class="nav-header"><span data-lang="快捷選單"></span></li>',
    '<li class="menu"><a href="/admin/monitor/list.html"><span data-lang="監控中心"></span></a></li>',
    '<li class="menu"><a href="/admin/news/create.html"><span data-lang="新增最新消息"></span></a></li>',
    '<li class="menu"><a href="/admin/rawdata/list.html"><span data-lang="原始資料"></span></a></li>',
    '<li class="menu"><a href="/admin/statuscode/list.html"><span data-lang="訊息代碼"></span></a></li>'
];
gs.menu.list["/admin/rawdata/list.html"] = [
    '<li class="nav-header"><span data-lang="監控"></span></li>',
    '<li class="menu"><a href="/admin/monitor/list.html"><span data-lang="監控中心"></span></a></li>',
    '<li class="menu"><a href="/admin/rawdata/list.html"><span data-lang="原始資料"></span></a></li>',
    '<li class="menu"><a href="/admin/statuscode/list.html"><span data-lang="訊息代碼"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/statuscode/list.html"><a href="/admin/statuscode/create.html"><span data-lang="新增訊息代碼"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/statuscode/list.html"><a href="/admin/statuscode/edit.html"><span data-lang="編輯訊息代碼"></span></a></li>'
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
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="依訂單狀態"></span></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=1"><span data-lang="新訂單"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=2"><span data-lang="處理中"></span></a></li>',
    '<li class="menu"><a href="/admin/orderinfo/list.html?order_status=3"><span data-lang="已完成"></span></a></li>',
];
gs.menu.list["/admin/aboutus/list.html"] = [
    '<li class="nav-header"><span data-lang="內容"></span></li>',
    '<li class="menu"><a href="/admin/aboutus/list.html"><span data-lang="公司簡介"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/aboutus/list.html"><a href="/admin/aboutus/create.html"><span data-lang="新增公司簡介"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/aboutus/list.html"><a href="/admin/aboutus/edit.html"><span data-lang="編輯公司簡介"></span></a></li>',
    '<li class="menu"><a href="/admin/solution/list.html"><span data-lang="系統套案"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/solution/list.html"><a href="/admin/solution/create.html"><span data-lang="新增系統套案"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/solution/list.html"><a href="/admin/solution/edit.html"><span data-lang="編輯系統套案"></span></a></li>',
    '<li class="menu"><a href="/admin/service/list.html"><span data-lang="專業服務"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/service/list.html"><a href="/admin/service/create.html"><span data-lang="新增專業服務"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/service/list.html"><a href="/admin/service/edit.html"><span data-lang="編輯專業服務"></span></a></li>',
    '<li class="menu"><a href="/admin/webpage/list.html"><span data-lang="其它頁面"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webpage/list.html"><a href="/admin/webpage/create.html"><span data-lang="新增其它頁面"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webpage/list.html"><a href="/admin/webpage/edit.html"><span data-lang="編輯其它頁面"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="訊息"></span></li>',
    '<li class="menu"><a href="/admin/banner/list.html"><span data-lang="輪撥圖"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/banner/list.html"><a href="/admin/banner/create.html"><span data-lang="新增輪撥圖"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/banner/list.html"><a href="/admin/banner/edit.html"><span data-lang="編輯輪撥圖"></span></a></li>',
    '<li class="menu"><a href="/admin/news/list.html"><span data-lang="最新消息"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/news/list.html"><a href="/admin/news/create.html"><span data-lang="新增最新消息"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/news/list.html"><a href="/admin/news/edit.html"><span data-lang="編輯最新消息"></span></a></li>',
    '<li class="menu"><a href="/admin/marquee/list.html"><span data-lang="跑馬燈"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/marquee/list.html"><a href="/admin/marquee/create.html"><span data-lang="新增跑馬燈"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/marquee/list.html"><a href="/admin/marquee/edit.html"><span data-lang="編輯跑馬燈"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="問與答"></span></li>',
    '<li class="menu"><a href="/admin/faqcategory/list.html"><span data-lang="問與答分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faqcategory/list.html"><a href="/admin/faqcategory/create.html"><span data-lang="新增問與答分類"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faqcategory/list.html"><a href="/admin/faqcategory/edit.html"><span data-lang="編輯問與答分類"></span></a></li>',
    '<li class="menu"><a href="/admin/faq/list.html"><span data-lang="問與答"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faq/list.html"><a href="/admin/faq/create.html"><span data-lang="新增問與答"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/faq/list.html"><a href="/admin/faq/edit.html"><span data-lang="編輯問與答"></span></a></li>'
];
gs.menu.list["/admin/customer/list.html"] = [
    '<li class="nav-header"><span data-lang="線上評估"></span></li>',
    '<li class="menu"><a href="/admin/contact2/list.html"><span data-lang="線上評估"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/contact2/list.html"><a href="/admin/contact2/edit.html"><span data-lang="檢視線上評估細節"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="客戶資料"></span></li>',
    '<li class="menu"><a href="/admin/customer/list.html"><span data-lang="客戶資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/customer/list.html"><a href="/admin/customer/create.html"><span data-lang="新增客戶資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/customer/list.html"><a href="/admin/customer/edit.html"><span data-lang="編輯客戶資料"></span></a></li>',
    '<li class="menu"><a href="/admin/caseinfo/list.html"><span data-lang="案場資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/caseinfo/list.html"><a href="/admin/caseinfo/create.html"><span data-lang="新增案場資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/caseinfo/list.html"><a href="/admin/caseinfo/edit.html"><span data-lang="編輯案場資料"></span></a></li>',
    '<li class="menu"><a href="/admin/equipment/list.html"><span data-lang="設備資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/equipment/list.html"><a href="/admin/equipment/create.html"><span data-lang="新增設備資料"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/equipment/list.html"><a href="/admin/equipment/edit.html"><span data-lang="編輯設備資料"></span></a></li>'
];
gs.menu.list["/admin/administrator/list.html"] = [
    '<li class="nav-header"><span data-lang="網站相關"></span></li>',
    '<li class="menu"><a href="/admin/websetting/list.html"><span data-lang="網站設定"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/websetting/list.html"><a href="/admin/websetting/create.html"><span data-lang="新增網站設定"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/websetting/list.html"><a href="/admin/websetting/edit.html"><span data-lang="編輯網站設定"></span></a></li>',
    '<li class="menu"><a href="/admin/webimage/list.html"><span data-lang="網站圖片"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webimage/list.html"><a href="/admin/webimage/create.html"><span data-lang="新增網站圖片"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webimage/list.html"><a href="/admin/webimage/edit.html"><span data-lang="編輯網站圖片"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="permissions_manage"></span></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><span data-lang="administrator_setting"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/administrator/list.html"><a href="/admin/administrator/create.html"><span data-lang="新增"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/administrator/list.html"><a href="/admin/administrator/edit.html"><span data-lang="編輯"></span></a></li>'
    /*
    '<li class="nav-header"><span data-lang="language_setting"></span></li>',
    '<li class="lang"><a href="#"><span data-lang="language_zhtw"></span></a></li>',
    '<li class="lang"><a href="#"><span data-lang="language_zhcn"></span></a></li>',
    '<li class="lang"><a href="#"><span data-lang="language_enus"></span></a></li>',
    '<li class="divider"></li>'
    */
];