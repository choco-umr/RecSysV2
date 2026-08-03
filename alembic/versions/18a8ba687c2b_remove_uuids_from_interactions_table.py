"""remove uuids from interactions table

Revision ID: 18a8ba687c2b
Revises: 425cded4b3db
Create Date: 2026-07-29 12:35:07.630630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18a8ba687c2b'
down_revision: Union[str, Sequence[str], None] = '425cded4b3db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
