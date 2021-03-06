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
Django management command to populate tickets associated with Equipment
'''

import sys
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l
from django.db import transaction

from hwdoc.functions import populate_tickets, search

from optparse import make_option


class Command(BaseCommand):
    '''
    Django management command to populate tickets associated with Equipment
    '''
    help = _l('Populates tickets for Equipment')
    args = '[key]'

    option_list = BaseCommand.option_list + (
        make_option('-c', '--closed',
                    action='store_true',
                    default=False,
                    dest='closed',
                    help=_l('Populated closed tickets as well')),
    )

    @transaction.commit_on_success
    def handle(self, *args, **options):
        '''
        Handle command
        '''

        if args is None or len(args) != 1:
            raise CommandError(_('You must supply a key'))

        try:
            key = args[0]
        except IndexError:
            print(_('Error in usage. See help'))
            sys.exit(1)

        es = search(key)
        populate_tickets(es, options['closed'])
