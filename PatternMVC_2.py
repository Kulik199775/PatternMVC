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