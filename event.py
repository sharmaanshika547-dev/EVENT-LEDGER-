from sqlalchemy.orm import Mapped, mapped_column
from .database import Base # Importing the Base we created earlier

class Event(Base):
    __tablename__ = "events"

    # id: int tells Python the type; mapped_column handles the SQL details
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    title: Mapped[str] = mapped_column(nullable=False)
    
    # Keeping user_id as you had it, but usually, this would be a ForeignKey
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, title='{self.title}')>"