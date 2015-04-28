#coding: utf-8
import sys
import random
import socket
import HTMLParser
import SimpleWebSocketServer
try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
import console

print dir(SimpleWebSocketServer)

@ui.in_background    
def show_hide_file_viewer(sender):
    #console.hud_alert("show_hide_file_viewer")
    view = sender.superview.superview
    old_width = view["fileViewContainer"].width
    show = old_width == 0
    width = 150 if show else 0
    x_mod = 8 if show else 0
    view["fileViewContainer"].width = width
    view["fileViewContainer"].set_needs_display()
    view.set_needs_display()
    
    for subview in ("contentContainer", "toolsContainer"):
        view[subview].x = width + x_mod
        view[subview].width = view.width - width - x_mod
    
@ui.in_background
def server_editor(sender):
    if sender.superview.superview.superview == None:
        console.hud_alert("server_editor")
    else:
        sender.superview.superview.superview.set_server_editor()
    
class WebViewDelegate(object):
    def __init__(self):
        pass
        
    def webview_should_start_load(self, webview, url, nav_type):
        print "Loading %r of type %r" % (url, nav_type)
        return True
        
    def webview_did_finish_load(self, webview):
        name = webview.evaluate_javascript("document.title")
        webview.name = name
        
    def webview_did_fail_load(self, webview, error_code, error_msg):
        print "%r Failed to load. %r %r" % (webview, error_code, error_msg)
    
@ui.in_background
def preview(sender):
    #console.hud_alert("preview")
    text = sender.superview.superview["contentContainer"].textview.evaluate_javascript("get_editor().getValue()")
    wv = ui.WebView()
    wv.delegate = WebViewDelegate()
    wv.load_html(text)
    wv.present("sheet")

@ui.in_background
def quitter(sender):
    try:
        result = console.alert("Close", "", "Close File", "Quit")
        if result == 1:
            if sender.superview.superview == None:
                console.hud_alert("Close File")
            else:
                sender.superview.superview.on_close_file()
        elif result == 2:
            sender.superview.superview["contentContainer"].active = False
            if sender.superview.superview.superview == None:
                sender.superview.superview.close()
            else:
                sender.superview.superview.superview.close()
    except KeyboardInterrupt as e:
        print "User cancled the input."

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
        #self["fileViewContainer"].add_subview(self.fileViewer)
        self.fileViewer.flex = "WH"
        self.fileViewer.frame =(0, 0, self["fileViewContainer"].frame[2], self["fileViewContainer"].frame[3])
        self.fileViewer.bring_to_front()
        self.fileViewer.size_to_fit()
        self.set_needs_display()
    
    def apply_fileview(self):
        self["fileViewContainer"].add_subview(self.fileViewer)
        
    def load_file(self, *args):
        self["contentContainer"].add_file(*args)
        
    def on_close_file(self):
        self["contentContainer"].on_close_file()
        
HTMLEdit = Editor

