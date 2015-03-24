JAVASCRIPT =    "function hello_world() {\n"\
                "    alert('hello world @file_name');\n"\
                "}\n"
                
HTML =    "<html>\n"\
          "\t<head>\n"\
          "\t\t<title> Hello World </title>\n"\
          "\t</head>\n"\
          "\t<body>\n"\
          "\t\t<p> Hello World </p>\n"\
          "\t</body>\n"\
          "</html>"
          
CSS =    "p {\n"\
         "    color: #000000;\n"\
         "}\n"
         
REQUEST_HANDLER =     "class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):\n"\
                      "    def do_GET(self):\n"\
                      "        print self.path\n"\
                      "        if self.path in ['', '/', '/index.html']:\n"\
                      "            self.send_response(200)\n"\
                      "            self.end_headers()\n"\
                      "            index = view['editor_view']['file_nav'].selected_index\n"\
                      "            if not index == -1:\n"\
                      "                file = view['editor_view']['file_nav'].segments[index]\n"\
                      "            #print file\n"\
                      "            file_data = file_system['data'][file][0]\n"\
                      "            #print file_data\n"\
                      "            self.wfile.write(file_data)\n"\
                      "        else:\n"\
                      "            name = self.path.split('/')[-1]\n"\
                      "            try:\n"\
                      "                self.send_response(200)\n"\
                      "                self.end_headers()\n"\
                      "                self.wfile.write(file_system['data'][name][0])\n"\
                      "            except:\n"\
                      "                pass"
