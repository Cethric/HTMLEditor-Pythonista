import ui

import FileManager
import HTMLEditor
import ServerEditor

DEBUG = False

fm = FileManager.Manager()
print HTMLEditor, ServerEditor


class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.htmlEditorView = HTMLEditor.Editor()
        self.serverEditorView = ServerEditor.Editor()
        self.add_subview(self.htmlEditorView)
        self.add_subview(self.serverEditorView)
        
        self.htmlEditorView.bring_to_front()


if __name__ == "__main__":
    view = MainView();
    view.present("fullscreen", hide_title_bar=DEBUG)
