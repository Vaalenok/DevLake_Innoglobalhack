import pandas as pd
from faker import Faker
import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.feedback import Feedback
from src.models.user import User


async def init_create_db(db: AsyncSession) -> None:
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

        feedback = Feedback(
            feedback=row['review'],
            informativeness=random.uniform(1, 5),
            objectivity=random.uniform(1, 5),
            reviewer_id=reviewer.id,
            under_reviewer_id=under_reviewer.id
        )

        db.add(feedback)

    await db.commit()
