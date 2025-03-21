import pytest
from main import BooksCollector

class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    def test_add_new_book_add_one_book(self):
        collector = BooksCollector()
        collector.add_new_book('1984')
        assert '1984' in collector.get_books_genre()

    @pytest.mark.parametrize("book_name", [
        "Очень длинное название книги, превышающее 40 символов",
        "Книга с невероятно длинным названием, которое никто не запомнит"
    ])
    def test_add_new_book_too_long(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    @pytest.mark.parametrize("book_name", ["1984", "Гарри Поттер", "Дюна"])
    def test_add_duplicate_book(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize("book_name, genre", [
        ("1984", "Фантастика"),
        ("Шерлок Холмс", "Детективы"),
        ("Гарри Поттер", "Мультфильмы")
    ])
    def test_set_book_genre(self, book_name, genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    def test_set_invalid_genre(self):
        collector = BooksCollector()
        book_name = "Незнайка"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Приключения")
        assert collector.get_book_genre(book_name) == ""

    def test_get_book_genre_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Фантастика")
        assert collector.get_book_genre("1984") == "Фантастика"

    def test_get_book_genre_nonexistent_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre("Неизвестная книга") is None

    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Фантастика")
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Мультфильмы")
        assert collector.get_books_genre() == {"1984": "Фантастика", "Гарри Поттер": "Мультфильмы"}

    def test_get_books_for_children_contains_valid_books(self):
        collector = BooksCollector()
        collector.add_new_book("Король Лев")
        collector.set_book_genre("Король Лев", "Мультфильмы")
        assert "Король Лев" in collector.get_books_for_children()

    def test_get_books_for_children_excludes_non_children_books(self):
        collector = BooksCollector()
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        collector.add_new_book("Безжанровая книга")
        assert "Оно" not in collector.get_books_for_children()
        assert "Безжанровая книга" not in collector.get_books_for_children()

    @pytest.mark.parametrize("book_name", ["Гарри Поттер", "Дюна", "1984"])
    def test_add_book_in_favorites(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("book_name", ["Гарри Поттер", "Дюна", "1984"])
    def test_delete_book_from_favorites(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_contains_added_book(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert collector.get_list_of_favorites_books() == ["Гарри Поттер"]

    def test_get_list_of_favorites_books_does_not_contain_non_favorite_books(self):
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Дюна")
        collector.add_book_in_favorites("Гарри Поттер")
        assert "Дюна" not in collector.get_list_of_favorites_books()
