/*
 jQuery paging plugin v1.0.1 09/04/2011
 http://www.xarg.org/project/jquery-color-plugin-xcolor/

 Copyright (c) 2011, Robert Eisele (robert@xarg.org)
 Dual licensed under the MIT or GPL Version 2 licenses.
 */
/**
 * jQuery.query - Query String Modification and Creation for jQuery
 * Written by Blair Mitchelmore (blair DOT mitchelmore AT gmail DOT com)
 * Licensed under the WTFPL (http://sam.zoy.org/wtfpl/).
 * Date: 2008/05/28
 *
 * @author Blair Mitchelmore
 * @version 2.0.0
 *
 **/
(function (k, n, p) {
    k.fn.paging = function (s, t) {
        function r(a) { a.preventDefault(); a = a.target; do if ("a" === a.nodeName.toLowerCase()) break; while (a = a.parentNode); o.setPage(k.data(a, "page")); if (o.n) n.location = a.href } var u = this, o = { setOptions: function (a) {
            this.a = k.extend(this.a || { lapping: 0, perpage: 10, page: 1, refresh: { interval: 10, url: null }, format: "", onFormat: function () { }, onSelect: function () { return true }, onRefresh: function () { } }, a || {}); this.a.perpage < 1 && (this.a.perpage = 10); if (this.a.refresh.url) this.k && n.clearInterval(this.k),
                this.k = n.setInterval(function (a, h) { h.ajax({ url: a.a.refresh.url, success: function (g) { try { var j = h.parseJSON(g) } catch (c) { return } a.a.onRefresh(j) } }) }, 1E3 * this.a.refresh.interval, this, k); this.l = function (a) {
                for (var h = 0, g = 0, j = 1, c = { e: [], h: 0, g: 0, c: 5, d: 3, j: 0, m: 0 }, f, k = /[*<>pq\[\]().-]|[nc]+!?/g, e = { "[": "first", "]": "last", "<": "prev", ">": "next", q: "left", p: "right", "-": "fill", ".": "leap" }, b = {}; f = k.exec(a); ) if (f = "" + f, p === e[f]) if ("(" === f) g = ++h; else if (")" === f) g = 0; else {
                    if (j) {
                        if ("*" === f) c.h = 1, c.g = 0; else if (c.h = 0, c.g = "!" ===
                            f.charAt(f.length - 1), c.c = f.length - c.g, !(c.d = 1 + f.indexOf("c"))) c.d = 1 + c.c >> 1; c.e[c.e.length] = { f: "block", i: 0, b: 0 }; j = 0
                    }
                } else c.e[c.e.length] = { f: e[f], i: g, b: p === b[f] ? b[f] = 1 : ++b[f] }, "q" === f ? ++c.m : "p" === f && ++c.j; return c
            } (this.a.format); return this
        }, setNumber: function (a) { this.o = p === a || a < 0 ? -1 : a; return this }, setPage: function (a) {
            if (p === a) { if (a = this.a.page, null === a) return this } else if (this.a.page == a) return this; this.a.page = a |= 0; var l = this.o, h = this.a, g, j, c, f, n = 1, e = this.l, b, d, i, m, o = e.e.length, q = o; h.perpage <= h.lapping &&
            (h.lapping = h.perpage - 1); m = l <= h.lapping ? 0 : h.lapping | 0; l < 0 ? (c = l = -1, g = Math.max(1, a - e.d + 1 - m), j = g + e.c) : (c = 1 + Math.ceil((l - h.perpage) / (h.perpage - m)), a = Math.max(1, Math.min(a < 0 ? 1 + c + a : a, c)), e.h ? (g = 1, j = 1 + c, e.d = a, e.c = c) : (g = Math.max(1, Math.min(a - e.d, c - e.c) + 1), j = e.g ? g + e.c : Math.min(g + e.c, 1 + c))); for (; q--; ) { d = 0; i = e.e[q]; switch (i.f) { case "left": d = i.b < g; break; case "right": d = j <= c - e.j + i.b; break; case "first": d = e.d < a; break; case "last": d = e.c < e.d + c - a; break; case "prev": d = 1 < a; break; case "next": d = a < c } n |= d << i.i } b = { number: l, lapping: m,
                pages: c, perpage: h.perpage, page: a, slice: [(d = a * (h.perpage - m) + m) - h.perpage, Math.min(d, l)]
            }; for (f = k(document.createElement("div")); ++q < o; ) {
                i = e.e[q]; d = n >> i.i & 1; switch (i.f) {
                    case "block": for (; g < j; ++g) b.value = g, b.pos = 1 + e.c - j + g, b.active = g <= c || l < 0, b.first = 1 === g, b.last = g == c && 0 < l, d = document.createElement("div"), d.innerHTML = h.onFormat.call(b, i.f), k("a", d = k(d)).data("page", b.value).click(r), f.append(d.contents()); continue; case "left": b.value = b.pos = i.b; b.active = i.b < g; break; case "right": b.value = c - e.j + i.b; b.pos = i.b;
                        b.active = j <= b.value; break; case "first": b.value = 1; b.pos = i.b; b.active = d && e.d < a; break; case "last": b.value = c; b.pos = i.b; b.active = d && e.c < e.d + c - a; break; case "prev": b.value = Math.max(1, a - 1); b.pos = i.b; b.active = d && 1 < a; break; case "next": b.pos = i.b; (b.active = l < 0) ? b.value = 1 + a : (b.value = Math.min(1 + a, c), b.active = d && a < c); break; case "leap": case "fill": b.pos = i.b; b.active = d; f.append(h.onFormat.call(b, i.f)); continue
                } b.last = b.first = p; d = document.createElement("div"); d.innerHTML = h.onFormat.call(b, i.f); k("a", d = k(d)).data("page",
                    b.value).click(r); f.append(d.contents())
            } u.html(f.contents()); this.n = h.onSelect.call({ number: l, lapping: m, pages: c, slice: b.slice }, a); return this
        }
        }; return o.setNumber(s).setOptions(t).setPage()
    }
})(jQuery, this);