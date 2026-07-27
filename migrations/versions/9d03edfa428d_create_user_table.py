"""create user table

Revision ID: 9d03edfa428d
Revises: 42adcd89468f
Create Date: 2026-07-24 14:21:07.196115

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9d03edfa428d"
down_revision: Union[str, Sequence[str], None] = "42adcd89468f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    "user",
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("created_on", sa.DateTime, nullable=False),
    sa.Column("modified_on", sa.DateTime, nullable=False),
    sa.Column("version", sa.Integer, nullable=False),
    sa.Column("external_id", sa.String(255), nullable=False, unique=True),
    sa.Column("email", sa.String(320), nullable=False, unique=True),
    sa.Column("name", sa.String(100), nullable=False),
    sa.Column("picture", sa.String(255), nullable=True),
    sa.Column("provider", sa.String(100), nullable=False),
    sa.Column("status", sa.String(15), nullable=False),
  )


def downgrade() -> None:
  """Downgrade schema."""
  pass
