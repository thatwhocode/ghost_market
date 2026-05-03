from user_service.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, Integer, DateTime, func
import enum
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from shared_packages.db.enums import CardRarity
if TYPE_CHECKING:
    from shared_packages.db.user import User
    from shared_packages.db.card_template import CardTemplate
    from shared_packages.db.skill_template import SkillTemplate

class Card(Base):
    __tablename__ = "cards"
    card_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id : Mapped[UUID] = mapped_column(ForeignKey("users.id"), default=uuid4)
    rarity: Mapped[CardRarity] = mapped_column(Enum(CardRarity))
    level: Mapped[int] = mapped_column(Integer)
    base_power  : Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    template_id : Mapped[int] = mapped_column(ForeignKey("card_template.id"))
    owner: Mapped["User"] = relationship("User", back_populates="cards")
    template: Mapped["CardTemplate"] = relationship("CardTemplate", back_populates="cards")
class CardToSkill(Base):
    __tablename__ = "card_skills"
    template_id: Mapped[int] = mapped_column(ForeignKey("card_template.id"), primary_key=True )
    skill_id : Mapped[int] = mapped_column(ForeignKey("skills.id"), primary_key=True)