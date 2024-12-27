import requests
import json

# Base API URL
BASE_URL = "https://www.vinmonopolet.no/vmpws/v2/vmp/search"

errorPages = []

# Parameters for the initial query
params = {
    "searchType": "product",
    "currentPage": 0,
    "q": ":price-asc"
}

# Function to fetch data from the API
def fetch_data(page):
    params["currentPage"] = page
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        errorPages.append(page)

# List to store the extracted data
response = []

# Initial API call to determine the total number of pages
initial_data = fetch_data(0)
total_pages = initial_data["productSearchResult"]["pagination"]["totalPages"]
totalItems = 0

print(f"Total pages to load: {total_pages}")

# Loop through all pages
for page in range(total_pages):
    data = fetch_data(page)
    products = data["productSearchResult"]["products"]
    
    for product in products:
        totalItems += 1

        name = product.get("name", None)
        url = product.get("url", None)
        alcohol = product.get("alcohol", {}).get("value", None)
        buyable = product.get("buyable", None)
        price = product.get("price", {}).get("value", None)
        volume = product.get("volume", {}).get("value", None)
        imageUrls = product.get("images", [])
        imageUrl = imageUrls[0].get("url", None) if imageUrls else None
        rawAlcoholPrice = (1 / ( volume / 100 ) * ( 100 / alcohol ) * price) if alcohol and volume and price else None

        response.append({
            "name": name,
            "alcohol": alcohol,
            "price": price,
            "volume": volume,
            "rawAlcoholPrice": int(rawAlcoholPrice) if rawAlcoholPrice is not None else None,
            "buyable": buyable,
            "image": imageUrl,
            "sufix": url
        })


while len(errorPages) > 0:
    fetch_data(errorPages[0])
    del errorPages[0]


cheapPrice = sorted(
    (item for item in response if item['price'] is not None),
    key=lambda x: x['price'],
    reverse=False
)

# Save the extracted data to a JSON file
with open("lowPrice.json", "w", encoding="utf-8") as f:
    json.dump(cheapPrice, f, ensure_ascii=False, indent=4)


# Sort the data by rawAlcoholPrice, filtering out items with None value
cheapestRawAlcohol = sorted(
    (item for item in response if item['rawAlcoholPrice'] is not None),
    key=lambda x: x['rawAlcoholPrice'],
    reverse=False
)

# Save the sorted data to a JSON file
with open("rawAlcoholPrice.json", "w", encoding="utf-8") as f:
    json.dump(cheapestRawAlcohol, f, ensure_ascii=False, indent=4)

highVolume = sorted(
    (item for item in response if item['volume'] is not None),
    key=lambda x: x['volume'],
    reverse=True
)

with open("highestVolume.json", "w", encoding="utf-8") as f:
    json.dump(highVolume, f, ensure_ascii=False, indent=4)

print("Data extraction complete. Saved to response.json.")