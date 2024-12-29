import requests
import json
import os

# Base API URL
BASE_URL = "https://www.vinmonopolet.no/vmpws/v2/vmp/search"

errorPages = []

# Parameters for the initial query
params = {
    "searchType": "product",
    "currentPage": 0,
    "q": ":price-asc"
}

# Global variables for total items and pages
totalItems = 0
total_pages_price = 0
total_pages_raw_alcohol = 0
total_pages_volume = 0
firstOpened = True

# Function to fetch data from the API
def fetch_data(page):
    params["currentPage"] = page
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        errorPages.append(page)

# Check if the necessary files exist
files_exist = all(os.path.exists(file) for file in ["rawAlcoholPrice.json", "lowPrice.json", "highestVolume.json"])

if files_exist and firstOpened:
    firstOpened = False
else:
    firstOpened = False
    totalItems = 0
    print("Fetching data from the API...")

    # Initial API call to determine the total number of pages
    initial_data = fetch_data(0)
    total_pages = initial_data["productSearchResult"]["pagination"]["totalPages"]

    response = []

    # Loop through all pages
    for page in range(total_pages):
        data = fetch_data(page)
        products = data["productSearchResult"]["products"]

        for product in products:
            totalItems += 1
            print(totalItems)

            name = product.get("name", None)
            url = product.get("url", None)
            alcohol = product.get("alcohol", {}).get("value", None)
            buyable = product.get("buyable", None)
            price = product.get("price", {}).get("value", None)
            volume = product.get("volume", {}).get("value", None)
            imageUrls = product.get("images", [])
            imageUrl = imageUrls[0].get("url", None) if imageUrls else None
            rawAlcoholPrice = (1 / (volume / 100) * (100 / alcohol) * price) if alcohol and volume and price else None

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

    print(f"Total pages calculated from API data: {total_pages}")

    # Sort and save data into JSON files
    cheapPrice = sorted(
        (item for item in response if item['price'] is not None),
        key=lambda x: x['price'],
        reverse=False
    )

    with open("lowPrice.json", "w", encoding="utf-8") as f:
        json.dump(cheapPrice, f, ensure_ascii=False, indent=4)

    cheapestRawAlcohol = sorted(
        (item for item in response if item['rawAlcoholPrice'] is not None),
        key=lambda x: x['rawAlcoholPrice'],
        reverse=False
    )

    with open("rawAlcoholPrice.json", "w", encoding="utf-8") as f:
        json.dump(cheapestRawAlcohol, f, ensure_ascii=False, indent=4)

    highVolume = sorted(
        (item for item in response if item['volume'] is not None),
        key=lambda x: x['volume'],
        reverse=True
    )


    with open("highestVolume.json", "w", encoding="utf-8") as f:
        json.dump(highVolume, f, ensure_ascii=False, indent=4)


# Loads new page lenght
with open("lowPrice.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    totalItems = len(loaded_data)
    full_pages = totalItems // 10
    rest_items = totalItems % 10
    total_pages = full_pages + (1 if rest_items > 0 else 0)

    
with open("rawAlcoholPrice.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    totalItems = len(loaded_data)
    full_pages = totalItems // 10
    rest_items = totalItems % 10
    total_pages_raw_alcohol = full_pages + (1 if rest_items > 0 else 0)
    
with open("rawAlcoholPrice.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    totalItems = len(loaded_data)
    full_pages = totalItems // 10
    rest_items = totalItems % 10
    total_pages_volume = full_pages + (1 if rest_items > 0 else 0)

print("Data extraction complete.")
