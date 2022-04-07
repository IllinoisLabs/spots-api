import os

from dotenv import load_dotenv

# Load environment variables.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class BaseConfig:
    """Do not load this config directly."""

    DEBUG = False
    MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
    MONGO_DB = os.environ["MONGO_DB"]


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    MONGO_DB = os.environ["MONGO_TEST_DB"]
    TESTING = True
