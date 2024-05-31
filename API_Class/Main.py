from NoFrills import NoFrillsScraper

if __name__ == "__main__":
    URL = 'https://www.nofrills.ca/food/fruits-vegetables/fresh-vegetables/c/28195'
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Success786!!',
        'database': 'nofrills_products'
    }

    scraper = NoFrillsScraper(URL, DB_CONFIG)
    scraper.run()