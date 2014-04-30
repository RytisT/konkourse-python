# views.py
import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet
from django.contrib.auth.models import User


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = []
    for result in sqs:
        user = User.objects.get(username=result.user)
        suggestion = {
            'id': user.id,
            'username': user.username,
            'label': user.get_full_name(),
            'img': user.get_profile().getImage()
        }
        suggestions.append(suggestion)

    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
