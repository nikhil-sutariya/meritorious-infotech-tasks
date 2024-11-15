from django.core.exceptions import ObjectDoesNotExist

def get_or_raise(model, obj_id, error_message):
    if obj_id:
        try:
            return model.objects.get(id=obj_id)
        except model.DoesNotExist:
            raise ObjectDoesNotExist(error_message)
    return model.objects.all()
