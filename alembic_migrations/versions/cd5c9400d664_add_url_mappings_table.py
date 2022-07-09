"""Add url_mappings table

Revision ID: cd5c9400d664
Revises: 8e66f0ae030b
Create Date: 2022-07-09 20:36:55.175930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd5c9400d664'
down_revision = '8e66f0ae030b'
branch_labels = None
depends_on = None

TABLE = 'url_mappings'


def upgrade():
    op.create_table(
        TABLE,
        sa.Column('id', sa.INTEGER, primary_key=True, nullable=False, autoincrement=True),
        sa.Column('original_url', sa.String(), nullable=False, unique=True),
        sa.Column('short_url', sa.String(), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table(TABLE)
