from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.domain_events import (
  AssessmentCompleted,
  AssessmentStarted,
)
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.assessment.value_objects.assessment_score import (
  AssessmentScore,
)
from src.domain.question.question import Question
from src.domain.question.value_objects.question_id import QuestionId
from src.shared.aggregate_root import AggregateRoot
from src.shared.option import Option
from src.shared.result import Result, Unit


class AssessmentStatus(Enum):
  PENDING = "PENDING"
  IN_PROGRESS = "IN_PROGRESS"
  COMPLETED = "COMPLETED"


@dataclass(kw_only=True)
class Assessment(AggregateRoot[AssessmentId]):
  status: AssessmentStatus
  score: Option["AssessmentScore"]
  questions: list[Question]
  started_on: Option[datetime]
  completed_on: Option[datetime]

  @staticmethod
  def create(questions: list[Question]) -> "Assessment":
    return Assessment(
      id=AssessmentId.create(),
      status=AssessmentStatus.PENDING,
      score=Option.nothing(),
      questions=questions,
      started_on=Option.some(datetime.now(UTC)),
      completed_on=Option.some(datetime.now(UTC)),
    )

  @staticmethod
  def reconstitute(
    id: AssessmentId,
    status: AssessmentStatus,
    score: Option[AssessmentScore],
    questions: list[Question],
    started_on: Option[datetime],
    completed_on: Option[datetime],
  ) -> "Assessment":
    return Assessment(
      id=id,
      status=status,
      score=score,
      questions=questions,
      started_on=started_on,
      completed_on=completed_on,
    )

  def start(self, started_on: datetime) -> Result[Unit]:
    if self.status != AssessmentStatus.PENDING:
      return Result.fail("AssessmentNotPending")

    self.started_on = Option.some(started_on)
    self.status = AssessmentStatus.IN_PROGRESS
    self.add_domain_event(
      AssessmentStarted(assessment_id=self.id, started_on=started_on)
    )

    return Result.ok(Unit)

  def complete(self, completed_on: datetime) -> Result[Unit]:
    if self.status != AssessmentStatus.IN_PROGRESS:
      return Result.fail("AssessmentNotInProgress")

    self.completed_on = Option.some(completed_on)
    self.score = Option.some(
      len([question for question in self.questions if question.is_correct])
    )
    self.status = AssessmentStatus.COMPLETED
    self.add_domain_event(
      AssessmentCompleted(assessment_id=self.id, completed_on=completed_on)
    )

    return Result.ok(Unit)

  def answer_question(
    self, question_id: QuestionId, selected_answer: AnswerOption, answer_on: datetime
  ) -> Result[Unit]:
    if self.status != AssessmentStatus.IN_PROGRESS:
      return Result.fail("AssessmentNotInProgress")

    question = next(
      (question for question in self.questions if question.id == question_id), None
    )

    if question is None:
      return Result.fail("QuestionNotFound")

    question.select_answer(selected_answer=selected_answer, answer_on=answer_on)

    return Result.ok(Unit)
