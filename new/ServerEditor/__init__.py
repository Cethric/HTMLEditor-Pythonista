try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
import console
    
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
def html_editor(sender):
    if sender.superview.superview.superview == None:
        console.hud_alert("html_editor")
    else:
        sender.superview.superview.superview.set_html_editor()
    
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
    console.hud_alert("preview")
    #text = sender.superview.superview["contentContainer"].textview.text
    #wv = ui.WebView()
    #wv.delegate = WebViewDelegate()
    #wv.load_html(text)
    #wv.present("sheet")

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
        #self["contentContainer"].on_close_file()
        pass
        
ServerEditor = Editor
        
        
def load_editor(file_manager = None, file_viewer = ui.View(), frame=(0, 0, 540, 575)):
    try:
        view = ui.load_view("ServerEditor/__init__")
    except ValueError as e:
        print "Attempt 1 'ServerEditor/__init__' failed"
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
    
__all__ = ["load_editor", "ServerEditor"]
    
if __name__ == "__main__":
    view = load_editor()
    view.present("fullscreen", hide_title_bar=True)
