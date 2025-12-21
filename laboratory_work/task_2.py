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


# Представление (View)
class ArticleView:
    """Представление для отображения статей."""

    @staticmethod
    def display_article(article: Article):
        """Отображает информацию о статье"""

        print("\n" + "=" * 40)
        print("Информация о статье")
        print("=" * 40)
        print(str(article))
        print("=" * 40)

    @staticmethod
    def show_message(message: str):
        """Показывает сообщение пользователю"""

        print(f"\n {message}")

    @staticmethod
    def get_input(prompt: str) -> str:
        """Получает ввод от пользователя"""

        return input(prompt) # подсказка для пользователя

    @staticmethod
    def display_menu():
        """Отображает главное меню."""

        print("\n" + "=" * 40)
        print("Управление статьями")
        print("=" * 40)
        print("1. Создать статью")
        print("2. Показать статью")
        print("3. Обновить статью")
        print("4. Показать данные статьи (JSON-формат)")
        print("5. Выйти")
        print("=" * 40)

def example_usage():
    """Использования MVC компонентов отдельно."""

    print("=" * 40)
    print("Использование компонентов MVC")
    print("=" * 40)

    print("\n1. Создание модели (Article):")
    article = Article(
        title="Введение в Python",
        author="Иван Иванов",
        char_count=15000,
        publication="Журнал 'Программирование'",
        description="Статья о базовых концепциях языка Python"
    )
    print(f"Создана статья: {article.title}")

    print("\n2. Создание представления (ArticleView):")
    view = ArticleView()

    print("\n3. Создание контроллера (ArticleController):")
    controller = ArticleController(article, view)

    print("\n4. Отображение статьи: ")
    controller.show_article()

    print("\n5. Обновление статьи: ")
    controller.update_article(
        char_count=18000,
        description="Обновленная статья о Python с примерами кода"
    )

    print("\n6. Отображение обновления статьи:")
    controller.show_article()

    print("\n" + "=" * 40)
    print("Завершено")
    print("=" * 40)

if __name__ == '__main__':
    example_usage()

    print("\n" + "=" * 40)
    print("Основное приложение")
    print("=" * 40)

    initial_article = Article("", "", 0, "", "")
    view = ArticleView()
    controller = ArticleController(initial_article, view)

    while True:
        view.display_menu()

        choice = input("\nВыберите действие (1-5): ")

        if choice == "1":
            print("\nСоздание новой статьи")
            print("-" * 30)

            title = view.get_input("Название статьи: ")
            author = view.get_input("Автор статьи: ")

            while True:
                try:
                    char_count = int(view.get_input("Количество знаков: "))
                    if char_count <= 0:
                        print("Количество знаков должно быть положительным числом!")
                        continue
                    break
                except ValueError:
                    print("Пожалуйста, введите целое число!")

            publication = view.get_input("Название издания/сайта: ")
            description = view.get_input("Краткое описание: ")

            controller.create_article(title, author, char_count, publication, description)

        elif choice == "2":
            controller.show_article()

        elif choice == "3":
            print("\nОбновление статьи")
            print("(оставьте поле пустым, чтобы не изменять)")
            print("-" * 30)

            current_data = controller.get_article_data()
            update_data = {}

            title = view.get_input(f"Название [{current_data['title']}]: ")
            if title:
                update_data['title'] = title

            author = view.get_input(f"Автор [{current_data['author']}]: ")
            if author:
                update_data['author'] = author

            char_count_input = view.get_input(f"Количество знаков [{current_data['char_count']}]: ")
            if char_count_input:
                try:
                    update_data['char_count'] = int(char_count_input)
                except ValueError:
                    view.show_message("Ошибка: количество знаков должно быть числом!")
                    continue

            publication = view.get_input(f"Издание [{current_data['publication']}]: ")
            if publication:
                update_data['publication'] = publication

            description = view.get_input(f"Описание [{current_data['description']}]: ")
            if description:
                update_data['description'] = description

            if update_data:
                controller.update_article(**update_data)
            else:
                view.show_message("Изменений не внесено.")

        elif choice == "4":
            data = controller.get_article_data()
            print("\nДанные статьи (JSON-формат):")
            print("-" * 30)
            for key, value in data.items():
                print(f"{key}: {value}")

        elif choice == "5":
            view.show_message("До свидания!")
            break

        else:
            view.show_message("Неверный выбор! Пожалуйста, выберите от 1 до 5.")