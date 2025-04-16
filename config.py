import os
from flask_appbuilder.security.manager import (
    AUTH_OID,
    AUTH_REMOTE_USER,
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
)

basedir = os.path.abspath(os.path.dirname(__file__))

# Your App secret key
SECRET_KEY = "khoi_sme"
# cau hinh get question
# 0 random all
# 1 random theo phong ban
GET_QUESTION_TYPE=0
# The SQLAlchemy connection string.
# SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
#SQLALCHEMY_DATABASE_URI ="oracle://checkin:123456@10.2.16.206:1521/bip?encoding=utf8"
SQLALCHEMY_DATABASE_URI = 'mysql://checkin_app:APYAYzr1F%40454@10.1.8.85:3306/sms_checkin?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
# SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

# ------------------------------
# GLOBALS FOR APP Builder
# ------------------------------
# Uncomment to setup Your App name
APP_NAME = "SME CHECK IN"

# Uncomment to setup Setup an App icon
APP_ICON = "/static/img/logo.png"

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
# AUTH_TYPE = AUTH_DB
AUTH_TYPE = AUTH_LDAP
AUTH_LDAP_SERVER = "ldap://10.1.6.11"
AUTH_LDAP_USE_TLS = False
AUTH_LDAP_SEARCH = "DC=BANK,DC=MB,DC=GROUP"
AUTH_LDAP_UID_FIELD = "sAMAccountName"
AUTH_LDAP_BIND_USER = "CN=BISystemUser,CN=Users,DC=BANK,DC=MB,DC=GROUP"
AUTH_LDAP_BIND_PASSWORD = "MBmb@2013"
# Uncomment to setup Full admin role name
# AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "AUTH_USERS"
# AUTH_USER_REGISTRATION_ROLE = "AUTH_USERS"
AUTH_USER_REGISTRATION_ROLE = "AUTH_USERS"
# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "en"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "translations"
# The allowed translation for you app
LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
    "pt": {"flag": "pt", "name": "Portuguese"},
    "pt_BR": {"flag": "br", "name": "Pt Brazil"},
    "es": {"flag": "es", "name": "Spanish"},
    "de": {"flag": "de", "name": "German"},
    "zh": {"flag": "cn", "name": "Chinese"},
    "ru": {"flag": "ru", "name": "Russian"},
    "pl": {"flag": "pl", "name": "Polish"},
}
# ---------------------------------------------------
# Image and file configuration
# ---------------------------------------------------
# The file upload folder, when using my_models with files
UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload folder, when using my_models with images
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload url, when using my_models with images
IMG_UPLOAD_URL = "/static/uploads/"
# Setup image size default is (300, 200, True)
IMG_SIZE = (300, 200, True)
FILE_ALLOWED_EXTENSIONS = ("txt", "pdf", "jpeg", "jpg", "gif", "png")
# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "cerulean.css"
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
APP_THEME = "my_app_theme.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
# APP_THEME = "spacelab.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"

# my conn db
# DB_USERNAME="etl"
# DB_PASSWORD="etl123"
# DB_HOST="10.2.16.206"
# DB_PORT=1521
# DB_SERVICE_NAME="bip"
# DB_SID=""
# REMEMBER_COOKIE_REFRESH_EACH_REQUEST=True
