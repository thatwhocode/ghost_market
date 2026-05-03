from user_service.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class SkillTemplate(Base):
    __tablename__  = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50),nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    damage: Mapped[int] = mapped_column(Integer, default=1)