
from __future__ import nested_scopes
from version import __version__

import urllib
import requests
from types import *
import re, os, base64
import base64
import Cookie

# SOAPpy modules
from Errors      import *
from Config      import Config
from Parser      import parseSOAPRPC
from SOAPBuilder import buildSOAP
from Utilities   import *
from Types       import faultType, simplify

################################################################################
# Client
################################################################################


def SOAPUserAgent():
    return "SOAPpy " + __version__


class SOAPAddress:
    def __init__(self, url, config = Config):
        proto, uri = urllib.splittype(url)

        # apply some defaults
        if uri[0:2] != '//':
            if proto != None:
                uri = proto + ':' + uri

            uri = '//' + uri
            proto = 'http'

        host, path = urllib.splithost(uri)

        try:
            int(host)
            host = 'localhost:' + host
        except:
            pass

        if not path:
            path = '/'

        if proto not in ('http', 'https'):
            raise IOError, "unsupported SOAP protocol"
        if proto == 'https' and not config.SSLclient:
            raise AttributeError, \
                "SSL client not supported by this Python installation"

        self.user,host = urllib.splituser(host)
        self.proto = proto
        self.host = host
        self.path = path

    def __str__(self):
        return "%(proto)s://%(host)s%(path)s" % self.__dict__

    __repr__ = __str__

class HTTPTransport:


    def __init__(self):
        self.cookies = Cookie.SimpleCookie();

    def getNS(self, original_namespace, data):
        """Extract the (possibly extended) namespace from the returned
        SOAP message."""

        if type(original_namespace) == StringType:
            pattern="xmlns:\w+=['\"](" + original_namespace + "[^'\"]*)['\"]"
            match = re.search(pattern, data)
            if match:
                return match.group(1)
            else:
                return original_namespace
        else:
            return original_namespace

    def call(self, addr, data, namespace, soapaction = None, encoding = None, config = Config, timeout=None):

        if not isinstance(addr, SOAPAddress):
            addr = SOAPAddress(addr, config)

        real_addr = addr.proto + "://" + addr.host
        real_path = real_addr + addr.path

        if addr.proto == 'https':
            cert = (config.SSL.cert_file, config.SSL.key_file)

        if encoding != None:
            t += '; charset=%s' % encoding
        r.putheader("Content-type", t)

        headers = {
            'User-Agent': SOAPUserAgent(),
            'Content-type': t,
            'SOAPAction': soapaction
        }

        r = requests.post(real_path, headers=headers, cert=cert)


        # read response line
        response = r.getresponse()
        code = r.status_code
        msg = r.status
        headers = r.headers

        self.cookies = r.cookies

        if headers:
            content_type = headers.get("Content-Type", "text/xml")
            content_length = headers.get("Content-Length")
        else:
            content_type = None
            content_length = None

        data = r.text
        if data is None:
            raise HTTPError(code, "Empty response from server\nCode: %s\nHeaders: %s" % (msg, headers))

        message_len = len(data)

        if code == 500 and not ( startswith(content_type, "text/xml") and message_len > 0 ):
            raise HTTPError(code, msg)

        if code not in (200, 500):
            raise HTTPError(code, msg)

        # get the new namespace
        if namespace is None:
            new_ns = None
        else:
            new_ns = self.getNS(namespace, data)

        # return response payload
        return data, new_ns

