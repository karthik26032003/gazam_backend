from datetime import datetime
from sqlalchemy import String, Text, JSON, DateTime, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
import enum


class UserType(str, enum.Enum):
    unknown = "unknown"
    buyer = "buyer"
    seller = "seller"
    agent = "agent"
    loan = "loan"


class LeadType(str, enum.Enum):
    buyer = "buyer"
    seller = "seller"
    agent = "agent"
    loan = "loan"
    support = "support"


class LeadStatus(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    closed = "closed"


class MessageDirection(str, enum.Enum):
    inbound = "inbound"
    outbound = "outbound"


class TemplateStatus(str, enum.Enum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class BroadcastStatus(str, enum.Enum):
    draft = "draft"
    queued = "queued"
    running = "running"
    done = "done"
    failed = "failed"


class WAUser(Base):
    __tablename__ = "wa_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=True)
    user_type: Mapped[UserType] = mapped_column(SAEnum(UserType), default=UserType.unknown)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WASession(Base):
    __tablename__ = "wa_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(20), index=True)
    current_flow: Mapped[str] = mapped_column(String(50), nullable=True)
    current_step: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WAMessage(Base):
    __tablename__ = "wa_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    wa_message_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), index=True)
    direction: Mapped[MessageDirection] = mapped_column(SAEnum(MessageDirection))
    message_type: Mapped[str] = mapped_column(String(30))
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(20), default="sent")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class WALead(Base):
    __tablename__ = "wa_leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(20), index=True)
    lead_type: Mapped[LeadType] = mapped_column(SAEnum(LeadType))
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[LeadStatus] = mapped_column(SAEnum(LeadStatus), default=LeadStatus.new)
    ai_score: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WATemplate(Base):
    __tablename__ = "wa_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[str] = mapped_column(String(50))
    language: Mapped[str] = mapped_column(String(10), default="en")
    components: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[TemplateStatus] = mapped_column(SAEnum(TemplateStatus), default=TemplateStatus.draft)
    meta_template_id: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WABroadcast(Base):
    __tablename__ = "wa_broadcasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    template_id: Mapped[int] = mapped_column(Integer, nullable=True)
    recipients: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[BroadcastStatus] = mapped_column(SAEnum(BroadcastStatus), default=BroadcastStatus.draft)
    sent_count: Mapped[int] = mapped_column(Integer, default=0)
    delivered_count: Mapped[int] = mapped_column(Integer, default=0)
    read_count: Mapped[int] = mapped_column(Integer, default=0)
    failed_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
