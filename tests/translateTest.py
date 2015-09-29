#!/usr/bin/env python

# Copyright (c) 2001 actzero, inc. All rights reserved.
ident = '$Id: translateTest.py,v 1.5 2003/05/21 14:52:37 warnes Exp $'

import os, re
import sys
sys.path.insert(1, "..")

from SOAPpy import SOAPProxy


server = SOAPProxy("http://services.xmethods.com:80/perl/soaplite.cgi")
babel = server._ns('urn:xmethodsBabelFish#BabelFish')

print babel.BabelFish(translationmode = "en_fr",
    sourcedata = "The quick brown fox did something or other")
