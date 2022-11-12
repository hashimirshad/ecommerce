import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-lgpe*4=lbk7&vo)(gfi1rb++iim&#lim-5o6y!0!=zz=uji&=m"

DEBUG = True

ALLOWED_HOSTS = ["yourdomain.com", "127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
    "basket",
    "account",
    "payment",
    "orders",
    "mptt",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # directing to where the template file exists
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.categories",  # for category view in drop down navigation bar for all templates
                "basket.context_processors.basket",  # available for each templates
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = "media/"
# import os will allow access directory system
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Basket session id  so we can call basket session data from setting (skey changed to settings.basket)
BASKET_SESSION_ID = "basket"

# Stripe Payment
os.environ.setdefault(
    "STRIPE_PUBLISHABLE_KEY",
    "pk_test_51LrnhHSB7ADfnySMZhBoCO5xXBRuY3eaYenatu878oanxTSjsJieNUFWlmjKOF4or7oqV5xFPosnu9Wck9SrgAt900US6O66yI",
)
STRIPE_SECRET_KEY = (
    "sk_test_51LrnhHSB7ADfnySMP7Ef2EbluaBBBnPeIWlEg2qT0PkRXSHtkktIj1x8EKswvnjede7jaRDb06lSozUn2KlLwhCT00N3nKSPrT"
)
# endpoint seceret is mandatory for working webhook and collecting payment status
STRIPE_ENDPOINT_SECRET = "whsec_63bdeb2ebb7044e6bb3ce87096957016eaf681e0b2291d90aaab4921fdd9337e"
# following command is mandatatory to listen the above stripe data
# stripe listen --forward-to localhost:8000/payment/webhook/

# Custom user model
AUTH_USER_MODEL = "account.Customer"  # where the class file
LOGIN_REDIRECT_URL = "/account/dashboard"  # url to look when user login viwes in action
LOGIN_URL = "/account/login/"

# PASSWORD+RESET_TIMEOUT_DAYS =2 will give howmany days will valid the tokken data visit documentation

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Stripe Payment
# PUBLISHABLE_KEY = 'pk_test_51LrnhHSB7ADfnySMZhBoCO5xXBRuY3eaYenatu878oanxTSjsJieNUFWlmjKOF4or7oqV5xFPosnu9Wck9SrgAt900US6O66yI'
# SECRET_KEY = 'sk_test_51LrnhHSB7ADfnySMP7Ef2EbluaBBBnPeIWlEg2qT0PkRXSHtkktIj1x8EKswvnjede7jaRDb06lSozUn2KlLwhCT00N3nKSPrT'
