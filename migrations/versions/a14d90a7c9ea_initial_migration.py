"""initial migration

Revision ID: a14d90a7c9ea
Revises:
Create Date: 2026-07-01 14:20:37.556562

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sap
from alembic import op

from src.infrastructure.adapters.outbound.persistence.models.question_model import (
  AnswerModel,
)
from src.infrastructure.adapters.outbound.persistence.util.jsonb_dataclass import (
  JSONBDataClassArray,
)

# revision identifiers, used by Alembic.
revision: str = "a14d90a7c9ea"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  op.create_table(
    "study_plan",
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("created_on", sa.DateTime, nullable=False),
    sa.Column("modified_on", sa.DateTime, nullable=False),
    sa.Column("version", sa.Integer, nullable=False),
    sa.Column("subject", sa.String(100), nullable=False),
    sa.Column("level", sa.String(24), nullable=False),
    sa.Column("status", sa.String(16), nullable=False),
  )

  op.create_table(
    "topic",
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("created_on", sa.DateTime, nullable=False),
    sa.Column("modified_on", sa.DateTime, nullable=False),
    sa.Column("version", sa.Integer, nullable=False),
    sa.Column("title", sa.String(100), nullable=False),
    sa.Column("study_plan_id", sa.Uuid, sa.ForeignKey("study_plan.id"), nullable=False),
  )

  op.create_table(
    "sub_topic",
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("created_on", sa.DateTime, nullable=False),
    sa.Column("modified_on", sa.DateTime, nullable=False),
    sa.Column("version", sa.Integer, nullable=False),
    sa.Column("title", sa.String(100), nullable=False),
    sa.Column("study_material", sap.JSONB, nullable=False),
    sa.Column("topic_id", sa.Uuid, sa.ForeignKey("topic.id"), nullable=False),
  )

  op.create_table(
    "assessment",
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("created_on", sa.DateTime, nullable=False),
    sa.Column("modified_on", sa.DateTime, nullable=False),
    sa.Column("version", sa.Integer, nullable=False),
    sa.Column("status", sa.String(16), nullable=False),
    sa.Column("score", sa.Integer, nullable=True),
    sa.Column("started_on", sa.DateTime, nullable=True),
    sa.Column("completed_on", sa.DateTime, nullable=True),
    sa.Column("topic_id", sa.Uuid, sa.ForeignKey("topic.id"), nullable=False),
  )

  op.create_table(
    "question",
    sa.Column("id", sa.Uuid, primary_key=True),
    sa.Column("created_on", sa.DateTime, nullable=False),
    sa.Column("modified_on", sa.DateTime, nullable=False),
    sa.Column("version", sa.Integer, nullable=False),
    sa.Column("text", sa.String(100), nullable=False),
    sa.Column("options", JSONBDataClassArray(AnswerModel), nullable=False),
    sa.Column("answer", sa.String(1), nullable=False),
    sa.Column("selected_answer", sa.String(1), nullable=False),
    sa.Column("assessment_id", sa.Uuid, sa.ForeignKey("assessment.id"), nullable=False),
  )


def downgrade() -> None:
  """Downgrade schema."""
  op.drop_table("question")
  op.drop_table("assessment")
  op.drop_table("sub_topic")
  op.drop_table("topic")
  op.drop_table("study_plan")