class HTMLParserd(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.open_tags = []
        self.files_list = []
        
    def handle_starttag(self, tag, attr):
        #print tag, attr
        if tag == "script":
            for x in attr:
                if "src" in x:
                    self.files_list.append(x[1])
        self.open_tags.append(tag)
    
    def handle_endtag(self, tag):
        #print tag
        try:
            self.open_tags.remove(tag)
        except:
            pass
        
    def handle_startendtag(self, tag, attr):
        #print tag, attr
        if tag == "link":
            for x in attr:
                if "href" in x:
                    self.files_list.append(x[1])
        
    def feed(self, *args, **kwargs):
        import console
        #print "Start"
        self.open_tags = []
        self.files_list = []
        HTMLParser.HTMLParser.feed(self, *args, **kwargs)
        #print "Done"
        #print "files_list = %r" % self.files_list
        if not self.open_tags == []:
            try:
                console.alert("Parse Error", "Not all tag/s have been closed.\nOpen tag/s %r" % self.open_tags)
            except:
                print "Not all tag/s have been closed.\nOpen tag/s %r" % self.open_tags
        #console.alert("parse done")


class TextEditorView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.html_parser = HTMLParserd()
        import threading
        self.threader = threading.Thread(target=self.threaded_saver)
        self.active = True
        
    def did_load(self):
        self.textview = self["text_control"]
        self.filecontrol = self["file_control"]
        self.filecontrol.action = self.select_file
        self.pagecontrol = self["page_control"]
        self.pagecontrol.action = self.select_page
        
        self.filecontrol.segments = ()
        self.pagecontrol.segments = ()
        
        print self.textview
        self.textview.delegate = self
        
        self.set_browser = False
        
        self.textview.load_html('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <title>Editor</title>
  <style type="text/css" media="screen">
    body {
        overflow: scroll;
        //height:1200px;
        -webkit-overflow-scrolling: touch;
        overflow-y:auto;
    }

    #editor {
        margin: 0;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        height:4096px;
        overflow: scroll;
    }
  </style>
</head>
<body <!--ontouchmove="event.preventDefault()-->">

<pre id="editor">
NO OPEN FILE
</pre>

<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.1.9/ace.js" type="text/javascript" charset="utf-8"></script>
<script>
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/kuroir");
    //editor.getSession().setMode("ace/mode/python");
    
    editor.setAutoScrollEditorIntoView(true);
    editor.setOption("maxLines", 4096);
    editor.setOption("minLines", 29);
    
    editor.setCursor(0, 0);
    
    function get_editor() {
        return editor;
    }
    document.getElementById('editor').style.fontSize='13px';
</script>

</body>
</html>''')
        self.can_update = False

    @ui.in_background
    def webview_did_finish_load(self, textview):
        self.can_update = True
        #console.hud_alert("Editor: " + textview.evaluate_javascript("get_editor().getValue()"))
        #import threading
        #threading.Thread(target=self.threaded_saver).start()
        self.auto_save_wait = 0.001 # Seconds to wait before saving
        self.force_save = False
        self.threader.daemon = True
        self.threader.start()
    
    def threaded_saver(self):
        import time
        pages = self.pagecontrol
        while self.active:
            try:
                time.sleep(self.auto_save_wait)
                    
                sindex = pages.selected_index
                page = pages.segments[sindex]
                contents = self.textview.evaluate_javascript("get_editor().getValue();")
                if self.superview.fileManager:
                    self.superview.fileManager.add_file(page, contents)
                #print "Hanging function"
                #print page
                #print contents
            except IndexError as e:
                print "IndexError"
                print e
        print "Saver Thread Stoped"
            
    def textview_should_change(self, textview, range, replacement):
        keys = {u"÷": "insert_comment", u"π": "preview"}
        print replacement
        #print keys[replacement]
        if replacement in keys:
            ui.in_background(console.hud_alert(keys[replacement]))
            if replacement == u"π":
                preview(textview)
            return False
        else:
            return True
        
    def add_file(self, file_path, file_contents):
        #print "Load File", file_path, file_contents
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
            #print i
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
            
        self.pagecontrol.segments = tuple()
        
        
    def select_file(self, sender):
        try:
            name = self.filecontrol.segments[self.filecontrol.selected_index]
            if self.superview.fileManager:
                self.pagecontrol.segments = ()
                self.add_page(name)
                self.pagecontrol.selected_index = 0
                self.select_page(None)
            else:
                #self.textview.text = "Error loading file."
                pass
        except:
            pass
            
    def select_page(self, sender):
        if self.superview.fileManager:
            name = self.pagecontrol.segments[self.pagecontrol.selected_index]
            file_data = self.superview.fileManager.get_file(name)[1]
            print "%r" % file_data
            self.textview.evaluate_javascript("get_editor().setValue(%r)" % file_data)
            self.textview.evaluate_javascript("get_editor().setCursor(0, 0);")
            self.textview.evaluate_javascript("get_editor().setReadOnly(false);")
        
            if name.endswith(".html"):
                self.html_parser.feed(file_data)
                self.pagecontrol.segments = ()
                self.add_page(name)
                for file in self.html_parser.files_list:
                    self.add_page(file)
                self.pagecontrol.selected_index = 0
                self.textview.evaluate_javascript("get_editor().getSession().setMode('ace/mode/html');")
            elif name.endswith(".js"):
                self.textview.evaluate_javascript("get_editor().getSession().setMode('ace/mode/javascript');")
            elif name.endswith(".css"):
                self.textview.evaluate_javascript("get_editor().getSession().setMode('ace/mode/css');")
        else:
            self.textview.text = "Error loading file."
            
class Delegate(object):
    pass
        

class PropertiesView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
    

def load_editor(file_manager = None, file_viewer = ui.View(), frame=(0, 0, 540, 575)):
    try:
        view = ui.load_view("HTMLEditor/__init__")
    except ValueError as e:
        print "Attempt 1 'HTMLEditor/__init__' failed"
        print e
        try:
            view = ui.load_view("__init__")
        except ValueError as e:
            print "Attempt 2 '__init__' failed"
            print e
            view = ui.Editor()
    view.frame = frame
    view.set_fv_fm(file_manager, file_viewer)
    return view


__all__ = ["load_editor", "Editor", "HTMLEdit", "TextEditorView", "PropertiesView"]

if __name__ == "__main__":
    view = load_editor()
    view.present("fullscreen", hide_title_bar=True)
    
    print "CLOSE"
