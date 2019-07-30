from .common import *


FEATURES.update({
    'ENABLE_MEMBERSHIP_INTEGRATION': True,

    # Whether to enable payments
    'ENABLE_PAYMENTS_INTEGRATION': True,
})

if FEATURES.get('ENABLE_MEMBERSHIP_INTEGRATION', False):
    INSTALLED_APPS.append('membership')
        REST_FRAMEWORK.update({'EXCEPTION_HANDLER': 'membership.utils.customer_exception_handler'})

    MEMBERSHIP_ROOT = REPO_ROOT / "../edx-membership"
    sys.path.append(MEMBERSHIP_ROOT)

    MAKO_MODULE_DIR = os.path.join(tempfile.gettempdir(), 'mako_lms')
    MAKO_TEMPLATE_DIRS_BASE.append(
        MEMBERSHIP_ROOT / 'membership' / 'templates',
    )
    STATICFILES_DIRS.append(
        MEMBERSHIP_ROOT / "membership" / "static",
    )

if FEATURES.get('ENABLE_PAYMENTS_INTEGRATION', False):
    ALIPAY_INFO = {
        "basic_info": {
            "KEY": "",
            "PARTNER": "",
            "SELLER_EMAIL": ""
        },
        "other_info": {
            "INPUT_CHARSET": "",
            "INPUT_DIRECT_CHARSET": "",
            "SIGN_TYPE": "",
            "RETURN_URL": "",
            "NOTIFY_URL": "",
            "PAY_RESULT_URL": "",
            "REFUND_NOTIFY_URL": "",
            "SHOW_URL": "",
            "ERROR_NOTIFY_URL": "",
            "TRANSPORT": "",
            "DEFAULT_BANK": "",
            "IT_B_PAY": "",
            "REFUND_URL": ""
        }
    }

    ALIPAY_APP_INFO = {
        "basic_info": {
            "APP_ID": "",
            "APP_PRIVATE_KEY": "",
            "ALIPAY_RSA_PUBLIC_KEY": ""
        },
        "other_info": {
            "SIGN_TYPE": "",
            "NOTIFY_URL": ""
        }
    }

    WECHAT_PAY_INFO = {
        "basic_info": {
            "APPID": "",
            "APPSECRET": "",
            "MCHID": "",
            "KEY": "",
            "ACCESS_TOKEN": ""
        },
        "other_info": {
            "BUY_COURSES_SUCCESS_TEMPLATE_ID": "",
            "BUY_COURSES_SUCCESS_HREF_URL": "",
            "COIN_SUCCESS_TEMPLATE_ID": "",
            "COIN_SUCCESS_HREF_URL": "",
            "SERVICE_TEL": "",
            "NOTIFY_URL": "",
            "JS_API_CALL_URL": "",
            "SSLCERT_PATH": "",
            "SSLKEY_PATH": ""
        }
    }

    WECHAT_APP_PAY_INFO = {
        "basic_info": {
            "APPID": "",
            "APPSECRET": "",
            "MCHID": "",
            "KEY": "",
            "ACCESS_TOKEN": ""
        },
        "other_info": {
            "NOTIFY_URL": ""
        }
    }

    WECHAT_H5_PAY_INFO = {
        "basic_info": {
            "APPID": "",
            "APPSECRET": "",
            "MCHID": "",
            "KEY": "",
            "ACCESS_TOKEN": ""
        },
        "other_info": {
            "SERVICE_TEL": "",
            "NOTIFY_URL": "",
            "JS_API_CALL_URL": "",
            "SSLCERT_PATH": "",
            "SSLKEY_PATH": "",
            "SPBILL_CREATE_IP": ""
        }
    }


#### Templates
TEMPLATES = [
    {
        'NAME': 'django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Don't look for template source files inside installed applications.
        'APP_DIRS': False,
        # Instead, look for template source files in these dirs.
        'DIRS': [
            PROJECT_ROOT / "templates",
            COMMON_ROOT / 'templates',
            COMMON_ROOT / 'lib' / 'capa' / 'capa' / 'templates',
            COMMON_ROOT / 'djangoapps' / 'pipeline_mako' / 'templates',
            COMMON_ROOT / 'static',  # required to statically include common Underscore templates
            MEMBERSHIP_ROOT / 'membership' / 'templates',
        ],
        # Options specific to this backend.
        'OPTIONS': {
            'loaders': [
                # We have to use mako-aware template loaders to be able to include
                # mako templates inside django templates (such as main_django.html).
                'openedx.core.djangoapps.theming.template_loaders.ThemeTemplateLoader',
                'edxmako.makoloader.MakoFilesystemLoader',
                'edxmako.makoloader.MakoAppDirectoriesLoader',
            ],
            'context_processors': CONTEXT_PROCESSORS,
            # Change 'debug' in your environment settings files - not here.
            'debug': False
        }
    },
    {
        'NAME': 'mako',
        'BACKEND': 'edxmako.backend.Mako',
        # Don't look for template source files inside installed applications.
        'APP_DIRS': False,
        # Instead, look for template source files in these dirs.
        'DIRS': _make_mako_template_dirs,
        # Options specific to this backend.
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
            # Change 'debug' in your environment settings files - not here.
            'debug': False,
        }
    },
]
derived_collection_entry('TEMPLATES', 1, 'DIRS')
DEFAULT_TEMPLATE_ENGINE = TEMPLATES[0]
DEFAULT_TEMPLATE_ENGINE_DIRS = DEFAULT_TEMPLATE_ENGINE['DIRS'][:]


def _add_microsite_dirs_to_default_template_engine(settings):
    """
    Derives the final DEFAULT_TEMPLATE_ENGINE['DIRS'] setting from other settings.
    """
    if settings.FEATURES.get('USE_MICROSITES', False) and getattr(settings, "MICROSITE_CONFIGURATION", False):
        DEFAULT_TEMPLATE_ENGINE_DIRS.append(settings.MICROSITE_ROOT_DIR)
    return DEFAULT_TEMPLATE_ENGINE_DIRS


DEFAULT_TEMPLATE_ENGINE['DIRS'] = _add_microsite_dirs_to_default_template_engine
derived_collection_entry('DEFAULT_TEMPLATE_ENGINE', 'DIRS')
