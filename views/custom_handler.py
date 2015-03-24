import ui
import SimpleHTTPServer

if __name__ in "__main__":
    view = ui.load_view("custom_handler")
    
    view.present("sheet")
    
    exec str(view["editor_view"].text)
