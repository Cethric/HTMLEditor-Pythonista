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

class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.htmlEditorView = HTMLEditor.load_editor(fm)
        self.serverEditorView = ui.load_view("ServerEditor/__init__")
        
        self.add_subview(self.htmlEditorView)
        self.add_subview(self.serverEditorView)
        
        self.htmlEditorView.bring_to_front()
        self.serverEditorView.send_to_back()


if __name__ == "__main__":
    print dir(HTMLEditor)
    view = MainView()
    view.present("sheet", hide_title_bar=DEBUG)
