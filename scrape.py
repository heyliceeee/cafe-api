import requests
from bs4 import BeautifulSoup
from main import app, db, Cafe

BASE = "https://laptopfriendly.co"

def scrape_porto():
    print("Scraping LaptopFriendly Porto...")

    html = requests.get(BASE + "/porto").text # Get the HTML content of the page
    soup = BeautifulSoup(html, "html.parser") # Parse the HTML content

    places = soup.select("a.place") # Select all the places

    with app.app_context(): # Create the database
        added = 0 # Count the number of cafes added

        for place in places: # For each place
            # Basic fields
            name = place.select_one("h3.card-title").get_text(strip=True)
            location = place.select_one("p.card-text").get_text(strip=True)
            img_url = BASE + place.select_one("img")["src"]
            map_url = BASE + place["href"]

            # Features (booleans)
            has_wifi = place.get("data-wifi") == "high"
            has_sockets = place.get("data-sockets") == "high"
            has_toilet = place.get("data-toilet") == "high"
            can_take_calls = place.get("data-skype") in ["medium", "high"]

            # Defaults
            seats = "Unknown"
            coffee_price = None

            # Avoid duplicates
            exists = db.session.execute(db.select(Cafe).where(Cafe.name == name)).scalar()
            if exists:
                print(f"Already exists: {name}")
                continue

            new_cafe = Cafe(
                name=name,
                map_url=map_url,
                img_url=img_url,
                location=location,
                seats=seats,
                has_wifi=has_wifi,
                has_sockets=has_sockets,
                has_toilet=has_toilet,
                can_take_calls=can_take_calls,
                coffee_price=coffee_price,
            )

            db.session.add(new_cafe) # Add the cafe to the database
            added += 1 # Increment the number of cafes added

        db.session.commit() # Commit the changes
    print(f"✔️ {added} added cafes to the database.")


scrape_porto()