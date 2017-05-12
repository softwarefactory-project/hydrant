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

from hydrant.backends import base


LOGGER = logging.getLogger('hydrant')
LOGGER.setLevel(logging.DEBUG)


class ElasticsearchBackend(base.BaseBackend):
    def __init__(self, host, port):
        self.es = Elasticsearch([host, ],
                                port=port)

    def add(self, msg, topic):
        self.es.index(index=topic,
                      body=msg,
                      doc_type='event')
        LOGGER.debug("Added %r to index %s" % (msg, topic))
