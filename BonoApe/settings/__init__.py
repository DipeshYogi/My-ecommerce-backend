import os

if os.environ.get('IS_DEV'):
    from .dev_settings import *
else:
    from .prod_settings import *
    