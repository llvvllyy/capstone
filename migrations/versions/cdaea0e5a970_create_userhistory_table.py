"""create UserHistory table

Revision ID: cdaea0e5a970
Revises: 5472e2304b48
Create Date: 2023-12-12 17:26:06.024075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdaea0e5a970'
down_revision: Union[str, None] = '5472e2304b48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_history',
        sa.Column('hist_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('hist_action', sa.String(length=255), nullable=False),
        sa.Column('hist_timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('hist_id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    op.drop_table('user_history')
