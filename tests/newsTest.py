#!/usr/bin/env python

ident = '$Id: newsTest.py,v 1.4 2003/05/21 14:52:37 warnes Exp $'

import os, re
import sys
sys.path.insert(1, "..")

from SOAPpy import SOAPProxy

SoapEndpointURL	   = 'http://www22.brinkster.com/prasads/BreakingNewsService.asmx?WSDL'

MethodNamespaceURI = 'http://tempuri.org/'

# Three ways to do namespaces, force it at the server level

server = SOAPProxy(SoapEndpointURL, namespace = MethodNamespaceURI,
                   soapaction='http://tempuri.org/GetCNNNews', encoding = None)
print "[server level CNN News call]"
print server.GetCNNNews()

# Do it inline ala SOAP::LITE, also specify the actually ns (namespace) and
# sa (soapaction)

server = SOAPProxy(SoapEndpointURL, encoding = None)
print "[inline CNNNews call]"
print server._ns('ns1',
    MethodNamespaceURI)._sa('http://tempuri.org/GetCNNNews').GetCNNNews()

# Create an instance of your server with specific namespace and then use
# inline soapactions for each call

dq = server._ns(MethodNamespaceURI)
print "[namespaced CNNNews call]"
print dq._sa('http://tempuri.org/GetCNNNews').GetCNNNews()
print "[namespaced CBSNews call]"
print dq._sa('http://tempuri.org/GetCBSNews').GetCBSNews()
