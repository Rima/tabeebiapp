
from django.http import Http404, HttpResponse
from tabeebi.directory.models import Provider
from django.utils.simplejson import dumps



def serializer(request):

    AVAILABLE_MODELS = {
        'Directory' : Provider,
        }

    type = request.GET.get("type", "json")
    model_name = request.GET.get("model", "Directory")
    limit = request.GET.get("limit", 10)
    fields = request.GET.get("fields", None)
    if not fields:
        fields = ('id',)
    else:
        fields = tuple(fields.split(","))

    #do some checks on data
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    else:
        if limit > 200: limit=10
    if model_name not in AVAILABLE_MODELS.keys():
        raise Http404
    if type not in ("json", "xml"): type="json"


    model = AVAILABLE_MODELS[model_name]

    filters = {}

    data = model.objects.filter( **filters )[:limit]
    j_data = { 'providers' : [ item.to_json() for item in data ]}
    return HttpResponse( dumps( j_data ) )



