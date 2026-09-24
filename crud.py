from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User, Plan


def get_user(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(User).where(
            User.user_id == user_id
        )
    )


def save_user(
    db: Session,
    data
):

    user = get_user(
        db,
        data.user_id
    )

    if user:

        user.name = data.name
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity

    else:

        user = User(
            user_id=data.user_id,
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity
        )

        db.add(user)

    db.commit()
    db.refresh(user)

    return user


def save_plan(
    db: Session,
    user_id: str,
    original_plan: str,
    nutrition_tip: str
):

    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)

    db.commit()

    db.refresh(plan)

    return plan


def get_latest_plan(
    db: Session,
    user_id: str
):

    return db.scalar(
        select(Plan)
        .where(
            Plan.user_id == user_id
        )
        .order_by(
            Plan.id.desc()
        )
    )


def update_plan(
    db: Session,
    plan: Plan,
    updated_plan: str,
    feedback: str
):

    plan.updated_plan = updated_plan
    plan.feedback = feedback
    plan.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(plan)

    return plan


def get_all_users(db: Session):

    return db.scalars(
        select(User)
        .order_by(User.id.desc())
    ).all()


def get_all_plans(db: Session):

    return db.scalars(
        select(Plan)
        .order_by(Plan.id.desc())
    ).all()