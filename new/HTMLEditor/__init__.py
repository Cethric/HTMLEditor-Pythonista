try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui


class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        print "Called"
        ui.View.__init__(self, *args, **kwargs)
        self.fileManager = None
        self.fileViewer = None
        
    def did_load(self):
        print "%r loaded" % self
        
    def bring_to_front(self):
        ui.View.bring_to_front(self)
        print self.fileManager
        print self.frame
        x,y,w,h = self.frame
        self.fileViewer.frame = (x,y,w*0.25,h)
        print self.fileViewer.frame
        self.fileViewer.bring_to_front()
        
HTMLEdit = Editor
        
def load_editor(file_manager = None, file_viewer = None):
    print "On Load Editor View"
    view = None
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
            view = ui.View()
    print "%r was loaded" % view
    view.fileManager = file_manager
    view.fileViewer = file_viewer
    #view.flex = "WH"
    view.set_needs_display()
    print "flex %r" % view.flex
    return view


__all__ = ["load_editor", "Editor", "HTMLEdit"]

if __name__ == "__main__":
    view = load_editor()
    view.present("sheet")
