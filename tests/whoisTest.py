#!/usr/bin/env python

ident = '$Id: whoisTest.py,v 1.4 2003/05/21 14:52:37 warnes Exp $'

import os, re
import sys
sys.path.insert(1, "..")

from SOAPpy import SOAPProxy

server = SOAPProxy("http://www.SoapClient.com/xml/SQLDataSoap.WSDL")

print "whois>>", server.ProcessSRL(SRLFile="WHOIS.SRI",
                                   RequestName="whois",
                                   key = "microsoft.com")
