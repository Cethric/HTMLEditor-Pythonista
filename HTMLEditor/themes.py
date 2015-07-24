import os
import tinycss

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
    themes = {"default":("#000000", "#FFFFFF")}
    p = theme_path()
    themes_list = list_themes()
    par = tinycss.make_parser("page3")
    for file in themes_list:
        with open("%s/%s" %(p, file), "r") as f:
            style = par.parse_stylesheet_file(f)
            i = [str(x) for x in style.rules]
            index = 0
            for x in i:
                if x.endswith("CodeMirror>"):
                    break
                else:
                    index+=1
            if index<len(style.rules):
                decs = style.rules[index].declarations
                background = ""
                text = ""
                for dec in decs:
                    if dec.name == "background":
                        background = str(dec.value.as_css())
                    if dec.name == "color":
                        text = str(dec.value.as_css())
                
                if background=="":
                    background = "#000000"
                if text=="":
                    text = "#FFFFFF"
                themes[file.replace(".css", "")] = (background, text)
    return themes
    
themes_data = get_background_color()
def recursive_style_set(root, style):
    try:
        for sub in root.subviews:
            if sub.name=="log_view":
                continue
            set_bg(sub, style)
    except SystemError as e:
        print exception_str(e)
        
def set_bg(sub, style):
    recursive_style_set(sub, style)
    sub.background_color = themes_data[style][0]
    try:
        sub.bar_tint_color = themes_data[style][0]
    except AttributeError as e:
        print exception_str(e)
    try:
        sub.text_color = themes_data[style][1]
    except AttributeError as e1:
        try:
            sub.title_color = themes_data[style][1]
        except AttributeError as e2:
            print exception_str(e1)
            print exception_str(e2)
    print "Style set"

if __name__ == "__main__":
    print get_background_color()
