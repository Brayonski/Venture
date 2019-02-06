# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

class VentureliftProfilesConfig(AppConfig):
    name = 'venturelift_profiles'
    verbose_name = "VLA Portal"

    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import User
        registry.register(User)
        registry.register(self.get_model('Supporter'))
        registry.register(self.get_model('Business'))