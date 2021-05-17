from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from .views import get_pdf_url

urlpatterns = (
    url(
        r'^pdf/(?P<file_path>.*)',
        get_pdf_url,
        name='pdf_get_url',
    ),
)