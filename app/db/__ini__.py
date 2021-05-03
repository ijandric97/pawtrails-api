# Import all the models, so that Base has them before being imported by Alembic
# FIXME: Not sure if this is correct to be in __ini__.py ?
from app.db.base import Base  # noqa
from app.models.user import User  # noqa
