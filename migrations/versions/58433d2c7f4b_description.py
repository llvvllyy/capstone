"""description

Revision ID: 58433d2c7f4b
Revises: cdaea0e5a970
Create Date: 2023-12-12 17:34:14.095891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58433d2c7f4b'
down_revision: Union[str, None] = 'cdaea0e5a970'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user_history', 'id', new_column_name='hist_id')
    op.alter_column('user_history', 'action', new_column_name='hist_action')
    op.alter_column('user_history', 'timestamp', new_column_name='hist_timestamp')


def downgrade() -> None:
    op.alter_column('user_history', 'hist_id', new_column_name='id')
    op.alter_column('user_history', 'hist_action', new_column_name='action')
    op.alter_column('user_history', 'hist_timestamp', new_column_name='timestamp')
