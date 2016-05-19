###
# Copyright (c) 2016, lod
# All rights reserved.
#
#
###

from supybot.test import *


class SearxTestCase(PluginTestCase):
    plugins = ('Searx','Config')

    def testSearx(self):
        self.assertNotError('searx google')

    def testLucky(self):
        self.assertResponse('lucky Hacker News',
                    'https://news.ycombinator.com/')
    def testSearchFormat(self):
        self.assertRegexp('searx foo', '<https?://.*>')
        self.assertNotError('config reply.format.url %s')
        self.assertRegexp('searx foo', 'https?://.*')
        self.assertNotRegexp('searx foo', '<https?://.*>')

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
