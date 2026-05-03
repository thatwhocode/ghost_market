from sqlalchemy import select
from shared_packages.db.card import Card
from sqlalchemy.ext.asyncio import AsyncSession


class CardRepository():
    def __init__(self, session: AsyncSession):
        self.session = session