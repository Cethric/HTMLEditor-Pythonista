#!/usr/bin/env python
# coding: utf-8

# the following line is recommended to ease porting to Python 3
#  from __future__ import (absolute_import, division, print_function, unicode_literals)
# todo: uncomment the line above and then fix up all the print commands
import os
import json
import time
import HTMLParser
import threading

try:
    import ui
    import console
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
    import dummyConsole as console

DEBUG = True


def exception_str(exception):
    return '{}: {}'.format(exception.__class__.__name__, exception)

@ui.in_background
def show_hide_file_viewer(sender):
    #console.hud_alert("show_hide_file_viewer")
    ss_view = sender.superview.superview
    old_width = ss_view["fileViewContainer"].width
    show = old_width == 0
    width = 188 if show else 0
    x_mod = 8 if show else 0
    ss_view["fileViewContainer"].width = width
    ss_view["fileViewContainer"].set_needs_display()
    ss_view.set_needs_display()

    for subview in ("contentContainer", "toolsContainer"):
        ss_view[subview].x = width + x_mod
        ss_view[subview].width = ss_view.width - width - x_mod
        ss_view[subview].size_to_fit()
        ss_view[subview].set_needs_display()
        for sub in ss_view[subview].subviews:
            sub.size_to_fit()
            sub.set_needs_display()

            try:
                sub.reload()
            except:
                try:
                    sub["web_view"].reload()
                except:
                    pass



@ui.in_background
def server_editor(sender):
    sss_view = sender.superview.superview.superview
    if sss_view:
        sss_view.set_server_editor()
    else:
        console.hud_alert("server_editor")


class WebViewDelegate(object):
    def __init__(self):
        pass

    def webview_should_start_load(self, webview, url, nav_type):
        print "Loading %r of type %r" % (url, nav_type)
        return True

    def webview_did_finish_load(self, webview):
        webview.name = webview.evaluate_javascript("document.title")

    def webview_did_fail_load(self, webview, error_code, error_msg):
        print "%r Failed to load. %r %r" % (webview, error_code, error_msg)

@ui.in_background
def preview(sender):
    #console.hud_alert("preview")
    print "WEBVIEW?", sender.superview.superview.subviews[2].subviews[2].subviews[0]
    text = sender.superview.superview.subviews[2].subviews[2].subviews[0]["web_view"].evaluate_javascript("editor.getValue()")
    wv = ui.WebView()
    wv.delegate = WebViewDelegate()
    wv.load_html(text)
    wv.present("sheet")

@ui.in_background
def quitter(sender):
    print "ON QUIT"
    try:
        print "QUIT UI"
        result = 2
        result = console.alert("Close", "Close File or Quit", "Close File", "Quit")
        if result == 1:
            if sender.superview.superview:
                sender.superview.superview.on_close_file()
            else:
                console.hud_alert("Close File")
        elif result == 2:
            sender.superview.superview["contentContainer"].active = False
            if sender.superview.superview.superview:
                sender.superview.superview.superview.close()
            else:
                sender.superview.superview.close()
    except KeyboardInterrupt as e:
        print "User canceled the input. " + exception_str(e)

@ui.in_background
def configure(sender):
    sss_view = sender.superview.superview.superview
    if sss_view:
        sss_view.config_view.present("sheet")
        sss_view.config_view.wait_modal()
        tv = sender.superview.superview["contentContainer"].subviews[2].subviews[0].subviews[1]
        config = sss_view.config_view.config

        font_size = config.get_value("editor.font.size")
        gutter = config.get_value("editor.show.gutter")
        style = config.get_value("editor.style")
        margin = config.get_value("editor.print.margin")
        wrap = config.get_value("editor.line.wrap")
        soft_tab = config.get_value("editor.soft.tabs")
        tab_size = config.get_value("editor.tab.size")
        
        fs = '''for (var elm in document.getElementsByClass('.CodeMirror')) {
    elm.style.font_size = '%ipt';"
}''' % font_size
        print fs
        tv.eval_js(fs)
        #tv.eval_js("get_editor().getSession().setTabSize(%s);" % tab_size)
        #tv.eval_js("get_editor().getSession().setUseSoftTabs(%s);" % soft_tab)
        #tv.eval_js("get_editor().getSession().setUseWrapMode(%s);" % wrap)
        #tv.eval_js("get_editor().getSession().setShowPrintMargin(%s);" % margin)
        #tv.eval_js("get_editor().getSession().setShowInvisibles(%s);" % gutter)
        #tv.eval_js("get_editor().getSession().setTheme(%s);" % style)
        
        '''
            value: "",
            mode: "htmlmixed",
            theme: "default",
            indentUnit: 4,
            smartIndent: true,
            tabSize: 4,
            indentWithTabs: false,
            electricChars: true,
            //spceialChars: \[]\,
            //specialCharPlaceholder: function() {},
            rtlMoveVissually: false,
            keyMap: "default",
            //extraKeys: {},
            lineWrapping: false,
            lineNumbers: true,
            firstLineNumber: 1,
            //lineNumberFormatter: function(line) {return ""},
            //gutters: {},
            fixedGutter: true,
            scrollbarStyle: "native",
            coverGutterNextToScrollbar: false,
            inputStyle: "contenteditable",
            readOnly: false,
            showCursorWhenSelecting: true,
            lineWiseCopyCut: true,
            undoDepth: 250,
            historyEventDelay: 1250,
            //tabIndex: 0,
            autofocus: true,
            dragDrop: true,
            cursorBlinkRate: 530,
            cursorScrollMargin: 0,
            cursorHeight: 1,
            resetSelctionOnContextMenu: true,
            workTime: 200,
            workDelay: 300,
            pollInterval: 100,
            flattenSpans: true,
            addModeClass: true,
            maxHighlightLength: 10000,
            viewportMargin: 100,
            matchBrackets: true,
        '''
    else:
        console.alert("Configuration is only available through the Main View")