################################################################################
# SOAP Proxy
################################################################################
class SOAPProxy:
    def __init__(self, proxy, namespace = None, soapaction = None,
                 header = None, methodattrs = None, transport = HTTPTransport,
                 encoding = 'UTF-8', throw_faults = 1, unwrap_results = None,
                 config = Config, noroot = 0, simplify_objects=None,
                 timeout=None):

        # Test the encoding, raising an exception if it's not known
        if encoding != None:
            ''.encode(encoding)

        # get default values for unwrap_results and simplify_objects
        # from config
        if unwrap_results is None:
            self.unwrap_results=config.unwrap_results
        else:
            self.unwrap_results=unwrap_results

        if simplify_objects is None:
            self.simplify_objects=config.simplify_objects
        else:
            self.simplify_objects=simplify_objects

        self.proxy          = SOAPAddress(proxy, config)
        self.namespace      = namespace
        self.soapaction     = soapaction
        self.header         = header
        self.methodattrs    = methodattrs
        self.transport      = transport()
        self.encoding       = encoding
        self.throw_faults   = throw_faults
        self.config         = config
        self.noroot         = noroot
        self.timeout        = timeout

        # GSI Additions
        if hasattr(config, "channel_mode") and \
               hasattr(config, "delegation_mode"):
            self.channel_mode = config.channel_mode
            self.delegation_mode = config.delegation_mode
        #end GSI Additions

    def invoke(self, method, args):
        return self.__call(method, args, {})

    def __call(self, name, args, kw, ns = None, sa = None, hd = None,
        ma = None):

        ns = ns or self.namespace
        ma = ma or self.methodattrs

        if sa: # Get soapaction
            if type(sa) == TupleType:
                sa = sa[0]
        else:
            if self.soapaction:
                sa = self.soapaction
            else:
                sa = name

        if hd: # Get header
            if type(hd) == TupleType:
                hd = hd[0]
        else:
            hd = self.header

        hd = hd or self.header

        if ma: # Get methodattrs
            if type(ma) == TupleType: ma = ma[0]
        else:
            ma = self.methodattrs
        ma = ma or self.methodattrs

        m = buildSOAP(args = args, kw = kw, method = name, namespace = ns,
            header = hd, methodattrs = ma, encoding = self.encoding,
            config = self.config, noroot = self.noroot)


        call_retry = 0
        try:
            r, self.namespace = self.transport.call(self.proxy, m, ns, sa,
                                                    encoding = self.encoding,
                                                    config = self.config,
                                                    timeout = self.timeout)

        except socket.timeout:
            raise SOAPTimeoutError

        except Exception, ex:
            #
            # Call failed.
            #
            # See if we have a fault handling vector installed in our
            # config. If we do, invoke it. If it returns a true value,
            # retry the call.
            #
            # In any circumstance other than the fault handler returning
            # true, reraise the exception. This keeps the semantics of this
            # code the same as without the faultHandler code.
            #

            if hasattr(self.config, "faultHandler"):
                if callable(self.config.faultHandler):
                    call_retry = self.config.faultHandler(self.proxy, ex)
                    if not call_retry:
                        raise
                else:
                    raise
            else:
                raise

        if call_retry:
            try:
                r, self.namespace = self.transport.call(self.proxy, m, ns, sa,
                                                        encoding = self.encoding,
                                                        config = self.config,
                                                        timeout = self.timeout)
            except socket.timeout:
                raise SOAPTimeoutError


        p, attrs = parseSOAPRPC(r, attrs = 1)

        try:
            throw_struct = self.throw_faults and \
                isinstance (p, faultType)
        except:
            throw_struct = 0

        if throw_struct:
            if self.config.debug:
                print p
            raise p

        # If unwrap_results=1 and there is only element in the struct,
        # SOAPProxy will assume that this element is the result
        # and return it rather than the struct containing it.
        # Otherwise SOAPproxy will return the struct with all the
        # elements as attributes.
        if self.unwrap_results:
            try:
                count = 0
                for i in p.__dict__.keys():
                    if i[0] != "_":  # don't count the private stuff
                        count += 1
                        t = getattr(p, i)
                if count == 1: # Only one piece of data, bubble it up
                    p = t
            except:
                pass

        # Automatically simplfy SOAP complex types into the
        # corresponding python types. (structType --> dict,
        # arrayType --> array, etc.)
        if self.simplify_objects:
            p = simplify(p)

        if self.config.returnAllAttrs:
            return p, attrs
        return p

    def _callWithBody(self, body):
        return self.__call(None, body, {})

    def __getattr__(self, name):  # hook to catch method calls
        if name in ( '__del__', '__getinitargs__', '__getnewargs__',
           '__getstate__', '__setstate__', '__reduce__', '__reduce_ex__'):
            raise AttributeError, name
        return self.__Method(self.__call, name, config = self.config)

    # To handle attribute weirdness
    class __Method:
        # Some magic to bind a SOAP method to an RPC server.
        # Supports "nested" methods (e.g. examples.getStateName) -- concept
        # borrowed from xmlrpc/soaplib -- www.pythonware.com
        # Altered (improved?) to let you inline namespaces on a per call
        # basis ala SOAP::LITE -- www.soaplite.com

        def __init__(self, call, name, ns = None, sa = None, hd = None,
            ma = None, config = Config):

            self.__call 	= call
            self.__name 	= name
            self.__ns   	= ns
            self.__sa   	= sa
            self.__hd   	= hd
            self.__ma           = ma
            self.__config       = config
            return

        def __call__(self, *args, **kw):
            if self.__name[0] == "_":
                if self.__name in ["__repr__","__str__"]:
                    return self.__repr__()
                else:
                    return self.__f_call(*args, **kw)
            else:
                return self.__r_call(*args, **kw)

        def __getattr__(self, name):
            if name == '__del__':
                raise AttributeError, name
            if self.__name[0] == "_":
                # Don't nest method if it is a directive
                return self.__class__(self.__call, name, self.__ns,
                    self.__sa, self.__hd, self.__ma)

            return self.__class__(self.__call, "%s.%s" % (self.__name, name),
                self.__ns, self.__sa, self.__hd, self.__ma)

        def __f_call(self, *args, **kw):
            if self.__name == "_ns": self.__ns = args
            elif self.__name == "_sa": self.__sa = args
            elif self.__name == "_hd": self.__hd = args
            elif self.__name == "_ma": self.__ma = args
            return self

        def __r_call(self, *args, **kw):
            return self.__call(self.__name, args, kw, self.__ns, self.__sa,
                self.__hd, self.__ma)

        def __repr__(self):
            return "<%s at %d>" % (self.__class__, id(self))
