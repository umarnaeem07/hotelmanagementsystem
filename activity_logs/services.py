from .models import ActivityLog


def log_activity(
    *,
    hotel,
    user,
    action,
    object_type,
    object_id,
    description
):

    ActivityLog.objects.create(
        hotel=hotel,
        user=user,
        action=action,
        object_type=object_type,
        object_id=object_id,
        description=description
    )