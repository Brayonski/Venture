from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register  # register the application
class HomeApphook(CMSApp):
    app_name = "venturelift_media"
    name = _("Homepage Application")

    def get_urls(self, page=None, language=None, **kwargs):
        return ["venturelift_media.urls"]