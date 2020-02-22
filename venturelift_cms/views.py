# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from venturelift_profiles.models import AllSystemUser
from django.utils import timezone

def make_user(request):
    check_user = AllSystemUser.objects.filter(email=request.POST['email'])
    if check_user is None:
        create_user_email = AllSystemUser(created_at=timezone.now(),username=request.POST['email'],email=request.POST['email'],user_type="Anonymus")

    template = loader.get_template('register.html')
    context = {
        'message': 'Sign Up Successful',
    }
    return HttpResponse(template.render(context, request))

def media_index(request):
        return redirect('en/media')