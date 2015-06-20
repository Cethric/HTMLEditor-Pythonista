from nose import with_setup


Manager = None
def setup_manager():
    import FileManager
    global Manager
    Manager = FileManager.Manager
    
def setup_manager_first():
    print '''
############################
#    FILE MANAGER TESTS    #
############################
'''

    import os
    try:
        os.remove("HTMLEditor.pick")
        os.remove("test.zip")
    except OSError:
        pass
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
    assert m.get_folder("dir1/dir1") == ("dir1", [{"test.txt": "Bassus victrix saepe imperiums galatae est."}, {}])

@with_setup(setup_manager, teardown_manager)
def test_manager_current_dir():
    m = Manager()
    assert m.current_dir == [{},{'dir1': [{}, {'dir1': [{'test.txt': 'Bassus victrix saepe imperiums galatae est.'}, {}]}], 'dir': [{}, {'folder': [{}, {'path': [{}, {}]}]}]}]

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

@with_setup(setup_manager, teardown_manager)
def test_manager_save_zip_dir():
    m = Manager()
    m.save_as_zip('test.zip', 'dir1/dir1', 0x02)
    
@with_setup(setup_manager, teardown_manager)
def test_manager_save_zip_file():
    m = Manager()
    m.save_as_zip('test.zip', 'dir1/dir1/test.txt', 0x01)

Config = None
def setup_config():
    import ConfigManager
    global Config
    Config = ConfigManager.Config
    
def setup_config_first():
    print '''
##############################
#    CONFIG MANAGER TESTS    #
##############################
'''
    import os
    os.remove("config.plist")
    del os
    import ConfigManager
    global Config
    Config = ConfigManager.Config
    
def teardown_config():
    global Config
    Config = None

@with_setup(setup_config_first, teardown_config)
def test_config_load_config():
    c = Config()
    c.load_config()
    
@with_setup(setup_config, teardown_config) 
def test_config_save_config():
    c = Config()
    c.save_config()

@with_setup(setup_config, teardown_config)
def test_config_set_value():
    c = Config()
    c.set_value("editor.font.size", 13)

@with_setup(setup_config, teardown_config)
def test_config_get_value():
    c = Config()
    assert c.get_value("editor.font.size") == 13
