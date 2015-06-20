from nose import with_setup
# {'folder_name': [{'file_name':'data'}, {'folder_name':'contents'}]}

Manager = None
def setup_manager():
    import FileManager
    global Manager
    Manager = FileManager.Manager
    
def setup_manager_first():
    import os
    os.remove("HTMLEditor.pick")
    del os
    import FileManager
    global Manager
    Manager = FileManager.Manager
    
def teardown_manager():
    global Manager
    Manager = None
    
@with_setup(setup_manager_first, teardown_manager)
def test_manager_add_file():
    m = Manager()
    m.add_file("dir1/dir1/test.txt", "Bassus victrix saepe imperiums galatae est.")
    return True

@with_setup(setup_manager, teardown_manager)
def test_manager_get_file():
    m = Manager()
    assert m.get_file("dir1/dir1/test.txt") == ("test.txt", "Bassus victrix saepe imperiums galatae est.")

@with_setup(setup_manager, teardown_manager)
def test_manager_new_folder():
    m = Manager()
    m.new_folder("dir/folder/path")

@with_setup(setup_manager, teardown_manager)
def test_manager_get_folder():
    m = Manager()
    assert m.get_folder("dir/folder/path") == ("path", [{}, {}])

@with_setup(setup_manager, teardown_manager)
def test_manager_get_folder2():
    m = Manager()
    assert m.get_folder("dir1/dir1") == ("dir1", [{}, {}])

@with_setup(setup_manager, teardown_manager)
def test_manager_current_dir():
    m = Manager()
    print m.current_dir

@with_setup(setup_manager, teardown_manager)
def test_manager_walk_directory():
    m = Manager()
    m.walk_directory("")

@with_setup(setup_manager, teardown_manager)
def test_manager_set_current_dir():
    m = Manager()
    m.set_current_dir("dir1/dir1")

@with_setup(setup_manager, teardown_manager)
def test_manager_walk_directory2():
    m = Manager()
    m.walk_directory("")

@with_setup(setup_manager, teardown_manager)
def test_manager_go_down_one_level():
    m = Manager()
    m.go_down_one_level()

@with_setup(setup_manager, teardown_manager)
def test_manager_go_to_home():
    m = Manager()
    m.go_to_home()

@with_setup(setup_manager, teardown_manager)
def test_manager_walk_directory_3():
    m = Manager()
    m.walk_directory("")
