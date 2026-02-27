from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(Integer, index=True)
    state_id: Mapped[int] = mapped_column(
        ForeignKey("state.id", ondelete="RESTRICT"),
        index=True
    )

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    ibge_code: Mapped[str | None] = mapped_column(String(10), nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "state_id", "name", name="uq_city_tenant_state_name"),
        Index("ix_city_tenant_state", "tenant_id", "state_id"),
    )
