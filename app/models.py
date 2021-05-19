from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.dialects.postgresql import UUID


@as_declarative()
class Base:
    pass


class ParseResults(Base):
    __tablename__ = 'parse_results'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    url = Column(String(255), index=True, nullable=False, comment='url для парсинга')
    date = Column(DateTime, nullable=False, comment='Дата парсинга url')
    result = Column(String(), nullable=False, comment='Результат парсинга')
