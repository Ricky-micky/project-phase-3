"""product table

Revision ID: cd6f5966754f
Revises: 03239b891f9e
Create Date: 2024-12-20 08:18:02.095221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd6f5966754f'
down_revision: Union[str, None] = '03239b891f9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
