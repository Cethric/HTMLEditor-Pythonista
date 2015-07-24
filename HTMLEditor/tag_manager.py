try:
    import ui
except ImportError:
    print "Using Dummy UI"
    import dummyUI as ui
import json


OPTION_FIELD_TEXT = 0x01
OPTION_FIELD_DROPDOWN = 0x02
OPTION_FIELD_NUMBER = 0x04
OPTION_FIELD_NONE = 0x08

class OptionField(ui.View):
    def __init__(self,
                 input_type=OPTION_FIELD_TEXT,
                 placeholder="",
                 description="",
                 html5compat=False,
                 *args, **kwargs):
        ui.View.__init__(self, *args, **kwargs)

GLOBAL_HTML_ATTR = {
                    "accesskey":ui.TextField(),
                    "class":ui.TextField(),
                    "cententeditable":ui.TextField(),
                    "contextmenu":ui.TextField(),
                    "dir":ui.TextField(),
                    "draggable":ui.TextField(),
                    "dropzone":ui.TextField(),
                    "hidden":ui.TextField(),
                    "id":ui.TextField(),
                    "lang":ui.TextField(),
                    "spellcheck":ui.TextField(),
                    "style":ui.TextField(),
                    "tabindex":ui.TextField(),
                    "title":ui.TextField(),
                    "translate":ui.TextField(),
                    "name":ui.TextField(),
                    }
                    
MISC_HTML_ATTR = {
                  "newlinechar":ui.TextField(),
                  }

WINDOW_EVENTS = {
                 "onafterprint":ui.TextField(),
                 "onbeforeprint":ui.TextField(),
                 "onbeforeunload":ui.TextField(),
                 "onerror":ui.TextField(),
                 "onhashchange":ui.TextField(),
                 "onload":ui.TextField(),
                 "onmessage":ui.TextField(),
                 "onoffline":ui.TextField(),
                 "ononline":ui.TextField(),
                 "onpagehide":ui.TextField(),
                 "onpageshow":ui.TextField(),
                 "onpopstate":ui.TextField(),
                 "onresize":ui.TextField(),
                 "onstorage":ui.TextField(),
                 "onunload":ui.TextField(),
                 }
                 
FORM_EVENTS = {
               "onblur":ui.TextField(),
               "onchange":ui.TextField(),
               "oncontextmenu":ui.TextField(),
               "onfocus":ui.TextField(),
               "oninput":ui.TextField(),
               "oninvalid":ui.TextField(),
               "onreset":ui.TextField(),
               "onsearch":ui.TextField(),
               "onselect":ui.TextField(),
               "onsubmit":ui.TextField(),
               }
               
KEYBOARD_EVENTS = {
                   "onkeydown":ui.TextField(),
                   "onkeypress":ui.TextField(),
                   "onkeyup":ui.TextField(),
                   }
                   
MOUSE_EVENTS = {
                "onclick":ui.TextField(),
                "ondblclick":ui.TextField(),
                "ondrag":ui.TextField(),
                "ondragend":ui.TextField(),
                "ondragenter":ui.TextField(),
                "ondragleave":ui.TextField(),
                "ondragover":ui.TextField(),
                "ondragstart":ui.TextField(),
                "ondrop":ui.TextField(),
                "onmousedown":ui.TextField(),
                "onmousemove":ui.TextField(),
                "onmouseout":ui.TextField(),
                "onmouseover":ui.TextField(),
                "onmouseup":ui.TextField(),
                "onmousewheel":ui.TextField(),
                "onscroll":ui.TextField(),
                "onwheel":ui.TextField(),
                }
                
CLIPBOARD_EVENTS = {
                    "oncopy":ui.TextField(),
                    "oncut":ui.TextField(),
                    "onpaste":ui.TextField(),
                    }

MEDIA_EVENTS = {
                "onabord":ui.TextField(),
                "oncanplay":ui.TextField(),
                "oncanplaythrough":ui.TextField(),
                "oncuechange":ui.TextField(),
                "onduraionchange":ui.TextField(),
                "onemptied":ui.TextField(),
                "onended":ui.TextField(),
                "onerror":ui.TextField(),
                "onloadeddata":ui.TextField(),
                "onloadedmetadata":ui.TextField(),
                "onloadstart":ui.TextField(),
                "onpause":ui.TextField(),
                "onplay":ui.TextField(),
                "onplaying":ui.TextField(),
                "onprogress":ui.TextField(),
                "onratechange":ui.TextField(),
                "onseeked":ui.TextField(),
                "onseeking":ui.TextField(),
                "onstalled":ui.TextField(),
                "onsuspend":ui.TextField(),
                "ontimeupdate":ui.TextField(),
                "onvolumechange":ui.TextField(),
                "onwaiting":ui.TextField(),
                }

MISC_EVENTS = {
               "onerror":ui.TextField(),
               "onshow":ui.TextField(),
               "ontoggle":ui.TextField(),
               }

