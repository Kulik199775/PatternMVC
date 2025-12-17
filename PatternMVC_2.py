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

