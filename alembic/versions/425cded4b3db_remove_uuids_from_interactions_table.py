"""remove uuids from interactions table

Revision ID: 425cded4b3db
Revises: 00c939c88011
Create Date: 2026-07-29 12:32:47.513655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '425cded4b3db'
down_revision: Union[str, Sequence[str], None] = '00c939c88011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
