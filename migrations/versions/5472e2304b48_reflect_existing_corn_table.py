"""Reflect existing Corn Table

Revision ID: 5472e2304b48
Revises: 241137d53ba1
Create Date: 2023-12-12 01:23:57.248985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5472e2304b48'
down_revision: Union[str, None] = '241137d53ba1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'corns', 
        sa.Column('corn_id', sa.Integer(), nullable=False),
        sa.Column('variety_name', sa.String(length=255), unique=True, nullable=False),
        sa.Column('year', sa.Integer()),
        sa.Column('nsic_regnum', sa.String(200)),
        sa.Column('variety_type', sa.String(200)),
        sa.Column('owner', sa.String(length=255)),
        sa.Column('domain', sa.String(length=255)),
        sa.Column('corn_yield', sa.Float()),
        sa.Column('height_dry', sa.Float()),
        sa.Column('height_wet', sa.Float()),
        sa.Column('ear_length', sa.Float()),
        sa.Column('shelling', sa.String(length=100)),
        sa.Column('lodging', sa.String(length=100)),
        sa.Column('reaction', sa.String(length=255)),
        sa.Column('climate', sa.Text()),
        sa.Column('image', sa.LargeBinary(), nullable=True),
        sa.PrimaryKeyConstraint('corn_id')
    )
    
def downgrade() -> None:
    op.drop_table('corn')