TAGS = [
        {"title": "anchor",
         "options": {
                         "tag-open":"a",
                         "tag-close":"a",
                         "content":ui.TextField(),
                         "charset":ui.TextField(),
                         "coords":ui.TextField(),
                         "download":ui.TextField(),
                         "href":ui.TextField(),
                         "hreflang":ui.TextField(),
                         "media":ui.TextField(),
                         "rel":ui.TextField(),
                         "rev":ui.TextField(),
                         "shape":ui.TextField(),
                         "target":ui.TextField(),
                         "type":ui.TextField(),
                         }},
        {"title":"abbreviation",
         "options": {
                          "tag-open":"abbr",
                          "tag-close":"abbr",
                          "content":ui.TextField(),
                          }},
        {"title":"acronym - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"acronym",
                          "tag-close":"acronym",
                          "contents":ui.TextField(),
                          }},
        {"title":"address",
         "options": {
                          "tag-open":"address",
                          "tag-close":"address",
                          "content":ui.TextView(),
                          }},
        {"title":"applet - (Not Avaliable in HTML5)",
         "options": {
                    "tag-open":"applet",
                    "tag-close":"applet",
                    "content":"",
                    "code":ui.TextField(),
                    "object":ui.TextField(),
                    "align":ui.TextField(),
                    "alt":ui.TextField(),
                    "archive":ui.TextField(),
                    "codebase":ui.TextField(),
                    "height":ui.TextField(),
                    "hspace":ui.TextField(),
                    "vspace":ui.TextField(),
                    "width":ui.TextField(),
                    }},
        {"title":"area",
         "options": {
                          "tag-open":"area",
                          "tag-close":"area",
                          "alt":ui.TextField(),
                          "coords":ui.TextField(),
                          "download":ui.TextField(),
                          "href":ui.TextField(),
                          "hreflang":ui.TextField(),
                          "media":ui.TextField(),
                          "nohref":ui.TextField(),
                          "rel":ui.TextField(),
                          "shape":ui.TextField(),
                          "target":ui.TextField(),
                          "type":ui.TextField(),
                          }},
        {"title":"article",
         "options": {
                          "tag-open":"article",
                          "tag-close":"article",
                          "content":ui.TextView(),
                          }},
        {"title":"aside",
         "options": {
                          "tag-open":"aside",
                          "tag-close":"aside",
                          "content":ui.TextView()
                          }},
        {"title":"audio",
         "options": {
                          "tag-open":"audio",
                          "tag-close":"audio",
                          "content":ui.TextField(),
                          "preload":ui.TextField(),
                          "src":ui.TextField(),
                          }},
        {"title":"bold",
         "options": {
                          "tag-open":"b",
                          "tag-close":"b",
                          "content":ui.TextView(),
                          }},
        {"title":"base",
         "options": {
                          "tag-open":"base",
                          "tag-close":"base",
                          "href":ui.TextField(),
                          "target":ui.TextField(),
                          "content":"",
                          }},
        {"title":"basefont - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"basefont",
                          "tag-close":"basefont",
                          "content":"",
                          "color":ui.TextField(),
                          "face":ui.TextField(),
                          "size":ui.TextField(),
                          }},
        {"title":"Bi-directional Isolation",
         "options": {
                          "tag-open":"bdi",
                          "tag-close":"bdi",
                          "content":ui.TextView(),
                          }},
        {"title":"Bi-directional Override",
         "options": {
                          "tag-open":"bdo",
                          "tag-close":"bdo",
                          "content":ui.TextView(),
                          "dir":ui.TextField(),
                          }},
        {"title":"big - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"big",
                          "tag-close":"big",
                          "content":ui.TextView(),
                          }},
        {"title":"blockquote",
         "options": {
                          "tag-open":"blockquote",
                          "tag-close":"blockquote",
                          "content":ui.TextView(),
                          "cite":ui.TextField(),
                          }},
        {"title":"body",
         "options": {
                          "tag-open":"body",
                          "tag-close":"body",
                          "content":ui.TextView(),
                          "alink":ui.TextField(),
                          "background":ui.TextField(),
                          "bgcolor":ui.TextField(),
                          "link":ui.TextField(),
                          "text":ui.TextField(),
                          "vlink":ui.TextField(),
                          }},
        {"title":"line break",
         "options": {
                          "tag-open":"br",
                          "tag-close":"br",
                          "content":ui.TextView(),
                          }},
        {"title":"button",
         "options": {
                          "tag-open":"button",
                          "tag-close":"button",
                          "content":ui.TextField(),
                          "autofocus":ui.TextField(),
                          "disabled":ui.TextField(),
                          "form":ui.TextField(),
                          "formaction":ui.TextField(),
                          "formenctype":ui.TextField(),
                          "formmethod":ui.TextField(),
                          "formnovalidate":ui.TextField(),
                          "formtarget":ui.TextField(),
                          "name":ui.TextField(),
                          "type":ui.TextField(),
                          "value":ui.TextField(),
                          }},
        {"title":"canvas",
         "options": {
                          "tag-open":"canvas",
                          "tag-close":"canvas",
                          "content":ui.TextField(),
                          "height":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"caption",
         "options": {
                          "tag-open":"caption",
                          "tag-close":"caption",
                          "content":ui.TextView(),
                          "align":ui.TextField(),
                          }},
        {"title":"center",
         "options": {
                          "tag-open":"center",
                          "tag-close":"center",
                          "content":ui.TextField(),
                          }},
        {"title":"cite",
         "options": {
                          "tag-open":"cite",
                          "tag-close":"cite",
                          "content":ui.TextField(),
                          }},
        {"title":"code - (CSS Provides Richer Effects)",
         "options": {
                          "tag-open":"code",
                          "tag-close":"code",
                          "content":ui.TextView(),
                          }},
        {"title":"col",
         "options": {
                          "tag-open":"col",
                          "align":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "span":ui.TextField(),
                          "valign":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"colgroup",
         "options": {
                          "tag-open":"colgroup",
                          "tag-close":"colgroup",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "span":ui.TextField(),
                          "valign":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"datalist",
         "options": {
                          "tag-open":"datalist",
                          "tag-close":"datalist",
                          "content":ui.TextView(),
                          }},
        {"title":"Description (dd)",
         "options": {
                          "tag-open":"dd",
                          "tag-close":"dd",
                          "content":ui.TextView(),
                          }},
        {"title":"delete (del)",
         "options": {
                          "tag-open":"del",
                          "tag-close":"del",
                          "content":ui.TextView(),
                          "cite":ui.TextField(),
                          "datetime":ui.TextField(),
                          }},
        {"title":"details",
         "options": {
                          "tag-open":"details",
                          "tag-close":"details",
                          "content":ui.TextView(),
                          "open":ui.TextField(),
                          }},
        {"title":"definition (dfn)",
         "options": {
                          "tag-open":"dfn",
                          "tag-close":"dfn",
                          "content":ui.TextField(),
                          }},
        {"title":"dialog",
         "options": {
                          "tag-open":"dialog",
                          "tag-close":"dialog",
                          "content":ui.TextView(),
                          "open":ui.TextField(),
                          }},
        {"title":"dir - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"dir",
                          "tag-close":"dir",
                          "content":ui.TextField(),
                          "compact":ui.TextField(),
                          }},
        {"title":"div",
         "options": {
                          "tag-open":"div",
                          "tag-close":"div",
                          "content":ui.TextView(),
                          "align":ui.TextField(),
                          }},
        {"title":"description list (dl)",
         "options": {
                          "tag-open":"dl",
                          "tag-close":"dl",
                          "content":ui.TextField(),
                          }},
        {"title":"description term (dt)",
         "options": {
                          "tag-open":"dt",
                          "tag-close":"dt",
                          "content":ui.TextField(),
                          }},
        {"title":"emphasis - em (Richer effects attained with CSS)",
         "options": {
                          "tag-open":"em",
                          "tag-close":"em",
                          "content":ui.TextField(),
                          }},
        {"title":"embed",
         "options": {
                          "tag-open":"embed",
                          "tag-close":"embed",
                          "content":ui.TextField(),
                          "height":ui.TextField(),
                          "src":ui.TextField(),
                          "type":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"fieldset",
         "options": {
                          "tag-open":"fieldset",
                          "tag-close":"fieldset",
                          "content":ui.TextView(),
                          "disabled":ui.TextField(),
                          "form_id":ui.TextField(),
                          }},
        {"title":"figcaption",
         "options": {
                          "tag-open":"figcaption",
                          "tag-close":"figcaption",
                          "content":ui.TextField(),
        
                          }},
        {"title":"figure",
         "options": {
                          "tag-open":"figure",
                          "tag-close":"figure",
                          "content":ui.TextField(),
        
                          }},
        {"title":"font - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"font",
                          "tag-close":"font",
                          "content":ui.TextField(),
                          "color":ui.TextField(),
                          "face":ui.TextField(),
                          "size":ui.TextField(),
                          }},
        {"title":"footer",
         "options": {
                          "tag-open":"footer",
                          "tag-close":"footer",
                          "content":ui.TextField(),
                          }},
        {"title":"form",
         "options": {
                          "tag-open":"form",
                          "tag-close":"form",
                          "content":ui.TextView(),
                          "accept":ui.TextField(),
                          "accept-charset":ui.TextField(),
                          "action":ui.TextField(),
                          "autocomplete":ui.TextField(),
                          "enctype":ui.TextField(),
                          "method":ui.TextField(),
                          "novalidate":ui.TextField(),
                          "target":ui.TextField(),
                          }},
        {"title":"frame - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"frame",
                          "tag-close":"frame",
                          "content":ui.TextField(),
                          "frameborder":ui.TextField(),
                          "longdesc":ui.TextField(),
                          "marginheight":ui.TextField(),
                          "marginwidth":ui.TextField(),
                          "noresize":ui.TextField(),
                          "scrolling":ui.TextField(),
                          "src":ui.TextField(),
                          }},
        {"title":"frameset - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"frameset",
                          "tag-close":"frameset",
                          "content":ui.TextField(),
                          "cols":ui.TextField(),
                          "rows":ui.TextField(),
                          }},
        {"title":"heading 1",
         "options": {
                          "tag-open":"h1",
                          "tag-close":"h1",
                          "conent":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"heading 2",
         "options": {
                          "tag-open":"h2",
                          "tag-close":"h2",
                          "conent":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"heading 3",
         "options": {
                          "tag-open":"h3",
                          "tag-close":"h3",
                          "conent":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"heading 4",
         "options": {
                          "tag-open":"h4",
                          "tag-close":"h4",
                          "conent":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"heading 5",
         "options": {
                          "tag-open":"h5",
                          "tag-close":"h5",
                          "conent":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"heading 6",
         "options": {
                          "tag-open":"h6",
                          "tag-close":"h6",
                          "conent":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"head",
         "options": {
                          "tag-open":"head",
                          "tag-close":"head",
                          "content":ui.TextField(),
                          "profile":ui.TextField(),
                          }},
        {"title":"header",
         "options": {
                          "tag-open":"header",
                          "tag-close":"header",
                          "content":ui.TextView(),
        
                          }},
        {"title":"hr",
         "options": {
                          "tag-open":"hr",
                          "align":ui.TextField(),
                          "noshade":ui.TextField(),
                          "size":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"html",
         "options": {
                          "tag-open":"html",
                          "tag-close":"html",
                          "content":ui.TextField(),
                          "manifest":ui.TextField(),
                          "xmlns":ui.TextField(),
                          }},
        {"title":"i",
         "options": {
                          "tag-open":"i",
                          "tag-close":"i",
                          "content":ui.TextField(),
                          }},
        {"title":"iframe",
         "options": {
                          "tag-open":"iframe",
                          "tag-close":"iframe",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "frameborder":ui.TextView(),
                          "height":ui.TextField(),
                          "longdesc":ui.TextField(),
                          "marginheight":ui.TextField(),
                          "marginwidth":ui.TextField(),
                          "sandbox":ui.TextField(),
                          "scrolling":ui.TextField(),
                          "seamless":ui.TextField(),
                          "src":ui.TextField(),
                          "srcdoc":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"image",
         "options": {
                          "tag-open":"img",
                          "tag-close":"img",
                          "content":"",
                          "align":ui.TextField(),
                          "alt":ui.TextField(),
                          "border":ui.TextField(),
                          "crossorigin":ui.TextField(),
                          "height":ui.TextField(),
                          "hspace":ui.TextField(),
                          "ismap":ui.TextField(),
                          "longdesc":ui.TextField(),
                          "src":ui.TextField(),
                          "usemap":ui.TextField(),
                          "vspace":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"input",
         "options": {
                          "tag-open":"input",
                          "accept":ui.TextField(),
                          "align":ui.TextField(),
                          "alt":ui.TextField(),
                          "autocomplete":ui.TextField(),
                          "autofocus":ui.TextField(),
                          "checked":ui.TextField(),
                          "disabled":ui.TextField(),
                          "form":ui.TextField(),
                          "formaction":ui.TextField(),
                          "formmethod":ui.TextField(),
                          "formnovalidate":ui.TextField(),
                          "formtarget":ui.TextField(),
                          "height":ui.TextField(),
                          "list":ui.TextField(),
                          "max":ui.TextField(),
                          "maxlength":ui.TextField(),
                          "min":ui.TextField(),
                          "multiple":ui.TextField(),
                          "pattern":ui.TextField(),
                          "placeholder":ui.TextField(),
                          "readonly":ui.TextField(),
                          "required":ui.TextField(),
                          "size":ui.TextField(),
                          "src":ui.TextField(),
                          "step":ui.TextField(),
                          "type":ui.TextField(),
                          "value":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"insert - (ins)",
         "options": {
                          "tag-open":"ins",
                          "tag-close":"ins",
                          "content":ui.TextField(),
                          "cite":ui.TextField(),
                          "datetime":ui.TextField(),
                          }},
        {"title":"keyboard (kbd)",
         "options": {
                          "tag-open":"kbd",
                          "tag-close":"kbd",
                          "content":ui.TextField(),
                          }},
        {"title":"keygen",
         "options": {
                          "tag-open":"keygen",
                          "autofocus":ui.TextField(),
                          "challenge":ui.TextField(),
                          "disabled":ui.TextField(),
                          "form":ui.TextField(),
                          "keytype":ui.TextField(),
                          }},
        {"title":"label",
         "options": {
                          "tag-open":"label",
                          "tag-close":"label",
                          "content":ui.TextField(),
                          "for":ui.TextField(),
                          "form":ui.TextField(),
                          }},
        {"title":"legend",
         "options": {
                          "tag-open":"legend",
                          "tag-close":"legend",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          }},
        {"title":"list item (li)",
         "options": {
                          "tag-open":"li",
                          "tag-close":"li",
                          "content":ui.TextField(),
                          "type":ui.TextField(),
                          "value":ui.TextField(),
                          }},
        {"title":"link",
         "options": {
                     "tag-open":"link",
                     "charset":ui.TextField(),
                     "crossorigin":ui.TextField(),
                     "href":ui.TextField(),
                     "hreflang":ui.TextField(),
                     "media":ui.TextField(),
                     "rel":ui.TextField(),
                     "rev":ui.TextField(),
                     "sizes":ui.TextField(),
                     "target":ui.TextField(),
                     "type":ui.TextField(),
                     }},
        {"title":"main",
         "options": {
                          "tag-open":"main",
                          "tag-close":"main",
                          "content":ui.TextField(),
                          }},
        {"title":"map",
         "options": {
                          "tag-open":"map",
                          "tag-close":"map",
                          "content":ui.TextField(),
                          }},
        {"title":"mark",
         "options": {
                          "tag-open":"mark",
                          "tag-close":"mark",
                          "content":ui.TextField(),
                          }},
        {"title":"menu",
         "options": {
                          "tag-open":"menu",
                          "tag-close":"menu",
                          "content":ui.TextField(),
                          "label":ui.TextField(),
                          "type":ui.TextField(),
                          }},
        {"title":"menuitem",
         "options": {
                          "tag-open":"menuitem",
                          "tag-close":"menuitem",
                          "content":ui.TextField(),
                          "checked":ui.TextField(),
                          "command":ui.TextField(),
                          "default":ui.TextField(),
                          "disable":ui.TextField(),
                          "icon":ui.TextField(),
                          "label":ui.TextField(),
                          "radiogroup":ui.TextField(),
                          "type":ui.TextField(),
                          }},
        {"title":"metadata",
         "options": {
                          "tag-open":"meta",
                          "tag-close":"meta",
                          "content":ui.TextField(),
                          "charset":ui.TextField(),
                          "http-equiv":ui.TextField(),
                          "scheme":ui.TextField(),
                          }},
        {"title":"meter",
         "options": {
                          "tag-open":"meter",
                          "tag-close":"meter",
                          "content":ui.TextField(),
                          "form":ui.TextField(),
                          "high":ui.TextField(),
                          "low":ui.TextField(),
                          "max":ui.TextField(),
                          "min":ui.TextField(),
                          "optimum":ui.TextField(),
                          "value":ui.TextField(),
                          }},
        {"title":"navigation block - (nav)",
         "options": {
                          "tag-open":"nav",
                          "tag-close":"nav",
                          "content":ui.TextField(),
                          }},
        {"title":"noframes - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"noframes",
                          "tag-close":"noframes",
                          "content":ui.TextField(),
                          }},
        {"title":"noscript",
         "options": {
                          "tag-open":"noscript",
                          "tag-close":"noscript",
                          "content":ui.TextField(),
                          }},
        {"title":"object",
         "options": {
                          "tag-open":"object",
                          "tag-close":"object",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "archive":ui.TextField(),
                          "border":ui.TextField(),
                          "classid":ui.TextField(),
                          "codebase":ui.TextField(),
                          "codetype":ui.TextField(),
                          "data":ui.TextField(),
                          "declare":ui.TextField(),
                          "form":ui.TextField(),
                          "height":ui.TextField(),
                          "hspace":ui.TextField(),
                          "standby":ui.TextField(),
                          "type":ui.TextField(),
                          "usemap":ui.TextField(),
                          "vspace":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"ordered list (ol)",
         "options": {
                          "tag-open":"ol",
                          "tag-close":"ol",
                          "content":ui.TextField(),
                          "compact":ui.TextField(),
                          "reversed":ui.TextField(),
                          "start":ui.TextField(),
                          "type":ui.TextField(),
                          }},
        {"title":"option group (optgroup)",
         "options": {
                          "tag-open":"optgroup",
                          "tag-close":"optgroup",
                          "content":ui.TextView(),
                          "disabled":ui.TextField(),
                          "label":ui.TextField(),
                          }},
        {"title":"option",
         "options": {
                          "tag-open":"option",
                          "tag-close":"option",
                          "content":ui.TextField(),
                          "disabled":ui.TextField(),
                          "label":ui.TextField(),
                          "selected":ui.TextField(),
                          "value":ui.TextField(),
                          }},
        {"title":"output",
         "options": {
                          "tag-open":"output",
                          "tag-close":"output",
                          "content":ui.TextField(),
                          "for":ui.TextField(),
                          "form":ui.TextField(),
                          }},
        {"title":"paragraph",
         "options": {
                     "tag-open":"p",
                     "tag-close":"p",
                     "content":ui.TextView(),
                     "align":ui.TextField(),
                     }},
        {"title":"parameter (param)",
         "options": {
                          "tag-open":"param",
                          "type":ui.TextField(),
                          "value":ui.TextField(),
                          "valuetype":ui.TextField(),
                          }},
        {"title":"preformatted text",
         "options": {
                          "tag-open":"pre",
                          "tag-close":"pre",
                          "content":ui.TextView(),
                          "width":ui.TextField(),
                          }},
        {"title":"progress",
         "options": {
                          "tag-open":"progress",
                          "tag-close":"progress",
                          "content":ui.TextField(),
                          "max":ui.TextField(),
                          "value":ui.TextField(),
                          }},
        {"title":"quotation (q)",
         "options": {
                          "tag-open":"q",
                          "tag-close":"q",
                          "content":ui.TextField(),
                          "cite":ui.TextField(),
                          }},
        {"title":"rp",
         "options": {
                          "tag-open":"rp",
                          "tag-close":"rp",
                          "content":ui.TextField(),
                          }},
        {"title":"rt",
         "options": {
                          "tag-open":"rt",
                          "tag-close":"rt",
                          "content":ui.TextField(),
                          }},
        {"title":"ruby",
         "options": {
                          "tag-open":"ruby",
                          "tag-close":"ruby",
                          "content":ui.TextField(),
                          }},
        {"title":"s",
         "options": {
                          "tag-open":"s",
                          "tag-close":"s",
                          "content":ui.TextField(),
                          }},
        {"title":"samp",
         "options": {
                          "tag-open":"samp",
                          "tag-close":"samp",
                          "content":ui.TextField(),
                          }},
        {"title": "script",
         "options": {
                     "tag-open":"script",
                     "tag-close":"script",
                     "content":ui.TextView(),
                     "async":ui.TextField(),
                     "charset":ui.TextField(),
                     "defer":ui.TextField(),
                     "src": ui.TextField(),
                     "type": ui.TextField(),
                     "xml:space":ui.TextField(),
                     }},
        {"title":"section",
         "options": {
                          "tag-open":"section",
                          "tag-close":"section",
                          "content":ui.TextField(),
                          }},
        {"title":"select",
         "options": {
                          "tag-open":"select",
                          "tag-close":"select",
                          "content":ui.TextField(),
                          "autofocus":ui.TextField(),
                          "disabled":ui.TextField(),
                          "form":ui.TextField(),
                          "multiple":ui.TextField(),
                          "required":ui.TextField(),
                          "size":ui.TextField(),
                          }},
        {"title":"small",
         "options": {
                          "tag-open":"small",
                          "tag-close":"small",
                          "content":ui.TextField(),
                          }},
        {"title":"source",
         "options": {
                          "tag-open":"source",
                          "tag-close":"source",
                          "content":ui.TextField(),
                          "media":ui.TextField(),
                          "src":ui.TextField(),
                          "type":ui.TextField(),
                          }},
        {"title":"span",
         "options": {
                          "tag-open":"span",
                          "tag-close":"span",
                          "content":ui.TextField(),
                          }},
        {"title":"strike - (Not Avaliable in HTML5)",
         "options": {
                          "tag-open":"strike",
                          "tag-close":"strike",
                          "content":ui.TextField(),
                          }},
        {"title":"strong",
         "options": {
                          "tag-open":"strong",
                          "tag-close":"strong",
                          "content":ui.TextField(),
                          }},
        {"title": "style",
         "options": {
                     "tag-open":"style",
                     "tag-close":"style",
                     "content":ui.TextView(),
                     "media":ui.TextField(),
                     "scoped":ui.TextField(),
                     "type":ui.TextField(),
                     }},
        {"title":"subscript - (sub)",
         "options": {
                          "tag-open":"sub",
                          "tag-close":"sub",
                          "content":ui.TextField(),
                          }},
        {"title":"summary",
         "options": {
                          "tag-open":"summary",
                          "tag-close":"summary",
                          "content":ui.TextField(),
                          }},
        {"title":"superscript - (sup)",
         "options": {
                          "tag-open":"sup",
                          "tag-close":"sup",
                          "content":ui.TextField(),
                          }},
        {"title":"table",
         "options": {
                          "tag-open":"table",
                          "tag-close":"table",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "bgcolor":ui.TextField(),
                          "border":ui.TextField(),
                          "cellpadding":ui.TextField(),
                          "cellspacing":ui.TextField(),
                          "frame":ui.TextField(),
                          "sortable":ui.TextField(),
                          "summary":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"table body (tbody)",
         "options": {
                          "tag-open":"tbody",
                          "tag-close":"tbody",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "valign":ui.TextField(),
                          }},
        {"title":"tablecell (td)",
         "options": {
                          "tag-open":"td",
                          "tag-close":"td",
                          "content":ui.TextField(),
                          "abbr":ui.TextField(),
                          "align":ui.TextField(),
                          "axis":ui.TextField(),
                          "bgcolor":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "colspan":ui.TextField(),
                          "headers":ui.TextField(),
                          "height":ui.TextField(),
                          "nowrap":ui.TextField(),
                          "rowspan":ui.TextField(),
                          "scope":ui.TextField(),
                          "valign":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"textarea",
         "options": {
                          "tag-open":"textarea",
                          "tag-close":"textarea",
                          "content":ui.TextField(),
                          "autofocus":ui.TextField(),
                          "cols":ui.TextField(),
                          "disabled":ui.TextField(),
                          "form":ui.TextField(),
                          "maxlength":ui.TextField(),
                          "placeholder":ui.TextField(),
                          "readonly":ui.TextField(),
                          "required":ui.TextField(),
                          "rows":ui.TextField(),
                          "wrap":ui.TextField(),
                          }},
        {"title":"table footer (tfoot)",
         "options": {
                          "tag-open":"tfoot",
                          "tag-close":"tfoot",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "valign":ui.TextField(),
                          }},
        {"title":"table header cell (th)",
         "options": {
                          "tag-open":"th",
                          "tag-close":"th",
                          "content":ui.TextField(),
                          "abbr":ui.TextField(),
                          "align":ui.TextField(),
                          "axis":ui.TextField(),
                          "bgcolor":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "colspan":ui.TextField(),
                          "headers":ui.TextField(),
                          "height":ui.TextField(),
                          "nowrap":ui.TextField(),
                          "rowspan":ui.TextField(),
                          "scope":ui.TextField(),
                          "sorted":ui.TextField(),
                          "valign":ui.TextField(),
                          "width":ui.TextField(),
                          }},
        {"title":"table header (thead)",
         "options": {
                          "tag-open":"thead",
                          "tag-close":"thead",
                          "content":ui.TextField(),
                          "align":ui.TextField(),
                          "char":ui.TextField(),
                          "charoff":ui.TextField(),
                          "valign":ui.TextField(),
                          }},
        {"title":"time",
         "options": {
                          "tag-open":"time",
                          "tag-close":"time",
                          "content":ui.TextField(),
                          "datetime":ui.TextField(),
                          }},
         {"title":"title",
          "options": {
                           "tag-open":"title",
                           "tag-close":"title",
                           "content":ui.TextField(),
                           }},
         {"title":"table row (tr)",
          "options": {
                           "tag-open":"tr",
                           "tag-close":"tr",
                           "content":ui.TextField(),
                           "align":ui.TextField(),
                           "bgcolor":ui.TextField(),
                           "char":ui.TextField(),
                           "charoff":ui.TextField(),
                           "valign":ui.TextField(),
                           }},
         {"title":"track",
          "options": {
                           "tag-open":"track",
                           "default":ui.TextField(),
                           "kind":ui.TextField(),
                           "label":ui.TextField(),
                           "src":ui.TextField(),
                           "srclang":ui.TextField(),
                           }},
         {"title":"teletype text (tt) - (Not Avaliable in HTML5)",
          "options": {
                           "tag-open":"tt",
                           "tag-close":"tt",
                           "content":ui.TextField(),
                           }},
         {"title":"underline (u)",
          "options": {
                           "tag-open":"u",
                           "tag-close":"u",
                           "content":ui.TextField(),
                           }},
         {"title":"unordered list (ul)",
          "options": {
                           "tag-open":"ul",
                           "tag-close":"ul",
                           "content":ui.TextField(),
                           "compact":ui.TextField(),
                           "type":ui.TextField(),
                           }},
         {"title":"variable (var)",
          "options": {
                           "tag-open":"var",
                           "tag-close":"var",
                           "content":ui.TextField(),
                           }},
         {"title":"video",
          "options": {
                           "tag-open":"video",
                           "tag-close":"video",
                           "content":ui.TextField(),
                           "autoplay":ui.TextField(),
                           "controls":ui.TextField(),
                           "height":ui.TextField(),
                           "loop":ui.TextField(),
                           "muted":ui.TextField(),
                           "poster":ui.TextField(),
                           "preload":ui.TextField(),
                           "src":ui.TextField(),
                           "width":ui.TextField(),
                           }},
         {"title":"word break opportunity (wbr)",
          "options": {
                           "tag-open":"wbr",
                           "tag-close":"wbr",
                           "content":ui.TextField(),
                           }},
         {"title": "comment",
          "options": {
                      "tag-open":"<!--",
                      "tag-close":"-->",
                      "content":ui.TextView(),
                      }},
]

ALL_EVENTS = dict(WINDOW_EVENTS,
                  **dict(FORM_EVENTS,
                         **dict(KEYBOARD_EVENTS,
                                **dict(MOUSE_EVENTS,
                                       **dict(CLIPBOARD_EVENTS,
                                              **dict(MEDIA_EVENTS,
                                                     **MISC_EVENTS))))))

print "%i GLOBAL_HTML_ATTR" % len(GLOBAL_HTML_ATTR)
print "%i ALL_EVENTS" % len(ALL_EVENTS)
print "%i TAGS" % len(TAGS)
print "%i TOTAL" % (len(GLOBAL_HTML_ATTR) + len(ALL_EVENTS) + len(TAGS))

class TagAddView(ui.View):
    def did_load(self):
        self.tabs = self["tab_selection"]
        self.options = self["items"]
        self.tabs.action = self.change_tab
        
        self.ok, self.cancle, self.preview = self["ok_btn"], self["cancle_btn"], self["preview_btn"]
        self.cancle.action = self.exit
        self.ok.action = self.set_tag
        
        self.pages = {}
        
        self.tag = ""
        self.cancled = False
        
    def add_page(self, page, values):
        p = ui.ScrollView()
        p.frame = self.options.frame
        p.y = 0
        p.background_color = "#DDDDDD"
        y = 20
        for k,v in sorted(values.iteritems()):
            if type(v) == type(""):
                t=v
                v = ui.Label()
                v.text = t
            t=k
            k = ui.Button()
            k.action = self.present_help
            k.title = t
            v.name = k.title
            k.width = 200
            v.width = 300
            k.x = 20
            v.x = 230
            k.y = y
            v.y = y
            k.height = 25
            v.height = 25 if type(v) != type(ui.TextView()) else 200
            y += v.height + 15
            p.add_subview(k)
            p.add_subview(v)
        p.content_size = (540, y+30)
        self.options.add_subview(p)
        self.pages[page] = p
        
    def present_help(self, sender):
        t = sender.title
        v = ui.WebView()
        v.width = 600
        v.height = 800
        v.load_url("http://www.w3schools.com/tags/default.asp")
        v.present("popover", popover_location=(sender.x+370, sender.y+180))
        print "Help Shown"
        
    def present_page(self, page):
        for p in self.options.subviews:
            p.send_to_back()
            
        if page in self.pages:
            p = self.pages[page]
            p.bring_to_front()
        
    def exit(self, sender):
        self.cancled = True
        self.close()
    
    def change_tab(self, sender):
        i = self.tabs.selected_index
        if i==3:
            x,y,w,h = self.tabs.frame
            t = ui.TableView()
            t.data_source = ui.ListDataSource([
                                               {"title":"Window Events"},
                                               {"title":"Form Events"},
                                               {"title":"Keyboard Events"},
                                               {"title":"Mouse Events"},
                                               {"title":"Clipboard Events"},
                                               {"title":"Media Events"},
                                               {"title":"Misc Events"},
                                               ])
            t.delegate = self
            
            t.width = 200
            t.height = 300
            t.present("popover", popover_location=(x+w+100, y+h+125))
            self.tabs.selected_index = -1
        else:
            self.present_page(self.tabs.segments[i])
    
    def tableview_did_select(self, tableview, section, row):
        tableview.close()
        i = tableview.data_source.items[row]
        self.present_page(i["title"])
        
    def set_tag(self, sender):
        self.close()
        kv = []
        content = None
        tag_start = None
        tag_end = None
        new_line = "\n"
        
        for sub in self.options.subviews:
            for elm in sub.subviews:
                if type(elm) != type(ui.Button()):
                    n,t = elm.name, elm.text
                    if type(elm) != type(ui.Label()):
                        if n == u'content':
                            content = t
                        elif n == u'newlinechar':
                            new_line = t if t else "\n"
                        else:
                            if t:
                                kv.append("%s=\'%s\'" % (n,t))
                    else:
                        if n:
                            print "%r\t%r" % (n,t)
                        if n == u'tag-open':
                            tag_start = t
                        elif n == u'tag-close':
                            tag_end = t
        kvstr = " ".join(kv)
        if not tag_end:
            tag = "<%(tag-start)s %(kvstr)s />" % {
                                                   "tag-start":tag_start,
                                                   "kvstr":kvstr,
                                                   }
        else:
            content = content.replace("\n", new_line) if content else ""
            tag = "<%(tag-start)s %(kvstr)s>%(content)s</%(tag-end)s>" % {
                                                                            "tag-start":tag_start,
                                                                            "tag-end":tag_end,
                                                                            "kvstr":kvstr,
                                                                            "content":content,
                                                                            }
        self.tag = tag



class TagDelegate (object):
    def __init__(self, js_eval):
        self.js_eval = js_eval
    
    def tableview_did_select(self, tableview, section, row):
        tableview.close()
        
        view = ui.load_view()
        view.name = tableview.data_source.items[row]["title"]
        view.add_page("General", tableview.data_source.items[row]["options"])
        view.add_page("Global Attributes", GLOBAL_HTML_ATTR)
        view.add_page("Misc Attributes", MISC_HTML_ATTR)
        view.add_page("Window Events", WINDOW_EVENTS)
        view.add_page("Form Events", FORM_EVENTS)
        view.add_page("Keyboard Events", KEYBOARD_EVENTS)
        view.add_page("Mouse Events", MOUSE_EVENTS)
        view.add_page("Clipboard Events", CLIPBOARD_EVENTS)
        view.add_page("Media Events", MEDIA_EVENTS)
        view.add_page("Misc Events", MISC_EVENTS)
        self.show(view)
        
    @ui.in_background
    def show(self, view):
        view.present("sheet")
        view.present_page("General")
        view.wait_modal()
        if not view.cancled:
            print "Done"
            out = json.dumps(view.tag)
            print "editor.replaceSelection(%s);" % out
            self.js_eval("editor.replaceSelection(%s);" % out)
        else:
            print "Cancled"
        
        
def add_tag(sender=None, pop_loc=None):
    if not pop_loc:
        pop_loc = (0,0)
    
    v = ui.TableView()
    v.data_source = ui.ListDataSource(TAGS)
    if sender:
        pass
    else:
        we = ui.WebView()
    v.delegate = TagDelegate(we.eval_js)
    v.name = "Add Tag"
    v.width = 350
    v.height = 500
    v.present("popover", popover_location=pop_loc)
    v.wait_modal()

if __name__ == "__main__":        
    add_tag()
