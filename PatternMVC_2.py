class Recipe:
    def __init__(self, recipe_id, name, author, recipe_type, description, ingredients, cuisine, video_link=None):
        self.recipe_id = recipe_id
        self.name = name
        self.author = author
        self.recipe_type = recipe_type
        self.description = description
        self.ingredients = ingredients  # список строк
        self.cuisine = cuisine
        self.video_link = video_link

    def to_dict(self):
        """Преобразование объекта в словарь"""
        return {
            'id': self.recipe_id,
            'name': self.name,
            'author': self.author,
            'type': self.recipe_type,
            'description': self.description,
            'ingredients': self.ingredients,
            'cuisine': self.cuisine,
            'video_link': self.video_link
        }

    def __str__(self):
        ingredients_str = ', '.join(self.ingredients[:3]) + ("..." if len(self.ingredients) > 3 else "")
        return f"{self.name} ({self.recipe_type}) - {self.cuisine} кухня"


class RecipeModel:
    def __init__(self):
        self.recipes = []
        self.next_id = 1

    def add_recipe(self, name, author, recipe_type, description, ingredients, cuisine, video_link=None):
        """Добавить новый рецепт"""
        recipe = Recipe(self.next_id, name, author, recipe_type, description, ingredients, cuisine, video_link)
        self.recipes.append(recipe)
        self.next_id += 1
        return recipe

    def get_all_recipes(self):
        """Получить все рецепты"""
        return self.recipes

    def get_recipe_by_id(self, recipe_id):
        """Найти рецепт по id"""
        for recipe in self.recipes:
            if recipe.recipe_id == recipe_id:
                return recipe
        return None

    def update_recipe(self, recipe_id, **kwargs):
        """Обновить данные рецепта"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return False

        for key, value in kwargs.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
        return True

    def delete_recipe(self, recipe_id):
        """Удалить рецепт"""
        recipe = self.get_recipe_by_id(recipe_id)
        if recipe:
            self.recipes.remove(recipe)
            return True
        return False

    def get_recipes_by_type(self, recipe_type):
        """Получить рецепты по типу (первое, второе и т.д.)"""
        return [recipe for recipe in self.recipes if recipe.recipe_type == recipe_type]

    def get_recipes_by_cuisine(self, cuisine):
        """Получить рецепты по кухне"""
        return [recipe for recipe in self.recipes if recipe.cuisine == cuisine]

    def get_recipes_by_ingredient(self, ingredient):
        """Найти рецепты по ингредиенту"""
        result = []
        for recipe in self.recipes:
            if any(ingredient.lower() in ing.lower() for ing in recipe.ingredients):
                result.append(recipe)
        return result

    def search_recipes(self, search_term):
        """Поиск рецептов по названию или описанию"""
        search_term = search_term.lower()
        result = []
        for recipe in self.recipes:
            if (search_term in recipe.name.lower() or
                    search_term in recipe.description.lower()):
                result.append(recipe)
        return result


class RecipeController:
    def __init__(self):
        self.model = RecipeModel()

    def create_recipe(self, name, author, recipe_type, description, ingredients, cuisine, video_link=None):
        """Создать новый рецепт"""
        if not name or not description:
            return None, "Название и описание обязательны"

        if not ingredients:
            return None, "Добавьте хотя бы один ингредиент"

        recipe = self.model.add_recipe(name, author, recipe_type, description, ingredients, cuisine, video_link)
        return recipe, "Рецепт успешно добавлен"

    def get_all_recipes(self):
        """Получить все рецепты"""
        return self.model.get_all_recipes()

    def get_recipe(self, recipe_id):
        """Получить рецепт по id"""
        return self.model.get_recipe_by_id(recipe_id)

    def update_recipe(self, recipe_id, **kwargs):
        """Обновить данные рецепта"""
        if self.model.update_recipe(recipe_id, **kwargs):
            return "Рецепт обновлен успешно"
        return "Рецепт не найден"

    def delete_recipe(self, recipe_id):
        """Удалить рецепт"""
        if self.model.delete_recipe(recipe_id):
            return "Рецепт удален успешно"
        return "Рецепт не найден"

    def search_recipes(self, search_term=None, recipe_type=None, cuisine=None, ingredient=None):
        """Поиск рецептов по различным критериям"""
        results = self.model.get_all_recipes()

        if search_term:
            results = self.model.search_recipes(search_term)

        if recipe_type:
            results = [recipe for recipe in results if recipe.recipe_type == recipe_type]

        if cuisine:
            results = [recipe for recipe in results if recipe.cuisine == cuisine]

        if ingredient:
            results = self.model.get_recipes_by_ingredient(ingredient)

        return results


class RecipeView:
    def __init__(self):
        self.controller = RecipeController()

    def show_menu(self):
        """Показать меню"""
        print("\n---Книга рецептов---")
        print("1. Добавить рецепт")
        print("2. Показать все рецепты")
        print("3. Найти рецепт по ID")
        print("4. Обновить рецепт")
        print("5. Удалить рецепт")
        print("6. Поиск рецептов")
        print("7. Выход")

    def add_recipe(self):
        """Добавить новый рецепт"""
        print("\n--- Добавление нового рецепта ---")

        name = input("Название рецепта: ")
        author = input("Автор рецепта: ")
        recipe_type = input("Тип блюда (первое, второе, десерт и т.д.): ")
        description = input("Описание рецепта: ")

        print("\nДобавление ингредиентов (введите 'готово' для завершения):")
        ingredients = []
        while True:
            ingredient = input("Ингредиент: ")
            if ingredient.lower() == 'готово':
                if not ingredients:
                    print("Добавьте хотя бы один ингредиент")
                    continue
                break
            ingredients.append(ingredient)

        cuisine = input("Кухня (итальянская, французская и т.д.): ")
        video_link = input("Ссылка на видео (необязательно): ")
        if not video_link:
            video_link = None

        recipe, message = self.controller.create_recipe(
            name, author, recipe_type, description, ingredients, cuisine, video_link
        )
        print(message)
        if recipe:
            print(f"id нового рецепта: {recipe.recipe_id}")

    def show_all_recipes(self):
        """Показать все рецепты"""
        recipes = self.controller.get_all_recipes()

        if not recipes:
            print("\nНет доступных рецептов")
            return

        print("\n--- Все рецепты ---")
        for recipe in recipes:
            print(f"ID: {recipe.recipe_id} | {recipe}")

    def find_recipe_by_id(self):
        """Найти рецепт по id"""
        try:
            recipe_id = int(input("\nВведите id рецепта: "))
        except ValueError:
            print("Ошибка: id должен быть числом")
            return

        recipe = self.controller.get_recipe(recipe_id)

        if recipe:
            self.show_recipe_details(recipe)
        else:
            print("Рецепт не найден")

    def show_recipe_details(self, recipe):
        """Показать детальную информацию о рецепте"""
        print(f"\n=== {recipe.name} ===")
        print(f"Автор: {recipe.author}")
        print(f"Тип: {recipe.recipe_type}")
        print(f"Кухня: {recipe.cuisine}")
        print(f"\nОписание: {recipe.description}")
        print(f"\nИнгредиенты:")
        for i, ingredient in enumerate(recipe.ingredients, 1):
            print(f"  {i}. {ingredient}")
        if recipe.video_link:
            print(f"\nВидео: {recipe.video_link}")
        print("=" * 40)

    def update_recipe(self):
        """Обновить данные рецепта"""
        try:
            recipe_id = int(input("\nВведите ID рецепта для обновления: "))
        except ValueError:
            print("Ошибка: ID должен быть числом")
            return

        print("\n--- Обновление рецепта ---")
        print("Оставьте поле пустым, если не хотите менять параметр")

        updates = {}

        name = input("Новое название: ")
        if name:
            updates['name'] = name

        author = input("Новый автор: ")
        if author:
            updates['author'] = author

        recipe_type = input("Новый тип: ")
        if recipe_type:
            updates['recipe_type'] = recipe_type

        description = input("Новое описание: ")
        if description:
            updates['description'] = description

        cuisine = input("Новая кухня: ")
        if cuisine:
            updates['cuisine'] = cuisine

        video_link = input("Новая ссылка на видео: ")
        if video_link:
            updates['video_link'] = video_link

        print("\nОбновить ингредиенты? (да/нет): ")
        if input().lower() == 'да':
            print("Введите новые ингредиенты (введите 'готово' для завершения):")
            ingredients = []
            while True:
                ingredient = input("Ингредиент: ")
                if ingredient.lower() == 'готово':
                    if not ingredients:
                        print("Добавьте хотя бы один ингредиент")
                        continue
                    break
                ingredients.append(ingredient)
            updates['ingredients'] = ingredients

        if updates:
            message = self.controller.update_recipe(recipe_id, **updates)
            print(message)
        else:
            print("Нечего обновлять")