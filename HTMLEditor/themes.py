import os
import tinycss

def theme_path():
    print os.getcwd()
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
    themes = {"default":"#000000"}
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
                for dec in decs:
                    if dec.name == "background":
                        themes[file.replace(".css", "")] = dec.value.as_css()
                        break
                    else:
                        themes[file.replace(".css", "")] = "#000000"
    return themes
            
    
if __name__ == "__main__":
    print get_background_color()
