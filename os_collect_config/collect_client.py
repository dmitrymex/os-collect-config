# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    client.apply_config(dct)
