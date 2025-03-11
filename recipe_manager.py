import json
import os
from typing import List, Optional, Dict, Any

DATA_FOLDER = 'data'
RECIPES_FILE = 'recipes.json'

class Step:
    def __init__(self, name: str, description: str, attributes: List[str], image: Optional[str], video: Optional[str], time_indicator: int):
        self.name = name
        self.description = description
        self.attributes = attributes
        self.image = self._load_media_file(image, ['jpg', 'png'])
        self.video = self._load_media_file(video, ['mp4', 'mov'])
        self.time_indicator = time_indicator

    def _load_media_file(self, filename: Optional[str], allowed_extensions: List[str]) -> Optional[str]:
        if not filename:
            return None

        file_extension = filename.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            print(f"⚠️ Warning: {filename} has unsupported extension.")
            return None

        filepath = os.path.join(DATA_FOLDER, filename)
        if os.path.exists(filepath):
            return filepath
        else:
            print(f"⚠️ Warning: Media file '{filename}' not found in '{DATA_FOLDER}/'.")
            return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "attributes": self.attributes,
            "image": os.path.basename(self.image) if self.image else None,
            "video": os.path.basename(self.video) if self.video else None,
            "time_indicator": self.time_indicator
        }

class Recipe:
    def __init__(self, name: str, description: str, steps: List[Step]):
        self.name = name
        self.description = description
        self.steps = steps


    def add_step(self, name: str, description: str, attributes: List[str], time_indicator: int, image: Optional[str] = None, video: Optional[str] = None):
        step = Step(name, description, attributes, image, video, time_indicator)
        self.steps.append(step)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "steps": [step.to_dict() for step in self.steps]
        }

class RecipeManager:
    def __init__(self):
        self.recipes: List[Recipe] = self.load_all_recipes()

    def load_all_recipes(self) -> List[Recipe]:
        if not os.path.exists(RECIPES_FILE):
            return []

        with open(RECIPES_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return [
            Recipe(
                name=recipe['name'],
                description=recipe['description'],
                steps=[
                    Step(
                        step['name'],
                        step['description'],
                        step['attributes'],
                        step.get('image'),
                        step.get('video'),
                        step['time_indicator']
                    )
                    for step in recipe['steps']
                ]
            )
            for recipe in data
        ]

    def save_all_recipes(self):
        data = [recipe.to_dict() for recipe in self.recipes]
        with open(RECIPES_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"✅ Recipes saved to {RECIPES_FILE}")

    def add_recipe(self, name: str, description: str) -> Recipe:
        recipe = Recipe(name=name, description=description, steps=[])
        self.recipes.append(recipe)
        return recipe

    def list_recipes(self):
        print("Available recipes:")
        for idx, recipe in enumerate(self.recipes, 1):
            print(f"{idx}. {recipe.name}")

    def get_recipe_by_name(self, name: str) -> Optional[Recipe]:
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe
        return None

if __name__ == "__main__":
    manager = RecipeManager()

    if not manager.recipes:
        print("No recipes found, starting fresh.")
    else:
        manager.list_recipes()

    new_recipe = manager.add_recipe("Chocolate Cake", "A delicious chocolate cake recipe.")

    new_recipe.add_step(
        name="Mix ingredients",
        description="Combine flour, cocoa, sugar, and eggs.",
        attributes=["mix"],
        image="mix-ingredients.jpg",
        time_indicator = 1
    )

    new_recipe.add_step(
        name="Bake cake",
        description="Place the batter into a preheated oven.",
        attributes=["hot"],
        video="bake-cake.mov",
        time_indicator = 2
    )
    
    manager.save_all_recipes()
