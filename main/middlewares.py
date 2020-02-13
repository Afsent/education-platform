from .models import SubRubric


def lwm_context_processor(request):
    context = {'rubrics': SubRubric.objects.all()}
    return context
