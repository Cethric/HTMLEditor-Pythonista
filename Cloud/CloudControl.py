import os
import webbrowser
from dropbox import client, rest, session
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import onedrive.api_v5 as onedrive
import keychain
try:
    import cPickle as pickle
except ImportError:
    print "cPickle is not available, using standard pickle module."
    import pickle
try:
    import ui
    import console
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
    import dummyConsole as console

KEYS = []
with open("security_keys", "rb") as f:
    KEYS = f.read().split("\n")


def print_dict(d):
    print "#" * 20
    for k, v in d.iteritems():
        print "%s:\t\t\t%s" % (k, v)
    print "#" * 20


class BaseConnection(object):

    def __init__(self, auto_connect=True, *args, **kwargs):
        self.api = None
        if auto_connect:
            self.connect()

    def connect(self):
        raise NotImplementedError("this function is not set up.")

    def read(self, file_name_path):
        raise NotImplementedError("this function is not set up.")

    def write(self, file_name_path, contents):
        raise NotImplementedError("this function is not set up.")

    def mk_dir(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def move(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def copy(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def delete(self, file_folder):
        raise NotImplementedError("this function is not set up.")

    def list_dir(self, dir):
        raise NotImplementedError("this function is not set up")

    def get_quota(self):
        raise NotImplementedError("this function is not set up.")

    def get_user_info(self):
        raise NotImplementedError("this function is not set up.")


# Main Functions Created by
# https://gist.githubusercontent.com/omz/4034526
class DropBoxConection(BaseConnection):

    def __init__(self, *args, **kwargs):
        self.app_key = KEYS[0]
        self.app_secret = KEYS[1]
        self.access_type = 'dropbox'
        BaseConnection.__init__(self, *args, **kwargs)

    def connect(self):
        print "Establishing a Connection"
        self.access_token = self._get_access_token()
        sess = session.DropboxSession(
            self.app_key, self.app_secret, self.access_type)
        sess.set_token(self.access_token.key, self.access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        self.api = dropbox_client

    def get_user_info(self):
        print self.api
        info = self.api.account_info()
        return {
            "username": info["display_name"],
            "email": info["email"],
        }

    def get_quota(self):
        return "%.3fGB" % (float(self.api.account_info()[u'quota_info'][u'quota']) / (1024 * 1024 * 1024))

    def _get_request_token(self):
        console.clear()
        print 'Getting request token...'
        sess = session.DropboxSession(
            self.app_key, self.app_secret, self.access_type)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        console.clear()
        v = ui.WebView()
        v.load_url(url)
        v.present()
        v.wait_modal()
        return request_token

    def _get_access_token(self):
        token_str = keychain.get_password('dropbox', self.app_key)
        if token_str:
            key, secret = pickle.loads(token_str)
            return session.OAuthToken(key, secret)
        request_token = self._get_request_token()
        sess = session.DropboxSession(
            self.app_key, self.app_secret, self.access_type)
        access_token = sess.obtain_access_token(request_token)
        token_str = pickle.dumps((access_token.key, access_token.secret))
        keychain.set_password('dropbox', self.app_key, token_str)
        return access_token

    def read(self, file_name_path):
        return self.api.get_file_and_metadata(file_name_path)[0].read()

    def write(self, file_name_path, contents):
        return self.api.put_file(file_name_path, contents)

    def list_dir(self, dir):
        return self.api.metadata(dir)["contents"]

    def move(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def copy(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def delete(self, file_folder):
        raise NotImplementedError("this function is not set up.")


class OneDriveConnection(BaseConnection):

    def __init__(self, *args, **kwargs):
        self.app_key = KEYS[3]
        self.app_secret = KEYS[4]
        BaseConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.api = onedrive.OneDriveAPI(
            client_id=self.app_key, client_secret=self.app_secret)
        token_str = keychain.get_password('onedrive', self.app_key)
        if token_str:
            at, ac, ar = pickle.loads(token_str)
            self.api.auth_access_token = at
            self.api.auth_refresh_token = ar
            self.auth_code = ac
            self.api.auth_get_token()
        else:
            request_token = self._get_request_token()
            self.api.auth_user_process_url(request_token)
            self.api.auth_get_token()
            keychain.set_password('onedrive', self.app_key, pickle.dumps(
                (self.api.auth_access_token, self.api.auth_code, self.api.auth_refresh_token)))

    def _get_request_token(self):
        console.clear()
        print 'Getting request token...'
        url = self.api.auth_user_get_url()
        console.clear()
        wv = ui.WebView()
        wv.load_url(url)
        wv.present()
        wv.wait_modal()
        purl = str(wv.eval_js("window.location.href"))
        return purl

    def get_client(self):
        self.access_token = self.get_access_token()
        sess = session.DropboxSession(
            self.app_key, self.app_secret, self.access_type)
        sess.set_token(self.access_token.key, self.access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        return dropbox_client

    def read(self, file_name_path):
        p = self.api.resolve_path(file_name_path)
        c = self.api.get(p)
        return c

    def write(self, file_name_path, contents):
        with open("tmp-dfile.tmp", "wb") as f:
            f.write(contents)

        path = file_name_path
        c = self.api.put((path, open("tmp-dfile.tmp", "rb")))
        print c

    def move(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def copy(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def delete(self, file_folder):
        raise NotImplementedError("this function is not set up.")

    def list_dir(self, dir):
        raise NotImplementedError("this function is not set up")

    def get_quota(self):
        raise NotImplementedError("this function is not set up.")

    def get_user_info(self):
        raise NotImplementedError("this function is not set up.")


class GoogleDriveConnections(BaseConnection):

    def __init__(self, *args, **kwargs):
        self.file_ids = {}
        BaseConnection.__init__(self, *args, **kwargs)

    def connect(self):
        gauth = GoogleAuth("settings.yaml")
        try:
            gauth.LocalWebserverAuth()
        except Exception as e:
            print e
            import traceback
            traceback.print_exc()
        self.api = drive = GoogleDrive(gauth)
        print "Connected to GoogleDrive"
        print "API OBJECT %r" % drive
        self._list_dir("root")
        print "ID List updated"

    def read(self, file_name_path):
        if os.path.basename(file_name_path) in self.file_ids:
            data = self.file_ids[os.path.basename(file_name_path)]
            if data[0] == "FILE":
                file = self.api.CreateFile({"id": data[1]})
                return file.GetContentString()
            else:
                print "Cannot read directory as string"
        else:
            print "File not found"

    def write(self, file_name_path, contents):
        file = self.api.CreateFile(
            {"title": os.path.basename(file_name_path), "mimeType": "text/plain"})
        file.SetContentString(contents)
        file.Upload()
        self.file_ids[file["title"]] = ["FILE", file["id"]]
        return file

    def mk_dir(self, path):
        file = self.api.CreateFile(
            {"title": path, "mimeType": "application/vnd.google-apps.folder"})
        file.Upload()
        self.file_ids[file["title"]] = ["FILE", file["id"]]
        return file

    def move(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def copy(self, src, dst):
        raise NotImplementedError("this function is not set up.")

    def delete(self, file_folder):
        raise NotImplementedError("this function is not set up.")

    def list_dir(self, dir):
        self._list_dir(dir)
        return self.file_ids

    def _list_dir(self, parent):
        file_list = self.api.ListFile(
            {'maxResults': 200, "q": "'%s' in parents" % parent}).GetList()
        for file in file_list:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                self.file_ids[file["title"]] = ["FOLDER", file["id"]]
                # self._list_dir(file["id"])
            else:
                self.file_ids[file["title"]] = ["FILE", file["id"]]

    def get_quota(self):
        raise NotImplementedError("this function is not set up.")

    def get_user_info(self):
        raise NotImplementedError("this function is not set up.")

if __name__ == '__main__':
    # keychain.reset_keychain()
    #db = DropBoxConection(True)
    # print len(db.list_dir("/"))
    # print db.write("/test.txt", "hello world this is a test")
    # print db.read("/test.txt")

    #od = OneDriveConnection()
    #od.write("test.txt", "hello world this is a test")
    # od.read("test.txt")

    gd = GoogleDriveConnections()
    # print "File Write"
    #gd.write("test2.txt", "hello world this is a test")
    print "File Read"
    print gd.read("test.txt")
    # print "MK DIR"
    # print_dict(gd.mk_dir("test"))
    print "List Dir"
    print_dict(gd.list_dir(u'0B51dU3wCnjZ8Y1p6REFkaTVsekE'))
