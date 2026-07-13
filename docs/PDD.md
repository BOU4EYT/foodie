# Product Design Document: Foodie

**Author:** Jaymes
**Status:** Draft v0.1
**Last updated:** July 13, 2026

---

## 1. Overview

Foodie is a personal meal planning, budgeting, grocery list, and recipe management application. It combines four typically-separate tools (recipe box, meal planner, grocery list, budget tracker) into one connected system, so that planning a week of meals automatically drives the grocery list and the grocery list is tied to a running budget.

## 2. Goals

- Let a user build/store recipes and plan meals around them
- Auto-generate a grocery list from a selected set of planned meals
- Track estimated and actual cost of groceries against a budget
- Reduce food waste and decision fatigue by making "what's for dinner" a planning problem, not a daily one

## 3. Target Users

- Primary: Jaymes and fiancée, household of 2
- Secondary (stretch): could open up to other users/households later, but not a v1 requirement

## 4. Platform & Stack

- **Locked in: single shared local machine** — you and your fiancée will use one shared computer, so no need for multi-device sync, accounts, or remote access
- This simplifies the stack significantly: a **local desktop app or a locally-served HTML app opened in a browser on that machine** both work fine — no server exposed to the network, no auth/session system needed
- Given prior experience with Flask (room-planner project), a lightweight local Flask app (running on localhost, opened in a browser) is a strong candidate — keeps the door open to Electron-style packaging later if you want a "real" desktop app feel, without needing it for v1
- SQLite remains the right DB choice — single-file, zero-config, perfect for single-machine use

## 5. Core Features (v1 — all equal priority)

### 5.1 Recipes
- Add/edit/delete recipes: title, servings, tags (e.g. cuisine, meal type)
- **Ingredients use a split model** (locked in):
  - **Raw ingredient** — what you actually buy (e.g. "onion"), with a shopping quantity/unit (e.g. "1 medium," "2 lb")
  - **Prep notes** — how it's used in this specific recipe (e.g. "diced," "1 cup"), attached to the raw ingredient but not part of the grocery item itself
  - This means the grocery list only ever reads raw ingredient + shopping quantity, so the same ingredient from different recipes reliably merges into one line, no matter how each recipe preps it
- **Step-by-step instructions**, split into:
  - **Prep steps** (chopping, marinating, mise en place, etc.)
  - **Cook steps** (the actual cooking sequence)
- **Separate prep time and cook time fields** (locked in) — total time can be derived from the two
- Search/filter recipes by tag, ingredient, or name

### 5.2 Meal Planning
- Calendar or weekly grid view to assign recipes to days/meals
- Adjust servings per planned meal (scales ingredient quantities)
- **Planning range slider**: user selects the planning horizon — presets: 4 hours, 1 day, 3 days, 1 week, 2 weeks, 1 month (locked in; custom range also allowed)
  - The slider controls the *view window* over the same underlying `MealPlanEntry` timeline — it doesn't create separate data per range
  - Short ranges (4 hrs, 1 day) render as a list/timeline (breakfast, lunch, snack, dinner)
  - Longer ranges (week, month) render as a calendar/grid
  - All other range-dependent features (grocery list, budget) key off whatever range is currently selected on this slider

### 5.3 Grocery List
- Auto-generate a consolidated grocery list from all recipes planned within the **currently selected planning range**
- Combine duplicate ingredients across recipes (e.g. 2 recipes needing onions → one line item)
- Manual add/remove items not tied to a recipe
- Checkbox/"got it" state for shopping mode
- **Export to phone (locked in)**: generate a markdown or PDF version of the shopping-mode list that can be sent to/opened on your phone for in-store use

### 5.4 Budgeting
- Assign estimated price per grocery item (manual entry, or pulled from local price data — see 5.7)
- Running total for the **currently selected planning range**'s grocery list vs. a set budget
- Track actual spend after shopping (optional: log actual receipt totals)
- Basic history: cost per week/month over time
- Budget panel can collapse/hide for very short ranges (e.g. 4 hours) where a running total isn't meaningful
- **"Prefer cheapest option" mode (user preference, locked in)**: when multiple product options exist for a raw ingredient (e.g. different brands/sizes of chicken breast), the app can auto-select the cheapest one for budgeting/grocery list purposes — off by default, toggleable in preferences, since some users care more about specific brands than lowest price

### 5.5 Grocery Pricing Data (Walmart-scoped)
- v1 price source is a **targeted local scraper** covering the household's actual shopping categories at Walmart (locked in), specifically:
  - Meat & Seafood
  - Fresh Produce
  - Bakery & Bread
  - Dairy & Eggs
  - Frozen
  - Pantry
  - Snacks
