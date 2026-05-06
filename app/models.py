from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel, UniqueConstraint, func


class Link(SQLModel, table=True):
    __tablename__ = "links"
    __table_args__ = (UniqueConstraint("short_name", name="uq_links_short_name"),)

    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str = Field(index=True)
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
