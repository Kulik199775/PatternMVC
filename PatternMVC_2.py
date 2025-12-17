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