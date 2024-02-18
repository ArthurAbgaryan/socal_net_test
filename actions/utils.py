from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone


#фу-ия для создания обекта класса Action
def create_action(user,verb,target=None):
    #поиск похожего действия совершенного за последнюю минуту
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                           verb=verb,
                                           date_created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct = target_ct, target_id = target.id)

    if not similar_actions:
         # похожее действие не найдено , создаем новое
         action = Action(user = user, verb = verb, target = target)
         action.save()
         return True
    return False