#!/usr/bin/env python
# coding: utf-8

# the following line is recommended to ease porting to Python 3
#  from __future__ import (absolute_import, division, print_function, unicode_literals)
# todo: uncomment the line above and then fix up all the print commands
import os

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
        tv = sender.superview.superview["contentContainer"].textview
        config = sss_view.config_view.config
        
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
    else:
        console.alert("Configuration is only available through the Main View")
        

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
        ss_view = self
        old_width = ss_view["fileViewContainer"].width
        show = True
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
        self.pagecontrol.segments = ()
        self.add_page(page)
        for file in self.html_parser.files_list:
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
