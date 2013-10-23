/*global window  */
/*global jQuery */
/*global $ */

var CKEDITOR_BASEPATH = "/template/backend/v1/ckeditor/";
var gs = null;
jQuery(function () {
    "use strict";
    gs = {
        init: function (lang) {
            //清除本地快取
            var loc_str = "";
            if (window.location.href.indexOf("localhost") > 0) {
                loc_str = Math.random().toString();
            }
            function padStr(i) {
                return (i < 10) ? "0" + i : i;
            }
            gs.information.application_version = $("body").data("application-version");
            gs.information.backend_version = $("body").data("backend-version");
            gs.information.version = "gs-" +
                gs.information.backend_version.toString() + gs.information.application_version.toString() + loc_str;
            if (window.localStorage) {
                if (window.localStorage.version !== gs.information.version) {
                    gs.ui.clearLocalStorageCache();
                    window.localStorage.version = gs.information.version;
                }
            }
            this.ui.init();
        },
        ajax: (function () {
            return {
                get: function (url, data, successCallback, errorCallback) {
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
                },
                json: function (url, data, successCallback, errorCallback) {
                    $.ajax({
                        url: url,
                        type: "POST",
                        dataType: "json",
                        data: data,
                        async: false,
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
                }
            };
        }()),
        cookie: (function () {
            var day = 30;
            return {
                setValue: function (name, value) {
                    var Days = day, the_day_sec = 86400000, exp  = new Date();
                    exp.setTime(exp.getTime() + Days * the_day_sec);
                    window.document.cookie = name.toString() + "=".encodeURI(value) + ";expires=" + exp.toGMTString();
                },
                getValue: function (name) {
                    var arr = window.document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
                    if (arr !== null) { return decodeURI(arr[2]); }
                    return null;
                },
                deleteValue: function (name) {
                    var exp = new Date(), cval = this.getValue(name);
                    exp.setTime(exp.getTime() - 1);
                    if (cval !== null) {
                        window.document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
                    }
                }
            };
        }()),
        lang: (function () {
            var current = "",
                current_setting = null,
                list = [],
                i = 0,
                isInList = function (lang) {
                    for (i = 0; i < list.length; i += 1) {
                        if (lang.indexOf(list[i].key) >= 0) {
                            return true;
                        }
                    }
                    return false;
                };
            return {
                append: function (lang, setting) {
                    if (isInList(lang) === false) {
                        var the_lang_need_to_insert = {key: lang, setting: setting};
                        list.push(the_lang_need_to_insert);
                        if (current_setting === null) {
                            current_setting = the_lang_need_to_insert;
                        }
                    }
                },
                change: function (lang) {
                    if (lang !== undefined) {
                        current = lang;
                        gs.cookie.setValue("gs.uiLang", lang);
                    }
                    if (isInList(lang)) {
                        gs.lang.applyToHtml();
                    } else {
                        gs.ui.insertLanguages(lang);
                    }
                },
                applyToHtml: function () {
                    var i = 0;
                    for (i = 0; i < list.length; i += 1) {
                        if (current.indexOf(list[i].key) >= 0) {
                            current_setting = list[i].setting;
                        }
                    }
                    jQuery("*").each(function () {
                        if (jQuery(this).data("lang") !== undefined) {
                            var msg = jQuery(this).data("lang").toLowerCase();
                            msg = gs.lang.getLocalization(msg);
                            jQuery(this).text(msg);
                        }
                    });
                },
                getLocalization: function (key) {
                    var i = 0;
                    if (current_setting !== null) {
                        for (i = 0; i < current_setting.length; i += 1) {
                            if (key.toLowerCase() === current_setting[i].key.toLowerCase()) {
                                return current_setting[i].label;
                            }
                        }
                    }
                    return key;
                },
                set: function (lang) {
                    current = lang;
                },
                get: function () {
                    return current;
                }
            };
        }()),
        menu: (function () {
            var theList = [],
                can_change_page = true;
            var setMainMenuStyle = function (url){
                gs.ui.areaMainMenu.find("li.menu a").each(function () {
                    if ($(this).attr("href").toString() === url) {
                        gs.ui.areaMainMenu.find("li.active").removeClass("active").find("a i").addClass("icon-white");
                        if (url != "/admin/welcome.html"){
                            $(this).parent().addClass("active").find("a i").removeClass("icon-white");
                        }
                    }
                });
            };
            var setSubMenuStyle = function (url){
                var not_find = true;
                gs.ui.areaSideMenu.find("li.menu a").each(function () {
                    if ($(this).attr("href").toString() === url && not_find) {
                        gs.ui.areaSideMenu.find("li.active").removeClass("active");
                        $(this).parent().addClass("active");
                        not_find = false;
                    }
                });
            }
            return {
                load: function () {
                    $("#page-footer").html('<ul id="temp_list" style="display:none"></ul>');
                    var i = 0, j = 0;
                    var url = "", sub_url = "";
                    var last_url = gs.interact.getLastUrl();
                    var sub_page_name = "";
                    for(i=0; i<gs.menu.list.length; i++)
                    {
                        var temp_list = gs.menu.list[gs.menu.list[i]];
                        $("#temp_list").html("");
                        for(var j=0; j<temp_list.length; j++)
                        {
                            $("#temp_list").append(temp_list[j]);
                        }
                        $("#temp_list").find("a").each(function(){
                            if (last_url.indexOf($(this).attr("href")) > -1)
                            {
                                url = gs.menu.list[i];
                                if ($(this).parent().hasClass("hide") == true){
                                    sub_url = $(this).parent().data("menu-for");
                                    if (sub_page_name == "")
                                    {
                                        sub_page_name = $(this).find("span").data("lang");
                                    }
                                }else{
                                    sub_url = $(this).attr("href");
                                }
                            }
                        });
                    }
                    var menu_list = gs.menu.list[url];
                    if (menu_list !== undefined) {
                        gs.ui.areaSideMenu.find(".nav-list").html('');
                        for (i = 0; i < menu_list.length; i += 1) {
                            gs.ui.areaSideMenu.find(".nav-list").append(menu_list[i]);
                        }
                    }
                    $("body").data("sub_page_name", sub_page_name);
                    setMainMenuStyle(url);
                    setSubMenuStyle(sub_url);
                    gs.ui.refresh();
                },
                lock: function () {
                    can_change_page = false;
                },
                unlock: function () {
                    can_change_page = true;
                },
                is_lock: function () {
                    return !can_change_page;
                },
                list : theList
            };
        }()),
        message: (function () {
            return {
                error : function (text) {
                    gs.ui.areaContent.prepend('<div class="alert alert-error">' + text + '<button type="button" class="close" data-dismiss="alert">&times;</button></div>');
                    setTimeout('gs.message.slideUp()', 5000);
                },
                information : function (text) {
                    gs.ui.areaContent.prepend('<div class="alert alert-info">' + text + '<button type="button" class="close" data-dismiss="alert">&times;</button></div>');
                    setTimeout('gs.message.slideUp()', 5000);
                },
                success : function (text) {
                    gs.ui.areaContent.prepend('<div class="alert alert-success">' + text + '<button type="button" class="close" data-dismiss="alert">&times;</button></div>');
                    setTimeout('gs.message.slideUp()', 5000);
                },
                warning : function (text) {
                    gs.ui.areaContent.prepend('<div class="alert">' + text + '<button type="button" class="close" data-dismiss="alert">&times;</button></div>');
                    setTimeout('gs.message.slideUp()', 5000);
                },
                slideUp : function () {
                    $(".alert").slideUp();
                }
            };
        }()),
        interact: (function () {
            var i = 0,
                lastPage = "",
                beforeJsonCallBack = null,
                afterJsonCallBack = null,
                beforePageLoadCallBack = null,
                afterPageLoadCallBack = null,
                beforeSubmitDataCallBack = null,
                afterSubmitDataCallBack = null,
                afterPageLoad = function (page, url) {
                    lastPage = url;
                    gs.ui.areaContent.html(page);
                    gs.menu.load();
                    if (afterPageLoadCallBack) {
                        afterPageLoadCallBack(url);
                    }
                    gs.ui.refresh();
                },
                afterSubmitData = function (data) {
                    if (afterSubmitDataCallBack) {
                        afterSubmitDataCallBack(data);
                    }
                };
            return {
                reload: function () {
                    var ls = lastPage;
                    lastPage = lastPage + "?" + Math.random();
                    this.load(ls);
                },
                load: function (new_url) {
                    if (new_url === "#") { return false; }
                    if (gs.menu.is_lock()) { return false; }
                    if (lastPage !== new_url) {
                        if (gs.ui.areaContent !== null) {
                            gs.ui.areaContent.html('<div style="padding:10px"><i class="icon-spinner icon-spin icon-2x pull-left"></i></div>');
                            var ajax_url = "";
                            if (new_url !== undefined) {
                                if (new_url.indexOf("?") >= 0) {
                                    ajax_url = new_url + "&r=" + Math.random();
                                } else {
                                    ajax_url = new_url + "?r=" + Math.random();
                                }
                                $("#uiTopBar").html("");
                                gs.menu.lock();
                                if (beforePageLoadCallBack) {
                                    beforePageLoadCallBack(new_url);
                                }
                                lastPage = new_url;
                                gs.ajax.get(ajax_url , null, function (page) {
                                    gs.menu.unlock();
                                    afterPageLoad(page, new_url);
                                    return false;
                                }, function (page) {
                                    gs.menu.unlock();
                                    afterPageLoad(page, new_url);
                                    return false;
                                });
                            }
                        }
                    }
                    return false;
                },
                submit: function (url) {
                    if (url === undefined) {
                        url = lastPage.toString();
                    }
                    var form = gs.ui.areaContent.find("form");
                    if (form.length === 0) {
                        gs.ui.areaContent.prepend("<form>").append("</form>");
                        form = gs.ui.areaContent.find("form");
                    }
                    if (beforeSubmitDataCallBack) {
                        beforeSubmitDataCallBack(url, form);
                    }
                    var d = form.serialize();
                    gs.ajax.json(url, d, afterSubmitData, afterSubmitData);
                },
                json: function (url, data) {
                    if (beforeJsonCallBack) {
                        beforeJsonCallBack();
                    }
                    gs.ajax.json(url, data, afterJsonCallBack, afterJsonCallBack);
                },
                beforeSubmit: function (callback) {
                    beforeSubmitDataCallBack = callback;
                },
                afterSubmit : function (callback) {
                    afterSubmitDataCallBack = callback;
                },
                beforeJson : function (callback) {
                    beforeJsonCallBack = callback;
                },
                afterJson : function (callback) {
                    afterJsonCallBack = callback;
                },
                beforeLoad : function (callback) {
                    beforePageLoadCallBack = callback;
                },
                afterLoad : function (callback) {
                    afterPageLoadCallBack = callback;
                },
                getLastUrl : function () {
                    return lastPage.toString();
                }
            };
        }()),
        ui: (function () {
            var uiLoader = {
                loading_progress: 0,
                load_test: 0,
                ui_is_ready: false,
                plugins_list : [],
                insertPlugins: function (fileUrl, fileType) {
                    if (this.isInList(fileUrl) === false) {
                        var the_plugins_need_to_insert = {fileUrl: fileUrl, fileType: fileType};
                        this.plugins_list.push(the_plugins_need_to_insert);
                    }
                },
                isInList: function (fileUrl) {
                    var i = 0;
                    for (i = 0; i < this.plugins_list.length; i += 1) {
                        if (fileUrl.indexOf(this.plugins_list[i].fileUrl) >= 0) {
                            return true;
                        }
                    }
                    return false;
                },
                start: function () {
                    var path = $("body").data("backend-path");
                    fileLoader.script(path + 'admin/javascript/' + gs.lang.get() + '.js', function () {
                        gs.ui.refresh();
                        uiLoader.jqueryAddress();
                    });
                },
                jqueryAddress: function () {
                    fileLoader.script('/static/jQueryAddress/jquery.address-1.5.min.js', function () {
                        $.address.change(function(event) {
                            var h = event.value;
                            if (h === "/") {
                                return false;
                            }
                            if (h == null || h.toString() !== "") {
                                if (h != gs.interact.getLastUrl())
                                {
                                    gs.interact.load(h, false);
                                }
                            }
                        });
                        uiLoader.bootstrapStyle();
                    });
                },
                bootstrapStyle: function () {
                    fileLoader
                        .script('/template/backend/v1/bootstrap/bootstrap.min.js')
                        .style('/template/backend/v1/bootstrap/bootstrap.min.css')
                        .wait(function () {
                            uiLoader.buildProgressBar();
                        });
                },
                buildProgressBar: function () {
                    fileLoader
                        .style('/template/backend/v1/css/v1.css', function () {
                            $("#progress-box").html('<div id="progress-info"><br/></div><div id="progress-bar" class="progress progress-striped active"><div class="bar" id="progress-ui-loading"></div></div>').show();
                            uiLoader.showProgress("uiLoader.buildProgressBar");
                            uiLoader.loadPlugins();
                        });
                },
                loadPlugins: function () {
                    var pn = this.plugins_list.pop();
                    if (pn === undefined) {
                        uiLoader.showProgress("uiLoader.complete");
                        uiLoader.complete();
                    } else {
                        uiLoader.showProgress(pn.fileUrl);
                        if (pn.fileType === "style") {
                            fileLoader.style(pn.fileUrl);
                        }
                        if (pn.fileType === "script") {
                            fileLoader.script(pn.fileUrl);
                        }
                        uiLoader.loadPlugins();
                    }
                },
                showProgress: function (msg) {
                    this.load_test += 1;
                    if (msg === undefined) {
                        msg = "";
                    }
                    this.loading_progress += 101 / (this.plugins_list.length + 2);
                    if (msg === "") {
                        msg = gs.lang.getLocalization("loading");
                    }
                    msg = gs.lang.getLocalization(msg);
                    $("#progress-info").text(msg);
                    $("#progress-ui-loading").width(this.loading_progress + "%");
                },
                complete: function () {
                    gs.ui.refresh();
                    var path = $("body").data("backend-path");
                    fileLoader.script(path + 'admin/javascript/menu.js', function () {
                        uiLoader.startPage();
                        uiLoader.startMenu();
                        $("#backend-logo").html($("#backend-logo-hide").html());
                        fileLoader.script('/template/backend/v1/js/admin.js', function () {
                            gs.ui.refresh();
                            $("#progress-box").remove();
                            fileLoader.style('/template/backend/v1/css/v1.css');
                            uiLoader.loadFirstPage();
                        });
                    });
                },
                startPage: function () {
                    var backend_title = $("body").data("backend-title");
                    var admin_user = $("body").data("administrator-account");
                    $("#page-content").html(
                        '<div class="container">' +
                            '<div id="uiMainMenu"><ul class="nav nav-list"></ul></div>' +
                            '<div id="uiSideMenu">' +
                                '<div class="user_infobox"><br /><br />' +
                                    backend_title + '<br />' +
                                    admin_user + '<br />' +
                                '</div>' +
                                '<ul class="nav nav-list"></ul>' +
                            '</div>' +
                            '<div id="uiLinkBox">' +
                                '<a href="/" target="_blank" data-lang="frontend" class="frontend"></a>' +
                                '<a href="/admin/logout.html" data-lang="logout" class="logout"></a>' +
                            '</div>' +
                            '<div id="uiTopBar"></div>' +
                            '<div id="uiContent">' +
                                '<div id="uiContentTop"></div>' +
                                '<div id="uiContentHr"></div>' +
                                '<div id="uiContentPage"></div>' +
                            '</div>' +
                            '<div class="clearfix"></div>' +
                        '</div>'
                    );
                    gs.ui.areaMainMenu = $("#uiMainMenu");
                    gs.ui.areaSideMenu = $("#uiSideMenu");
                    gs.ui.areaContent = $("#uiContentPage");
                },
                startMenu : function () {
                    var mainList = gs.menu.list["main"],
                        i = 0;
                    for (i = 0; i < mainList.length; i += 1) {
                        gs.ui.areaMainMenu.find("ul").append(mainList[i]);
                    }
                    gs.ui.areaMainMenu.find("li.menu a").each(function () {
                        gs.menu.list.push($(this).attr("href"));
                    }).live("click", function () {
                        if (gs.menu.is_lock() === false) {
                            $.address.value($(this).attr('href'));
                        }
                        return false;
                    });
                    gs.ui.areaSideMenu.find("li.lang a").live("click", function () {
                        var lang = $(this).find("span").data("lang");
                        lang = lang.replace("language_", "");
                        gs.lang.change(lang);
                        return false;
                    });
                    gs.ui.areaSideMenu.find("li.menu a").live("click", function () {
                        if (gs.menu.is_lock() === false) {
                            $.address.value($(this).attr('href'));
                        }
                        return false;
                    });
                    gs.ui.areaContent.find("button").live("click", function () {
                        if ($(this).data("page-url") !== undefined) {
                            $.address.value($(this).data("page-url"));
                        }
                        if ($(this).data("window-url") !== undefined) {
                            var p = $(this).data("window-name");
                            if (p == "")
                            {
                                p = "_blank";
                            }
                            var n = window.open($(this).data("window-url"), p);
                        }
                        if ($(this).data("json-url") !== undefined) {
                            gs.interact.json($(this).data("json-url"));
                        }
                        if ($(this).attr("type") !== undefined && $(this).attr("type") === "submit") {
                            var url = $(this).parents("form").attr("action");
                            gs.interact.submit(url);
                            return false;
                        }
                        return false;
                    });
                    $("#uiContentTop").find("button").live("click", function () {
                        if ($(this).data("page-url") !== undefined) {
                            $.address.value($(this).data("page-url"));
                        }
                        if ($(this).data("window-url") !== undefined) {
                            var p = $(this).data("window-name");
                            if (p == "")
                            {
                                p = "_blank";
                            }
                            var n = window.open($(this).data("window-url"), p);
                        }
                        if ($(this).data("json-url") !== undefined) {
                            gs.interact.json($(this).data("json-url"));
                        }
                        if ($(this).attr("type") !== undefined && $(this).attr("type") === "submit") {
                            var url = $(this).parents("form").attr("action");
                            gs.interact.submit(url);
                            return false;
                        }
                        return false;
                    });
                },
                loadFirstPage: function () {
                    if (location.hash == "") {
                        gs.interact.load($("body").data("backend-start-page"))
                    }else{
                        gs.interact.load(location.hash.replace("#",""));
                    }
                    $(window).resize(function(){
                        var w0 = $(this).width() - 302;
                        var h0 = $(this).height();
                        var h1 = $(this).height() - 86;
                        $("#uiMainMenu").height(h0);
                        $("#uiSideMenu").height(h0);
                        $("#uiContentPage").height(h1);
                        $("#uiContent").width(w0);
                        $("#uiTopBar").width(w0);

                    });
                    $(window).resize();
                }
            };
            var fileLoader = (function (window) {
                var scripts = [],
                    executedCount = 0,
                    waitCount = 0,
                    waitCallbacks = [],
                    localStorage = window.localStorage || null,
                    get = function (url, callback) {
                        gs.ajax.get(url,null,callback,function(){
                            callback("error");
                        });
                    },
                    scriptEval = function (text) {
                        var script = window.document.createElement("script"),
                            head = window.document.getElementsByTagName("head")[0],
                            textNode = window.document.createTextNode(text);
                        script.setAttribute('type', 'text/javascript');
                        try {
                            script.appendChild(window.document.createTextNode(text));
                            head.insertBefore(script, head.firstChild);
                            head.removeChild(script);
                        } catch (e) {
                            script.text = text;
                            window.document.getElementsByTagName('body')[0].appendChild(script);
                        }

                    },
                    insertStyle = function (text) {
                        var style = window.document.createElement("style"),
                            head = window.document.getElementsByTagName("head")[0];
                        style.type = "text/css";
                        try {
                            style.appendChild(window.document.createTextNode(text));
                            head.appendChild(style);
                        } catch (e) {
                            style.text = text;
                            window.document.getElementsByTagName('body')[0].appendChild(style);
                        }
                    },
                    queueExec = function (waitCount) {
                        var script, i, j, callback;
                        if (executedCount >= waitCount) {
                            for (i = 0; i < scripts.length; i += 1) {
                                script = scripts[i];
                                if (script) {
                                    scripts[i] = null;
                                    scriptEval(script);
                                    executedCount += 1;
                                    for (j = i; j < executedCount; j += 1) {
                                        if (callback = waitCallbacks[j]) {
                                            waitCallbacks[j] = null;
                                            callback();
                                        }
                                    }
                                }
                            }
                        }
                    };
                return {
                    script: function (path, callback) {
                        var key = gs.information.version + "-" + path,
                            scriptIndex = scripts.length,
                            waitCount_in = waitCount;
                        scripts[scriptIndex] = null;
                        if (localStorage && localStorage[key]) {
                            scripts[scriptIndex] = localStorage[key];
                            queueExec(waitCount_in);
                            if (callback) {
                                callback();
                            }
                        } else {
                            get(path, function (text) {
                                if (text != "" & text != "error")
                                {
                                    try {
                                        localStorage[key] = text;
                                    } catch (e) {

                                    }
                                    scripts[scriptIndex] = text;
                                    queueExec(waitCount_in);
                                }
                                if (callback) {
                                    callback(text);
                                }
                            });
                        }
                        return this;
                    },
                    style: function (path, callback) {
                        var key = gs.information.version + "-" + path;
                        if (localStorage && localStorage[key]) {
                            insertStyle(localStorage[key]);
                            //css = '<style type="text/css">' + localStorage[key] + '</style>';
                            // document.write(css);
                            if (callback) {
                                callback();
                            }
                        } else {
                            get(path, function (text) {
                                if (localStorage) {
                                    localStorage[key] = text;
                                }
                                insertStyle(text);
                                if (callback) {
                                    callback();
                                }
                            });
                        }
                        return this;
                    },
                    wait: function (callback) {
                        waitCount = scripts.length;
                        if (callback) {
                            if (executedCount >= waitCount - 1) {
                                callback();
                            } else {
                                waitCallbacks[waitCount - 1] = callback;
                            }
                        }
                        return this;
                    },
                    remove: function (paths) {
                        var i, key;
                        for (i = 0; i < paths.length; i += 1) {
                            key = gs.information.version + "-" + paths[i];
                            localStorage.removeItem(key);
                        }
                    },
                    clear: function () {
                        localStorage.clear();
                        return this;
                    }
                };
            }(window));
            return {
                areaMainMenu :  null,
                areaSideMenu :  null,
                areaContent :  null,
                init: function (lang) {
                    if (lang === undefined) {
                        lang = "zhtw";
                    }
                    if (gs.cookie.getValue("gs.uiLang") !== null) {
                        lang = gs.cookie.getValue("gs.uiLang");
                        if (lang.toString() === "undefined") {
                            lang = "zhtw";
                        }
                    }
                    gs.lang.set(lang);
                    uiLoader.start();
                },
                refresh: function () {
                    gs.lang.applyToHtml();
                    $(window).resize();
                },
                insertPlugins: function (fileUrl, fileType) {
                    return uiLoader.insertPlugins(fileUrl, fileType);
                },
                clearLocalStorageCache : (function () {
                    fileLoader.clear();
                }),
                insertLanguages : function (lang) {
                    var path = $("body").data("backend-path");
                    fileLoader.script(path + 'admin/javascript/' + lang + '.js', function () {
                        gs.lang.change(lang);
                    });
                }
            };
        }()),
        load : (function (){

        }),
        information: (function(){
            return {
                version: "",
                backend_version: "",
                application_version: ""
            }
        })
    };
    gs.ui.insertPlugins('/template/backend/v1/FortAwesome/css/font-awesome.css', 'style');
    gs.ui.insertPlugins('/template/backend/v1/artDialog/artDialog.skin.twitter.css', 'style');
    gs.ui.insertPlugins('/template/backend/v1/farbtastic/farbtastic.css', 'style');
    gs.ui.insertPlugins('/template/backend/v1/artDialog/jquery.artDialog.js', 'script');
    gs.ui.insertPlugins('/template/backend/v1/farbtastic/farbtastic.js', 'script');
    gs.ui.insertPlugins('/template/backend/v1/ckeditor/ckeditor.js', 'script');
    gs.ui.insertPlugins('/template/backend/v1/js/jquery-ui-1.9.2.custom.min.js', 'script');
    gs.ui.insertPlugins('/template/backend/v1/js/pager.js', 'script');
    gs.ui.insertPlugins('/template/backend/v1/js/jquery.hash.js', 'script');
    gs.init();
});