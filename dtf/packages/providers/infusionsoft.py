import xmlrpclib
from packages import settings

key = settings.INFUSIONSOFT_API_KEY
company = settings.INFUSIONSOFT_COMPANY
server = xmlrpclib.ServerProxy("https://%s.infusionsoft.com:443/api/xmlrpc" % company);
