import ui
import sys
import threading
import HTMLParser
import BaseHTTPServer
import SimpleHTTPServer

import templates
reload(templates)

try:
    import cPickle as pickle
except ImportError:
    import pickle

nav_hide = False
view = None
hadler_editor = None
fs_filename = "projects_data.pick"

def pickle_dump(data, filename):  # saves data into filename
    with open(filename, "w") as out_file:
        pickle.dump(data, out_file)

def pickle_load(filename):        # reads data out of filename
    with open(filename) as in_file:
        return pickle.load(in_file)

try:
    file_system = pickle_load(fs_filename)
except:
    file_system = {"data":{}}


class DataSource(ui.ListDataSource):
    def tableview_delete(self, tableview, section, row):
        deleted_item = ui.ListDataSource.tableview_cell_for_row(self, tableview, section, row).text_label.text
        ui.ListDataSource.tableview_delete(self, tableview, section, row)
        #print "deleted_item", deleted_item
        del file_system["data"][deleted_item]
        pickle_dump(file_system, fs_filename)
        

#Classes first then functions
class ProjectNav(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.root_view = ui.TableView("App")
        self.root_view.name = "Projects"
        self.nav_view = ui.NavigationView(self.root_view)
        self.add_subview(self.nav_view)
        
        self.root_view.right_button_items = [
                                             ui.ButtonItem(image=
                                                           ui.Image.named("ionicons-hammer-24"))
                                             ]
        self.root_view.right_button_items[0].action = self.set_edit
        self.root_view.delegate = self
        self.editing = False
        
        self.setup_list_view()
        
    def setup_list_view(self):
        list_data = []
        for item in dict(file_system["data"]):
            #print item
            list_data.append({"title": item})
        #print list_data
        #print self.root_view.data_source
        #self.root_view.data_source = ui.ListDataSource(list_data)
        self.root_view.data_source = DataSource(list_data)
        self.root_view.reload()
        #print self.root_view.data_source
    
    def _add_file_folder(self, path):
        # cclauss: you could also write this as:
        #head, _, tail = path.partition('/')

        path = path.split("/")
        head = path[0]
        tail = path[1:]
        
        
    def tableview_did_select(self, tableview, section, row):
        selection = tableview.data_source.selected_row
        #print selection
        data = self.root_view.data_source.tableview_cell_for_row(tableview, section, row)
        #data = self.root_view.data_source.items[selection]
        #print data 
        #open_file(data["title"])
        open_file(data.text_label.text)
                       
    def set_edit(self, sender):
        self.editing = not self.editing
        self.root_view.editing = self.editing
        #self.root_view.directional_lock_enabled = self.editing
        if self.editing:
            add = ui.ButtonItem(image=ui.Image.named("ionicons-compose-24"))
            add.action = self.add_file
            self.root_view.left_button_items = [add]
        else:
            self.root_view.left_button_items = []
    
    def add_file(self, sender):
        import console
        result = None
        in_alert = ui.load_view("views/InputAlert")
        in_alert.center = view.center
        def cancle_event(sender):
            view.remove_subview(in_alert)
        def accept_event(sender):
            result = in_alert["input_field"].text
            if result:
                # cclauss: consider making HTML and JAVASCRIPT format strings with {} instead of @file_name
                # you could then write: templates.HTML.format(result)
                if result.endswith(".html"):
                    file_system["data"][result] = [templates.HTML.replace("@file_name", result), templates.REQUEST_HANDLER]
                elif result.endswith(".js"):
                    file_system["data"][result] = [templates.JAVASCRIPT.replace("@file_name", result)]
                elif result.endswith(".css"):
                    file_system["data"][result] = [templates.CSS]
                else:
                    file_system["data"][result] = [""]
                pickle.dump(file_system, fs_filename)
                self.setup_list_view()
                cancle_event(sender)
            
        in_alert["ok_btn"].action = accept_event
        in_alert["cancle_btn"].action = cancle_event
        
        view.add_subview(in_alert)
        
    def set_width_height(self, view):
        self.root_view.width  = self.nav_view.width  = 200
        self.root_view.height = self.nav_view.height = view.height

        
class ToolMenu(ui.View):
    def __init__(self, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.open_tags_label = ui.Label()
        self.add_subview(self.open_tags_label)
        self.open_tags_label.flex = "LRWB"
    
    def reload_label(self, tags):
        label = "Open Tags: " + ", ".join(tags) if tags else "No Open Tags"
        self.open_tags_label.text = label
    
class TextViewDelegate(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.check_tags = False
        self.check_tabs = False
        self.insert_close = False
        self.insert_close_str = ""
        self.tab_num = 0
        self.range_start = 0
        
    def textview_should_change(self, textview, text_range, replacement):
        current_text = textview.text
        if not text_range[0]:
            last = current_text[text_range[0]-1]
            opp = "> ] } )".split()
            try:
                forward = current_text[text_range[0]]
            except:
                forward = current_text[-1]
            if last in "< [ { (".split():
                if replacement == "/" and last == "<":
                    self.check_tags = True
                    self.range_start = text_range[1] + 1
                elif replacement != "": # and  forward == "\n":
                    self.insert_close = True
                    self.range_start = text_range[1] + 1
                    self.insert_close_str = opp[["<", "[", "{", "("].index(last)]
            elif replacement == "\n":
                self.get_current_line_tab(textview)
                self.check_tabs = True
                self.range_start = text_range[1] + 1
                    
        #print textview, text_range, "%r" % replacement
        return True
    
    def get_current_line_tab(self, textview):
        text, selection = textview.text, textview.selected_range
        try:
            ctext = text[selection[0] - 1 : selection[1] - 1]
            x = selection[1] - 1
            while True:
                c = text[x]
                if c != "\n":
                    ctext += c
                    x += 1
                else:
                    break
            x = selection[0] - 1
            try:
                while True:
                    c = text[x]
                    if c != "\n" and c != 0:
                        ctext = c + ctext
                        x -= 1
                    else:
                        break
            except:
                pass
            print "%r" % ctext
            tabs = ctext.count("\t")
            print tabs
            should_remove_one = True
            for x in ctext:
                if x != "\t":
                    should_remove_one = False
            if should_remove_one:
                tabs -= 1
        except:
            tabs = 0
        self.tab_num = tabs
        
    def insert_text_at(self, textview, replacement_text, start_point, selected_range=None):
        text = textview.text
        selection = selected_range or textview.selected_range
        
        t_range = (start_point, len(text))
        rep_text = text[start_point:]
        textview.replace_range(t_range, replacement_text + rep_text)
        
        print selection
        selection = (selection[0] + len(replacement_text), selection[0] + len(replacement_text))
        print selection
        print len(textview.text)
        
        file_system["data"][self.file_name][0] = textview.text
        pickle_dump(file_system, fs_filename)
        
        try:
            textview.selected_range = selection
        except Exception as e:
            print e
    
    def textview_did_change(self, textview):
        text = textview.text
        selection = textview.selected_range
        if self.check_tags:
            self.check_tags = False
            parser = HTMLParserd()
            parser.feed(text)
            open_tags = parser.open_tags
            tag = open_tags[-1]
            self.insert_text_at(textview, "%s>" % tag, self.range_start)
        if self.check_tabs:
            print self.tab_num
            self.check_tabs = False
            self.insert_text_at(textview, "\t" * self.tab_num, self.range_start)
        if self.insert_close:
            self.insert_close = False
            self.insert_text_at(textview, self.insert_close_str, self.range_start, (textview.selected_range[0]-1, textview.selected_range[0]-1))
            
        
        file_system["data"][self.file_name][0] = textview.text
        
        data = open("projects_data.pick", "w")
        pickle.dump(file_system, data)
        data.close()
        
        parser = HTMLParserd()
        parser.feed(textview.text)
        
        view["tools_menu"].reload_label(parser.open_tags)
    

class HTMLParserd(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.open_tags = []
        self.files_list = []
        
    def handle_starttag(self, tag, attr):
        #print tag, attr
        if tag == "script":
            for x in attr:
                if "src" in x:
                    self.files_list.append(x[1])
        self.open_tags.append(tag)
    
    def handle_endtag(self, tag):
        #print tag
        try:
            self.open_tags.remove(tag)
        except:
            pass
        
    def handle_startendtag(self, tag, attr):
        #print tag, attr
        if tag == "link":
            for x in attr:
                if "href" in x:
                    self.files_list.append(x[1])
        
    def feed(self, *args, **kwargs):
        import console
        #print "Start"
        HTMLParser.HTMLParser.feed(self, *args, **kwargs)
        #print "Done"
        #print "files_list = %r" % self.files_list
        if not self.open_tags == []:
            try:
                console.alert("Parse Error", "Not all tag/s have been closed.\nOpen tag/s %r" % self.open_tags)
            except:
                print "Not all tag/s have been closed.\nOpen tag/s %r" % self.open_tags
        #console.alert("parse done")
        
    
@ui.in_background
def build_script_selection(file_name, file_data):
    #print file_name, file_data
    view["editor_view"]["script_nav"].segments = tuple([file_name])
    view["editor_view"]["script_nav"].selected_index = 1
    if file_name.endswith(".html"):
        parser = HTMLParserd()
        parser.feed(file_data[0])
        scrips = parser.files_list
        #print scrips
        for script in scrips:
            #print script
            try:
                #data = file_system["data"][script]
                segments = list(view["editor_view"]["script_nav"].segments)
                segments.append(script)
                view["editor_view"]["script_nav"].segments = tuple(segments)
            except Exception as e:
                import console
                console.alert("Error", "So yeah there has been an error with the file so umm, I'm not going to open it...\n%r" % str(e))
    else:
        print view["editor_view"]["script_nav"].segments
        
                
def load_file(name):
    try:
        file_data = file_system["data"][name]
        view["editor_view"]["editor_text"].text = file_data[0]
        view["editor_view"]["editor_text"].delegate = TextViewDelegate(name)
    except Exception as e:
        import console
        console.alert("Error", "So yeah there has been an error with the file so umm, I'm not going to open it...\n%r" % str(e))
    
            
@ui.in_background
def set_selected_script(sender):
    index = sender.selected_index
    if index != -1:
        file = sender.segments[index]
        #print file
        load_file(file)

@ui.in_background
def set_selected_file(sender):
    #print "set_selected_file(%r)" % sender
    index = sender.selected_index
    if index != -1:
        try:
            file = sender.segments[index]
            #print file
            file_data = file_system["data"][file]
            #print file_data
            #view["editor_view"]["editor_text"].text = file_data
            #print file_data
            build_script_selection(file, file_data)
        except Exception as e:
            import console
            console.alert("Error", "So yeah there has been an error with the file so umm, I'm not going to open it...\n%r" % str(e))
    else:
        print "File Has No Data"
        
def open_file(name):
    #print name
    old = list(view["editor_view"]["file_nav"].segments)
    if not name in old:
        old.append(name)
    view["editor_view"]["file_nav"].segments = old
    view["editor_view"]["file_nav"].selected_index = len(old)-1
    set_selected_file(view["editor_view"]["file_nav"])

def show_hide_project_nav(sender):
    global nav_hide
    nav_hide = not nav_hide
    #print nav_hide
    view = sender.superview.superview
    view["project_nav_view"].hidden = nav_hide
    width = 0 if nav_hide else 200
    for subview in ("editor_view", "tools_menu"):
        view[subview].x = width
        view[subview].width = view.width - width

class WebViewDelegate(object):
    def webview_did_finish_load(self, wv):
        #print "finished loading"
        wv.name = wv.evaluate_javascript("document.title")
        #print "title collected"
        

@ui.in_background
def show_web_view(sender):
    index = view["editor_view"]["file_nav"].selected_index
    if index != -1:
        file = view["editor_view"]["file_nav"].segments[index]
        print file
        if file.endswith(".html"):
            handler = file_system["data"][file][1]
            import console
            response = 0 #console.alert("Is this Handler Ok?", handler, "Yes", "No", hide_cancel_button=True)
            print response
            if response == 0:
                exec handler
                
                httpd = BaseHTTPServer.HTTPServer(("127.0.0.1", 80), Handler)
                ts = threading.Thread(target=httpd.serve_forever)
                ts.start()
                print "Server Started"
                wv = ui.WebView("Preview")
                wv.delegate = WebViewDelegate()
                wv.present("sheet")
                wv.load_url("http://127.0.0.1/")
                wv.wait_modal()
                httpd.shutdown()
                ts.join()
                print "Server Closed"
    
# cclauss: you should be able to have all three buttons share a single action function
#  if you edit the .pyui file to set the button.names to 'tags', 'cssref', and 'jsref'
#   and set the button.actions to help_action
def help_action(sender):
    wv = ui.WebView()
    wv.load_url("http://www.w3schools.com/{}/default.asp".format(sender.name))
    wv.delegate = WebViewDelegate()
    wv.present("sheet")
    wv.wait_modal()

#def help_html_tags(sender):
#    help_wv("http://www.w3schools.com/tags/default.asp")
    
#def help_js(sender):
#    help_wv("http://www.w3schools.com/cssref/default.asp")
    
#def help_css(sender):
#    help_wv("http://www.w3schools.com/jsref/default.asp")
    
#def help_wv(path):
#    wv = ui.WebView()
#    wv.delegate = WebViewDelegate()
#    wv.present("sheet")
#    wv.load_url(path)
#    wv.wait_modal()
    
def quit_prog(sender):
    sender.superview.close()
    view.close()
    print "Goodbye"
    
def close_file(sender):
    sender.superview.close()
    try:
        view["editor_view"]["file_nav"].selected_index
        old = list(view["editor_view"]["file_nav"].segments)
        old.remove(old[view["editor_view"]["file_nav"].selected_index])
        view["editor_view"]["file_nav"].segments = old
        view["editor_view"]["script_nav"].segments = ()
        set_selected_file(view["editor_view"]["file_nav"])
        view["editor_view"]["editor_text"].text = "NO OPEN FILES"
    except:
        print "All Files Closed"
        view["editor_view"]["editor_text"].text = "NO OPEN FILES"

def quit(sender):
    quit_view = ui.load_view("views/quit_view")
    quit_view.height = 32
    quit_view["quit_prog"].action = quit_prog
    quit_view["close_file"].action = close_file
    quit_view.present("popover", hide_title_bar=True)


def edit_handler(sender):
    index = view["editor_view"]["file_nav"].selected_index
    if not index == -1:
        file = view["editor_view"]["file_nav"].segments[index]
        print file
        if file.endswith(".html"):
            try:
                handler = file_system["data"][file][1]
                hadler_editor["editor_view"].text = handler
                hadler_editor.present("sheet", hide_title_bar=True)
            except:
                pass
    
def close_editor(sender):
    index = view["editor_view"]["file_nav"].selected_index
    if index != -1:
        file = view["editor_view"]["file_nav"].segments[index]
        print file
        if file.endswith(".html"):
            handler = hadler_editor["editor_view"].text
            file_system["data"][file][1] = handler
            
            with open("projects_data.pick", "w") as data:
                pickle.dump(file_system, data)
            
            hadler_editor.close()

hadler_editor = ui.load_view("./views/custom_handler")

## NO View Specific functions below this point
view = ui.load_view()

view["project_nav_view"].send_to_back()
view["project_nav_view"].set_width_height(view)
view["project_nav_view"].hidden = False

view["editor_view"]["file_nav"].action = set_selected_file
view["editor_view"]["file_nav"].segments = ()
view["editor_view"]["script_nav"].action = set_selected_script
view["editor_view"]["script_nav"].segments = ()

view.present("fullscreen", hide_title_bar=True)
