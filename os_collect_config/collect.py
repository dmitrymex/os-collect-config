import json
import os
import subprocess
import sys

from openstack.common import log
from oslo.config import cfg
from oslo import messaging

from os_collect_config import cache
from os_collect_config import version


opts = [
    cfg.StrOpt('command', short='c',
               help='Command to run on metadata changes. If specified,'
                    ' os-collect-config will continue to run until killed. If'
                    ' not specified, os-collect-config will print the'
                    ' collected data as a json map and exit.'),
    cfg.StrOpt('cachedir',
               default='/var/run/os-collect-config',
               help='Directory in which to store local cache of metadata'),
    cfg.BoolOpt('print_only', dest='print_only',
               default=False,
                help='Query normally, print the resulting configs as a json'
                     ' map, and exit immediately without running command if it is'
                     ' configured.'),
    cfg.StrOpt('server_id',
               help='A string uniquely identifying current instance. Used'
                    'by server to distinguish instances.'),
    cfg.StrOpt('topic_name',
               default='os-collect-config_topic'),
]
CONF = cfg.CONF
CONF.register_cli_opts(opts)


logger = None


class AgentEndpoint(object):
    def apply_config(self, ctxt, dct):
        changed, filename = cache.store('messaging', dct)

        env = dict(os.environ)
        env['OS_CONFIG_FILES'] = filename
        logger.info('Will run "%s" with OS_CONFIG_FILES=%s' %
                    (CONF.command, env["OS_CONFIG_FILES"]))

        if not CONF.print_only:
            logger.info('Executing...')
            subprocess.check_call(CONF.command, env=env, shell=True)


def setup_agent():
    global logger
    CONF(sys.argv[1:], project='os-collect-config', version=version.version_info.version_string()) 
    log.setup('os-collect-config')
    logger = log.getLogger(__name__)


def main():
    setup_agent()

    logger.info('Running os-collect-config from main()')

    transport = messaging.get_transport(cfg.CONF)
    target = messaging.Target(topic=CONF.topic_name, version='1.0',
                              server=CONF.server_id)
    server = messaging.get_rpc_server(transport, target,
                                      endpoints=[AgentEndpoint()])

    server.start()
    server.wait()


if __name__ == '__main__':
    setup_agent()

    logger.info('Running os-collect-config')

    with open('/tmp/config/elements/seed-stack-config/config.json') as fl:
        dct = json.load(fl)
    AgentEndpoint().apply_config(dct)
