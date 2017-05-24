from .dev import DevelopmentConfig
from .test import TestingConfig
from .prod import ProducionConfig


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'prodution': ProducionConfig
}
