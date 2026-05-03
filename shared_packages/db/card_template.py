from user_service.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum
from shared_packages.db.enums import CardRarity, GhostFamily
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from shared_packages.db.card import Card
class CardTemplate(Base):
    __tablename__="card_template"
    id:Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    base_power: Mapped[int] = mapped_column(nullable=False)
    rarity_type : Mapped[CardRarity] = mapped_column(Enum(CardRarity))
    ghost_family : Mapped[GhostFamily] = mapped_column(Enum(GhostFamily))
    image_asset : Mapped[str] = mapped_column(nullable=False)
    cards  = relationship("Card", back_populates="template")