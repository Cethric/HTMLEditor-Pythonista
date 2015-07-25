import editor
import os

CONTENTS = '''language: python
python:
     - "2.6"
     - "2.7"

script: nosetest
'''
path = os.path.abspath(".travis.yml")
print path
# with open(path, "wb") as f:
#    f.write(CONTENTS)

editor.open_file("HTMLEditor-Pythonista/.travis.yml")
