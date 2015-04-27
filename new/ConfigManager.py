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
        
if __name__ == "__main__":
    c = Config()
