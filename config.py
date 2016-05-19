###
# Copyright (c) 2016, lod
# All rights reserved.
#
#
###

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Searx')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified themself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Searx', True)

class NumSearchResults(registry.PositiveInteger):
    """Value must be 1 <= n <= 8"""
    def setValue(self, v):
        if v > 8:
            self.error()
        super(self.__class__, self).setValue(v)

Searx = conf.registerPlugin('Searx')
conf.registerChannelValue(Searx, 'url',
    registry.String('https://searx.me/', _("""Determines the URL used for
    requests.""")))
conf.registerChannelValue(Searx, 'bold',
    registry.Boolean(True, _("""Determines whether results are bolded.""")))
conf.registerChannelValue(Searx, 'oneToOne',
    registry.Boolean(False, _("""Determines whether results are sent in
    different lines or all in the same one.""")))
conf.registerChannelValue(Searx, 'maximumResults',
    NumSearchResults(3, _("""Determines the maximum number of results returned
    from the google command.""")))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
