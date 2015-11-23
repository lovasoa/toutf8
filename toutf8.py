#!/usr/bin/env python3
#coding: utf8

import encodings
import re
import sys

if   len(sys.argv) == 1: filein,fileout = ("/dev/stdin", "/dev/stdout")
elif len(sys.argv) == 2: filein,fileout = (sys.argv[1],  sys.argv[1])
else                   : filein,fileout = (sys.argv[1],  sys.argv[2])

with open(filein, "rb") as f:
    buf = f.read()

wordlists = tuple(map(lambda f:set(map(str.strip, open(f,"r"))),
                    ("/usr/share/dict/russian",
                     "/usr/share/dict/french",
                     "/usr/share/dict/american-english")))

scores = dict()

tok = re.compile("\w+")
codings = set(encodings.aliases.aliases.values())
for i,encoding in enumerate(codings):
    try: txt = encodings.codecs.decode(buf, encoding)
    except: continue
    if type(txt) is not str: continue
    found_words = (sum(m.group(0) in wl for m in tok.finditer(txt)) for wl in wordlists)
    scores[encoding] = max(found_words) 

codec = max(scores.keys(), key=lambda k:scores[k])

with open(fileout, "w") as f:
    f.write(encodings.codecs.decode(buf, codec))

