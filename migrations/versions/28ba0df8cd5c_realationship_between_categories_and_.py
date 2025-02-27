"""realationship between categories and transactions

Revision ID: 28ba0df8cd5c
Revises: e5e8b20edfdc
Create Date: 2025-02-27 18:26:51.545133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28ba0df8cd5c'
down_revision: Union[str, None] = 'e5e8b20edfdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
