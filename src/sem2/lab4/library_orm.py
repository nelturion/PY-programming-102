"""
Разработайте простую модель системы бронирования книг в библиотеке, используя SQLAlchemy ORM (без использования Flask/Django).
Система должна включать следующие сущности:
User
1. id (int, primary key)
2. name (string, not null)
3. email (string, unique, not null)

Book
1. id (int, primary key)
2. title (string, not null)
3. author (string, not null)
4. copies_available (int)

Booking
1. id (int, primary key)
2. user_id (foreign key → User.id)
3. book_id (foreign key → Book.id)
4. booking_date (date)

Необходимо:
Использовать SQLAlchemy ORM для определения моделей.
Настроить SQLite-базу данных для хранения данных. Если хотите - можете любую другую (например Postgres).
Рекомендую поднимать базу данных в docker-контейнере и подключаться к ней. Команды можно найти в интернете, например по
запросу create docker container with postgres database первая ссылка дает ответ - https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/
Создать таблицы в базе данных через Base.metadata.create_all().

Необходимо реализовать функции:
Добавление пользователя.
Добавление книги.
Создание бронирования (уменьшать copies_available при бронировании).
Удаление бронирования (и увеличение copies_available).

Подсказки:
Используйте declarative_base() для определения моделей.
Применяйте session.add() и session.commit() для операций.
Модуль datetime.date.today() поможет с датой бронирования.
"""

import os
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "postgresql://myuser:mysecretpassword@localhost:5432/library_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # relationship with user bookings
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    copies_available = Column(Integer, default=1)

    # ограничиваем цифры, чтобы количество доступных копий было неотрицательным
    __table_args__ = (
        CheckConstraint('copies_available >=0', name='check_copies_positive'),
    )

    bookings = relationship("Booking", back_populates="book", cascade="all, delete-orphan")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    booking_date = Column(Date, default=date.today())

    # связи
    user = relationship("User", back_populates="bookings")
    book = relationship("Book", back_populates="bookings")


def init_db():
    # чистим старое
    Base.metadata.drop_all(bind=engine)
    # создаем новое
    Base.metadata.create_all(bind=engine)


# CRUD
def add_user(name: str, email: str) -> User:
    """ Добавление нового пользователя """
    session = SessionLocal()
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def add_book(title: str, author: str, copies_available: int = 1) -> Book:
    """ Добавление новой книги """
    session = SessionLocal()
    try:
        book = Book(title=title, author=author, copies_available=copies_available)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def create_booking(user_id: int, book_id: int) -> Booking:
    """ Создание бронирования с учетом количества доступных копий """
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Книга с ID {book_id} не найдена")

        if book.copies_available <= 0:
            raise ValueError(f"Книга {book.title} недоступна для бронирования (закончились)")

        book.copies_available -= 1
        booking = Booking(user_id=user_id, book_id=book_id, booking_date=date.today())
        session.add(booking)

        session.commit()
        session.refresh(booking)
        return booking
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_booking(booking_id: int) -> bool:
    session = SessionLocal()
    try:
        booking = session.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            print(f"Брони с ID {booking_id} не существует")
            return False

        book = session.query(Book).filter(Book.id == booking.book_id).first()
        if book:
            book.copies_available += 1

        session.delete(booking)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# ------ demo ------
def main():
    print("1) инициализация БД")
    init_db()

    print("\n2) создание пользователей")
    try:
        user1 = add_user("bob", email="bob@mail.mail")
        user2 = add_user("alice", email="alice@mail.mail")
        print("success!")
    except Exception as e:
        raise e

    input("\nхочу посмотреть что происходит с дб")
    print("\n3) инвернтаризируем книги")
    try:
        book1 = add_book("Alice in wonderland", author="Lewis Carroll", copies_available=2)
        book2 = add_book("Faust", author="Iogan Gete", copies_available=1)
        book3 = add_book("1984", author="George Orwell", copies_available=2)
        book4 = add_book("Do Androids dream of electric sheep?", author="Philip K. Dick", copies_available=1)
        print("success!")
    except Exception as e:
        raise e

    input("\nтеперь когда все книги и юзеры есть смотрим как работают бронирования")

    print("\n4) создание бронирований")
    booking = create_booking(user1.id, book1.id)
    print(f"[{booking.id}] забронирована книга {book1.title} пользователем {user1.name}")

    input("\nщас должна была появиться новая запись в букингс и уменьшен счетчик в букс")

    s_booking = create_booking(user2.id, book2.id)
    print(f"[{s_booking.id}] забронирована книга {book2.title} пользователем {user2.name}")

    input("\nтолько что уменьшился Фауст и появилась бронь id[2]")

    # проверяем остаток книг через новую сессию
    session = SessionLocal()
    updated_book = session.query(Book).filter(Book.id == book1.id).first()
    print(f"\nостаток книги {updated_book.title} в библиотеке: {updated_book.copies_available}")

    print("\n5) отмена бронирования")
    delete_booking(booking.id)

    input("\nубралась бронь с id[1]")

    session = SessionLocal()
    restored_book = session.query(Book).filter(Book.id == book1.id).first()
    print(f"книга {restored_book.title} более не забронирована. остаток: {book1.copies_available}")
    session.close()


if __name__ == "__main__":
    main()
