import re
from xml.sax.saxutils import escape
import xmltodict
from uuid import uuid4 as unique

def tag(tag, mode='intuit'):
    intuit = '{http://developer.intuit.com/}'
    soap = '{http://schemas.xmlsoap.org/soap/envelope/}'
    return intuit + tag if mode == 'intuit' else soap + tag

def xml_soap(xml):
    return escape(xml)

def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_qbc_file(app_name = "Quickbooks Integrator", app_id = 0,
        app_url = "http://localhost:8000/quickbooks/", app_description="Localhost Quickbooks ",
        app_support = "http://localhost:8000/",
        username="quickbooks", owner_id="{%s}" %(unique()), file_id="{%s}" %(unique()), qb_type="QBFS",
        run_every="RunEveryNMinutes", run_time = 1, read_only=False):

    """ Generates a quickbooks webconnector xml
    :param app_name:
    :param app_id:
    :param app_url:
    :param app_description:
    :param app_support:
    :param username:
    :param owner_id:
    :param file_id:
    :param qb_type:
    :param run_every:
    :param run_time:
    :param read_only:
    :return: xml string
    """

    c = {
        "QBWCXML" : {
            "AppName" : app_name,
            "AppID" : app_id,
            "AppURL" : app_url,
            "AppDescription" : app_description,
            "AppSupport" : app_support,
            "UserName" : username,
            "OwnerID" : owner_id,
            "FileID" : file_id,
            "QBType" : qb_type,
            "Scheduler" : {
                run_every : run_time
            },
            "IsReadOnly" : "false" if read_only == False else "true"
        }
    }

    return xmltodict.unparse(c)