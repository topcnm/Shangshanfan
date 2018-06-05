# coding=utf-8
from flask_sqlalchemy import SQLAlchemy
import logging


# DB ORM
db = SQLAlchemy()

# Log recorder
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

handler = logging.FileHandler('./log/log.txt')
handler.setLevel(level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
