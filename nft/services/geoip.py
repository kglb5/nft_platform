import geoip2.webservice
import geoip2.database
from os.path import dirname
import patreon


def get_reader():
    reader = geoip2.database.Reader(dirname(patreon.constants.__file__) + '/geoip.mmdb')
    return reader
