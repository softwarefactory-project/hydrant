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


import logging
from elasticsearch import Elasticsearch

from sfhydrant.backends import base


LOGGER = logging.getLogger('hydrant')
LOGGER.setLevel(logging.DEBUG)


class ElasticsearchBackend(base.BaseBackend):
    def __init__(self, host, port):
        self.es = Elasticsearch([host, ],
                                port=port)

    def add(self, msg, topic):
        # clean up gerrit topics, keep simply "gerrit"
        t = topic.split('/')[0]
        if t != topic:
            event_type = topic.split('/')[-1]
        else:
            if "EVENT" in msg:
                event_type = msg["EVENT"]
            else:
                event_type = topic
        # convert timestamps, ids... to the right type
        if "TIMESTAMP" in msg:
            msg["TIMESTAMP"] = int(msg["TIMESTAMP"])
        if "NODE_ID" in msg:
            msg["NODE_ID"] = int(msg["NODE_ID"])
        if "ZUUL_CHANGE" in msg:
            try:
                msg["ZUUL_CHANGE"] = int(msg["ZUUL_CHANGE"])
            except ValueError:
                # Happens with periodic changes
                msg["ZUUL_CHANGE"] = 0
        if "ZUUL_PATCHSET" in msg:
            try:
                msg["ZUUL_PATCHSET"] = int(msg["ZUUL_PATCHSET"])
            except ValueError:
                msg["ZUUL_PATCHSET"] = 0
        if "build" in msg:
            msg["build"] = int(msg["build"])
        self.es.index(index=t,
                      body=msg,
                      doc_type=event_type)
        LOGGER.debug("Added %r to index %s" % (msg, topic))
