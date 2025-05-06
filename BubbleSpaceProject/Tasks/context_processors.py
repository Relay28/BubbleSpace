from django.utils.timezone import now, timedelta
from .models import Task

def notifications_context(request):
    if request.user.is_authenticated:
        nearing_deadline_tasks = Task.objects.filter(
            created_by=request.user,
            project__isnull=True,
            due_date__lte=now() + timedelta(days=1),
            due_date__gte=now()
        )
        return {'nearing_deadline_tasks': nearing_deadline_tasks}
    return {}
