from app import db


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tags = db.Column(db.String(300))  # comma-separated, incl. macro tags like "high protein"
    servings = db.Column(db.Integer, default=1)
    prep_time_minutes = db.Column(db.Integer)
    cook_time_minutes = db.Column(db.Integer)
    prep_steps = db.Column(db.Text)  # newline-separated for now
    cook_steps = db.Column(db.Text)


class RawIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    shopping_quantity = db.Column(db.Float)
    shopping_unit = db.Column(db.String(50))  # supports weight-based units (g) for food-scale users
    est_price = db.Column(db.Float)
    price_source = db.Column(db.String(20), default="manual")  # manual | scraped
    nutrition_per_unit = db.Column(db.Text)  # JSON blob: protein/carbs/fat/calories
    nutrition_source = db.Column(db.String(20), default="manual")  # manual | database


class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    raw_ingredient_id = db.Column(db.Integer, db.ForeignKey("raw_ingredient.id"), nullable=False)
    prep_notes = db.Column(db.String(200))  # e.g. "diced", "1 cup"


class MealPlanEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(20))  # breakfast/lunch/dinner/snack
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
    servings = db.Column(db.Integer, default=1)


class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_ingredient_id = db.Column(db.Integer, db.ForeignKey("raw_ingredient.id"))
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(50))
    est_price = db.Column(db.Float)
    actual_price = db.Column(db.Float)
    checked = db.Column(db.Boolean, default=False)
    source = db.Column(db.String(20), default="recipe")  # recipe | manual


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period_start = db.Column(db.Date)
    period_end = db.Column(db.Date)
    target_amount = db.Column(db.Float)
    actual_amount = db.Column(db.Float)


class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dietary_restrictions = db.Column(db.Text)  # JSON list, blocked ingredients
    macro_awareness_enabled = db.Column(db.Boolean, default=False)
    prefer_cheapest_option = db.Column(db.Boolean, default=False)
    household_size = db.Column(db.Integer, default=2)
    default_budget = db.Column(db.Float)
    default_planning_range = db.Column(db.String(20), default="1_week")
    unit_system = db.Column(db.String(10), default="imperial")
