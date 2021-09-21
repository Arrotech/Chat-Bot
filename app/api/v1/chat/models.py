from enum import unique

from sqlalchemy.sql.expression import null
from app.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text
from sqlalchemy import inspect


class Question(db.Model):
    """Questions model."""
    __tablename__ = 'questions'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   server_default=sa_text("uuid_generate_v4()"))
    question = db.Column(db.String(500), unique=False)
    answer = db.Column(db.String(500), unique=False)

    def as_dict(self):
        """Get records as a dictionary."""
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        """Print question object."""
        return "<Question '{}'>".format(self.question)
