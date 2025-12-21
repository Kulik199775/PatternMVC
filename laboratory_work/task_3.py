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