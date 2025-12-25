from .database import Base, engine
from .models.form_models import FormSubmission, EmailLog


def init_db() -> None:
    """Create all database tables based on SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
