from sqlalchemy import Column, TIMESTAMP, func, text, Boolean, BIGINT, ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class VideoInfo(Base):
    __tablename__ = 'videos_info'

    uuid = Column(UUID(as_uuid=True), primary_key=True, index=True, name='uuid',
                  server_default=text('uuid_generate_v4()'))
    author_uuid = Column(UUID(as_uuid=True), nullable=False, index=True, name='author_id')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), name='created_at')
    is_complete = Column(Boolean, nullable=False, server_default='false', name='is_complete')
    likes_count = Column(BIGINT, nullable=False, server_default='0', name='likes_count')
    dislikes_count = Column(BIGINT, nullable=False, server_default='0', name='dislikes_count')
    views_count = Column(BIGINT, nullable=False, server_default='0', name='views_count')