class TagDelegate (object):
    def __init__(self, js_eval):
        self.js_eval = js_eval
        
    def tableview_did_select(self, tableview, section, row):
        value = tableview.data_source.items[row]
        tableview.close()
        opts = ui.ScrollView()
        opts.bounces = True
        opts.always_bounce_horizontal = False
        opts.always_bounce_vertical = True
        opts.name = "Add Tag: %r" % value["title"]
        y = 10
        for k,v in value["options"].iteritems():
            print type(v) == type("str")
            if type(v) == type("str"):
                t = v
                v = ui.Label()
                v.text = t
            print "NEXT"
            v.name = k
            v.y = y
            v.x = 150
            l = ui.Label()
            l.text = "%s:" % k.title()
            l.y = y
            l.height = 25
            l.x = 20
            
            if k=="content":
                v.width = 350
                v.height = 300
                y+=305
            else:
                v.width = 200
                v.height = 25
                y+=30
            opts.add_subview(l)
            opts.add_subview(v)
        
        ok_btn = ui.Button()
        ok_btn.title = "Ok"
        ok_btn.y = y
        ok_btn.x = 20
        ok_btn.height = 25
        ok_btn.width = 100
        ok_btn.action = self.add
        print ok_btn.frame
        opts.add_subview(ok_btn)
        opts.size_to_fit()
        w,h = opts.content_size
        opts.content_size = (w, y+50)
        opts.present("sheet")
        
    @ui.in_background
    def add(self, sender):
        try:
            i = sender.superview.subviews
            sender.superview.close()
            data = {"type": sender.superview.name[9:].replace("'","")}
            for item in i:
                try:
                    if item.name:
                        data[item.name] = item.text
                except AttributeError as e:
                    print exception_str(e)
            out = json.dumps(self.get_element(data))
            print "editor.replaceSelection(%s);" % out
            self.js_eval("editor.replaceSelection(%s);" % out)
            
            #console.alert("Added Tag at Cursor")
        except KeyboardInterrupt as e:
            print "User Cancled the Function"
            print exception_str(e)
    
    def get_element(self, data):
        print data
        t = data["type"]
        del data["type"]
        tag_open = data["tag-open"]
        del data["tag-open"]
        if "content" in data or "tag-close" in data:
            tag_close = data["tag-close"]
            del data["tag-close"]
            if "content" in data:
                content = data["content"]
                del data["content"]
            else:
                content = ""
                
            if tag_open=="p":
                content = content.replace("\n", "<br/>")
            prop_str = []
            for k,v in data.iteritems():
                if v:
                    prop_str.append("%s='%s'" % (k, v))
            if t=="comment":
                elm_str = "%(tag-open)s %(content)s %(tag-close)s" % {
                                                                     "tag-open":tag_open,
                                                                     "tag-close":tag_close,
                                                                     "content": content,
                                                                     }
            else:
                elm_str = "<%(tag-open)s %(data)s> %(content)s </%(tag-close)s>" % {"tag-open":tag_open,
                                                                                    "tag-close":tag_close,
                                                                                    "content":content,
                                                                                    "data":" ".join(prop_str),
                                                                                     }
        else:
            prop_str = []
            for k,v in data.iteritems():
                if v:
                    prop_str.append("%s='%s'" % (k, v))
            elm_str = "<%(tag-open)s %(data)s />" % {"tag-open": tag_open,
                                                     "data": " ".join(prop_str),
                                                    }
        return elm_str# + "\n"

    def tableview_did_deselect(self, tableview, section, row):
        # Called  when a row was de-selected (in multiple selection mode).
        pass

    def tableview_title_for_delete_button(self, tableview, section, row):
        # Return the title for the 'swipe-to-***' button.
        return 'Delete'

GLOBAL_HTML_ATTR = {
                    "id":ui.TextField(),
                    "class":ui.TextField(),
                    "name":ui.TextField(),
                    "title":ui.TextField(),
                    }

