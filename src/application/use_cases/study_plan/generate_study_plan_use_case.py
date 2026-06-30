import asyncio
import json
from datetime import datetime

from src.application.dtos.answer import AnswerAIDTO
from src.application.dtos.question import QuestionAIDTO
from src.application.dtos.study_plan import (
  GeneratedStudyPlanDTO,
  GeneratStudyPlanDTO,
  StudyPlanResponseDTO,
)
from src.application.dtos.sub_topic import SubTopicAIDTO
from src.application.dtos.topic import TopicAIDTO
from src.application.ports.outbound.ai.ai_agent import AIAgent
from src.application.ports.outbound.ai.prompt_provider import PromptProvider
from src.application.ports.outbound.messaging.event_publisher import EventPublisher
from src.application.ports.outbound.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.application.ports.outbound.repositories.question_repository import (
  QuestionRepository,
)
from src.application.ports.outbound.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.application.ports.outbound.repositories.sub_topic_respository import (
  SubTopicRepository,
)
from src.application.ports.outbound.repositories.topic_repository import TopicRepository
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.answer.answer import Answer
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.assessment import AddQuestionParam
from src.domain.question.value_objects.question_text import QuestionText
from src.domain.study_plan.study_plan import AddTopicParams
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.topic.topic import AddSubTopicParams, Topic
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.util.date_util import utc_now
from src.util.result_util import traverse


class GenerateStudyPlanUseCase(UseCaseEventPublisher):
  def __init__(
    self,
    study_plan_repository: StudyPlanRepository,
    topic_repository: TopicRepository,
    sub_topic_repository: SubTopicRepository,
    assessment_repository: AssessmentRepository,
    question_repository: QuestionRepository,
    event_publisher: EventPublisher,
    ai_agent: AIAgent,
    study_plan_prompt_provider: PromptProvider,
  ):
    self.study_plan_repository = study_plan_repository
    self.topic_repository = topic_repository
    self.sub_topic_repository = sub_topic_repository
    self.assessment_repository = assessment_repository
    self.question_repository = question_repository
    self.event_publisher = event_publisher
    self.ai_agent = ai_agent
    self.study_plan_prompt_provider = study_plan_prompt_provider

  async def execute(self, dto: GeneratStudyPlanDTO) -> StudyPlanResponseDTO:
    study_plan = (
      await self.study_plan_repository.get(
        StudyPlanId.parse(dto.study_plan_id).unwrap_or_raise()
      )
    ).get_or_raise(ValueError("StudyPlanNotFound"))

    system_prompt = await self.study_plan_prompt_provider.get_system_prompt(
      {"subject": str(study_plan.subject), "level": str(study_plan.level)}
    )
    prompt = await self.study_plan_prompt_provider.get_prompt(
      {"subject": str(study_plan.subject), "level": str(study_plan.level)}
    )

    response_text = await self.ai_agent.send_content(
      prompt, system_prompt=system_prompt
    )

    generated_study_plan = GeneratedStudyPlanDTO(**json.loads(response_text))

    now = utc_now()

    for ai_topic in generated_study_plan.ts:
      params, ai_questions, ai_sub_topics = self._map_topic_ai_to_parameters(ai_topic)

      topic = study_plan.add_topic(params=params)

      await self.topic_repository.save(topic=topic)

      await self._add_topic_assessment(topic=topic, ai_questions=ai_questions, now=now)
      await self._add_topic_sub_topics(topic=topic, ai_sub_topics=ai_sub_topics)

    study_plan.report_plan_generated(generated_on=now)

    await self.study_plan_repository.save(study_plan=study_plan)

    await self._publish_events(study_plan)

    return StudyPlanResponseDTO(study_plan_id=str(study_plan.id))

  async def _add_topic_assessment(
    self, topic: Topic, ai_questions: list[QuestionAIDTO], now: datetime
  ):
    assessment = topic.generate_assessment(now)

    await self.assessment_repository.save(assessment=assessment)

    questions = [
      assessment.add_question(self._map_question_ai_to_parameters(ai_question))
      for ai_question in ai_questions
    ]

    async with asyncio.TaskGroup() as tg:
      for question in questions:
        tg.create_task(self.question_repository.save(question=question))

  async def _add_topic_sub_topics(
    self, topic: Topic, ai_sub_topics: list[SubTopicAIDTO]
  ):
    sub_topics = [
      topic.add_sub_topic(self._map_sub_topic_ai_to_parameters(ai_sub_topic))
      for ai_sub_topic in ai_sub_topics
    ]

    async with asyncio.TaskGroup() as tg:
      for sub_topic in sub_topics:
        tg.create_task(self.sub_topic_repository.save(sub_topic=sub_topic))

  def _map_topic_ai_to_parameters(self, topicAI: TopicAIDTO):
    params = AddTopicParams(title=TopicTitle.parse(topicAI.t).unwrap_or_raise())

    return params, topicAI.qs, topicAI.st

  def _map_sub_topic_ai_to_parameters(self, subTopicAI: SubTopicAIDTO):
    return AddSubTopicParams(
      title=SubTopicTitle.parse(subTopicAI.t).unwrap_or_raise(),
      study_material=traverse(
        [NonEmptyString.parse(sm) for sm in subTopicAI.sm]
      ).unwrap_or_raise(),
    )

  def _map_question_ai_to_parameters(self, questionAI: QuestionAIDTO):
    return AddQuestionParam(
      text=QuestionText.parse(questionAI.t).unwrap_or_raise(),
      options=[self._map_answer_ai_dto_to_domain(ans) for ans in questionAI.os],
      answer=AnswerOption.parse(questionAI.a).unwrap_or_raise(),
    )

  def _map_answer_ai_dto_to_domain(self, dto: AnswerAIDTO) -> Answer:
    return Answer.create(
      text=NonEmptyString.parse(dto.t).unwrap_or_raise(),
      option=AnswerOption.parse(dto.o).unwrap_or_raise(),
    )
