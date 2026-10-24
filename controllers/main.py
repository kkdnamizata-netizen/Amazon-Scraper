import os, time
from .scraper import create_driver, find_subcategories, scrape_subcategory, TECH_CATEGORY_URL, OUTPUT_DIR, summary, errors
from views.reporter import Reporter

def main():
    start = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    driver = create_driver()
    subcats = find_subcategories(driver, TECH_CATEGORY_URL)
    print(f"Trouvé {len(subcats)} sous-catégories.")
    for name, link in subcats[:1]:
        print(f"Scraping sous-catégorie: {name}")
        scrape_subcategory(driver, name, link)
    end = time.time()
    Reporter.generate_report(OUTPUT_DIR, summary, errors, start, end)

    print("\nTerminé. Chrome reste ouvert et ne se fermera pas tout seul.")
    print(f"Résultats : {os.path.abspath(OUTPUT_DIR)}")
    input("Appuyez sur Entrée uniquement quand vous avez fini (cela ferme le script, pas Chrome)...")

if __name__ == "__main__":
    main()