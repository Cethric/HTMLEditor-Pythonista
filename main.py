try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui

import FileManager
reload(FileManager)
import HTMLEditor
reload(HTMLEditor)
import ServerEditor
reload(ServerEditor)
import ConfigManager
reload(ConfigManager)

DEBUG = True

fm = FileManager.Manager()
fv = FileManager.FileViewer(fm)
c = ConfigManager.Config()
cv = ConfigManager.load_view(c)
cv.set_config(c)
print fv.name

class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.htmlEditorView = ui.View()
        self.serverEditorView = ui.View()
        
        global cv
        self.config_view = cv
    
    def did_load(self):
        print "%r did load" % self
        print self.config_view
        
    def present(self, *args, **kwargs):
        ui.View.present(self, *args, **kwargs)
        print "Present"
        print self.frame
        self.htmlEditorView = HTMLEditor.load_editor(fm, fv, (0, 0, self.frame[2], self.frame[3]))
        self.add_subview(self.htmlEditorView)
        #self.htmlEditorView.bring_to_front()
        
        self.serverEditorView = ServerEditor.load_editor(fm, fv, (0, 0, self.frame[2], self.frame[3]))
        self.add_subview(self.serverEditorView)
        #self.serverEditorView.send_to_back()
        
        self.set_html_editor()
        
        self.htmlEditorView.update_config(self.config_view)
        
    def set_html_editor(self):
        self.htmlEditorView.bring_to_front()
        self.htmlEditorView.apply_fileview()
        fv.file_load_callback = self.htmlEditorView.load_file
        self.serverEditorView.send_to_back()
        
    def set_server_editor(self):
        self.serverEditorView.bring_to_front()
        self.serverEditorView.apply_fileview()
        fv.file_load_callback = self.serverEditorView.load_file
        self.htmlEditorView.send_to_back()
        
    def on_close_file(self):
        print "Closing File"


if __name__ == "__main__":
    #cv.present("sheet")
    view = ui.load_view()
    #view.right_button_items = [ui.ButtonItem("TEST")]
    #view.left_button_items = [ui.ButtonItem("HI")]
    view.present("sheet" if DEBUG else "fullscreen", hide_title_bar=not DEBUG)
    view.wait_modal()
    print "Goodbye"
    raise KeyboardInterrupt("TODO Change this to be a safe exit of the save thread")
    print "??"
