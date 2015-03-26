

class View(object):
    def __init__(self):
        pass

    def present(self, *args, **kwargs):
        print "Presenting view %r" % self
        print "Args: %r" % args
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)