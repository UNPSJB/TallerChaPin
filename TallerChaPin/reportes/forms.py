from django.urls import reverse
from django.utils.http import urlencode
from django import forms
from . import models as ordenes
import taller.models as taller
from TallerChaPin.utils import FiltrosForm
from datetime import datetime

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url
    
# Reportes

