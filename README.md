# ☕ Café API — Flask + SQLite + Web Scraping

A lightweight REST API built with **Flask**, **SQLAlchemy**, and **SQLite**, designed to store and serve information about cafés.  
The project includes a web scraper that imports real cafés from *LaptopFriendly Porto*.

---

## 🚀 Features

### API Endpoints

| Method | Route                                  | Description |
|--------|----------------------------------------|-------------|
| `GET` | `/random`                              | Returns a random café. |
| `GET` | `/all`                                 | Lists all cafés sorted by name. |
| `GET` | `/search?loc=<location>`               | Finds cafés by location. |
| `POST` | `/add`                                 | Creates a new café entry. |
| `PATCH` | `/update-price/<id>?new_price=<value>` | Updates the coffee price of a café. |
| `DELETE` | `/report-closed/<id>?api_key=<value>`  | Deletes a café (API key required). |

---

## 🗄️ Database Model

The `Cafe` table contains:

- `id` — primary key  
- `name` — café name  
- `map_url` — link to map  
- `img_url` — image URL  
- `location` — textual location  
- `seats` — number of seats  
- `has_toilet` — boolean  
- `has_wifi` — boolean  
- `has_sockets` — boolean  
- `can_take_calls` — boolean  
- `coffee_price` — optional price

---

## 🧩 Web Scraper (LaptopFriendly Porto)

The scraper fetches cafés from:

```
https://laptopfriendly.co/porto
```

For each café, it extracts:

- name  
- map URL  
- image URL  
- location  
- seats (default: `"Unknown"`)  
- has_toilet  
- has_wifi  
- has_sockets  
- can_take_calls  
- coffee_price (default: `None`)  

It avoids duplicates and inserts new cafés into the database.

---

## 🛠️ Technologies Used

- Python 3  
- Flask‑SQLAlchemy  
- SQLite  
- Postman
- BeautifulSoup4  
- Requests  

---

## ▶️ Running the Project

Populate the database:

```
python scrape.py
```

Start the API:

```
python main.py
```