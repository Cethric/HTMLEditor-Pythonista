# coding: utf-8

import ui


def info(sender):
    print "info"
    
class Delegate (object):
    def tableview_did_select(self, tableview, section, row):
        print "did selected"
        tag = tableview.data_source.tableview_cell_for_row(tableview, section, row).text_label.text
        result = "<%s> data </%s>" % (tag, tag)
        print result
    


view = ui.load_view("HTML_Tools")
view["insert_tag"].delegate = Delegate()

view.present("sheet")
