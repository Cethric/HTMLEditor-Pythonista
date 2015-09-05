import os
try:
    import ui
    import console
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
    import dummyConsole as console
import plistlib
import logging

from EditorView import WebDelegate as wd
#reload(wd)


def get_logger(file_name):
    logger = logging.getLogger(os.path.split(file_name)[-1])
    logger.setLevel(logging.DEBUG)
    if len(logger.handlers) == 0:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s --> %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

logger = get_logger(__file__)


class Config(object):

    def __init__(self):
        self.config_dict = {}
        self.load_config()

        self.save_config()

    def load_config(self):
        try:
            self.config_dict = plistlib.readPlist("config.plist")
        except Exception as e:
            logger.exception(e)
            self.config_dict = {
                "editor.font.size": 13,
                "editor.style": "cobolt",
                                "editor.show.gutter": "true",

            }

    def save_config(self):
        plistlib.writePlist(self.config_dict, "config.plist")

    def get_value(self, key, default=""):
        if key in self.config_dict:
            return self.config_dict[key]
        else:
            return default

    def set_value(self, key, value, dontSave=False):
        self.config_dict[key] = value
        if not dontSave:
            self.save_config()


class ConfigView(ui.View):

    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.config = None

    def set_config(self, config):
        self.config = config

        self.editor["Font_Size"].text = "Font Size: %i" % (
            self.config.get_value("editor.font.size"))
        self.editor["editor.font.size"].value = self.config.get_value(
            "editor.font.size") / 25.0
        self.editor["editor.theme.view"].title = self.config.get_value(
            "editor.style")

    def did_load(self):
        self.tabs = self["TabControl"]
        self.editor = self["Editor"]
        logger.debug(self.tabs)
        self.tabs.action = self.change_tab

        self.editor.bounces = True
        self.editor.always_bounce_vertical = True
        self.editor["editor.font.size"].action = self.font_size_change
        self.editor["editor.show.gutter"].action = self.show_gutter
        self.editor["editor.print.margin"].action = self.print_margin
        self.editor["editor.line.wrap"].action = self.line_wrap
        self.editor["editor.soft.tabs"].action = self.soft_tabs
        self.editor["editor.tab.size"].action = self.tab_size

        btn_l = wd.create_mode_btn(self.style_change)
        self.editor["editor.theme.view"].action = btn_l.action

        logger.debug(self.editor["editor.theme.view"].subviews)

    def change_tab(self, sender):
        tab = sender.segments[sender.selected_index]
        logger.debug(self[tab])
        self[tab].bring_to_front()

    def font_size_change(self, sender):
        self.editor["Font_Size"].text = "Font Size: %i" % (sender.value * 25)
        self.config.set_value("editor.font.size", int(sender.value * 25))

    def show_gutter(self, sender):
        self.config.set_value("editor.show.gutter", str(sender.value).lower())

    def style_change(self, i):
        logger.debug("Style Changed to: %s" % i["title"])
        self.config.set_value("editor.style", str(i["title"]).lower())
        self.editor["editor.theme.view"].title = self.config.get_value(
            "editor.style")

    def tab_size(self, sender):
        self.config.set_value("editor.tab.size", str(sender.text).lower())

    def print_margin(self, sender):
        self.config.set_value("editor.print.margin", str(sender.value).lower())

    def line_wrap(self, sender):
        self.config.set_value("editor.line.wrap", str(sender.value).lower())

    def soft_tabs(self, sender):
        self.config.set_value("editor.soft.tabs", str(sender.value).lower())


def load_view(config):
    view = ui.load_view("ConfigManager")
    view.set_config(config)
    return view

if __name__ == "__main__":
    c = Config()
    c.set_value("editor.font.size", 13)

    cv = load_view(c)
    cv.present("sheet")