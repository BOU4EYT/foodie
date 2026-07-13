# Foodie

A personal meal planning, budgeting, grocery list, and recipe management app.

Foodie combines recipe storage, meal planning (with a flexible time-horizon slider — 4 hours up to a month), grocery list generation, budgeting, and macro tracking into one connected tool, so planning meals automatically drives your grocery list and keeps your spending in check.

Full spec: see [`docs/PDD.md`](docs/PDD.md).

## Status

Early development — scaffolding stage.

## Stack

- Backend: Python / Flask
- Database: SQLite
- Frontend: server-rendered templates (Jinja2) + vanilla JS, run locally on a single shared machine (no multi-device sync needed for v1)

## Project Structure

```
foodie/
├── app/
│   ├── models/       # DB models (Recipe, RawIngredient, MealPlanEntry, GroceryItem, Budget, UserPreferences)
│   ├── routes/        # Flask routes/blueprints
│   ├── templates/     # Jinja2 templates
│   └── static/        # CSS/JS
├── scraper/           # Walmart category price scraper (Meat & Seafood, Produce, Bakery, Dairy & Eggs, Frozen, Pantry, Snacks)
├── data/              # SQLite DB file lives here (gitignored)
├── tests/
└── docs/
    └── PDD.md          # Full product design document
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

## License

Personal project — no license specified yet.
