#!/usr/bin/env python

# Copyright (c) 2001 actzero, inc. All rights reserved.

ident = '$Id: alanbushTest.py,v 1.5 2003/05/21 14:52:37 warnes Exp $'

import os, re,sys

# add local SOAPpy code to search path
sys.path.insert(1, "..")

from SOAPpy import *
Config.debug=0

SoapEndpointURL	   = 'http://www.alanbushtrust.org.uk/soap/compositions.asp'
MethodNamespaceURI = 'urn:alanbushtrust-org-uk:soap.methods'
SoapAction	   = MethodNamespaceURI + ".GetCategories"

server = SOAPProxy(SoapEndpointURL,
                        namespace=MethodNamespaceURI,
                        soapaction=SoapAction,
                        )

for category in server.GetCategories():
   print category
