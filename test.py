###
# Copyright (c) 2016, lod
# All rights reserved.
#
#
###

from supybot.test import *


class SearxTestCase(PluginTestCase):
    plugins = ('Searx',)

    def testSearx(self):
        self.assertNotError('searx google')
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
