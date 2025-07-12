from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'

    def ready(self):
        if os.environ.get('RUN_ONCE', 'true') == 'true':
            User = get_user_model()
            try:
                user, created = User.objects.get_or_create(
                    username='a',
                    defaults={
                        'email': 'admin@example.com',
                        'is_superuser': True,
                        'is_staff': True,
                    }
                )

                # Always update password to 'ab'
                user.set_password('ab')
                user.is_superuser = True
                user.is_staff = True
                user.save()

                if created:
                    print('[INFO] Superuser "a" created with password "ab".')
                else:
                    print('[INFO] Superuser "a" already existed — password reset to "ab".')

            except Exception as e:
                print(f'[ERROR] Could not create or update superuser: {e}')