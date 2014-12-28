def tag(tag, mode='intuit'):
    intuit = '{http://developer.intuit.com/}'
    soap = '{http://schemas.xmlsoap.org/soap/envelope/}'
    return intuit + tag if mode == 'intuit' else soap + tag

def xml_soap(xml):
    return xml