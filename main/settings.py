from pathlib import Path
import os
from django.utils.html import mark_safe




BASE_DIR              = Path(__file__).resolve().parent.parent
SECRET_KEY            = 'django-insecure-@imh6cz9cmj99sdj34!ce!7@k+9#emb*_^=qudukfsa&p25'
DEBUG                 = True
ALLOWED_HOSTS         = ['*']
LANGUAGE_CODE         = 'en-us'
TIME_ZONE             = 'Egypt'
USE_I18N              = True
USE_L10N              = True
USE_TZ                = True
DEFAULT_AUTO_FIELD    = 'django.db.models.BigAutoField'
STATIC_URL            = '/static/'
STATIC_ROOT           = os.path.join(BASE_DIR,'RootStaticFiels')
STATICFILES_DIRS      = [os.path.join(BASE_DIR,'StatiFilesDirs')]
MEDIA_URL             = '/media/'
MEDIA_ROOT            = os.path.join(BASE_DIR, 'mediaRoot')

USE_L10N = True
USE_TZ = True  
USE_I18N = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
JAZZMIN_SETTINGS = {
    "language_chooser": False,
    "show_ui_builder" : False,
    "copyright": "Omar Hosny",
    "custom_css": "main.css",
    "site_brand": "Kababge",

    "welcome_sign": mark_safe("السلام عليكم  <br> نظام الاستاذ محمد الكبابجي"),
    "icons" :{
        "Thoth.Recp"         : "fas fa-file-signature",
        "Thoth.Employee"     : "fas fa-head-side-mask",
        "config.CourseType"  : "fas fa-file-signature",
        "config.Clients"     : "fas fa-file-signature",
        "Thoth.Course"       : "fas fa-compact-disc",
        "config.JobPosition" : "fas fa-sort",
        "auth"               : "fas fa-users-cog",
        "auth.user"          : "fas fa-user",
        "users.User"         : "fas fa-user",
        "auth.Group"         : "fas fa-users",
        "admin.LogEntry"     : "fas fa-file",
    }
    } 



INSTALLED_APPS = [
    "jazzmin",  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Thoth',
    "config",
    "lib",
]


MIDDLEWARE = [

    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [

{
    
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [os.path.join(BASE_DIR, "templates")],
'APP_DIRS': False   ,
'OPTIONS': {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
# "from django.template.context_processors.media",
# "from django.template.context_processors.static",
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
},
},
]
WSGI_APPLICATION = 'main.wsgi.application'
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}


AUTH_PASSWORD_VALIDATORS = [
{
'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
},
]


# handler404 = 'api.views.handler'

''' 


JAZZMIN_SETTINGS = {
    "site_title": "your_site_name",
    "site_header": "your_site_header",
    "site_brand": "your_site_brand",
    "site_icon": "images/favicon.png",
    # Add your own branding here
    "site_logo": None,
    "welcome_sign": "Welcome to the your_site_name",
    # Copyright on the footer
    "copyright": "your_site_name",
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "your_site_name", "url": "home", "permissions": ["auth.view_user"]},
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
    },
    # # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    # Uncomment this line once you create the bootstrap-dark.css file
    "custom_css": "css/bootstrap-dark.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}
'''