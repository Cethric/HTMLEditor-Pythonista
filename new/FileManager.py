import os
try:
    from cPickle import load, dump
except ImportError:
    print "CPickle is not avaliable using statard pickle module"
    from pickle import load, dump
    
## File Data format
# {'path': [{'file_name':'data'}, {'folder_name':'contents'}]}
    
    
class Manager(object):
    file_data = {"/": [{}, {}]}
    def __init__(self, pickled_fs="data.pick"):
        self.pickled_fs_name = pickled_fs
        if (os.path.exists(pickled_fs)):
            self.load_data()
        else:
            self.save_data()
                
    def load_data(self):
        with open(self.pickled_fs_name, "rb") as f:
            self.file_data = load(f)
    
    def save_data(self):
        with open(self.pickled_fs_name, "wb") as f:
            dump(self.file_data, f)
    
    def add_file(self, name):
        self._add_file(name, self.file_data)
        
    def _add_file(self, name, last):
        tail, _, head = name.rpartition("/")
        print "Tail: %r Head: %r" % (tail, head)
        if not head:
            print "Final File"
            print tail
        else:
            print "Dir"
            print head
            self._add_file(tail, last)
        

# Simple testing
if __name__ in "__main__":
    m = Manager()
    m.add_file("dir1/test.txt")
