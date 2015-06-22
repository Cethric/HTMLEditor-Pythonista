import webbrowser
from dropbox import client, rest, session
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

import onedrive.api_v5 as onedrive

KEYS = []
with open("security_keys", "rb") as f:
    KEYS = f.read().split("\n")
    
class BaseConnection(object):
    def __init__(self):
        pass
        
    def connect(self):
        raise NotImplementedError("this function is not set up.")
        
    def read(file_name_path):
        raise NotImplementedError("this function is not set up.")
        
    def write(file_name_path, contents):
        raise NotImplementedError("this function is not set up.")
        
    def move(self, src, dst):
        raise NotImplementedError("this function is not set up.")
        
    def copy(self, src, dst):
        raise NotImplementedError("this function is not set up.")
        
    def delete(self, file_folder):
        raise NotImplementedError("this function is not set up.")
    
    def get_quota(self):
        raise NotImplementedError("this function is not set up.")
    
    def get_user_info(self):
        raise NotImplementedError("this function is not set up.")


# Main Functions Created by
# https://gist.githubusercontent.com/omz/4034526
class DropBoxConection(BaseConnection):
    app_key = KEYS[0]
    app_secret = KEYS[1]
    access_type = 'dropbox'
    
    def __init__(self):
        super(BaseConnection, self).__init__()
        print 'Getting account info...'
        dropbox_client = self.get_client()
        account_info = dropbox_client.account_info()
        print 'linked account:', account_info
    
    def get_request_token(self):
        console.clear()
        print 'Getting request token...'
        sess = session.DropboxSession(self.app_key, self.app_secret, self.access_type)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        console.clear()
        v = ui.WebView()
        v.open_url(url)
        v.present()
        v.wait_modal()
        webbrowser.open(url, modal=True)
        
        return request_token
    
    def get_access_token(self):
        token_str = keychain.get_password('dropbox', self.app_key)
        if token_str:
            key, secret = pickle.loads(token_str)
            return session.OAuthToken(key, secret)
        request_token = self.get_request_token()
        sess = session.DropboxSession(self.app_key, self.app_secret, self.access_type)
        access_token = sess.obtain_access_token(request_token)
        token_str = pickle.dumps((access_token.key, access_token.secret))
        keychain.set_password('dropbox', self.app_key, token_str)
        return access_token
    
    def get_client(self):
        self.access_token = self.get_access_token()
        sess = session.DropboxSession(self.app_key, self.app_secret, self.access_type)
        sess.set_token(self.access_token.key, self.access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        return dropbox_client

class OneDriveConnection(BaseConnection):
    app_key = KEYS[3]
    app_secret = KEYS[4]
    def __init__(self):
        super(BaseConnection, self).__init__()
        self.api = onedrive.OneDriveAPI(client_id=self.app_key, client_secret=self.app_secret)
        self.get_access_token()
        
    def get_request_token(self):
        console.clear()
        print 'Getting request token...'
        url = self.api.auth_user_get_url()
        console.clear()
        #webbrowser.open(url, modal=True)
        wv = ui.WebView()
        wv.load_url(url)
        wv.present()
        wv.wait_modal()
        purl = str(wv.eval_js("window.location.href"))
        print purl
        return purl
        
    def auth(self, token):
        self.api.auth_user_process_url(token)
        self.api.auth_get_token()
        
    def get_access_token(self):
        token_str = keychain.get_password('onedrive', self.app_key)
        if token_str:
            print "%r" % str(token_str)
            self.auth(token_str)
        else:
            request_token = self.get_request_token()
            print "%r" % request_token
            self.auth(request_token)
            keychain.set_password('onedrive', self.app_key, request_token)
        #return access_token
        
    def get_client(self):
        self.access_token = self.get_access_token()
        sess = session.DropboxSession(self.app_key, self.app_secret, self.access_type)
        sess.set_token(self.access_token.key, self.access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        return dropbox_client
        
if __name__ == '__main__':
    #keychain.reset_keychain()
    #db = DropBoxConection()
    od = OneDriveConnection()
