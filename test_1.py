from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import date
from typing import List

Base = declarative_base()

# DB data model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    subscriptions = relationship("Subscription", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean)

    user = relationship("User", back_populates="subscriptions")

# Pydantic models: for serialization
class SubscriptionOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    is_active: bool

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    name: str
    subscriptions: List[SubscriptionOut]

    class Config:
        orm_mode = True

# Main layer
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()


def get_db():
    engine = create_engine(
        "sqlite:///xxx.db",
        pool_pre_ping=True,
    )
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/users/active-subscriptions", response_model=list[UserOut])
def get_users_with_active_subscriptions(db: Session = Depends(get_db)):
    users = (
        db.query(User)
        .join(Subscription)
        .filter(Subscription.is_active == True)
        .options(selectinload(User.subscriptions))
        .order_by(Subscription.start_date)
        .distinct()
        .all()
    )

    return users
