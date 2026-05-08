"""Merge migration heads

Revision ID: 4e006103e09f
Revises: 2df0dfa9e073, c68c0f2619de
Create Date: 2026-05-08 10:26:42.273829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e006103e09f'
down_revision = ('2df0dfa9e073', 'c68c0f2619de')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
