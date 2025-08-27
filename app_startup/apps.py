import time
from django.apps import AppConfig
from .cache import APP_CACHE

class AppStartupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_startup'

    def ready(self):
        """This method is called when the app is ready"""
        print("--> AppStartupConfig.ready() is called")

        # Ensure this is idempotent: only run the expensive task once

        if not APP_CACHE.get('is_warmed_up'):
            print("Cache is cold. Warming up now...")

            # Similate an expensive operation, like loading data from a file or DB
            time.sleep(0)
            expensive_data = {"user_count": 1000, "version": "1.2.3"}
            APP_CACHE['data'] = expensive_data
            APP_CACHE['is_warmed_up'] = True

            print("Cache has been warmed up! ")
        else:
            print("Cache is already warm")
        
        

