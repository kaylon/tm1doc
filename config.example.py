


class Config:
    # Flask things
    # secret key for session encryption
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'foo_bar_42'

    @staticmethod
    def get_tm1_instances():
        # There has to be at least one instance.
        #
        instances = []
        instances.append({'address': 'https://127.0.0.1:42/api/v1/',
                          'user': 'admin',
                          'password': 'apple',
                          'ssl_verify': False,
                          })

        return instances


    # parsing the complete log might get you into trouble if it is large. There are smarter ways to do it though.
    # if you have trouble set this to false
    @staticmethod
    def process_logs_in_batch():
        return True

    @staticmethod
    def get_cache_timeout():
        return timedelta(hours=1)


    @staticmethod
    def get_ignore_technical_objects():
        return True
