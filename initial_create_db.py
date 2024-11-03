import json
import re
import uuid
from enum import Enum

import pandas as pd
from faker import Faker
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.criteria_type import CriteriaType
from src.models.feedback import Feedback
from src.models.feedback_score import FeedbackScore
from src.models.score import Score
from src.models.user import User


class CriteriaTypeEnum(Enum):
    PROFESSIONALISM = 1
    TEAMWORK = 2
    COMMUNICATION_SKILL = 3
    INITIATIVE = 4


criteria_map = {
    "профессионализм": CriteriaTypeEnum.PROFESSIONALISM,
    "командная работа": CriteriaTypeEnum.TEAMWORK,
    "коммуникабельность": CriteriaTypeEnum.COMMUNICATION_SKILL,
    "инициативность": CriteriaTypeEnum.INITIATIVE,
}


def convert_russian_to_enum(russian_word):
    # Приводим входное слово к нижнему регистру и удаляем лишние пробелы
    normalized_word = russian_word.strip().lower()

    # Пытаемся найти соответствующий элемент перечисления
    if normalized_word in criteria_map:
        return criteria_map[normalized_word].name
    else:
        raise ValueError(f"Неизвестный критерий: {russian_word}")




async def init_create_db(db: AsyncSession) -> None:
    async def get_criteria_id(name: str) -> uuid.UUID:
        criteria = await db.execute(
            select(CriteriaType).where(name == CriteriaType.name)
        )
        return criteria.scalars().first().id

    fake = Faker("ru_RU")

    file_path = 'assets/review_dataset.json'
    df = pd.read_json(file_path)

    combined_ids = pd.concat([df['ID_reviewer'], df['ID_under_review']]).drop_duplicates().reset_index(drop=True)
    unique_ids_df = pd.DataFrame(combined_ids, columns=['Unique_ID'])
    unique_ids_df = unique_ids_df.dropna()
    unique_ids_df['Unique_ID'] = unique_ids_df['Unique_ID'].astype(int)

    def generate_full_name_with_gender():
        gender = random.choice(['male', 'female'])
        if gender == 'male':
            return f"{fake.last_name_male()} {fake.first_name_male()} {fake.middle_name_male()}"
        else:
            return f"{fake.last_name_female()} {fake.first_name_female()} {fake.middle_name_female()}"

    unique_ids_df['Name'] = [generate_full_name_with_gender() for _ in range(len(unique_ids_df))]

    unique_companies = [fake.company() for _ in range(100)]
    unique_ids_df['Company'] = [random.choice(unique_companies) for _ in range(len(unique_ids_df))]
    unique_ids_df['Experience'] = [random.randint(1, 35) for _ in range(len(unique_ids_df))]

    print(f"Inserting {len(unique_ids_df)} new users into the database.")

    for index, row in unique_ids_df.iterrows():
        user = User(
            external_id=row['Unique_ID'],
            full_name=row['Name'],
            experience=row['Experience'],
            company=row['Company']
        )
        db.add(user)

    await db.commit()

    for i in criteria_map.values():
        criteria_type = CriteriaType(
            name=i.name
        )
        db.add(criteria_type)
    await db.commit()

    with open("/Users/a.belozerov/PycharmProjects/DevLake_Innoglobalhack/assets/scores_dataset.txt", "r",
              encoding='utf-8') as file:
        data = file.read()

    # Удаляем ненужные строки
    cleaned_data = re.sub(r'LLM Evaluation of Employee based on Reviews: \d+\n', '', data)
    cleaned_data2 = re.sub(r'Ошибка при декодировании JSON для отзыва \d+\. Повторная попытка\.\.\.', '', cleaned_data)

    # Извлечение JSON объектов
    scores_strings = re.findall(r'\{[^}]+\}', cleaned_data2)

    scores = []
    for score_str in scores_strings:
        # Преобразование одинарных кавычек в двойные кавычки
        valid_json_str = re.sub(r"(?<={|,)\s*'([^']*?)'\s*:", r'"\1":', score_str)
        valid_json_str = re.sub(r":\s*'([^']*?)'\s*(?=,|})", r':"\1"', valid_json_str)
        valid_json_str = valid_json_str.replace("'", '')
        valid_json_str = valid_json_str.replace("_", ' ')
        try:
            score = json.loads(valid_json_str)
            scores.append(score)
        except json.JSONDecodeError as e:
            scores.append({})
            print(f"Ошибка декодирования JSON: {e}")
            print(f"Проблемная строка: {valid_json_str}")

    j = 0
    for _, row in df.iterrows():
        reviewer = await db.execute(
            select(User).where(User.external_id == row['ID_reviewer'])
        )
        reviewer = reviewer.scalars().first()

        under_reviewer = await db.execute(
            select(User).where(User.external_id == row['ID_under_review'])
        )
        under_reviewer = under_reviewer.scalars().first()

        if reviewer is None or under_reviewer is None:
            continue

        if j >= len(scores)-2:
            pass
        else:
            print(j, len(scores))

            feedback = Feedback(
                feedback=row['review'],
                informativeness = 0 if scores[j] == {} else scores[j]['информативность'],
                objectivity= 0 if scores[j] == {} else scores[j]['объективность'],
                reviewer_id=reviewer.id,
                under_reviewer_id=under_reviewer.id
            )

            db.add(feedback)

            for k in criteria_map.keys():
                score = Score(
                    score=0 if scores[j] == {} else scores[j][k + ' балл'],
                    commentary='' if scores[j] == {} else scores[j][k + ' объяснение'],
                    criteria_type_id=await get_criteria_id(convert_russian_to_enum(k)),

                )

                db.add(score)

                await db.commit()

                feedback_score = FeedbackScore(
                    score_id=score.id,
                    feedback_id=feedback.id
                )

                db.add(feedback_score)

            j += 1

    await db.commit()
