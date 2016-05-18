###
# Copyright (c) 2016, lod
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.utils.minisix as minisix

import sys
import json
import socket
import unicodedata

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Searx')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Searx(callbacks.Plugin):
    """does a search on https://searx.me/"""
    threaded = True
    
    def __init__(self, irc):
        self.__parent = super(Searx, self)
        self.__parent.__init__(irc)

    def search(self, query, channel):
        """search("search phrase")"""

        ref = 'http://%s/%s' % (dynamic.irc.server, dynamic.irc.nick)
        headers = dict(utils.web.defaultHeaders)
        headers['Referer'] = ref
        opts = {'q': query}
      
        #defLang = self.registryValue('defaultLanguage', channel)

        text = utils.web.getUrlFd('%s&%s' % ('https://searx.me/?format=json',
                                           utils.web.urlencode(opts)),
                                headers=headers)
        return text

    def formatData(self, data, bold=True, max=0, onetoone=False):
        data = json.loads(data.read().decode('utf-8'))
        data = data['results']
        results = []
        if max:
            data = data[:max]

        for result in data:
            title = result['title']
            url = result['url']
            if minisix.PY2:
                url = url.encode('utf-8')
            if title:
                if bold:
                    title = ircutils.bold(title)
                results.append(format('%s: %u', title, url))
            else:
                results.append(url)
        if minisix.PY2:
            repl = lambda x:x if isinstance(x, unicode) else unicode(x, 'utf8')
            results = list(map(repl, results))
        if not results:
            return [_('No matches found.')]
        elif onetoone:
            return results
        else:
            return [minisix.u('; ').join(results)]

    def searx(self, irc, msg, args, text):
        """<search> <value>]"""

        data = self.search(text, msg.args[0])
        bold = self.registryValue('bold', msg.args[0])
        max = self.registryValue('maximumResults', msg.args[0])
        # We don't use supybot.reply.oneToOne here, because you generally
        # do not want @google to echo ~20 lines of results, even if you
        # have reply.oneToOne enabled.
        onetoone = self.registryValue('oneToOne', msg.args[0])
        for result in self.formatData(data,
                                  bold=bold, max=max, onetoone=onetoone):
            irc.reply(result)
    searx = wrap(searx, ['text'])

Class = Searx


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
