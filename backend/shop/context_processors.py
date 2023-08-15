import pytz
from datetime import datetime
from django.contrib.sessions.models import Session



def site_settings(request):
    request.session.clear_expired()
    request.session.save()
    request.session.modified = True
    # request.session["foo"] = "bar"

    now = datetime.now()
    datenow = pytz.utc.localize(now)

    context = {
        'datenow': datenow,
        'user': request.user
    }
    return context