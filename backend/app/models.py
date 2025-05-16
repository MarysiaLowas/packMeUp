import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional, TypeVar

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.crud import CrudMixin


# Define a proper typed base class for SQLAlchemy models
class Base(DeclarativeBase, CrudMixin):
    """Base class for all SQLAlchemy models with typing support."""

    pass


# Define type variables for type annotations
ModelType = TypeVar("ModelType", bound=Base)

# Association table for Many-to-Many relationship between Trips and Tags
trip_tags_table = Table(
    "trip_tags",
    Base.metadata,
    Column(
        "trip_id",
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# Association table for Many-to-Many relationship between SpecialLists and Tags
special_list_tags_table = Table(
    "special_list_tags",
    Base.metadata,
    Column(
        "special_list_id",
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("special_lists.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=expression.false()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    trips: Mapped[List["Trip"]] = relationship(
        "Trip", back_populates="user", cascade="all, delete-orphan"
    )
    special_lists: Mapped[List["SpecialList"]] = relationship(
        "SpecialList", back_populates="user", cascade="all, delete-orphan"
    )
    generated_lists: Mapped[List["GeneratedList"]] = relationship(
        "GeneratedList", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship
    user: Mapped["User"] = relationship("User", backref="active_session")

    def __repr__(self):
        return f"<ActiveSession(user_id={self.user_id}, expires_at={self.expires_at})>"


class Item(Base):
    __tablename__ = "items"
    # Note: CHECK constraint 'weight >= 0' should be added in migration
    __table_args__ = (
        CheckConstraint("weight >= 0", name="check_item_weight_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    weight: Mapped[Optional[float]] = mapped_column(Numeric(5, 3), nullable=True)
    dimensions: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # "WxHxD"
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    # Relationship to the association object for special lists
    special_list_associations: Mapped[List["SpecialListItem"]] = relationship(
        "SpecialListItem", back_populates="item", cascade="all, delete-orphan"
    )
    # Relationship to generated list items (referencing this item)
    generated_list_items: Mapped[List["GeneratedListItem"]] = relationship(
        "GeneratedListItem", back_populates="original_item"
    )  # No cascade needed here for deletion restriction

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}')>"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships (Many-to-Many through association tables)
    trips: Mapped[List["Trip"]] = relationship(
        "Trip", secondary=trip_tags_table, back_populates="tags"
    )
    special_lists: Mapped[List["SpecialList"]] = relationship(
        "SpecialList", secondary=special_list_tags_table, back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"


class Trip(Base):
    __tablename__ = "trips"
    # Note: CHECK constraints 'duration_days > 0' and 'num_adults >= 0' should be added in migration
    __table_args__ = (
        CheckConstraint("duration_days > 0", name="check_trip_duration_positive"),
        CheckConstraint("num_adults >= 0", name="check_trip_num_adults_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    destination: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    num_adults: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    children_ages: Mapped[Optional[List[int]]] = mapped_column(
        ARRAY(Integer), nullable=True
    )
    accommodation: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Enum managed by app
    catering: Mapped[Optional[List[int]]] = mapped_column(
        ARRAY(Integer), nullable=True
    )  # List selection managed by app
    transport: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Enum managed by app
    activities: Mapped[Optional[List[str]]] = mapped_column(
        ARRAY(String), nullable=True
    )
    season: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )  # Enum managed by app
    available_luggage: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )  # Schema validated by app
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="trips")
    # One-to-One relationship with GeneratedList
    generated_list: Mapped["GeneratedList"] = relationship(
        "GeneratedList",
        back_populates="trip",
        uselist=False,
        cascade="all, delete-orphan",
    )
    # Many-to-Many relationship with Tags
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=trip_tags_table, back_populates="trips"
    )

    def __repr__(self):
        return f"<Trip(id={self.id}, destination='{self.destination}', user_id={self.user_id})>"


class SpecialList(Base):
    __tablename__ = "special_lists"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String, nullable=False)  # Enum managed by app
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Properties to support Pydantic DTO field names
    @property
    def userId(self) -> uuid.UUID:
        return self.user_id

    @property
    def createdAt(self) -> datetime:
        return self.created_at

    @property
    def updatedAt(self) -> datetime:
        return self.updated_at

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="special_lists")
    # Many-to-Many relationship with Tags
    tags: Mapped[List["Tag"]] = relationship(
        "Tag", secondary=special_list_tags_table, back_populates="special_lists"
    )
    # Relationship to the association object for items
    item_associations: Mapped[List["SpecialListItem"]] = relationship(
        "SpecialListItem", back_populates="special_list", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<SpecialList(id={self.id}, name='{self.name}', user_id={self.user_id})>"
        )


class SpecialListItem(Base):
    """Association object between SpecialList and Item, including quantity."""

    __tablename__ = "special_list_items"
    # Note: CHECK constraint 'quantity > 0' should be added in migration
    __table_args__ = (
        CheckConstraint(
            "quantity > 0", name="check_special_list_item_quantity_positive"
        ),
    )

    special_list_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("special_lists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")

    # Relationships
    special_list: Mapped["SpecialList"] = relationship(
        "SpecialList", back_populates="item_associations"
    )
    item: Mapped["Item"] = relationship(
        "Item", back_populates="special_list_associations"
    )

    def __repr__(self):
        return f"<SpecialListItem(special_list_id={self.special_list_id}, item_id={self.item_id}, quantity={self.quantity})>"


class GeneratedList(Base):
    __tablename__ = "generated_lists"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Unique constraint ensures 1:1 relationship with Trip
    trip_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Properties to support Pydantic DTO field names
    @property
    def userId(self) -> uuid.UUID:
        return self.user_id

    @property
    def tripId(self) -> uuid.UUID:
        return self.trip_id

    @property
    def createdAt(self) -> datetime:
        return self.created_at

    @property
    def updatedAt(self) -> datetime:
        return self.updated_at

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="generated_lists")
    # One-to-One relationship back to Trip
    trip: Mapped["Trip"] = relationship("Trip", back_populates="generated_list")
    # One-to-Many relationship with GeneratedListItem
    items: Mapped[List["GeneratedListItem"]] = relationship(
        "GeneratedListItem",
        back_populates="generated_list",
        cascade="all, delete-orphan",
        order_by="GeneratedListItem.created_at",
    )

    def __repr__(self):
        return (
            f"<GeneratedList(id={self.id}, name='{self.name}', user_id={self.user_id})>"
        )


class GeneratedListItem(Base):
    __tablename__ = "generated_list_items"
    # Note: CHECK constraints 'quantity > 0' and 'item_weight >= 0' should be added in migration
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_gen_list_item_quantity_positive"),
        CheckConstraint(
            "item_weight >= 0", name="check_gen_list_item_weight_non_negative"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    generated_list_id: Mapped[uuid.UUID] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("generated_lists.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # item_id is nullable=True and ON DELETE RESTRICT allows keeping the item in the list even if the original global item is deleted (as per schema notes)
    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("items.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    is_packed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=expression.false()
    )
    # Copied item details at the time of generation
    item_name: Mapped[str] = mapped_column(String, nullable=False)
    item_weight: Mapped[Optional[float]] = mapped_column(Numeric(5, 3), nullable=True)
    item_dimensions: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    item_category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Properties to support Pydantic DTO field names
    @property
    def generatedListId(self) -> uuid.UUID:
        return self.generated_list_id

    @property
    def itemId(self) -> Optional[uuid.UUID]:
        return self.item_id

    @property
    def itemName(self) -> str:
        return self.item_name

    @property
    def isPacked(self) -> bool:
        return self.is_packed

    @property
    def itemWeight(self) -> Optional[float]:
        return self.item_weight

    @property
    def itemDimensions(self) -> Optional[str]:
        return self.item_dimensions

    @property
    def itemCategory(self) -> Optional[str]:
        return self.item_category

    @property
    def createdAt(self) -> datetime:
        return self.created_at

    @property
    def updatedAt(self) -> datetime:
        return self.updated_at

    # Relationships
    generated_list: Mapped["GeneratedList"] = relationship(
        "GeneratedList", back_populates="items"
    )
    # Optional relationship back to the original Item for reference
    original_item: Mapped[Optional["Item"]] = relationship(
        "Item", back_populates="generated_list_items"
    )

    def __repr__(self):
        status = "Packed" if self.is_packed else "Unpacked"
        return f"<GeneratedListItem(id={self.id}, name='{self.item_name}', qty={self.quantity}, status='{status}', list_id={self.generated_list_id})>"


# Example usage (optional, for testing or setup)
# if __name__ == "__main__":
#     # Replace with your actual database URL
#     DATABASE_URL = "postgresql+psycopg2://user:password@host:port/database"
#     engine = create_engine(DATABASE_URL)
#
#     # Create tables (use Alembic for production migrations)
#     # Base.metadata.create_all(bind=engine)
#
#     print("SQLAlchemy models defined.")
