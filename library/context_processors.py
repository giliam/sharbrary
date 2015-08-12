from sharbrary.settings import MEDIA_URL, STATIC_URL

def urls_processor(request):
	return {'MEDIA_URL': MEDIA_URL,'STATIC_URL': STATIC_URL}