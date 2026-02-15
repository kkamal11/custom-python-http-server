from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path

settings.configure(
    DEBUG=True,
    SECRET_KEY="super-secret-key-1234567890$@qwertyuiop",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[],
)


def home(request):
    return HttpResponse("Hello from Django via custom HTTP server!")


urlpatterns = [
    path("", home),
]

app = get_wsgi_application()
