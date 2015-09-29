#!/usr/bin/env python

ident = '$Id: BabelfishWSDLTest.py,v 1.1 2003/07/18 15:58:28 warnes Exp $'

import os, re
import sys
sys.path.insert(1, "..")

from SOAPpy import WSDL

server = WSDL.Proxy('http://www.xmethods.net/sd/2001/BabelFishService.wsdl')

english = "Hi Friend!"

print "Babelfish Translations"
print "------------------------"
print "English: '%s'" % english
print "French:  '%s'" % server.BabelFish('en_fr',english)
print "Spanish: '%s'" % server.BabelFish('en_es',english)
print "Italian: '%s'" % server.BabelFish('en_it',english)
print "German:  '%s'" % server.BabelFish('en_de',english)

print "Done."
