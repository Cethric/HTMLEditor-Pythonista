try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui


class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.fileManager = None
        self.fileViewer = None
        
    def did_load(self):
        print "%r loaded" % self
        #x,y,w,h = self.frame
        #self.fileViewer.frame = (x,y,w*0.25,h)
        #print self.fileViewer.frame
        
    def set_fv_fm(self, file_manager, file_viewer):
        self.fileManager = file_manager
        self.fileViewer = file_viewer
        self["fileViewContainer"].add_subview(self.fileViewer)
        self.fileViewer.flex = "WH"
        print self["fileViewContainer"].frame
        self.fileViewer.frame =(0, 0, self["fileViewContainer"].frame[2], self["fileViewContainer"].frame[3])
        self.fileViewer.bring_to_front()
        self.fileViewer.size_to_fit()
        self.set_needs_display()
        
        
HTMLEdit = Editor
        
def load_editor(file_manager = None, file_viewer = ui.View(), frame=(0, 0, 540, 575)):
    try:
        view = ui.load_view("HTMLEditor/__init__")
        #view.fileManager = file_manager
        #view.fileViewer = file_viewer
    except ValueError as e:
        print "Attempt 1 'HTMLEditor/__init__' failed"
        print e
        try:
            view = ui.load_view("__init__")
            #view.fileManager = file_manager
            #view.fileViewer = file_viewer
        except ValueError as e:
            print "Attempt 2 '__init__' failed"
            print e
            view = ui.Editor()
            #view.fileManager = file_manager
            #view.fileViewer = file_viewer
    view.frame = frame
    view.set_fv_fm(file_manager, file_viewer)
    return view


__all__ = ["load_editor", "Editor", "HTMLEdit"]

if __name__ == "__main__":
    view = load_editor()
    view.present("fullscreen")
