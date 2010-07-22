import settings

DATABASE_ENGINE = 'sqlite3'         # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = settings.PROJECT_PATH +'/nevede.sqlite'   # Or path to database file if using sqlite3.
DATABASE_USER = ''                  # Not used with sqlite3.
DATABASE_PASSWORD = ''              # Not used with sqlite3.
DATABASE_HOST = ''                  # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                  # Set to empty string for default. Not used with sqlite3.

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'CHANGEMENOW'

#Google Analytics
GA_KEY = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jane Doe', 'jane@example.com'),
)

# send emails?
EMAIL = False
