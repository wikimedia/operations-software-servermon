# -*- coding: utf-8 -*- vim:encoding=utf-8:
# vim: tabstop=4:shiftwidth=4:softtabstop=4:expandtab

# Copyright © 2010-2012 Greek Research and Technology Network (GRNET S.A.)
# Copyright © 2012 Faidon Liambotis
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND ISC DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL ISC BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF
# USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.

from servermon.puppet.models import Host, Fact, FactValue
from servermon.updates.models import Package
from servermon.compat import render
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from settings import HOST_TIMEOUT, INSTALLED_APPS
import re

def index(request):
    timeout = datetime.now() - timedelta(seconds=HOST_TIMEOUT)

    hosts = Host.objects.all()
    problemhosts = Host.objects.filter(updated_at__lte=timeout).order_by('-updated_at')
    factcount = Fact.objects.count()
    factvaluecount = FactValue.objects.count()
    updatecount = Host.objects.filter(package__isnull=False).distinct().count()
    packagecount = Package.objects.count()
    securitycount = Package.objects.filter(update__is_security=True).distinct().count()
    if 'servermon.hwdoc' in INSTALLED_APPS:
        hwdoc_installed = True
    else:
        hwdoc_installed = False

    return render(request, "index.html", {
        'problemhosts': problemhosts, 
        'timeout': timeout,
        'hosts': hosts,
        'factcount': factcount,
        'factvaluecount': factvaluecount,
        'updatecount': updatecount,
        'packagecount': packagecount,
        'securitycount': securitycount,
        'hwdoc_installed': hwdoc_installed,
        })

def search(request):
    if not request.POST or (not 'search' in request.POST):
        return HttpResponseRedirect('/')

    fieldmap = [
            ('Hostname', 'fqdn'),
            ('MAC Address', 'macaddress_'),
            ('IPv4 Address', 'ipaddress_'),
            ('IPv6 Address', 'ipaddress6_'),
            ('Vendor', 'manufacturer'),
            ('Model', 'productname'),
            ('Puppet class', 'puppetclass'),
            ('Operating system', 'operatingsystem')
            ]
    
    matches = []
    regex = re.compile(r'(' + request.POST['search'] + ')', re.IGNORECASE)

    base = FactValue.objects.filter(value__icontains=request.POST['search'])
    base = base.distinct().order_by('host__name')

    for name, field in fieldmap:
        res = base
        if field.endswith('_'):
            res = res.filter(fact_name__name__startswith=field)
        else:
            res = res.filter(fact_name__name=field)
        res = res.select_related()

        for r in res:
            matches.append({
                'name': r.host.name,
                'attribute': name,
                'value': regex.sub(r'<strong>\1</strong>', r.value),
                })

    return render(request, "search.html", {
            'matches': matches,
            'search': request.POST['search']
            })
