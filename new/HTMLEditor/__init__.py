import sys
import random
import HTMLParser
try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
import console
    

@ui.in_background    
def show_hide_file_viewer(sender):
    console.hud_alert("show_hide_file_viewer")
    
@ui.in_background
def server_editor(sender):
    console.hud_alert("server_editor")
    
@ui.in_background
def preview(sender):
    console.hud_alert("preview")

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
        self["fileViewContainer"].add_subview(self.fileViewer)
        self.fileViewer.flex = "WH"
        self.fileViewer.frame =(0, 0, self["fileViewContainer"].frame[2], self["fileViewContainer"].frame[3])
        self.fileViewer.bring_to_front()
        self.fileViewer.size_to_fit()
        self.set_needs_display()
        
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
        
    def did_load(self):
        self.textview = self["text_control"]
        self.filecontrol = self["file_control"]
        self.filecontrol.action = self.select_file
        self.pagecontrol = self["page_control"]
        
        self.filecontrol.segments = ()
        self.pagecontrol.segments = ()
        
        print self.textview
        self.textview.delegate = self
        
    def textview_should_change(self, textview, range, replacement):
        print replacement
        return True
        
    def textview_did_change(self, textview):
        if self.superview.fileManager:
            name = self.filecontrol.segments[self.filecontrol.selected_index]
            self.superview.fileManager.add_file(name, textview.text)
            self.superview.fileManager.save_data()
        
    def add_file(self, file_path, file_contents):
        #print "Load File", file_path, file_contents
        index = self.filecontrol.selected_index
        if file_path not in self.filecontrol.segments:
            i = list(self.filecontrol.segments)
            i.append(file_path)
            self.filecontrol.segments = i
        self.filecontrol.selected_index = self.filecontrol.segments.index(file_path)
        self.select_file(None)
            
    def on_close_file(self):
        segment = self.filecontrol.segments[self.filecontrol.selected_index]
        i = list(self.filecontrol.segments)
        i.remove(segment)
        self.filecontrol.segments = i
        self.filecontrol.selected_index = -1
        self.select_file(None)
        
        
    def select_file(self, sender):
        name = self.filecontrol.segments[self.filecontrol.selected_index]
        if self.superview.fileManager:
            contents = self.superview.fileManager.get_file(name)[1]
            self.textview.text = contents
            self.html_parser.feed(contents)
            #print self.html_parser.open_tags
            #print self.html_parser.files_list
        else:
            self.textview.text = "Error loading file."
            
    def select_page(self, sender):
        pass
    

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


__all__ = ["load_editor", "Editor", "HTMLEdit", "TextEditorView"]

if __name__ == "__main__":
    view = load_editor()
    view.present("fullscreen", hide_title_bar=True)
