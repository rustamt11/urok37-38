from datetime import datetime, timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import Journal

User = get_user_model()


@receiver(post_save, sender=User)
def update_journal_on_user_save(sender, instance, created, **kwargs):
    if not created and instance.Passed_Tests > 0:
        test_results = cache.get(f'test_results_{instance.username}')

        if test_results:
            Journal.objects.create(
                user=instance,
                right_answers=test_results['right_answers'],
                wrong_answers=test_results['wrong_answers'],
                date=datetime.now(timezone.utc)
            )

            cache.delete(f'test_results_{instance.username}')
