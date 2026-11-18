"""replace auth0 user fields with app managed password auth

Revision ID: c7e1a3f0d2b4
Revises: b2888ca8e7f0
Create Date: 2026-11-12 10:00:00.000000

Existing users were created by Auth0 and have no password, so they (and all the
study plan data that references them) are deleted. This cannot be undone by the
downgrade.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7e1a3f0d2b4"
down_revision: str | Sequence[str] | None = "b2888ca8e7f0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# Children first, so foreign keys are never violated.
_TABLES_TO_WIPE = ["question", "assessment", "sub_topic", "topic", "study_plan", "user"]


def upgrade() -> None:
  """Upgrade schema."""
  for table in _TABLES_TO_WIPE:
    op.execute(sa.text(f'DELETE FROM "{table}"'))

  op.drop_column("user", "external_id")
  op.drop_column("user", "picture")
  op.drop_column("user", "provider")

  op.add_column("user", sa.Column("password_hash", sa.LargeBinary(), nullable=False))
  op.add_column(
    "user",
    sa.Column("last_login_on", sa.DateTime(timezone=True), nullable=True),
  )


def downgrade() -> None:
  """Downgrade schema."""
  for table in _TABLES_TO_WIPE:
    op.execute(sa.text(f'DELETE FROM "{table}"'))

  op.drop_column("user", "last_login_on")
  op.drop_column("user", "password_hash")

  op.add_column(
    "user",
    sa.Column("external_id", sa.String(255), nullable=False, unique=True),
  )
  op.add_column("user", sa.Column("picture", sa.String(255), nullable=True))
  op.add_column("user", sa.Column("provider", sa.String(100), nullable=False))
