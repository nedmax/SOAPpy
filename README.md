# SOAPpy
Simple to use SOAP library for Python


The goal of the SOAPpy team is to provide a full-featured SOAP library
for Python that is very simple to use and that fully supports dynamic
interaction between clients and servers.

### Included

- General SOAP Parser based on sax.xml
- General SOAP Builder
- SOAP Proxy for RPC client code
- SOAP Server framework for RPC server code

### Features
- Handles all SOAP 1.0 types
- Handles faults
- Allows namespace specification
- Allows SOAPAction specification
- Homogeneous typed arrays
- Supports multiple schemas
- Header support (mustUnderstand and actor)
- XML attribute support
- Multi-referencing support (Parser/Builder)
- Understands SOAP-ENC:root attribute
- Good interop, passes all client tests for Frontier, SOAP::LITE, SOAPRMI
- Encodings
- SSL clients (with Python compiled with OpenSSL support)
- SSL servers (with Python compiled with OpenSSL support and M2Crypto installed)
- Encodes XML tags per SOAP 1.2 name mangling specification (Gregory Warnes)
- Automatic stateful SOAP server support (Apache v2.x) (blunck2)
- WSDL client support
- WSDL server support


## Installation

### Using PIP + GitHub

    pip install -e "git+http://github.com/kiroky/SOAPpy.git@develop#egg=SOAPpy"

### Manual

    python setup.py install


## DOCUMENTATION

A simple "Hello World" http SOAP server::

    import SOAPpy
    def hello():
        return "Hello World"
    server = SOAPpy.SOAPServer(("localhost", 8080))
    server.registerFunction(hello)
    server.serve_forever()

And the corresponding client:

    import SOAPpy
    server = SOAPpy.SOAPProxy("http://localhost:8080/")
    print server.hello()


Support
============
Github: https://github.com/nedmax/SOAPpy
Issues: https://github.com/nedmax/SOAPpy/issues
