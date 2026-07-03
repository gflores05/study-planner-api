"""add grade column

Revision ID: b14822e68a5a
Revises: a14d90a7c9ea
Create Date: 2026-07-03 12:21:09.814622

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b14822e68a5a"
down_revision: Union[str, Sequence[str], None] = "a14d90a7c9ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.add_column("study_plan", sa.Column("grade", sa.Integer(), nullable=False))


def downgrade() -> None:
  """Downgrade schema."""
  op.drop_column("study_plan", "grade")
