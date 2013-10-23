
gs.menu.list["main"] = [
    //'<li class="menu"><a href="/backend/page/index.html"><i class="icon-th-list icon-white"></i> <span data-lang="內容"></span></a></li>',
    '<li class="menu"><a href="/admin/customer/index.html"><i class="icon-th-list icon-white"></i> <span data-lang="客戶資料"></span></a></li>',
    //'<li class="menu"><a href="/backend/marquee/index.html"><i class="icon-th-list icon-white"></i> <span data-lang="跑馬燈"></span></a></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><i class="icon-cog icon-white"></i> <span data-lang="setting"></span></a></li>'
];
gs.menu.list["/admin/page/index.html"] = [
    '<li class="nav-header"><span data-lang="內容"></span></li>',
    '<li class="menu"><a href="/admin/page/edit.html?name=index"><span data-lang="關於安祐"></span></a></li>',
    '<li class="menu"><a href="/admin/page/edit.html?name=envir"><span data-lang="環境介紹"></span></a></li>',
    '<li class="menu"><a href="/admin/page/edit.html?name=contact"><span data-lang="聯絡我們"></span></a></li>'
];
gs.menu.list["/admin/customer/index.html"] = [
    '<li class="nav-header"><span data-lang="客戶資料"></span></li>',
    '<li class="menu"><a href="/admin/customer/create.html"><span data-lang="新增客戶資料"></span></a></li>',
    '<li class="menu"><a href="/admin/customer/list.html"><span data-lang="檢視客戶資料"></span></a></li>'
];
gs.menu.list["/admin/marquee/index.html"] = [
    '<li class="nav-header"><span data-lang="跑馬燈"></span></li>',
    '<li class="menu"><a href="/admin/marquee/create.html"><span data-lang="新增跑馬燈"></span></a></li>',
    '<li class="menu"><a href="/admin/marquee/list.html"><span data-lang="檢視跑馬燈"></span></a></li>'
];
gs.menu.list["/admin/interactive.html"] = [
    '<li class="nav-header"><span data-lang="member"></span></li>',
    '<li class="menu"><a href="/admin/newsletter/list.html"><span data-lang="edm_list"></span></a></li>',
    '<li class="menu"><a href="/admin/newsletter/sender.html"><span data-lang="edm_send"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="our_jobs_related_functions"></span></li>',
    '<li class="menu"><a href="/admin/recruit/list.html"><span data-lang="job_seekers"></span></a></li>',
    '<li class="divider"></li>',
    '<li class="nav-header"><span data-lang="contact_us"></span></li>',
    '<li class="menu"><a href="/admin/contact/list.html"><span data-lang="guestbook_list"></span></a></li>'
];
gs.menu.list["/admin/administrator/list.html"] = [
    '<li class="nav-header"><span data-lang="permissions_manage"></span></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><span data-lang="administrator_setting"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/administrator/list.html"><a href="/admin/administrator/edit.html"><span data-lang="administrator_setting"></span></a></li>',
    '<li class="divider"></li>'
    /*
    '<li class="nav-header"><span data-lang="language_setting"></span></li>',
    '<li class="lang"><a href="#"><span data-lang="language_zhtw"></span></a></li>',
    '<li class="lang"><a href="#"><span data-lang="language_zhcn"></span></a></li>',
    '<li class="lang"><a href="#"><span data-lang="language_enus"></span></a></li>',
    '<li class="divider"></li>'
    */
];