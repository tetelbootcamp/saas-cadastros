from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class State(Base):
    __tablename__ = "state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(Integer, index=True)
    country_id: Mapped[int] = mapped_column(
        ForeignKey("country.id", ondelete="RESTRICT"),
        index=True
    )

    code: Mapped[str] = mapped_column(String(2), nullable=False)   # UF
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    __table_args__ = (
        UniqueConstraint("tenant_id", "country_id", "code", name="uq_state_tenant_country_code"),
        UniqueConstraint("tenant_id", "country_id", "name", name="uq_state_tenant_country_name"),
        Index("ix_state_tenant_country", "tenant_id", "country_id"),
    )
