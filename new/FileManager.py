import os

try:
    import cPickle as pickle
except ImportError:
    print "cPickle is not avaliable, using standard pickle module."
    import pickle

def pickle_dump(data, filename):  # saves data into filename
    with open(filename, "w") as out_file:
        pickle.dump(data, out_file)

def pickle_load(filename):        # reads data out of filename
    with open(filename) as in_file:
        return pickle.load(in_file)
    
## File Data format
# {'path': [{'file_name':'data'}, {'folder_name':'contents'}]}
    
    
class Manager(object):
    file_data = {"/": [{}, {}]}
    def __init__(self, pickled_fs="HTMLEditor.pick"):
        self.pickled_fs_name = pickled_fs
        if (os.path.exists(pickled_fs)):
            self.load_data()
        else:
            self.save_data()
                
    def load_data(self):
        self.file_data = pickle_load(self.pickled_fs_name)
    
    def save_data(self):
        pickle_dump(self.file_data, self.pickled_fs_name)
    
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
if __name__ == "__main__":
    m = Manager()
    m.add_file("dir1/test.txt")
