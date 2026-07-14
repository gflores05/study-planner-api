"""make selected_answer nullable

Revision ID: 42adcd89468f
Revises: b14822e68a5a
Create Date: 2026-07-14 13:41:51.243831

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "42adcd89468f"
down_revision: Union[str, Sequence[str], None] = "b14822e68a5a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.alter_column(
    "question", "selected_answer", existing_type=sa.String(1), nullable=True
  )


def downgrade() -> None:
  """Downgrade schema."""
  op.alter_column(
    "question", "selected_answer", existing_type=sa.String(1), nullable=False
  )
