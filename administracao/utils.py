from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import string
from django.http import HttpResponse

from io import StringIO

from django.template.loader import render_to_string
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from datetime import *
from django.db.models import Case, IntegerField, Q, When, Sum
import json


def paginar_registros(request, registros, qtd_por_pagina):
    paginator = Paginator(registros, qtd_por_pagina)
    page = request.GET.get('page')

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)