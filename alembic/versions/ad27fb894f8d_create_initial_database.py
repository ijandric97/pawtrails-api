"""Create initial database

Revision ID: ad27fb894f8d
Revises:
Create Date: 2021-04-28 21:04:44.384010

"""
# TODO: Finish this revision
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ad27fb894f8d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    pass


def downgrade():
    pass
