import json
import sys

from openstack.common import log
from oslo.config import cfg
from oslo import messaging

from os_collect_config import version


CONF = cfg.CONF

opts = [
    cfg.StrOpt('topic_name',
               default='os-collect-config_topic'),
    cfg.StrOpt('server_id',
               help='A string uniquely identifying target instance.'),
    cfg.StrOpt('json_file',
               help='JSON file to apply on the instance.'),
]
CONF = cfg.CONF
CONF.register_cli_opts(opts)


class CollectClient(object):
    def __init__(self, transport):
        target = messaging.Target(topic=CONF.topic_name, version='1.0',
                                  server=CONF.server_id)
        self._client = messaging.RPCClient(transport, target)

    def apply_config(self, dct):
        return self._client.call({}, 'apply_config', dct=dct)


def main():
    log.setup('collect-client')

    CONF(sys.argv[1:], project='os-collect-config-client',
         version=version.version_info.version_string())

    transport = messaging.get_transport(cfg.CONF)
    client = CollectClient(transport)

    with open(CONF.json_file) as fl:
        dct = json.load(fl)

    #print dct

    print client.apply_config(dct)
