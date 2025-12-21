# Модель
class Film:
    """Класс Фильм, представляющий модель данных"""

    def __init__(self, title: str, genre: str, director: str,
                 year: int, duration: int, studio: str, actors: list = None):

        self.title = title
        self.genre = genre
        self.director = director
        self.year = year
        self.duration = duration
        self.studio = studio
        self.actors = actors or []

    def update(self, title: str = None, genre: str = None, director: str = None,
               year: int = None, duration: int = None, studio: str = None,
               actors: list = None):
        """Обновляет информацию о фильме"""

        if title is not None:
            self.title = title
        if genre is not None:
            self.genre = genre
        if director is not None:
            self.director = director
        if year is not None:
            self.year = year
        if duration is not None:
            self.duration = duration
        if studio is not None:
            self.studio = studio
        if actors is not None:
            self.actors = actors

    def add_actor(self, name: str, role: str):
        """Добавляет актера в фильм"""

        self.actors.append({'name': name, 'role': role})

    def remove_actor(self, name: str):
        """Удаляет актера из фильма"""

        self.actors = [actor for actor in self.actors if actor['name'] != name]

    def to_dict(self) -> dict:
        """Преобразует фильм в словарь"""

        return {
            'title': self.title,
            'genre': self.genre,
            'director': self.director,
            'year': self.year,
            'duration': self.duration,
            'studio': self.studio,
            'actors': self.actors.copy()
        }

    def __str__(self) -> str:
        """Строковое представление фильма."""
        actors_str = "\n".join([f"  - {actor['name']} ({actor['role']})"
                                for actor in self.actors]) if self.actors else "  Нет информации"

        return (f"Фильм: {self.title}\n"
                f"Жанр: {self.genre}\n"
                f"Режиссер: {self.director}\n"
                f"Год выпуска: {self.year}\n"
                f"Длительность: {self.duration} мин.\n"
                f"Студия: {self.studio}\n"
                f"Актеры:\n{actors_str}")

# Контроллер
class FilmController:
    """Контроллер для управления фильмами."""

    def __init__(self, model: Film, view):
        self.model = model
        self.view = view

    def create_film(self, title: str, genre: str, director: str,
                    year: int, duration: int, studio: str, actors: list = None):
        """Создает новый фильм"""

        self.model = Film(title, genre, director, year, duration, studio, actors)
        self.view.show_message(f"Фильм '{title}' создан!")

    def update_film(self, **kwargs):
        """Обновляет данные фильма"""

        self.model.update(**kwargs)
        self.view.show_message("Фильм обновлен!")

    def show_film(self):
        """Отображает информацию о фильме"""

        self.view.display_film(self.model)

    def get_film_data(self) -> dict:
        """Возвращает данные фильма"""

        return self.model.to_dict()

    def add_actor_to_film(self, name: str, role: str):
        """Добавляет актера в фильм"""

        self.model.add_actor(name, role)
        self.view.show_message(f"Актер {name} добавлен!")

    def remove_actor_from_film(self, name: str):
        """Удаляет актера из фильма"""

        self.model.remove_actor(name)
        self.view.show_message(f"Актер {name} удален!")


# Представление (View)
class FilmView:
    """Представление для отображения фильмов."""

    @staticmethod
    def display_film(film: Film):
        """Отображает информацию о фильме"""

        print("\n" + "=" * 50)
        print("Информация о фильме")
        print("=" * 50)
        print(str(film))
        print("=" * 50)

    @staticmethod
    def show_message(message: str):
        """Показывает сообщение пользователю"""

        print(f"\n {message}")

    @staticmethod
    def get_input(prompt: str) -> str:
        """Получает ввод от пользователя"""
        return input(prompt)

    @staticmethod
    def display_menu():
        """Отображает главное меню."""
        print("\n" + "=" * 50)
        print("Управление фильмами")
        print("=" * 50)
        print("1. Создать фильм")
        print("2. Показать фильм")
        print("3. Обновить фильм")
        print("4. Добавить актера")
        print("5. Удалить актера")
        print("6. Показать данные фильма (JSON-формат)")
        print("7. Выйти")
        print("=" * 50)


