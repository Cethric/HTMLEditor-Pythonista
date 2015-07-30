import os
import copy
import zipfile
try:
    import ui
    import console
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
    import dummyConsole as console

import templates
from HTMLEditor import themes
from ConfigManager import Config

try:
    import cPickle as pickle
except ImportError:
    print "cPickle is not available, using standard pickle module."
    import pickle

reload(themes)
reload(templates)


def pickle_dump(data, filename):  # saves data into filename
    with open(filename, "w") as out_file:
        pickle.dump(data, out_file)


def pickle_load(filename):        # reads data out of filename
    with open(filename) as in_file:
        return pickle.load(in_file)


# File Data format
# {'folder_name': [{'file_name':'data'}, {'folder_name':'contents'}]}

class FileManagerException(Exception):
    pass


FILE = 0x01
FOLDER = 0x02


class Manager(object):
    file_data = {"/": [{}, {}]}

    def __init__(self, pickled_fs="HTMLEditor.pick"):
        self.pickled_fs_name = pickled_fs
        if os.path.exists(pickled_fs):
            self.load_data()
        else:
            self.save_data()

        self.current_dir = self.file_data["/"]
        self.current_path = self.current_root = self.home = "/"

    def load_data(self):
        self.file_data = pickle_load(self.pickled_fs_name)
        self.current_dir = self.file_data["/"]

    def save_data(self):
        pickle_dump(self.file_data, self.pickled_fs_name)

    def add_file(self, name, contents):
        self._add_file(name, contents, self.current_dir)
        self.save_data()

    def get_file(self, name):
        return self._get_file(name, self.current_dir)

    def new_folder(self, path):
        self._new_folder(path, self.current_dir)
        self.save_data()

    def get_folder(self, path):
        return self._get_folder(path, self.current_dir)

    def delete_file(self, path):
        self._delete_file(path, self.current_dir)

    def delete_folder(self, path):
        self._delete_folder(path, self.current_dir)

    def walk_directory(self, start):
        self._walk_to_start(start, self.current_dir)

    def set_current_dir(self, new_dir):
        if new_dir == "/":
            self.current_dir = self.file_data["/"]
            self.current_root = "/"
        else:
            self._cd(new_dir, self.current_dir, new_dir, self.current_root)

    def go_down_one_level(self):
        l = self.current_root.split("/")[0:-2]
        new_dir = "/".join(l)
        if new_dir:
            self._cd(new_dir, self.current_dir, new_dir, self.current_root)

    def go_to_home(self):
        if self.home == "/":
            self.current_dir = self.file_data["/"]
            self.current_root = "/"
        else:
            self._cd(self.home, self.current_dir, self.home, self.current_root)

    def get_home(self):
        return self.home

    def get_current_root(self):
        return self.current_root

    def get_current_dir(self):
        return self.current_dir

    def save_as_zip(self, zip_name, path, type=FOLDER):
        c = self.current_dir
        if type == FOLDER:
            d = self.get_folder(path)
            self._save_zip_data(zip_name, d[1], path)
        elif type == FILE:
            f = self.get_file(path)
            self._save_as_zip(zip_name, [path, f[1]], "w")

    def _save_zip_data(self, zip_name, base, path):
        # print "DIR"
        for dir in base[1]:
            p = os.path.join(path, dir)
            self._save_zip_data(zip_name, base[1][dir], p)
        # print "FILE"
        for file in base[0]:
            # print file
            self._save_as_zip(
                zip_name, [os.path.join(path, file), base[0][file]])
        # print base

    def _save_as_zip(self, zip_name, data, mode="a"):
        zip_file = zipfile.ZipFile(zip_name, mode, zipfile.ZIP_DEFLATED, True)
        zip_file.writestr(data[0], data[1])
        zip_file.close()

    def _add_file(self, name, contents, last):
        name = name.split("/")
        head = name[0]
        name.remove(head)
        if head == "":
            head = name[0]
            name.remove(head)
        tail = name
        if not tail:
            last[0][head] = contents
        else:
            if head not in last[1]:
                last[1][head] = [{}, {}]
            self._add_file("/".join(tail), contents, last[1][head])

    def _get_file(self, name, last):
        name = name.split("/")
        head = name[0]
        name.remove(head)
        if head == "":
            head = name[0]
            name.remove(head)
        tail = name
        # print head, tail
        if not tail:
            return head, last[0][head]
        else:
            if head not in last[1]:
                raise FileManagerException(
                    "File/Folder {} does not exist".format(head))
            return self._get_file("/".join(tail), last[1][head])

    def _new_folder(self, path, last):
        path = path.split("/")
        head = path[0]
        path.remove(head)
        if head == "":
            head = path[0]
            path.remove(head)
        tail = path
        if not tail:
            last[1][head] = [{}, {}]
        else:
            if head not in last[1]:
                last[1][head] = [{}, {}]
            self._new_folder("/".join(tail), last[1][head])

    def _get_folder(self, path, last):
        path = path.split("/")
        head = path[0]
        path.remove(head)
        if head == "":
            head = path[0]
            path.remove(head)
        tail = path
        if not tail:
            return head, last[1][head]
        else:
            if head not in last[1]:
                raise FileManagerException(
                    "File/Folder %r does not exist" % head)
            return self._get_folder("/".join(tail), last[1][head])

    def _delete_folder(self, path, last):
        path = path.split("/")
        head = path[0]
        path.remove(head)
        if head == "":
            head = name[0]
            path.remove(head)
        tail = path
        if not tail:
            del last[1][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            self._delete_folder("/".join(tail), last[1][head])

    def _delete_file(self, path, last):
        path = path.split("/")
        head = path[0]
        path.remove(head)
        if head == "":
            head = name[0]
            path.remove(head)
        tail = path
        if not tail:
            del last[0][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            self._delete_file("/".join(tail), last[1][head])

    def _walk_to_start(self, path, last, root_str=None):
        root_str = root_str or self.current_root
        if path:
            last = self._get_folder(path, last)
        self._walk_directory(path, last, root_str)

    def _walk_directory(self, path, last, root_str):
        if root_str == "/":
            root_str = ""
        path = path.split("/")
        head = path[0]
        path.remove(head)
        tail = path
        if not tail:
            for x in last[1]:
                self._walk_to_start("", last[1][x], "%s/%s/" % (root_str, x))
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            self._walk_directory(
                "/".join(tail), last[1][head], "%s/%s/" % (root_str, head))

    def _cd(self, path, last, new_cd, old_cd):
        ncd = self._get_folder(path, last)
        self.current_root = new_cd
        self.current_dir = ncd[1]


class AddAction(object):

    def __init__(self, tableview, tableview_data, fileManager):
        self.tableview_data = tableview_data
        self.tableview = tableview
        self.fileManager = fileManager

    @ui.in_background
    def invoke(self, sender):
        print sender
        try:
            c = console.alert("New", "File/Folder", "File", "Folder") - 1
            r = console.input_alert("New File", "Enter Filename")
            if c == 0:
                if r.endswith(".html"):
                    self.tableview_data[c][r] = templates.HTML.format(r)
                elif r.endswith(".css"):
                    self.tableview_data[c][r] = templates.CSS
                elif r.endswith(".js"):
                    try:
                        text = templates.JAVASCRIPT.format(r)
                    except KeyError as e:
                        text = templates.JAVASCRIPT.replace("{}", r)
                    self.tableview_data[c][r] = text
                elif r.endswith("_handler.py"):
                    self.tableview_data[c][r] = templates.REQUEST_HANDLER
                else:
                    self.tableview_data[c][r] = "Hello World from %r" % r
            elif c == 1:
                self.tableview_data[c][r] = [{}, {}]
            self.fileManager.save_data()
        except KeyboardInterrupt:
            print "The user cancled the input"
        self.tableview.reload_data()


class EditAction(object):

    def __init__(self, tableview, tableview_data, fileManager):
        self.tableview = tableview
        self.tableview_data = tableview_data
        self.fileManager = fileManager
        self.tableview.editing = False
        self.tableview.data_source.edit_action = self.edit

        self.tableview.allows_selection_during_editing = True
        self.tableview.allows_multiple_selection_during_editing = True

    @ui.in_background
    def invoke(self, sender):
        self.tableview.editing = not self.tableview.editing
        if self.tableview.editing:
            zipper = ui.ButtonItem(
                action=self.zipup,
                image=ui.Image.named("ionicons-ios7-photos-outline-24")
            )
            self.tableview.left_button_items = [zipper]

        else:
            self.tableview.left_button_items = []

    @ui.in_background
    def edit(self, datasource, *args, **kwargs):
        x = copy.copy(self.tableview_data)
        try:
            for i in datasource.items:
                if i["d_type"] == FOLDER:
                    del x[1][i["title"]]
                elif i["d_type"] == FILE:
                    del x[0][i["title"]]
        except ValueError as e:
            print e

        file_key = ""
        try:
            for file_key in x[0]:
                del self.tableview_data[0][file_key]
        except RuntimeError as e:
            print "Error occured deleting file %r."
            print "refresh view to check what happend" % file_key
            print e.message

        dir_key = ""
        try:
            for dir_key in x[1]:
                del self.tableview_data[1][dir_key]
        except RuntimeError as e:
            print "Error occured deleting directory %r."
            print "refresh view to check what happend" % dir_key
            print e.message
        self.fileManager.save_data()
        self.tableview.reload_data()

    def zipup(self, sender):
        print "Zipping Data"
        si = self.tableview.delegate.selected_items
        if len(si) < 1:
            self.error_alert("No Selections Made")
        else:
            self.zip(si)

    @ui.in_background
    def error_alert(self, msg):
        console.alert("ERROR", msg)

    @ui.in_background
    def zip(self, si):
        try:
            zn = console.input_alert("Enter the zip file name")
            if not zn.endswith(".zip"):
                zn += ".zip"
            print "Saving contents to the zip %r" % zn
            for i in si:
                self.fileManager.save_as_zip(zn, i["d_path"], i["d_type"])

            print "Saved contents to the zip %r" % zn
            console.hud_alert("Zipped", "success")
            console.open_in(os.path.abspath(zn))
        except KeyboardInterrupt as e:
            print "User cancled the procces"


def dummy_file_callback(file_name, file_data):
    print "The file %r was loaded\nContents:\n%s" % (file_name, file_data)
    v = ui.TextView()
    v.text = file_data
    v.name = file_name
    v.present("sheet")


class FileViewer(ui.View):

    def __init__(self, fileManager, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.name = "FileViewer<%r>" % self
        self.fileManager = fileManager
        self.file_load_callback = dummy_file_callback
        self.listview = ui.TableView()
        self.listview.flex = "WH"
        self.listview.frame = self.frame
        self.listview.name = "root"
        self.listview.delegate = self
        self.navview = ui.NavigationView(self.listview)
        self.navview.flex = "WH"
        self.navview.frame = self.frame
        self.navview.name = "NAME"
        self.add_subview(self.navview)
        self.listview.set_needs_display()
        self.navview.set_needs_display()
        self.set_needs_display()
        self.init_list()

        self.selected_items = []

        self.current_list = None
        c = Config()
        self.style = c.get_value("editor.style")
        
    def set_style(self):
        themes.set_bg(self, self.style)
        themes.set_bg(self.listview, self.style)
        themes.set_bg(self.navview, self.style)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.ListDataSource.tableview_cell_for_row(
            tableview.data_source, tableview, section, row)
        if self.style:
            if cell.content_view:
                themes.set_bg(cell.content_view, self.style)
            if cell.text_label:
                themes.set_bg(cell.text_label, self.style)
            if cell.detail_text_label:
                themes.set_bg(cell.detail_text_label, self.style)
                cell.detail_text_label.text = "test"
            if cell.image_view:
                themes.set_bg(cell.image_view, self.style)
        else:
            cell.content_view.background_color = self.listview.background_color
        return cell

    def init_list(self):
        d = self.fileManager.get_current_dir()
        files = d[0]
        dirs = d[1]
        fdlist = []
        for file_name, file_data in files:
            data = {
                "title": file_name,
                "image": "ionicons-document-text-24",
                "accessory_type": "none",
                "d_type": FILE,
                "d_data": file_data,
                "d_path": "/" + file_name
            }
            fdlist.append(data)
        for dir_name, dir_data in dirs.iteritems():
            data = {
                "title": dir_name,
                "image": "ionicons-folder-24",
                "accessory_type": "disclosure_indicator",
                "d_type": FOLDER,
                "d_data": dir_data,
                "d_path": "/" + dir_name
            }
            fdlist.append(data)
        self.listview.data_source = ui.ListDataSource(fdlist)
        self.listview.data_source.tableview_cell_for_row =\
            self.tableview_cell_for_row
        self.listview.reload()

        add_act = AddAction(self.listview, d, self.fileManager)
        add_btn = ui.ButtonItem(
            action=add_act.invoke,
            image=ui.Image.named("ionicons-ios7-compose-outline-24")
        )
        edit_act = EditAction(self.listview, d, self.fileManager)
        edit_btn = ui.ButtonItem(
            action=edit_act.invoke,
            image=ui.Image.named("ionicons-hammer-24")
        )

        self.listview.right_button_items = [edit_btn, add_btn]

    def populate_list(self, path, d_path, directory=[]):
        print path
        files = directory[0]
        dirs = directory[1]
        fdlist = []
        for file_name, file_data in files.items():
            data = {
                "title": file_name,
                "image": "ionicons-document-text-24",
                "accessory_type": "none",
                "d_type": FILE,
                "d_data": file_data,
                "d_path": d_path + "/" + file_name
            }
            fdlist.append(data)
        for dir_name, dir_data in dirs.iteritems():
            data = {
                "title": dir_name,
                "image": "ionicons-folder-24",
                "accessory_type": "disclosure_indicator",
                "d_type": FOLDER,
                "d_data": dir_data,
                "d_path": d_path + "/" + dir_name,
                "background_color":  "#FFFF00",
            }
            fdlist.append(data)

        listview = ui.TableView()
        listview.background_color = self.listview.background_color
        listview.data_source = ui.ListDataSource(fdlist)
        listview.data_source.tableview_cell_for_row =\
            self.tableview_cell_for_row
        listview.data_source.move_enabled = True
        listview.reload()
        listview.delegate = self
        listview.name = path
        self.navview.push_view(listview)

        add_act = AddAction(self.listview, directory, self.fileManager)
        add_btn = ui.ButtonItem(
            action=add_act.invoke,
            image=ui.Image.named("ionicons-ios7-compose-outline-24")
        )
        edit_act = EditAction(listview, directory, self.fileManager)
        edit_btn = ui.ButtonItem(
            action=edit_act.invoke,
            image=ui.Image.named("ionicons-hammer-24")
        )

        listview.right_button_items = [edit_btn, add_btn]
        self.current_list = listview

    def tableview_did_select(self, tableview, section, row):
        items = tableview.data_source.items
        item = items[row]
        if tableview.editing:
            self.selected_items.append(item)
        else:
            self.selected_items = []
            if item["d_type"] == FOLDER:
                self.populate_list(
                    item["title"], item["d_path"], item["d_data"])
            elif item["d_type"] == FILE:
                self.file_load_callback(item["d_path"], item["d_data"])
            else:
                raise FileManagerException(
                    "Unknow object descriptor %s" % hex(item["d_type"]))

    def tableview_did_deselect(self, tableview, section, row):
        items = tableview.data_source.items
        item = items[row]
        if tableview.editing:
            self.selected_items.remove(item)

# Simple testing
if __name__ == "__main__":
    print "running simple file manager tests"
    m = Manager()
    print '''m.add_file("dir1/dir1/test.txt",
            "Bassus victrix saepe imperiums galatae est.")'''
    m.add_file("dir1/dir1/test.txt",
               "Bassus victrix saepe imperiums galatae est.")
    print 'print m.get_file("dir1/dir1/test.txt")'
    print m.get_file("dir1/dir1/test.txt")
    print 'm.new_folder("dir/folder/path")'
    m.new_folder("dir/folder/path")
    print 'm.get_folder("dir/folder/path")'
    print m.get_folder("dir/folder/path")
    print 'm.get_folder("dir1/dir1")'
    print m.get_folder("dir1/dir1")
    print 'm.current_dir'
    print m.current_dir
    print 'm.walk_directory("")'
    m.walk_directory("")
    print 'm.set_current_dir("dir1/dir1")'
    m.set_current_dir("dir1/dir1")
    print 'm.walk_directory("")'
    m.walk_directory("")
    print "m.go_down_one_level()"
    m.go_down_one_level()
    print 'm.go_to_home()'
    m.go_to_home()
    print 'm.walk_directory("")'
    print m.walk_directory("")
    print "m.save_as_zip('test.zip', 'dir1/dir1', FOLDER)"
    m.save_as_zip('test.zip', 'dir1/dir1', FOLDER)
    print "running file viewer tests"
    fv = FileViewer(m)
    fv.present("sheet")
