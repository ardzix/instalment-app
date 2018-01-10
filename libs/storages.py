import os
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_unicode, smart_str
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage

def generate_name(instance, filename):
    if getattr(settings, "FLATTEN_PATH_NAME", False):
        form = '%Y-%m-%d-%H%M%S'
    else:
        form = '%Y/%m/%d/%H%M%S'

    extension   = os.path.splitext(filename)[1]
    prefix      = os.path.normpath(
        force_unicode(
            timezone.now().strftime(
                smart_str(form)
            )
        )
    )
    suffix     = '%s%s' % (get_random_string(), extension)
    
    return '%s-%s' % (prefix, suffix)

STORAGE_FILE = FileSystemStorage(
    location = settings.MEDIA_ROOT + settings.FILE_FOLDER,
    base_url = settings.MEDIA_URL + settings.FILE_FOLDER
)