try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui


class Editor(ui.View):
    pass
