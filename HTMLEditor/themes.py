import os
import tinycss
import logging


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


def exception_str(exception):
    return '{}: {}'.format(exception.__class__.__name__, exception)


def theme_path():
    if os.getcwd().endswith("HTMLEditor"):
        path = os.path.abspath("../EditorView/CodeMirror-5.3.0/theme")
    else:
        path = os.path.abspath("EditorView/CodeMirror-5.3.0/theme")
    return path


def list_themes():
    path = theme_path()
    themes_lists = os.listdir(path)
    return themes_lists


def get_background_color():
    themes = {"default": ("#000000", "#FFFFFF")}
    p = theme_path()
    themes_list = list_themes()
    par = tinycss.make_parser("page3")
    for file in themes_list:
        with open("%s/%s" % (p, file), "r") as f:
            style = par.parse_stylesheet_file(f)
            i = [str(x) for x in style.rules]
            index = 0
            for x in i:
                if x.endswith("CodeMirror>"):
                    break
                else:
                    index += 1
            if index < len(style.rules):
                decs = style.rules[index].declarations
                background = ""
                text = ""
                for dec in decs:
                    if dec.name == "background":
                        background = str(dec.value.as_css())
                    if dec.name == "color":
                        text = str(dec.value.as_css())

                if background == "":
                    background = "#FFFFFF"
                if text == "":
                    text = "#000000"
                themes[file.replace(".css", "")] = (background, text)
                background = ""
                text = ""
    return themes

themes_data = get_background_color()
view_list = []


def get_view_list(root):
    # print "Loading views for %r" % root
    global view_list
    try:
        # print root
        # print root.subviews
        for sub in root.subviews:
            view_list.append(sub)
            try:
                get_view_list(sub)
            except SystemError as se:
                logger.error("Error loading view list. Load fial")
                logger.exception(exception_str(se))
    except SystemError as se:
        logger.error("Error loading view list. Appent func fial")
        logger.exception(exception_str(se), exc_info=False)


def recursive_style_set(style):
    global view_list
    # print "GLOABAL view_list: %r" % view_list
    logger.debug(len(view_list))
    for sub in view_list:
        try:
            if sub.name == "log_view":
                continue
            set_bg(sub, style)
        except SystemError as e:
            logger.exception(exception_str(e), exc_info=False)


def set_bg(sub, style):
    try:
        sub.background_color = themes_data[style][0]
    except Exception as e:
        logger.exception(exception_str(e), exc_info=False)
    try:
        sub.bar_tint_color = themes_data[style][0]
    except AttributeError as e:
        logger.exception(exception_str(e), exc_info=False)
    try:
        sub.text_color = themes_data[style][1]
    except AttributeError as e1:
        try:
            sub.title_color = themes_data[style][1]
        except AttributeError as e2:
            logger.exception(exception_str(e1), exc_info=False)
            logger.exception(exception_str(e2), exc_info=False)
    logger.debug("Style set for %r", sub)

if __name__ == "__main__":
    print get_background_color()
