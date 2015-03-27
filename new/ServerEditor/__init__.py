try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui


class Editor(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)

    def did_load(self):
        print "%r loaded" % self
