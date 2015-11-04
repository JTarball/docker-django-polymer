"""
    (Local) Development Settings for django_website project.
        These settings shoudl override whats in settings/base.py.
        You can use this file for experimenting with apps or for specific local settings.
"""
from project.settings.base import *


DEBUG = True
TEMPLATE_DEBUG = True

# ============================================================================ #
# DEBUG
# ============================================================================ #
if DEBUG:
    # ------------------------------------------------------------------------ #
    # General Settings
    # ------------------------------------------------------------------------ #
    LOG_LEVEL = logging.DEBUG

    # Show emails in the console during development.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INTERNAL_IPS = ('127.0.0.1')

    INSTALLED_APPS += (
        &#39;debug_toolbar&#39;,
        &#39;django_nose&#39;, # testing - better functionality
        &#39;django_dynamic_fixture&#39;, # testing - fixtures (best test integration with fixtures. (dynamic data generation)

     )

    #TEMPLATE_CONTEXT_PROCESSORS = (
    #  # ...
    #  'django.contrib.auth.context_processors.auth',
    #  'django.core.context_processors.request',
    #  # ...
    #)

    # ------------------------------------------------------------------------ #
    # Application Settings
    # ------------------------------------------------------------------------ #

    ##########################################################################
    #  debug_toolbar app 
    MIDDLEWARE_CLASSES += ('blog.middleware.WhodidMiddleware',)
        #'debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    DEBUG_TOOLBAR_CONFIG = {
    # If set to True (default), the debug toolbar will show an intermediate
    # page upon redirect so you can view any debug information prior to
    # redirecting. This page will provide a link to the redirect destination
    # you can follow when ready. If set to False, redirects will proceed as
    # normal.
    #'INTERCEPT_REDIRECTS': False,

    # If not set or set to None, the debug_toolbar middleware will use its
    # built-in show_toolbar method for determining whether the toolbar should
    # show or not. The default checks are that DEBUG must be set to True and
    # the IP of the request must be in INTERNAL_IPS. You can provide your own
    # method for displaying the toolbar which contains your custom logic. This
    # method should return True or False.
    #'SHOW_TOOLBAR_CALLBACK': None,

    # An array of custom signals that might be in your project, defined as the
    # python path to the signal.
    #'EXTRA_SIGNALS': [],

    # If set to True (the default) then code in Django itself won't be shown in
    # SQL stacktraces.
    'HIDE_DJANGO_SQL': False,

    # If set to True (the default) then a template's context will be included
    # with it in the Template debug panel. Turning this off is useful when you
    # have large template contexts, or you have template contexts with lazy
    # datastructures that you don't want to be evaluated.
    #    'SHOW_TEMPLATE_CONTEXT': True,

    # If set, this will be the tag to which debug_toolbar will attach the debug
    # toolbar. Defaults to 'body'.
    #    'TAG': 'body',
    }
    ######################## end of debug_toolbar app settings #################
