import os
import ui

try:
    import cPickle as pickle
except ImportError:
    print "cPickle is not available, using standard pickle module."
    import pickle


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


class Manager(object):
    file_data = {"/": [{}, {}]}

    def __init__(self, pickled_fs="HTMLEditor.pick"):
        self.pickled_fs_name = pickled_fs
        if os.path.exists(pickled_fs):
            self.load_data()
        else:
            self.save_data()
        
        self.current_dir = self.file_data["/"]
        self.current_root = "/"
        self.home = "/"

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
        if new_dir=="/":
            self.current_dir = self.file_data["/"]
            self.current_root = "/"
        else:
            self._cd(new_dir, self.current_dir, new_dir, self.current_root)
        
    def go_to_home(self):
        if self.home=="/":
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

    def _add_file(self, name, contents, last):
        name = name.split("/")
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
        tail = name
        if not tail:
            return head, last[0][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            return self._get_file("/".join(tail), last[1][head])

    def _new_folder(self, path, last):
        path = path.split("/")
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
        tail = path
        if not tail:
            return head, last[1][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder %r does not exist" % head)
            return self._get_folder("/".join(tail), last[1][head])
            
    def _delete_folder(self, path, last):
        path = path.split("/")
        head = path[0]
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
        tail = path
        if not tail:
            del last[0][head]
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            self._delete_file("/".join(tail), last[1][head])
            
    def _walk_to_start(self, path, last, root_str=None):
        root_str = root_str or self.current_root
        if path == "":
            self._walk_directory("", last, root_str)
        else:
            last = self._get_folder(path, last)
            self._walk_directory(path, last, root_str)
        
    def _walk_directory(self, path, last, root_str):
        if root_str=="/":
            root_str=""
        path = path.split("/")
        head = path[0]
        path.remove(head)
        tail = path
        if not tail:
            # print last
            print root_str, last[0].keys(), last[1].keys()
            for x in last[1]:
                self._walk_to_start("", last[1][x], "%s/%s/" % (root_str, x))
        else:
            if head not in last[1]:
                raise FileManagerException("File/Folder does not exist")
            self._walk_directory("/".join(tail), last[1][head], "%s/%s/" % (root_str, head))
            
    def _cd(self, path, last, new_cd, old_cd):
        ncd = self._get_folder(path, last)
        self.current_root = new_cd
        self.current_dir = ncd[1]

FILE = 0x01
FOLDER = 0x02



class FileViewer(ui.View):
    def __init__(self, fileManager, *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)
        self.fileManager = fileManager
        self.listview = ui.TableView()
        self.listview.flex = "TL"
        self.listview.frame = self.frame
        self.listdata = ui.ListDataSource([])
        self.navview = ui.NavigationView(self.listview)
        self.add_subview(self.navview)
        self.populate_list("dir")
        
    def populate_list(self, directory):
        if directory != "/":
            directory = directory
        print directory
        self.fileManager.set_current_dir(directory)
        d = self.fileManager.get_current_dir()
        files = d[0].keys()
        dirs = d[1].keys()
        fdlist = []
        for file in files:
            data = {
                    "title": file,
                    "image": None,
                    "accessory_type": "none",
                    "d_type": FILE
                    }
            fdlist.append(data)
        for dir in dirs:
            data = {
                    "title": dir,
                    "image": None,
                    "accessory_type": "none",
                    "d_type": FOLDER
                    }
            fdlist.append(data)
        
        listview = ui.TableView()
        listdata = ui.ListDataSource(fdlist)
        listview.data_source = listdata
        listview.reload()
        
        self.navview.push_view(listview)

# Simple testing
if __name__ == "__main__":
    print "running simple file manager tests"
    m = Manager()
    print 'm.add_file("dir1/dir1/test.txt", "Bassus victrix saepe imperiums galatae est.")'
    m.add_file("dir1/dir1/test.txt", "Bassus victrix saepe imperiums galatae est.")
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
    print 'm.set_current_dir("dir1")'
    m.set_current_dir("dir1")
    print 'm.walk_directory("")'
    m.walk_directory("")
    print 'm.go_to_home()'
    m.go_to_home()
    print 'm.walk_directory("")'
    m.walk_directory("")
    
    print "running file viewer tests"
    fv = FileViewer(m)
    fv.present("sheet")
