
gs.menu.list["main"] = [
    '<li class="menu"><a href="/admin/welcome.html" id="backend-logo"></li>',
    '<li class="menu"><a href="/admin/webpage/list.html"><i class="icon-file icon-white"></i><br /><span data-lang="內容"></span></a></li>',
    '<li class="menu"><a href="/admin/administrator/list.html"><i class="icon-cog icon-white"></i><br /><span data-lang="setting"></span></a></li>'
];
gs.menu.list["/admin/welcome.html"] = [
    '<li class="nav-header menu hide"><a href="/admin/welcome.html"><span data-lang="歡迎"></span></a></li>',
    '<li class="menu"></li>',
    '<li class="nav-header"><span data-lang="快捷選單"></span></li>',
    '<li class="menu"><a href="/admin/pastcase/create.html"><span data-lang="新增歷屆案例"></span></a></li>',
    '<li class="menu"><a href="/admin/pastcase/list.html"><span data-lang="檢視歷屆案例"></span></a></li>',
    '<li class="menu"><a href="/admin/hotcase/create.html"><span data-lang="新增熱銷專案"></span></a></li>',
    '<li class="menu"><a href="/admin/hotcase/list.html"><span data-lang="檢視熱銷專案"></span></a></li>',
    '<li class="menu"><a href="/admin/webimage/list.html"><span data-lang="網站圖片維護"></span></a></li>',
];
gs.menu.list["/admin/webpage/list.html"] = [
    '<li class="nav-header"><span data-lang="內容"></span></li>',
    '<li class="menu"><a href="/admin/webpage/list.html"><span data-lang="網站頁面"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webpage/list.html"><a href="/admin/webpage/create.html"><span data-lang="新增網站頁面"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/webpage/list.html"><a href="/admin/webpage/edit.html"><span data-lang="編輯網站頁面"></span></a></li>',
    '<li class="nav-header"><span data-lang="歷屆案例"></span></li>',
    '<li class="menu"><a href="/admin/pastcase/create.html"><span data-lang="新增歷屆案例"></span></a></li>',
    '<li class="menu"><a href="/admin/pastcase/list.html"><span data-lang="檢視歷屆案例"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/pastcase/list.html"><a href="/admin/pastcase/edit.html"><span data-lang="編輯歷屆案例"></span></a></li>',
    '<li class="nav-header"><span data-lang="熱銷專案"></span></li>',
    '<li class="menu"><a href="/admin/hotcase/create.html"><span data-lang="新增熱銷專案"></span></a></li>',
    '<li class="menu"><a href="/admin/hotcase/list.html"><span data-lang="檢視熱銷專案"></span></a></li>',
    '<li class="menu hide" data-menu-for="/admin/hotcase/list.html"><a href="/admin/hotcase/edit.html"><span data-lang="編輯熱銷專案"></span></a></li>'
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
];