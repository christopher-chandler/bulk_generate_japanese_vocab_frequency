import sys
import os

# Get the path to the add-on's directory
addon_path = os.path.dirname(__file__)

# Add the 'libs' directory to sys.path
lib_path = os.path.join(addon_path, "libs")
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)




# Import janome from the local 'libs' directory
from  janome.tokenizer import Tokenizer

# Create a Tokenizer object
t = Tokenizer()

# Tokenize the Japanese sentence
sentence = 'いつか昔のように接することができればいいなと思う。'
f = open("/Users/christopherchandler/Library/Application Support/Anki2/addons21/1004691625/text.txt",
         encoding="utf-8",mode="w+")
for token in t.tokenize(sentence):
    # Print each token and its attributes
    f.write(str(token) + "\n")