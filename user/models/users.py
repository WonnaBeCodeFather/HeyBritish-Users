import datetime
import enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class TimestampModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        onupdate=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None))


class Tenant(TimestampModel):
    __tablename__ = 'tenant'

    name: Mapped[str] = mapped_column(String(30))
    users: Mapped[list["User"]] = relationship(back_populates="tenant")


class User(TimestampModel):
    __tablename__ = 'user'

    class Status(str, enum.Enum):
        active = 'active'
        inactive = 'inactive'

    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")
    tutor: Mapped["Tutor"] = relationship("Tutor", back_populates="user")
    student: Mapped["Student"] = relationship("Student", back_populates="user")
    status: Mapped[Status] = mapped_column(default=Status.inactive)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenant.id", name='tenant_constrain'))
    password: Mapped[str]


class Student(TimestampModel):
    __tablename__ = 'student'

    user: Mapped["User"] = relationship("User", back_populates="student", single_parent=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", name='student_user_constrain'))
    tutors: Mapped[list["Tutor"]] = relationship(
        back_populates='students',
        secondary='tutor_student'
    )


class Tutor(TimestampModel):
    __tablename__ = 'tutor'

    user: Mapped["User"] = relationship("User", back_populates="tutor", single_parent=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", name='tutor_user_constrain'))
    rate: Mapped[float]
    cost_per_lesson: Mapped[float] = mapped_column(server_default='0.0')
    students: Mapped[list["Student"]] = relationship(
        back_populates='tutors',
        secondary='tutor_student'
    )


class TutorStudent(TimestampModel):
    __tablename__ = 'tutor_student'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete='CASCADE'),
        primary_key=True, name='student_id'
    )
    tutor_id: Mapped[int] = mapped_column(
        ForeignKey("tutor.id", ondelete='CASCADE'),
        primary_key=True, name='tutor_id'
    )
