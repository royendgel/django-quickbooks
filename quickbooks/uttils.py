import re
from xml.sax.saxutils import escape
def tag(tag, mode='intuit'):
    intuit = '{http://developer.intuit.com/}'
    soap = '{http://schemas.xmlsoap.org/soap/envelope/}'
    return intuit + tag if mode == 'intuit' else soap + tag

def xml_soap(xml):
    return escape(xml)

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()