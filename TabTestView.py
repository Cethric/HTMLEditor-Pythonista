import console, ui

class TabTestView(ui.View):
    def __init__(self):
        self.textview = ui.TextView()
        self.textview.text = '\n'.join('{}{}'.format('\t' * i, i) for i in xrange(10))
        self.add_subview(self.textview)
        self.right_button_items = [ui.ButtonItem(action=self.button_action, image=ui.Image.named("ionicons-hammer-24"))]
        self.present()
        self.textview.frame = self.bounds

    def button_action(self, sender):
        self.get_current_line_tab(self.textview)

    def get_current_line_tab(self, textview):
        text, selection = textview.text, textview.selected_range
        print(selection)
        try:
            ctext = text[selection[0] - 1 : selection[1] - 1]
            print('ctext', ctext)
            x = selection[1] - 1
            while True:
                c = text[x]
                if c != "\n":
                    ctext += c
                    x += 1
                else:
                    break
            x = selection[0] - 1
            try:
                while True:
                    c = text[x]
                    if c != "\n" and c != 0:
                        ctext = c + ctext
                        x -= 1
                    else:
                        break
            except:
                pass
            print "%r" % ctext
            tabs = ctext.count("\t")
            print tabs
            should_remove_one = True
            for x in ctext:
                if x != "\t":
                    should_remove_one = False
            if should_remove_one:
                tabs -= 1
        except:
            tabs = 0
        console.hud_alert('tabs: {}'.format(tabs))
        self.tab_num = tabs

print('=' * 25)
TabTestView()
