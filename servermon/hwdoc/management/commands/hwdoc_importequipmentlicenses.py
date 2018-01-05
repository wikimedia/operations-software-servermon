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
Django management command to import a CSV of BMC licenses
'''

from django.core.management.base import BaseCommand, CommandError
from hwdoc.models import Equipment
from django.utils.translation import ugettext as _
import csv
import io


class Command(BaseCommand):
    '''
    Django management command to import a CSV of BMC licenses
    '''
    help = _('Loads a specific csv to equipment licenses')
    args = "<file>"
    label = _('file name to be imported')

    def handle(self, *args, **options):
        '''
        Handle command
        '''

        if args is None or len(args) != 1:
            raise CommandError(_('You must supply a file name'))
        csvname = args[0]
        licenses = []

        with io.open(csvname, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                (foo, license, serial) = row
                licenses.append(license)

        for eq in Equipment.objects.exclude(servermanagement__isnull=True):
            mgmt = eq.servermanagement
            mgmt.license = licenses.pop()
            mgmt.save()
            print('OK: %s' % eq.serial)

        print(_('OK; %s licenses left') % len(licenses))
