import ui
import console
import plistlib



class Config(object):
    def __init__(self):
        self.config_dict = {}
        self.load_config()
        
        self.save_config()
        
    def load_config(self):
        try:
            self.config_dict = plistlib.readPlist("config.plist")
            print "Config Loaded From File"
        except:
            self.config_dict = {
                                "editor.font.size": 13,
                                "editor.style": "ace/theme/kuroir",
                                "editor.show.gutter": "true",
                                
                                }
            print "Config Default"
            
    def save_config(self):
        print "saving config %r" % self.config_dict
        plistlib.writePlist(self.config_dict, "config.plist")
        
    def get_value(self, key, default="FAILED_TO_LOAD_PROPERTY"):
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
        
    def did_load(self):
        self.tabs = self["TabControl"]
        self.editor = self["Editor"]
        print self.tabs
        self.tabs.action = self.change_tab
        
        self.editor["slider1"].action = self.font_size_change
        self.editor["editor.show.gutter"].action = self.show_gutter
        self.editor["editor.style"].action = self.style_change
        
    def change_tab(self, sender):
        tab = sender.segments[sender.selected_index]
        print self[tab]
        self[tab].bring_to_front()
        
    def font_size_change(self, sender):
        self.editor["editor.font.size"].text = "Font Size: %i" % (sender.value * 50)
        self.config.set_value("editor.font.size", int(sender.value * 50))
    
    def show_gutter(self, sender):
        self.config.set_value("editor.show.gutter", str(sender.value).lower())
    
    def style_change(self, sender):
        self.config.set_value("editor.style", str(sender.text).lower())
        
def load_view(config):
    view = ui.load_view("ConfigManager")
    view.set_config(config)
    return view
        
if __name__ == "__main__":
    c = Config()
    c.set_value("editor.font.size", 15)
    print c.get_value("editor.font.size")
    
    cv = load_view(c)
    cv.present("sheet")
    
    #cv = ui.load_view("ConfigManager")
    #cv.present("sheet")
    #cv.set_config(c)