def example_usage():
    """Пример использования MVC компонентов отдельно"""

    print("=" * 60)
    print("Использование компонентов MVC")
    print("=" * 60)

    print("\n1. Создание модели (Film):")
    film = Film(
        title="Матрица",
        genre="Научная фантастика",
        director="Лана и Лилли Вачовски",
        year=1999,
        duration=136,
        studio="Warner Bros.",
        actors=[
            {'name': 'Киану Ривз', 'role': 'Нео'},
            {'name': 'Лоренс Фишберн', 'role': 'Морфеус'},
            {'name': 'Керри-Энн Мосс', 'role': 'Тринити'}
        ]
    )
    print(f"Создан фильм: {film.title}")

    print("\n2. Создание представления (FilmView):")
    view = FilmView()

    print("\n3. Создание контроллера (FilmController):")
    controller = FilmController(film, view)

    print("\n4. Отображение фильма через контроллер:")
    controller.show_film()

    print("\n5. Добавление актера через контроллер:")
    controller.add_actor_to_film('Хьюго Уивинг', 'Агент Смит')

    print("\n6. Обновление фильма через контроллер:")
    controller.update_film(year=1999, duration=138)

    print("\n7. Обновленный фильм:")
    controller.show_film()

    print("\n" + "=" * 60)
    print("Завершено")
    print("=" * 60)

if __name__ == '__main__':
    """Основная функция приложения"""

    example_usage()

    initial_film = Film("", "", "", 0, 0, "", [])

    view = FilmView()

    controller = FilmController(initial_film, view)

    while True:
        view.display_menu()

        choice = input("\nВыберите действие (1-7): ")

        if choice == "1":
            print("\nСоздание нового фильма")
            print("-" * 30)

            title = view.get_input("Название фильма: ")
            genre = view.get_input("Жанр: ")
            director = view.get_input("Режиссер: ")

            while True:
                try:
                    year = int(view.get_input("Год выпуска: "))
                    if year < 1888 or year > 2100:
                        print("Введите корректный год (1888-2100)!")
                        continue
                    break
                except ValueError:
                    print("Пожалуйста, введите целое число!")

            while True:
                try:
                    duration = int(view.get_input("Длительность (минут): "))
                    if duration <= 0:
                        print("Длительность должна быть положительной!")
                        continue
                    break
                except ValueError:
                    print("Пожалуйста, введите целое число!")

            studio = view.get_input("Студия: ")

            actors = []
            print("\nДобавление актеров (оставьте имя пустым для завершения):")
            while True:
                actor_name = view.get_input("ФИО актера: ")
                if not actor_name:
                    break
                actor_role = view.get_input("Роль актера: ")
                actors.append({'name': actor_name, 'role': actor_role})
                print(f"Актер {actor_name} добавлен!")

            controller.create_film(title, genre, director, year, duration, studio, actors)

        elif choice == "2":
            controller.show_film()

        elif choice == "3":
            print("\nОбновление фильма")
            print("(оставьте поле пустым, чтобы не изменять)")
            print("-" * 30)

            current_data = controller.get_film_data()

            update_data = {}

            title = view.get_input(f"Название [{current_data['title']}]: ")
            if title:
                update_data['title'] = title

            genre = view.get_input(f"Жанр [{current_data['genre']}]: ")
            if genre:
                update_data['genre'] = genre

            director = view.get_input(f"Режиссер [{current_data['director']}]: ")
            if director:
                update_data['director'] = director

            year_input = view.get_input(f"Год выпуска [{current_data['year']}]: ")
            if year_input:
                try:
                    update_data['year'] = int(year_input)
                except ValueError:
                    view.show_message("Ошибка: год должен быть числом!")
                    continue

            duration_input = view.get_input(f"Длительность [{current_data['duration']}]: ")
            if duration_input:
                try:
                    update_data['duration'] = int(duration_input)
                except ValueError:
                    view.show_message("Ошибка: длительность должна быть числом!")
                    continue

            studio = view.get_input(f"Студия [{current_data['studio']}]: ")
            if studio:
                update_data['studio'] = studio

            if update_data:
                controller.update_film(**update_data)
            else:
                view.show_message("Изменений не внесено.")

        elif choice == "4":
            print("\nДобавление актера")
            print("-" * 30)

            name = view.get_input("ФИО актера: ")
            role = view.get_input("Роль актера: ")

            controller.add_actor_to_film(name, role)

        elif choice == "5":
            print("\nУдаление актера")
            print("-" * 30)

            current_data = controller.get_film_data()

            if not current_data['actors']:
                view.show_message("В фильме нет актеров для удаления!")
                continue

            print("Текущие актеры:")
            for i, actor in enumerate(current_data['actors'], 1):
                print(f"{i}. {actor['name']} - {actor['role']}")

            name = view.get_input("Введите ФИО актера для удаления: ")
            controller.remove_actor_from_film(name)

        elif choice == "6":
            data = controller.get_film_data()
            print("\nДанные фильма (JSON-формат):")
            print("-" * 30)
            for key, value in data.items():
                if key == 'actors':
                    print(f"{key}:")
                    for actor in value:
                        print(f"  - {actor['name']}: {actor['role']}")
                else:
                    print(f"{key}: {value}")

        elif choice == "7":
            view.show_message("До свидания!")
            break

        else:
            view.show_message("Неверный выбор! Пожалуйста, выберите от 1 до 7.")

