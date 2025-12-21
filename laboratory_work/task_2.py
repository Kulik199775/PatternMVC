# модель
class Article:
    """Класс Статья, представляющий модель данных"""

    def __init__(self, title: str, author: str, char_count: int,
                 publication: str, description: str = ""):

        self.title = title
        self.author = author
        self.char_count = char_count
        self.publication = publication
        self.description = description

    def update(self, title: str = None, author: str = None,
               char_count: int = None, publication: str = None,
               description: str = None):
        """Обновляет информацию о статье"""

        if title:
            self.title = title
        if author:
            self.author = author
        if char_count:
            self.char_count = char_count
        if publication:
            self.publication = publication
        if description:
            self.description = description

    def to_dict(self) -> dict:
        """Преобразует статью в словарь"""

        return {
            'title': self.title,
            'author': self.author,
            'char_count': self.char_count,
            'publication': self.publication,
            'description': self.description
        }

    def __str__(self) -> str:
        """Строковое представление статьи."""
        return (f"Статья: {self.title}\n"
                f"Автор: {self.author}\n"
                f"Количество знаков: {self.char_count}\n"
                f"Издание: {self.publication}\n"
                f"Описание: {self.description}")


# Контроллер
class ArticleController:
    """Контроллер для управления статьями"""

    def __init__(self, model: Article, view):
        self.model = model
        self.view = view

    def create_article(self, title: str, author: str, char_count: int,
                       publication: str, description: str):
        """Создание новой статьи"""

        self.model = Article(title, author, char_count, publication, description)
        self.view.show_message(f"Статья '{title}' создана!")

    def update_article(self, **kwargs):
        """Обновление данных статьи"""

        self.model.update(**kwargs)
        self.view.show_message("Статья обновлена!")

    def show_article(self):
        """Отображение информации о статье"""
        self.view.display_article(self.model)

    def get_article_data(self) -> dict:
        """Возврат данных статьи"""

        return self.model.to_dict()