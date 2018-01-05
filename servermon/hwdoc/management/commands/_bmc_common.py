# -*- coding: utf-8 -*- vim:fileencoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

# Copyright © 2010-2012 Greek Research and Technology Network (GRNET S.A.)
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHORS DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
'''
Django common code for management commands
'''

from django.core.management.base import CommandError
from hwdoc.models import ServerManagement
from hwdoc.functions import search
from django.utils.translation import ugettext as _

from optparse import make_option

option_list = (
    make_option('-u', '--username',
                action='store',
                type='string',
                dest='username',
                default=None,
                help=_('Provide username used to login to BMC')),
    make_option('-p', '--password',
                action='store',
                type='string',
                dest='password',
                default=None,
                help=_('Provide password used to login to BMC')),
)


def handle(self, *args, **options):
    '''
    Handle command
    '''

    if args is None or len(args) != 1:
        raise CommandError(_('You must supply a key'))
    key = args[0]

    es = search(key)
    if es.count() == 0:
        print(_('No Equipment found'))
        return

    for e in es:
        try:
            e.servermanagement
        except ServerManagement.DoesNotExist:
            continue
        if int(options['verbosity']) > 0:
            print(e)
        opts = options.copy()
        for term in ['username', 'password', 'command']:
            if term in opts:
                opts.pop(term)
        command = getattr(e.servermanagement, options['command'])
        result = command(options['username'], options['password'], **opts)
        # TODO: Figure out what to do with this
        if int(options['verbosity']) > 1:
            print(result)
    return
