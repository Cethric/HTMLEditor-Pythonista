try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui


class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        print "__init__"
        self = ui.load_view("__init__")
        print self
        
    def did_load(self):
        print "%r loaded" % self
