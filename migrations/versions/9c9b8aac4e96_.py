"""empty message

Revision ID: 9c9b8aac4e96
Revises: fad20242c9e3_
Create Date: 2024-06-30 22:18:33.620008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c9b8aac4e96'
down_revision: Union[str, None] = 'fad20242c9e3_'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
