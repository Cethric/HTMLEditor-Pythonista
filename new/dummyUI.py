

class View(object):
    def __init__(self, *args, **kwargs):
        print "Initializing view %r" % self
        print "Args: %r" % list(args)
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)

    def present(self, *args, **kwargs):
        print "Presenting view %r" % self
        print "Args: %r" % args
        for k, v in kwargs.items():
            print "Key: %r\t\tValue: %r" % (k, v)


def load_view(ui_view_name):
    return View()