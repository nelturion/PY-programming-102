import unittest

# Импортируем модели, функции, engine, Base из основного файла
from src.sem2.lab4.library_orm import Base, User, Book, Booking, add_user, add_book, create_booking, delete_booking, SessionLocal, engine


class TestLibraryApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Настройка перед запуском ВСЕХ тестов: пересоздаем чистые таблицы """
        Base.metadata.drop_all(bind=engine)  # Сбрасываем старое
        Base.metadata.create_all(bind=engine)  # Создаем с нуля

    def setUp(self):
        """ Выполняется ПЕРЕД каждым отдельным тестом: чистим таблицы, чтобы тесты не влияли друг на друга """
        session = SessionLocal()
        try:
            session.query(Booking).delete()
            session.query(User).delete()
            session.query(Book).delete()
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

    def test_add_user_success(self):
        """ Тест успешного добавления пользователя """
        user = add_user(name="тестовый боб", email="test_bob@mail.com")
        self.assertIsNotNone(user.id)
        self.assertEqual(user.name, "тестовый боб")

    def test_add_book_success(self):
        """ Тест успешного добавления книги """
        book = add_book(title="Тестовая книга", author="Тестовый автор", copies_available=5)
        self.assertIsNotNone(book.id)
        self.assertEqual(book.copies_available, 5)

    def test_create_booking_success(self):
        """ Тест успешного бронирования и уменьшения счетчика книг """
        user = add_user(name="Юзер", email="user@mail.com")
        book = add_book(title="Книга для брони", author="Автор", copies_available=1)

        booking = create_booking(user_id=user.id, book_id=book.id)

        self.assertIsNotNone(booking.id)
        self.assertEqual(booking.user_id, user.id)

        # Проверяем, что количество доступных копий уменьшилось до 0
        session = SessionLocal()
        db_book = session.query(Book).filter(Book.id == book.id).first()
        self.assertEqual(db_book.copies_available, 0)
        session.close()

    def test_create_booking_no_copies_error(self):
        """ Тест защиты: нельзя забронировать книгу, если доступно 0 копий """
        user = add_user(name="Алиса", email="alice_test@mail.com")
        book = add_book(title="Дефицитная книга", author="Автор", copies_available=0)

        # Проверяем, что функция выбрасывает ValueError, когда книги кончились
        with self.assertRaises(ValueError):
            create_booking(user_id=user.id, book_id=book.id)

    def test_delete_booking_success(self):
        """ Тест отмены бронирования и возврата книги на склад """
        user = add_user(name="Кевин", email="kevin@mail.com")
        book = add_book(title="Исчезающая книга", author="Автор", copies_available=1)
        booking = create_booking(user_id=user.id, book_id=book.id)

        # Удаляем бронь
        result = delete_booking(booking_id=booking.id)
        self.assertTrue(result)

        # Проверяем, что книга вернулась (стало снова 1 штука)
        session = SessionLocal()
        db_book = session.query(Book).filter(Book.id == book.id).first()
        self.assertEqual(db_book.copies_available, 1)
        session.close()


if __name__ == "__main__":
    unittest.main()