- Scraper needs to be scoped to the user's local store/zip (Walmart's pricing varies by location/pickup-delivery setting) — this needs to be set in the scraping session, not just the URL
- Given these are dynamic, paginated pages, a headless browser approach (e.g. Playwright) is the practical implementation, not simple HTML parsing
- Price data feeds the `RawIngredient.est_price` field — falls back to manual entry for anything outside these 7 categories or if the scrape is stale/unavailable
- **Refresh cadence (locked in)**: re-scrape every 12-24 hours rather than on-demand or real-time — keeps prices reasonably current without hammering the site
- Same ToS caveat as before: fine for personal household use, not something to scale to other users without revisiting

### 5.6 Meal Prep Mode
- Given the currently planned range (e.g. a full week), generates a **consolidated, step-by-step prep walkthrough** for batch-prepping everything at once — not just per-recipe steps, but an optimized combined sequence (e.g. "chop all onions across all 5 recipes now," "these 3 things go in the oven together")
- Takes the current **budget** into account — e.g. flags if the planned range is over budget before you start prepping, so you're not mid-prep when you realize you're over
- Distinct from normal recipe cook steps — this mode is specifically about batch-prepping a whole planning range in one sitting

### 5.7 User Preferences
Extensive preference system so the app adapts to the household rather than the other way around. Categories to support:
- **Dietary**: allergies/intolerances and disliked ingredients are **blocked** (locked in) — recipes containing them can't be added to a meal plan, not just filtered/suggested around
- **Macro awareness (toggle)**: default mode uses simple tags (e.g. "high protein," "low carb") set manually per recipe; toggling on **full macro awareness** switches to calculated macros (protein/carbs/fat/calories) per recipe and per planned range, computed from ingredient-level nutrition data
  - Nutrition data supports **both manual entry and database lookup** (locked in) — user can type in macros for a raw ingredient directly, or pull them from a nutrition database/API when available
  - **Food scale support**: raw ingredients can be entered/logged by precise weight (grams) in addition to standard units (cups, whole items, etc.), so users weighing ingredients on a small food scale get accurate macro calculations rather than estimates based on "1 cup" or "1 medium"
- **Pricing**: "prefer cheapest option" toggle (see 5.4) — off by default
- **Household**: number of people to plan/scale for by default, per-person serving adjustments
- **Budget**: default budget amount per range, alert thresholds (e.g. warn at 90% of budget)
- **Planning**: default planning range (from the slider presets), default meal types shown (breakfast/lunch/dinner/snacks)
- **Grocery**: preferred grocery categories/aisle grouping for list sorting, default units (imperial vs metric)
- **Recipe display**: preferred units in recipes, default sort/filter for recipe browsing
- **Notifications** (if applicable): reminders to plan the next range, reminders to shop
- **UI**: theme/display preferences, shopping-mode specific settings (e.g. large text for in-store use)

## 6. Data Model (rough sketch)

- **Recipe**: id, name, tags (incl. simple macro tags like "high protein"), servings, prep_time, cook_time, ingredients[], prep_steps[], cook_steps[], calculated_macros (optional, populated when macro toggle is on)
- **RawIngredient**: name, shopping_quantity, shopping_unit (supports weight-based units like grams for food-scale users), est_price, price_source (manual/scraped), price_options[] (when multiple products match, for cheapest-option selection), nutrition_per_unit (protein/carbs/fat/calories — manual entry or database lookup), nutrition_source (manual/database)
- **RecipeIngredient**: links a Recipe to a RawIngredient, plus prep_notes (e.g. "diced," "1 cup") specific to that recipe
- **MealPlanEntry**: date, meal_type, recipe_id, servings
- **GroceryItem**: raw_ingredient_id, quantity, unit, est_price, actual_price, checked (bool), source (recipe-derived or manual)
- **Budget**: period (matches selected planning range), target_amount, actual_amount
- **UserPreferences**: dietary restrictions/dislikes, household size, default budget/alert thresholds, default planning range, unit preferences, grocery sort preferences, notification settings, UI settings

## 7. Non-Functional Requirements

- Single shared local machine (locked in) — no multi-user concurrency/conflict handling needed for v1
- Data persistence (local DB — SQLite is a natural fit given Flask/Python background)
- Simple, fast UI — this is a tool used while cooking or standing in a store, not a polished consumer product (at least for v1)

## 8. Out of Scope (v1)

- Recipe import from external sites/scraping
- Multi-household/public accounts
- Native mobile app

## 9. Open Questions

All open questions resolved as of this draft — see decisions below.

## 10. Milestones (draft)

1. Recipe CRUD + storage (with split ingredient model, prep/cook steps)
2. Meal planner calendar view + range slider
3. Grocery list generation from planned meals
4. Grocery pricing scraper (7 target categories, store/zip-scoped) + budget tracking layer
5. User preferences system
6. Meal prep mode (batch prep walkthrough, budget-aware)
7. Polish: shopping mode, ingredient consolidation edge cases
