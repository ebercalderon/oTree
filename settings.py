from os import environ


SESSION_CONFIGS = [
    dict(
        name='dropout_end_game',
        display_name="Dropout end game",
        app_sequence=['dropout_end_game', 'payment_info'],
        num_demo_participants=3,
    ),
    dict( 
        name='random_num_rounds_multiplayer', 
        display_name="Random num rounds multiplayer", 
        app_sequence=['random_num_rounds_multiplayer', 'payment_info'],
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='live_demo', 
        display_name='Room for live demo (no participant labels)'
    ),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '8562055223473'

INSTALLED_APPS = ['otree']
