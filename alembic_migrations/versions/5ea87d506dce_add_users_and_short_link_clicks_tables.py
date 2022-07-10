"""Add users and short_link_clicks tables

Revision ID: 5ea87d506dce
Revises: cd5c9400d664
Create Date: 2022-07-10 18:17:52.402855

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5ea87d506dce'
down_revision = 'cd5c9400d664'
branch_labels = None
depends_on = None

USERS_TABLE = 'users'
SHORT_LINK_CLICKS = 'short_link_clicks'

constraint = (f'{SHORT_LINK_CLICKS}_unique_together_user_id_um_id',
              f'{SHORT_LINK_CLICKS}',
              ['user_id', 'url_mapping_id'])


def upgrade():
    op.create_table(
        USERS_TABLE,
        sa.Column('id', sa.INTEGER, primary_key=True, nullable=False, autoincrement=True),
        sa.Column('public_identifier', sa.String(), nullable=False, unique=True)
    )

    op.create_table(
        SHORT_LINK_CLICKS,
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('url_mapping_id', sa.Integer(), sa.ForeignKey('url_mappings.id', ondelete='CASCADE'), nullable=False),
        sa.Column('count', sa.Integer(), default=0, nullable=False)
    )

    op.create_unique_constraint(f'{SHORT_LINK_CLICKS}_unique_together_user_id_id_url_mp_id',
                                f'{SHORT_LINK_CLICKS}',
                                ['user_id', 'url_mapping_id'])


def downgrade():
    op.drop_constraint(f'{SHORT_LINK_CLICKS}_unique_together_user_id_id_url_mp_id',
                       f'{SHORT_LINK_CLICKS}',
                       type_='unique')
    for table in (SHORT_LINK_CLICKS, USERS_TABLE):
        op.drop_table(table)
