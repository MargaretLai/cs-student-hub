"""
Environment-specific configurations for CS Student Hub
Handles development, staging, and production settings
"""

from decouple import config
import os


def get_environment():
    """Get current environment from ENV variable"""
    return config("ENVIRONMENT", default="development")


def is_production():
    """Check if running in production"""
    return get_environment() == "production"


def is_development():
    """Check if running in development"""
    return get_environment() == "development"


def get_database_config():
    """Get database configuration based on environment"""
    env = get_environment()

    if env == "production":
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DATABASE_NAME"),
            "USER": config("DATABASE_USER"),
            "PASSWORD": config("DATABASE_PASSWORD"),
            "HOST": config("DATABASE_HOST"),
            "PORT": config("DATABASE_PORT", default="5432"),
            "OPTIONS": {
                "connect_timeout": 20,
                "sslmode": "require",  # Required for production
            },
        }
    elif env == "staging":
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DATABASE_NAME", default="cshub_staging"),
            "USER": config("DATABASE_USER", default="cshub_user"),
            "PASSWORD": config("DATABASE_PASSWORD", default="cshub_password"),
            "HOST": config("DATABASE_HOST", default="localhost"),
            "PORT": config("DATABASE_PORT", default="5432"),
            "OPTIONS": {
                "connect_timeout": 20,
            },
        }
    else:  # development
        database_engine = config("DATABASE_ENGINE", default="sqlite")
        if database_engine == "postgresql":
            return {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("DATABASE_NAME", default="cshub_db"),
                "USER": config("DATABASE_USER", default="cshub_user"),
                "PASSWORD": config("DATABASE_PASSWORD", default="cshub_password"),
                "HOST": config("DATABASE_HOST", default="localhost"),
                "PORT": config("DATABASE_PORT", default="5432"),
                "OPTIONS": {
                    "connect_timeout": 20,
                },
            }
        else:
            # SQLite fallback for development
            from pathlib import Path

            BASE_DIR = Path(__file__).resolve().parent.parent
            return {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }


def get_cors_settings():
    """Get CORS settings based on environment"""
    env = get_environment()

    if env == "production":
        # Production domains - you'll update these when you deploy
        return {
            "ALLOWED_ORIGINS": [
                config("FRONTEND_URL", default="https://your-domain.com"),
                config("ADMIN_URL", default="https://admin.your-domain.com"),
            ],
            "ALLOW_CREDENTIALS": True,
        }
    elif env == "staging":
        return {
            "ALLOWED_ORIGINS": [
                "https://staging.your-domain.com",
                "http://localhost:3000",  # For testing
            ],
            "ALLOW_CREDENTIALS": True,
        }
    else:  # development
        return {
            "ALLOWED_ORIGINS": [
                "http://localhost:3000",  # React default port
                "http://127.0.0.1:3000",
                "http://localhost:8080",  # Alternative ports
                "http://127.0.0.1:8080",
            ],
            "ALLOW_CREDENTIALS": True,
        }


def get_allowed_hosts():
    """Get allowed hosts based on environment"""
    env = get_environment()

    if env == "production":
        return [
            config("DOMAIN_NAME", default="your-domain.com"),
            config("API_DOMAIN", default="api.your-domain.com"),
            config("AWS_ELB_DOMAIN", default=""),  # AWS Load Balancer
        ]
    elif env == "staging":
        return [
            "staging.your-domain.com",
            "localhost",
            "127.0.0.1",
        ]
    else:  # development
        return [
            "localhost",
            "127.0.0.1",
            "0.0.0.0",
        ]


def get_security_settings():
    """Get security settings based on environment"""
    env = get_environment()

    if env == "production":
        return {
            "DEBUG": False,
            "SECURE_SSL_REDIRECT": True,
            "SECURE_HSTS_SECONDS": 31536000,  # 1 year
            "SECURE_HSTS_INCLUDE_SUBDOMAINS": True,
            "SECURE_HSTS_PRELOAD": True,
            "SECURE_CONTENT_TYPE_NOSNIFF": True,
            "SECURE_BROWSER_XSS_FILTER": True,
            "SESSION_COOKIE_SECURE": True,
            "CSRF_COOKIE_SECURE": True,
            "X_FRAME_OPTIONS": "DENY",
        }
    elif env == "staging":
        return {
            "DEBUG": config("DEBUG", default=False, cast=bool),
            "SECURE_SSL_REDIRECT": True,
            "SESSION_COOKIE_SECURE": True,
            "CSRF_COOKIE_SECURE": True,
        }
    else:  # development
        return {
            "DEBUG": config("DEBUG", default=True, cast=bool),
            "SECURE_SSL_REDIRECT": False,
            "SESSION_COOKIE_SECURE": False,
            "CSRF_COOKIE_SECURE": False,
        }


def get_redis_config():
    """Get Redis configuration based on environment"""
    env = get_environment()

    if env == "production":
        return {
            "BROKER_URL": config("REDIS_URL", default="redis://localhost:6379"),
            "RESULT_BACKEND": config("REDIS_URL", default="redis://localhost:6379"),
            "CHANNEL_LAYERS": {
                "default": {
                    "BACKEND": "channels_redis.core.RedisChannelLayer",
                    "CONFIG": {
                        "hosts": [
                            config("REDIS_URL", default="redis://localhost:6379")
                        ],
                    },
                },
            },
        }
    else:  # development and staging
        return {
            "BROKER_URL": "redis://localhost:6379",
            "RESULT_BACKEND": "redis://localhost:6379",
            "CHANNEL_LAYERS": {
                "default": {
                    "BACKEND": "channels_redis.core.RedisChannelLayer",
                    "CONFIG": {
                        "hosts": [("127.0.0.1", 6379)],
                    },
                },
            },
        }


def get_logging_config():
    """Get logging configuration based on environment"""
    env = get_environment()

    if env == "production":
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "verbose": {
                    "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                    "style": "{",
                },
                "simple": {
                    "format": "{levelname} {message}",
                    "style": "{",
                },
            },
            "handlers": {
                "file": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "filename": "/var/log/cshub/django.log",
                    "formatter": "verbose",
                },
                "console": {
                    "level": "ERROR",
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },
            },
            "root": {
                "handlers": ["file", "console"],
                "level": "INFO",
            },
            "loggers": {
                "django": {
                    "handlers": ["file", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
                "dashboard": {
                    "handlers": ["file", "console"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    else:  # development and staging
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "INFO",
            },
            "loggers": {
                "dashboard": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
