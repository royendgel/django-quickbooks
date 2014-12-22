from suds.client import Client
client = Client('http://127.0.0.1:8000/quickbooks/wsdl')

client = Client('http://127.0.0.1:8000/quickbooks/wsdl')
from suds.plugin import MessagePlugin

class LogPlugin(MessagePlugin):
  def sending(self, context):
    print(str(context.envelope))
  def received(self, context):
    print(str(context.reply))

client = Client("http://127.0.0.1:8000/quickbooks/wsdl", plugins=[LogPlugin()])

client.service.authenticate()