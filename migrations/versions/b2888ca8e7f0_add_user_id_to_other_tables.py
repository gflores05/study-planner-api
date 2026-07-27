"""add user id to other tables

Revision ID: b2888ca8e7f0
Revises: 9d03edfa428d
Create Date: 2026-07-27 10:43:56.745489

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2888ca8e7f0"
down_revision: Union[str, Sequence[str], None] = "9d03edfa428d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.add_column(
    "study_plan",
    sa.Column(
      "created_by_user_id", sa.Uuid(), sa.ForeignKey("user.id"), nullable=False
    ),
  )
  op.add_column(
    "topic",
    sa.Column(
      "created_by_user_id", sa.Uuid(), sa.ForeignKey("user.id"), nullable=False
    ),
  )
  op.add_column(
    "sub_topic",
    sa.Column(
      "created_by_user_id", sa.Uuid(), sa.ForeignKey("user.id"), nullable=False
    ),
  )
  op.add_column(
    "assessment",
    sa.Column(
      "created_by_user_id", sa.Uuid(), sa.ForeignKey("user.id"), nullable=False
    ),
  )
  op.add_column(
    "question",
    sa.Column(
      "created_by_user_id", sa.Uuid(), sa.ForeignKey("user.id"), nullable=False
    ),
  )


def downgrade() -> None:
  """Downgrade schema."""
  op.drop_column("study_plan", "created_by_user_id")
  op.drop_column("topic", "created_by_user_id")
  op.drop_column("sub_topic", "created_by_user_id")
  op.drop_column("assessment", "created_by_user_id")
  op.drop_column("question", "created_by_user_id")
