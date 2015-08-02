try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
import os
import logging

import FileManager
import HTMLEditor
import ServerEditor
import ConfigManager
from EditorView import WebDelegate

reload(FileManager)
reload(HTMLEditor)
reload(ServerEditor)
reload(ConfigManager)
reload(WebDelegate)


def get_logger(file_name):
    logger = logging.getLogger(os.path.split(file_name)[-1])
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s --> %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

logger = get_logger(__file__)

DEBUG = True

fm = FileManager.Manager()
fv = FileManager.FileViewer(fm)
c = ConfigManager.Config()
cv = ConfigManager.load_view(c)
cv.set_config(c)
logger.debug(fv.name)


class MainView(ui.View):

    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.htmlEditorView = ui.View()
        self.serverEditorView = ui.View()

        global cv
        self.config_view = cv

    def did_load(self):
        logger.debug("%r did load", self)

    def present(self, *args, **kwargs):
        ui.View.present(self, *args, **kwargs)
        logger.debug(str(WebDelegate))
        self.htmlEditorView = HTMLEditor.load_editor(fm, fv,
                                                     (0, 0, self.frame[
                                                      2], self.frame[3]),
                                                     WebDelegate
                                                     )

        self.add_subview(self.htmlEditorView)

        self.serverEditorView = ServerEditor.load_editor(fm, fv,
                                                         (0, 0, self.frame[
                                                          2], self.frame[3]),
                                                         WebDelegate
                                                         )
        self.add_subview(self.serverEditorView)
        self.set_html_editor()

        try:
            self.htmlEditorView.update_config(self.config_view)
        except Exception as e:
            logger.exception("Error updating config")
            logger.error(e)

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
        logger.debug("Closing File")

    def will_close(self):
        logger.info("Goodbye")


if __name__ == "__main__":
    view = ui.load_view()
    view.present("sheet" if DEBUG else "fullscreen", hide_title_bar=not DEBUG)
