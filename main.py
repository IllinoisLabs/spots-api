import os

import config as config
from src.app_factory import create_app

if __name__ == "__main__":
    if os.environ["FLASK_ENV"] == "production":
        app = create_app(config.ProductionConfig)
    else:
        app = create_app(config.DevelopmentConfig)
    app.run("0.0.0.0", port=8000)
