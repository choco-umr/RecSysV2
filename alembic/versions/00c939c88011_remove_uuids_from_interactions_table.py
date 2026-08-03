"""remove uuids from interactions table

Revision ID: 00c939c88011
Revises: ad30dffff913
Create Date: 2026-07-29 12:32:02.093852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00c939c88011'
down_revision: Union[str, Sequence[str], None] = 'ad30dffff913'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
