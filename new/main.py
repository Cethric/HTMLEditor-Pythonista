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

DEBUG = False

fm = FileManager.Manager()
fv = FileManager.FileViewer(fm)
print fv.name

class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.htmlEditorView = ui.View()
        self.serverEditorView = ui.View()
    
    def did_load(self):
        print "%r did load" % self
        self.serverEditorView = ui.load_view("ServerEditor/__init__")
        
        self.add_subview(self.serverEditorView)
        
        self.serverEditorView.send_to_back()
        
    def present(self, *args, **kwargs):
        ui.View.present(self, *args, **kwargs)
        print "Present"
        print self.frame
        self.htmlEditorView = HTMLEditor.load_editor(fm, fv, (0, 0, self.frame[2], self.frame[3]))
        self.add_subview(self.htmlEditorView)
        fv.file_load_callback = self.htmlEditorView.load_file
        self.htmlEditorView.bring_to_front()
        
    def on_close_file(self):
        print "Closing File"


if __name__ == "__main__":
    view = ui.load_view()
    view.present("fullscreen", hide_title_bar=DEBUG)
