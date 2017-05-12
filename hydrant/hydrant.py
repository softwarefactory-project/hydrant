#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import argparse
import logging
import os
import sys
# import json

import paho.mqtt.client as mqtt
import yaml

# import datetime
# import time


LOGGER = logging.getLogger('hydrant')
LOGGER.setLevel(logging.DEBUG)


def on_connect(client, userdata, flags, rc):
    LOGGER.info("MQTT: Connected with result code "+str(rc))
    client.subscribe("#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    LOGGER.debug(msg.topic+": "+str(msg.payload))


def main():
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    LOGGER.addHandler(console)

    parser = argparse.ArgumentParser(description="hydrant")
    parser.add_argument('--config-file', '-c', metavar='/PATH/TO/CONF',
                        help='The path to the configuration file to use.')
    parser.add_argument('--verbose', '-v', default=False, action='store_true',
                        help='Run in debug mode')

    args = parser.parse_args()
    if args.verbose:
        console.setLevel(logging.DEBUG)
    else:
        console.setLevel(logging.INFO)
    if not args.config_file:
        sys.exit('Please provide a configuration file with option -c.')
    if not os.path.isfile(args.config_file):
        sys.exit('%s not found.' % args.config_file)
    with open(args.config_file, 'r') as raw_conf:
        conf = yaml.load(raw_conf)
    if 'mqtt' not in conf:
        sys.exit('MQTT configuration missing in %s' % args.config_file)
    if 'elasticsearch' not in conf:
        sys.exit('Elasticsearch configuration missing in %s' %
                 args.config_file)

    LOGGER.debug(
        'Creating MQTT listener on %s:%s' % (conf['mqtt']['host'],
                                             conf['mqtt']['port']))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("iot.eclipse.org", 1883, 60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        LOGGER.info('Manual interruption, bye!')
        sys.exit(2)


if __name__ == "__main__":
    main()