@ui.in_background
def add_tag(sender):
    v = ui.TableView()
    v.data_source = ui.ListDataSource([
                                       {"title": "anchor",
                                        "options": dict({
                                                    "tag-open":"a",
                                                    "tag-close":"a",
                                                    "content":ui.TextField(),
                                                    "charset":ui.TextField(),
                                                    "coords":ui.TextField(),
                                                    "download":ui.TextField(),
                                                    "href":ui.TextField(),
                                                    "hreflang":ui.TextField(),
                                                    "media":ui.TextField(),
                                                    "rel":ui.TextField(),
                                                    "rev":ui.TextField(),
                                                    "shape":ui.TextField(),
                                                    "target":ui.TextField(),
                                                    "type":ui.TextField(),
                                                    }, **GLOBAL_HTML_ATTR)},
                                       {"title":"abbreviation",
                                        "options": dict({
                                                         "tag-open":"abbr",
                                                         "tag-close":"abbr",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"acronym - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"acronym",
                                                         "tag-close":"acronym",
                                                         "contents":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"address",
                                        "options": dict({
                                                         "tag-open":"address",
                                                         "tag-close":"address",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"applet - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"applet",
                                                         "tag-close":"applet",
                                                         "content":"",
                                                         "code":ui.TextField(),
                                                         "object":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "alt":ui.TextField(),
                                                         "archive":ui.TextField(),
                                                         "codebase":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "hspace":ui.TextField(),
                                                         "vspace":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"area",
                                        "options": dict({
                                                         "tag-open":"area",
                                                         "tag-close":"area",
                                                         "alt":ui.TextField(),
                                                         "coords":ui.TextField(),
                                                         "download":ui.TextField(),
                                                         "href":ui.TextField(),
                                                         "hreflang":ui.TextField(),
                                                         "media":ui.TextField(),
                                                         "nohref":ui.TextField(),
                                                         "rel":ui.TextField(),
                                                         "shape":ui.TextField(),
                                                         "target":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"article",
                                        "options": dict({
                                                         "tag-open":"article",
                                                         "tag-close":"article",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"aside",
                                        "options": dict({
                                                         "tag-open":"aside",
                                                         "tag-close":"aside",
                                                         "content":ui.TextView()
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"audio",
                                        "options": dict({
                                                         "tag-open":"audio",
                                                         "tag-close":"audio",
                                                         "content":ui.TextField(),
                                                         "preload":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"bold",
                                        "options": dict({
                                                         "tag-open":"b",
                                                         "tag-close":"b",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"base",
                                        "options": dict({
                                                         "tag-open":"base",
                                                         "tag-close":"base",
                                                         "href":ui.TextField(),
                                                         "target":ui.TextField(),
                                                         "content":"",
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"basefont - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"basefont",
                                                         "tag-close":"basefont",
                                                         "content":"",
                                                         "color":ui.TextField(),
                                                         "face":ui.TextField(),
                                                         "size":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"Bi-directional Isolation",
                                        "options": dict({
                                                         "tag-open":"bdi",
                                                         "tag-close":"bdi",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"Bi-directional Override",
                                        "options": dict({
                                                         "tag-open":"bdo",
                                                         "tag-close":"bdo",
                                                         "content":ui.TextView(),
                                                         "dir":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"big - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"big",
                                                         "tag-close":"big",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"blockquote",
                                        "options": dict({
                                                         "tag-open":"blockquote",
                                                         "tag-close":"blockquote",
                                                         "content":ui.TextView(),
                                                         "cite":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"body",
                                        "options": dict({
                                                         "tag-open":"body",
                                                         "tag-close":"body",
                                                         "content":ui.TextView(),
                                                         "alink":ui.TextField(),
                                                         "background":ui.TextField(),
                                                         "bgcolor":ui.TextField(),
                                                         "link":ui.TextField(),
                                                         "text":ui.TextField(),
                                                         "vlink":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"line break",
                                        "options": dict({
                                                         "tag-open":"br",
                                                         "tag-close":"br",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"button",
                                        "options": dict({
                                                         "tag-open":"button",
                                                         "tag-close":"button",
                                                         "content":ui.TextField(),
                                                         "autofocus":ui.TextField(),
                                                         "disabled":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "formaction":ui.TextField(),
                                                         "formenctype":ui.TextField(),
                                                         "formmethod":ui.TextField(),
                                                         "formnovalidate":ui.TextField(),
                                                         "formtarget":ui.TextField(),
                                                         "name":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"canvas",
                                        "options": dict({
                                                         "tag-open":"canvas",
                                                         "tag-close":"canvas",
                                                         "content":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"caption",
                                        "options": dict({
                                                         "tag-open":"caption",
                                                         "tag-close":"caption",
                                                         "content":ui.TextView(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"center",
                                        "options": dict({
                                                         "tag-open":"center",
                                                         "tag-close":"center",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"cite",
                                        "options": dict({
                                                         "tag-open":"cite",
                                                         "tag-close":"cite",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"code - (CSS Provides Richer Effects)",
                                        "options": dict({
                                                         "tag-open":"code",
                                                         "tag-close":"code",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"col",
                                        "options": dict({
                                                         "tag-open":"col",
                                                         "align":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "span":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"colgroup",
                                        "options": dict({
                                                         "tag-open":"colgroup",
                                                         "tag-close":"colgroup",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "span":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"datalist",
                                        "options": dict({
                                                         "tag-open":"datalist",
                                                         "tag-close":"datalist",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"Description (dd)",
                                        "options": dict({
                                                         "tag-open":"dd",
                                                         "tag-close":"dd",
                                                         "content":ui.TextView(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"delete (del)",
                                        "options": dict({
                                                         "tag-open":"del",
                                                         "tag-close":"del",
                                                         "content":ui.TextView(),
                                                         "cite":ui.TextField(),
                                                         "datetime":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"details",
                                        "options": dict({
                                                         "tag-open":"details",
                                                         "tag-close":"details",
                                                         "content":ui.TextView(),
                                                         "open":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"definition (dfn)",
                                        "options": dict({
                                                         "tag-open":"dfn",
                                                         "tag-close":"dfn",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"dialog",
                                        "options": dict({
                                                         "tag-open":"dialog",
                                                         "tag-close":"dialog",
                                                         "content":ui.TextView(),
                                                         "open":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"dir - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"dir",
                                                         "tag-close":"dir",
                                                         "content":ui.TextField(),
                                                         "compact":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"div",
                                        "options": dict({
                                                         "tag-open":"div",
                                                         "tag-close":"div",
                                                         "content":ui.TextView(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"description list (dl)",
                                        "options": dict({
                                                         "tag-open":"dl",
                                                         "tag-close":"dl",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"description term (dt)",
                                        "options": dict({
                                                         "tag-open":"dt",
                                                         "tag-close":"dt",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"emphasis - em (Richer effects attained with CSS)",
                                        "options": dict({
                                                         "tag-open":"em",
                                                         "tag-close":"em",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"embed",
                                        "options": dict({
                                                         "tag-open":"embed",
                                                         "tag-close":"embed",
                                                         "content":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"fieldset",
                                        "options": dict({
                                                         "tag-open":"fieldset",
                                                         "tag-close":"fieldset",
                                                         "content":ui.TextView(),
                                                         "disabled":ui.TextField(),
                                                         "form_id":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"figcaption",
                                        "options": dict({
                                                         "tag-open":"figcaption",
                                                         "tag-close":"figcaption",
                                                         "content":ui.TextField(),
                                                         
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"figure",
                                        "options": dict({
                                                         "tag-open":"figure",
                                                         "tag-close":"figure",
                                                         "content":ui.TextField(),
                                                         
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"font - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"font",
                                                         "tag-close":"font",
                                                         "content":ui.TextField(),
                                                         "color":ui.TextField(),
                                                         "face":ui.TextField(),
                                                         "size":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"footer",
                                        "options": dict({
                                                         "tag-open":"footer",
                                                         "tag-close":"footer",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"form",
                                        "options": dict({
                                                         "tag-open":"form",
                                                         "tag-close":"form",
                                                         "content":ui.TextView(),
                                                         "accept":ui.TextField(),
                                                         "accept-charset":ui.TextField(),
                                                         "action":ui.TextField(),
                                                         "autocomplete":ui.TextField(),
                                                         "enctype":ui.TextField(),
                                                         "method":ui.TextField(),
                                                         "novalidate":ui.TextField(),
                                                         "target":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"frame - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"frame",
                                                         "tag-close":"frame",
                                                         "content":ui.TextField(),
                                                         "frameborder":ui.TextField(),
                                                         "longdesc":ui.TextField(),
                                                         "marginheight":ui.TextField(),
                                                         "marginwidth":ui.TextField(),
                                                         "noresize":ui.TextField(),
                                                         "scrolling":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"frameset - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"frameset",
                                                         "tag-close":"frameset",
                                                         "content":ui.TextField(),
                                                         "cols":ui.TextField(),
                                                         "rows":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"heading 1",
                                        "options": dict({
                                                         "tag-open":"h1",
                                                         "tag-close":"h1",
                                                         "conent":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"heading 2",
                                        "options": dict({
                                                         "tag-open":"h2",
                                                         "tag-close":"h2",
                                                         "conent":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"heading 3",
                                        "options": dict({
                                                         "tag-open":"h3",
                                                         "tag-close":"h3",
                                                         "conent":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"heading 4",
                                        "options": dict({
                                                         "tag-open":"h4",
                                                         "tag-close":"h4",
                                                         "conent":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"heading 5",
                                        "options": dict({
                                                         "tag-open":"h5",
                                                         "tag-close":"h5",
                                                         "conent":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"heading 6",
                                        "options": dict({
                                                         "tag-open":"h6",
                                                         "tag-close":"h6",
                                                         "conent":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"head",
                                        "options": dict({
                                                         "tag-open":"head",
                                                         "tag-close":"head",
                                                         "content":ui.TextField(),
                                                         "profile":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"header",
                                        "options": dict({
                                                         "tag-open":"header",
                                                         "tag-close":"header",
                                                         "content":ui.TextView(),
                                                         
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"hr",
                                        "options": dict({
                                                         "tag-open":"hr",
                                                         "align":ui.TextField(),
                                                         "noshade":ui.TextField(),
                                                         "size":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"html",
                                        "options": dict({
                                                         "tag-open":"html",
                                                         "tag-close":"html",
                                                         "content":ui.TextField(),
                                                         "manifest":ui.TextField(),
                                                         "xmlns":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"i",
                                        "options": dict({
                                                         "tag-open":"i",
                                                         "tag-close":"i",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"iframe",
                                        "options": dict({
                                                         "tag-open":"iframe",
                                                         "tag-close":"iframe",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "frameborder":ui.TextView(),
                                                         "height":ui.TextField(),
                                                         "longdesc":ui.TextField(),
                                                         "marginheight":ui.TextField(),
                                                         "marginwidth":ui.TextField(),
                                                         "sandbox":ui.TextField(),
                                                         "scrolling":ui.TextField(),
                                                         "seamless":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         "srcdoc":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"image",
                                        "options": dict({
                                                         "tag-open":"img",
                                                         "tag-close":"img",
                                                         "content":"",
                                                         "align":ui.TextField(),
                                                         "alt":ui.TextField(),
                                                         "border":ui.TextField(),
                                                         "crossorigin":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "hspace":ui.TextField(),
                                                         "ismap":ui.TextField(),
                                                         "longdesc":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         "usemap":ui.TextField(),
                                                         "vspace":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"input",
                                        "options": dict({
                                                         "tag-open":"input",
                                                         "accept":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "alt":ui.TextField(),
                                                         "autocomplete":ui.TextField(),
                                                         "autofocus":ui.TextField(),
                                                         "checked":ui.TextField(),
                                                         "disabled":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "formaction":ui.TextField(),
                                                         "formmethod":ui.TextField(),
                                                         "formnovalidate":ui.TextField(),
                                                         "formtarget":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "list":ui.TextField(),
                                                         "max":ui.TextField(),
                                                         "maxlength":ui.TextField(),
                                                         "min":ui.TextField(),
                                                         "multiple":ui.TextField(),
                                                         "pattern":ui.TextField(),
                                                         "placeholder":ui.TextField(),
                                                         "readonly":ui.TextField(),
                                                         "required":ui.TextField(),
                                                         "size":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         "step":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"insert - (ins)",
                                        "options": dict({
                                                         "tag-open":"ins",
                                                         "tag-close":"ins",
                                                         "content":ui.TextField(),
                                                         "cite":ui.TextField(),
                                                         "datetime":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"keyboard (kbd)",
                                        "options": dict({
                                                         "tag-open":"kbd",
                                                         "tag-close":"kbd",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"keygen",
                                        "options": dict({
                                                         "tag-open":"keygen",
                                                         "autofocus":ui.TextField(),
                                                         "challenge":ui.TextField(),
                                                         "disabled":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "keytype":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"label",
                                        "options": dict({
                                                         "tag-open":"label",
                                                         "tag-close":"label",
                                                         "content":ui.TextField(),
                                                         "for":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"legend",
                                        "options": dict({
                                                         "tag-open":"legend",
                                                         "tag-close":"legend",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"list item (li)",
                                        "options": dict({
                                                         "tag-open":"li",
                                                         "tag-close":"li",
                                                         "content":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"link",
                                        "options": dict({
                                                    "tag-open":"link",
                                                    "charset":ui.TextField(),
                                                    "crossorigin":ui.TextField(),
                                                    "href":ui.TextField(),
                                                    "hreflang":ui.TextField(),
                                                    "media":ui.TextField(),
                                                    "rel":ui.TextField(),
                                                    "rev":ui.TextField(),
                                                    "sizes":ui.TextField(),
                                                    "target":ui.TextField(),
                                                    "type":ui.TextField(),
                                                    }, **GLOBAL_HTML_ATTR)},
                                       {"title":"main",
                                        "options": dict({
                                                         "tag-open":"main",
                                                         "tag-close":"main",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"map",
                                        "options": dict({
                                                         "tag-open":"map",
                                                         "tag-close":"map",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"mark",
                                        "options": dict({
                                                         "tag-open":"mark",
                                                         "tag-close":"mark",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"menu",
                                        "options": dict({
                                                         "tag-open":"menu",
                                                         "tag-close":"menu",
                                                         "content":ui.TextField(),
                                                         "label":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"menuitem",
                                        "options": dict({
                                                         "tag-open":"menuitem",
                                                         "tag-close":"menuitem",
                                                         "content":ui.TextField(),
                                                         "checked":ui.TextField(),
                                                         "command":ui.TextField(),
                                                         "default":ui.TextField(),
                                                         "disable":ui.TextField(),
                                                         "icon":ui.TextField(),
                                                         "label":ui.TextField(),
                                                         "radiogroup":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"metadata",
                                        "options": dict({
                                                         "tag-open":"meta",
                                                         "tag-close":"meta",
                                                         "content":ui.TextField(),
                                                         "charset":ui.TextField(),
                                                         "http-equiv":ui.TextField(),
                                                         "scheme":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"meter",
                                        "options": dict({
                                                         "tag-open":"meter",
                                                         "tag-close":"meter",
                                                         "content":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "high":ui.TextField(),
                                                         "low":ui.TextField(),
                                                         "max":ui.TextField(),
                                                         "min":ui.TextField(),
                                                         "optimum":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"navigation block - (nav)",
                                        "options": dict({
                                                         "tag-open":"nav",
                                                         "tag-close":"nav",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"noframes - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"noframes",
                                                         "tag-close":"noframes",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"noscript",
                                        "options": dict({
                                                         "tag-open":"noscript",
                                                         "tag-close":"noscript",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"object",
                                        "options": dict({
                                                         "tag-open":"object",
                                                         "tag-close":"object",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "archive":ui.TextField(),
                                                         "border":ui.TextField(),
                                                         "classid":ui.TextField(),
                                                         "codebase":ui.TextField(),
                                                         "codetype":ui.TextField(),
                                                         "data":ui.TextField(),
                                                         "declare":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "hspace":ui.TextField(),
                                                         "standby":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         "usemap":ui.TextField(),
                                                         "vspace":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"ordered list (ol)",
                                        "options": dict({
                                                         "tag-open":"ol",
                                                         "tag-close":"ol",
                                                         "content":ui.TextField(),
                                                         "compact":ui.TextField(),
                                                         "reversed":ui.TextField(),
                                                         "start":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"option group (optgroup)",
                                        "options": dict({
                                                         "tag-open":"optgroup",
                                                         "tag-close":"optgroup",
                                                         "content":ui.TextView(),
                                                         "disabled":ui.TextField(),
                                                         "label":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"option",
                                        "options": dict({
                                                         "tag-open":"option",
                                                         "tag-close":"option",
                                                         "content":ui.TextField(),
                                                         "disabled":ui.TextField(),
                                                         "label":ui.TextField(),
                                                         "selected":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"output",
                                        "options": dict({
                                                         "tag-open":"output",
                                                         "tag-close":"output",
                                                         "content":ui.TextField(),
                                                         "for":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"paragraph",
                                        "options": dict({
                                                    "tag-open":"p",
                                                    "tag-close":"p",
                                                    "content":ui.TextView(),
                                                    "align":ui.TextField(),
                                                    }, **GLOBAL_HTML_ATTR)},
                                       {"title":"parameter (param)",
                                        "options": dict({
                                                         "tag-open":"param",
                                                         "type":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         "valuetype":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"preformatted text",
                                        "options": dict({
                                                         "tag-open":"pre",
                                                         "tag-close":"pre",
                                                         "content":ui.TextView(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"progress",
                                        "options": dict({
                                                         "tag-open":"progress",
                                                         "tag-close":"progress",
                                                         "content":ui.TextField(),
                                                         "max":ui.TextField(),
                                                         "value":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"quotation (q)",
                                        "options": dict({
                                                         "tag-open":"q",
                                                         "tag-close":"q",
                                                         "content":ui.TextField(),
                                                         "cite":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"rp",
                                        "options": dict({
                                                         "tag-open":"rp",
                                                         "tag-close":"rp",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"rt",
                                        "options": dict({
                                                         "tag-open":"rt",
                                                         "tag-close":"rt",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"ruby",
                                        "options": dict({
                                                         "tag-open":"ruby",
                                                         "tag-close":"ruby",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"s",
                                        "options": dict({
                                                         "tag-open":"s",
                                                         "tag-close":"s",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"samp",
                                        "options": dict({
                                                         "tag-open":"samp",
                                                         "tag-close":"samp",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title": "script",
                                        "options": dict({
                                                    "tag-open":"script",
                                                    "tag-close":"script",
                                                    "content":ui.TextView(),
                                                    "async":ui.TextField(),
                                                    "charset":ui.TextField(),
                                                    "defer":ui.TextField(),
                                                    "src": ui.TextField(),
                                                    "type": ui.TextField(),
                                                    "xml:space":ui.TextField(),
                                                    }, **GLOBAL_HTML_ATTR)},
                                       {"title":"section",
                                        "options": dict({
                                                         "tag-open":"section",
                                                         "tag-close":"section",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"select",
                                        "options": dict({
                                                         "tag-open":"select",
                                                         "tag-close":"select",
                                                         "content":ui.TextField(),
                                                         "autofocus":ui.TextField(),
                                                         "disabled":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "multiple":ui.TextField(),
                                                         "required":ui.TextField(),
                                                         "size":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"small",
                                        "options": dict({
                                                         "tag-open":"small",
                                                         "tag-close":"small",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"source",
                                        "options": dict({
                                                         "tag-open":"source",
                                                         "tag-close":"source",
                                                         "content":ui.TextField(),
                                                         "media":ui.TextField(),
                                                         "src":ui.TextField(),
                                                         "type":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"span",
                                        "options": dict({
                                                         "tag-open":"span",
                                                         "tag-close":"span",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"strike - (Not Avaliable in HTML5)",
                                        "options": dict({
                                                         "tag-open":"strike",
                                                         "tag-close":"strike",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"strong",
                                        "options": dict({
                                                         "tag-open":"strong",
                                                         "tag-close":"strong",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title": "style",
                                        "options": dict({
                                                    "tag-open":"style",
                                                    "tag-close":"style",
                                                    "content":ui.TextView(),
                                                    "media":ui.TextField(),
                                                    "scoped":ui.TextField(),
                                                    "type":ui.TextField(),
                                                    }, **GLOBAL_HTML_ATTR)},
                                       {"title":"subscript - (sub)",
                                        "options": dict({
                                                         "tag-open":"sub",
                                                         "tag-close":"sub",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"summary",
                                        "options": dict({
                                                         "tag-open":"summary",
                                                         "tag-close":"summary",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"superscript - (sup)",
                                        "options": dict({
                                                         "tag-open":"sup",
                                                         "tag-close":"sup",
                                                         "content":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"table",
                                        "options": dict({
                                                         "tag-open":"table",
                                                         "tag-close":"table",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "bgcolor":ui.TextField(),
                                                         "border":ui.TextField(),
                                                         "cellpadding":ui.TextField(),
                                                         "cellspacing":ui.TextField(),
                                                         "frame":ui.TextField(),
                                                         "sortable":ui.TextField(),
                                                         "summary":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"table body (tbody)",
                                        "options": dict({
                                                         "tag-open":"tbody",
                                                         "tag-close":"tbody",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"tablecell (td)",
                                        "options": dict({
                                                         "tag-open":"td",
                                                         "tag-close":"td",
                                                         "content":ui.TextField(),
                                                         "abbr":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "axis":ui.TextField(),
                                                         "bgcolor":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "colspan":ui.TextField(),
                                                         "headers":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "nowrap":ui.TextField(),
                                                         "rowspan":ui.TextField(),
                                                         "scope":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"textarea",
                                        "options": dict({
                                                         "tag-open":"textarea",
                                                         "tag-close":"textarea",
                                                         "content":ui.TextField(),
                                                         "autofocus":ui.TextField(),
                                                         "cols":ui.TextField(),
                                                         "disabled":ui.TextField(),
                                                         "form":ui.TextField(),
                                                         "maxlength":ui.TextField(),
                                                         "placeholder":ui.TextField(),
                                                         "readonly":ui.TextField(),
                                                         "required":ui.TextField(),
                                                         "rows":ui.TextField(),
                                                         "wrap":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"table footer (tfoot)",
                                        "options": dict({
                                                         "tag-open":"tfoot",
                                                         "tag-close":"tfoot",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"table header cell (th)",
                                        "options": dict({
                                                         "tag-open":"th",
                                                         "tag-close":"th",
                                                         "content":ui.TextField(),
                                                         "abbr":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "axis":ui.TextField(),
                                                         "bgcolor":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "colspan":ui.TextField(),
                                                         "headers":ui.TextField(),
                                                         "height":ui.TextField(),
                                                         "nowrap":ui.TextField(),
                                                         "rowspan":ui.TextField(),
                                                         "scope":ui.TextField(),
                                                         "sorted":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         "width":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"table header (thead)",
                                        "options": dict({
                                                         "tag-open":"thead",
                                                         "tag-close":"thead",
                                                         "content":ui.TextField(),
                                                         "align":ui.TextField(),
                                                         "char":ui.TextField(),
                                                         "charoff":ui.TextField(),
                                                         "valign":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                       {"title":"time",
                                        "options": dict({
                                                         "tag-open":"time",
                                                         "tag-close":"time",
                                                         "content":ui.TextField(),
                                                         "datetime":ui.TextField(),
                                                         }, **GLOBAL_HTML_ATTR)},
                                        {"title":"title",
                                         "options": dict({
                                                          "tag-open":"title",
                                                          "tag-close":"title",
                                                          "content":ui.TextField(),
                                                          }, **GLOBAL_HTML_ATTR)},
                                        {"title":"table row (tr)",
                                         "options": dict({
                                                          "tag-open":"tr",
                                                          "tag-close":"tr",
                                                          "content":ui.TextField(),
                                                          "align":ui.TextField(),
                                                          "bgcolor":ui.TextField(),
                                                          "char":ui.TextField(),
                                                          "charoff":ui.TextField(),
                                                          "valign":ui.TextField(),
                                                          }, **GLOBAL_HTML_ATTR)},
                                        {"title": "comment",
                                         "options": {
                                                     "tag-open":"<!--",
                                                     "tag-close":"-->",
                                                     "content":ui.TextView(),
                                                     }},
                                       ])
    try:
        we = sender.superview.superview["contentContainer"].subviews[2].subviews[0].subviews[1]
    except IndexError as e:
        print exception_str(e)
        we = ui.WebView()
    v.delegate = TagDelegate(we.eval_js)
    v.name = "Add Tag"
    v.width = 350
    v.height = 500
    v.present("popover", popover_location=(sender.superview.x, sender.superview.y))
    v.wait_modal()
    

class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.fileManager = None
        self.fileViewer = None

    def did_load(self):
        print "%r loaded" % self

    def set_fv_fm(self, file_manager, file_viewer):
        self.fileManager = file_manager
        self.fileViewer = file_viewer
        self.fileViewer.flex = "WH"
        _, _, w, h = self["fileViewContainer"].frame
        self.fileViewer.frame =(0, 0, 188, h)
        self.fileViewer.bring_to_front()
        self.fileViewer.size_to_fit()

        self.set_needs_display()

    def update_config(self, config_view):
        self["contentContainer"].update_from_config(config_view)

    def apply_fileview(self):
        self["fileViewContainer"].add_subview(self.fileViewer)
        show_hide_file_viewer(self["contentContainer"].subviews[0])
        show_hide_file_viewer(self["contentContainer"].subviews[0])

    def load_file(self, *args):
        self["contentContainer"].add_file(*args)

    def on_close_file(self):
        try:
            self["contentContainer"].on_close_file()
        except Exception as e:  # todo: this should be a qualified exception
            print "Error Closing File. " + exception_str(e)

HTMLEdit = Editor

class Parser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.open_tags = []
        self.files_list = []

    def handle_starttag(self, tag, attr):
        if tag == "script":
            for x in attr:
                if "src" in x:
                    self.files_list.append(x[1])
        self.open_tags.append(tag)

    def handle_endtag(self, tag):
        try:
            self.open_tags.remove(tag)
        except ValueError as e:
            print exception_str(e)

    def handle_startendtag(self, tag, attr):
        if tag == "link":
            for x in attr:
                if "href" in x:
                    self.files_list.append(x[1])

    def feed(self, *args, **kwargs):
        self.open_tags = []
        self.files_list = []
        HTMLParser.HTMLParser.feed(self, *args, **kwargs)
        if not self.open_tags == []:
            print "Not all tag/s have been closed.\nOpen tag/s %r" % self.open_tags


def save(page_contents, tev):
    try:
        sindex = tev.pagecontrol.selected_index
        page = tev.pagecontrol.segments[sindex]
        tev.superview.fileManager.add_file(page, page_contents)
        if page.endswith(".html"):
            tev.parse_page(None, page, page_contents)

        print "File saved"
        print "%s saved with contents\n%s" % (page, page_contents)
    except Exception as e:
        print "Failed to save. " + exception_str(e)

class TextEditorView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.html_parser = Parser()

    def did_load(self):
        print "DID LOAD %r" % self
        self.textview = self["editor_view"]
        print "self.textview = %r" % self.textview
        print self.textview.subviews
        self.filecontrol = self["file_control"]
        self.filecontrol.action = self.select_file
        self.pagecontrol = self["page_control"]
        self.pagecontrol.action = self.select_page

        self.filecontrol.segments = ()
        self.pagecontrol.segments = ()

    def update_from_config(self, config_view):
        tv = self.textview["web_view"]
        config = config_view.config

        font_size = config.get_value("editor.font.size")
        gutter = config.get_value("editor.show.gutter")
        style = config.get_value("editor.style")
        margin = config.get_value("editor.print.margin")
        wrap = config.get_value("editor.line.wrap")
        soft_tab = config.get_value("editor.soft.tabs")
        tab_size = config.get_value("editor.tab.size")

        tv.evaluate_javascript("document.getElementById('editor').style.fontSize='%ipx'" % font_size)
        tv.evaluate_javascript("get_editor().getSession().setTabSize(%s);" % tab_size)
        tv.evaluate_javascript("get_editor().getSession().setUseSoftTabs(%s);" % soft_tab)
        tv.evaluate_javascript("get_editor().getSession().setUseWrapMode(%s);" % wrap)
        tv.evaluate_javascript("get_editor().getSession().setShowPrintMargin(%s);" % margin)
        tv.evaluate_javascript("get_editor().getSession().setShowInvisibles(%s);" % gutter)
        tv.evaluate_javascript("get_editor().getSession().setTheme(%s);" % style)

    def add_file(self, file_path, file_contents):
        if file_path not in self.filecontrol.segments:
            i = list(self.filecontrol.segments)
            i.append(file_path)
            self.filecontrol.segments = i
            self.add_page(file_path)
        self.filecontrol.selected_index = self.filecontrol.segments.index(file_path)
        self.select_file(None)

    def add_page(self, file_path):
        if file_path not in self.pagecontrol.segments:
            i = list(self.pagecontrol.segments)
            i.append(file_path)
            self.pagecontrol.segments = i

    def on_close_file(self):
        segment = self.filecontrol.segments[self.filecontrol.selected_index]
        print segment
        i = list(self.filecontrol.segments)
        i.remove(segment)
        self.filecontrol.segments = i
        self.filecontrol.selected_index = 0
        self.select_file(None)

    def close_file(self, file):
        print "Closing file: %s" % (file)
        for page in self.pagecontrol.segments:
            self.pagecontrol.selected_index = self.pagecontrol.segments.indexof(page)
            self.select_page(None)
        self.pagecontrol.segments = tuple("NO OPEN FILE/s")


    def select_file(self, sender):
        try:
            name = self.filecontrol.segments[self.filecontrol.selected_index]
            if self.superview.fileManager:
                self.pagecontrol.segments = ()
                self.add_page(name)
                self.pagecontrol.selected_index = 0
                self.select_page(None)
            else:
                print "Error opening file"
        except Exception as e:
            print "Error loading file " + exception_str(e)


    def select_page(self, sender):
        if self.superview.fileManager:
            name = self.pagecontrol.segments[self.pagecontrol.selected_index]
            file_data = self.superview.fileManager.get_file(name)[1]
            if name.endswith(".html"):
                self.parse_page(sender, name, file_data)

            self.set_editor_value(file_data)
        else:
            self.set_editor_value("Error loading file.\nFileManager not found")

    @ui.in_background
    def parse_page(self, sender, page, file_data):
        self.html_parser.feed(file_data)
        print self.html_parser.files_list
        print list(self.pagecontrol.segments[1:])
        if self.html_parser.files_list != list(self.pagecontrol.segments[1:]):
            self.pagecontrol.segments = ()
            self.add_page(page)
            for file in self.html_parser.files_list:
                if file:
                    self.add_page(file)
            self.pagecontrol.selected_index = 0

    @ui.in_background
    def set_editor_value(self, text):
        we = self.subviews[2].subviews[0].subviews[1]
        print self.subviews[2].subviews[0].subviews[1]
        name = self.pagecontrol.segments[self.pagecontrol.selected_index]
        we.delegate.open(name, text)



class PropertiesView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)


def load_editor(file_manager=None, file_viewer=ui.View(), frame=(0, 0, 540, 600), webdelegate=None):
    try:
        view = ui.load_view("HTMLEditor/__init__")
    except ValueError as e:
        print "Attempt 1 'HTMLEditor/__init__' failed " + exception_str(e)
        try:
            view = ui.load_view("__init__")
        except ValueError as e:
            print "Attempt 2 '__init__' failed " + exception_str(e)
            view = ui.Editor()
    view.frame = frame
    view.set_fv_fm(file_manager, file_viewer)
    view.size_to_fit()
    view.set_needs_display()

    vx,vy,vw,vh = view["contentContainer"]["editor_view"].frame
    width = vw-vx
    height = vh-vy

    if webdelegate:
        def save_func(contents):
            save(contents, view["contentContainer"])
        edit_view = webdelegate.load_console()
        edit_view.name = "WebEditor"
        edit_view["console_input"].delegate = webdelegate.WebViewInputDelegate(edit_view["web_view"])
        edit_view["web_view"].delegate = webdelegate.WebViewDelegate(save_func, edit_view)
        edit_view["web_view"].load_url(webdelegate.load_html_editor_view())

        edit_view["web_view"].delegate.open
    else:
        edit_view = ui.WebView()
        edit_view.name = "web_view"
        edit_view.flex = "WH"
        edit_view.load_url("file://%s"%os.path.abspath("../EditView/index.html"))

    edit_view.size_to_fit()
    edit_view.frame = (0, 0, width, height)
    edit_view.set_needs_display()

    view["contentContainer"]["editor_view"].add_subview(edit_view)
    view["contentContainer"]["editor_view"].size_to_fit()
    view["contentContainer"]["editor_view"].set_needs_display()

    return view


__all__ = ["load_editor", "Editor", "HTMLEdit", "TextEditorView", "PropertiesView"]

if __name__ == "__main__":
    DEBUG = False
    view = load_editor()
    view.present("sheet" if DEBUG else "fullscreen", hide_title_bar=not DEBUG)
