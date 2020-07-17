import os
from datetime import timedelta


class Config:
    # Flask things
    # secret key for session encryption
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'foo_bar_42'

    @staticmethod
    def get_tm1_instances():
        # There has to be at least one instance.
        #
        instances = []
        instances.append({'address': '127.0.0.1',
                          'port': '8080',
                          'user': 'admin',
                          'password': 'apple',
                          'ssl_verify': False,
                          })

        return instances


    @staticmethod
    def get_cache_timeout():
        return timedelta(hours=1)


    @staticmethod
    def get_ignore_technical_objects():
        return True
