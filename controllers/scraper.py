import os, re, time, random, requests, traceback
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from models.product import Product
from views.saver import Saver

HEADLESS = False
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
BASE_URL = "https://www.amazon.fr/"
TECH_CATEGORY_URL = "https://www.amazon.fr/s?k=ordinateur+portable"
OUTPUT_DIR = "output_amazon_technologies"

# Limites de test (augmentez-les une fois que tout fonctionne)
MAX_PAGES = 1
MAX_PRODUCTS = 5

summary = {"subcategories_processed": 0, "products_extracted": 0, "images_downloaded": 0}
errors = []

def create_driver():
    options = Options()

    if HEADLESS:
        options.add_argument("--headless=new")

    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    return driver

def safe_get(driver, url):
    try:
        # VÃ©rifier que la fenÃªtre Chrome est toujours ouverte
        if not driver.window_handles:
            errors.append("Erreur : la fenÃªtre Chrome est fermÃ©e.")
            return False

        driver.get(url)
        time.sleep(5)
        return True

    except WebDriverException as e:
        errors.append(f"Erreur navigation {url}: {e}")
        return False

ASIN_RE = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})")

def clean_product_url(href):
    """Retourne (url_propre, asin) ou (None, None) si ce n'est pas un produit."""
    m = ASIN_RE.search(href or "")
    if not m:
        return None, None
    asin = m.group(1)
    return f"https://www.amazon.fr/dp/{asin}", asin

def full_size_image(src):
    """Enleve le suffixe de miniature ._AC_US40_. pour obtenir l'image grande taille."""
    return re.sub(r"\._[^.]+_\.", ".", src)

def extract_images(soup):
    urls = []
    landing = soup.select_one("#landingImage")
    if landing:
        dyn = landing.get("data-a-dynamic-image")
        if dyn:
            try:
                import json
                urls.extend(json.loads(dyn).keys())
            except Exception:
                pass
        if landing.get("src"):
            urls.append(landing["src"])
    for img in soup.select("#altImages img"):
        if img.get("src"):
            urls.append(img["src"])
    out = []
    for u in urls:
        if "/images/I/" in u:
            u = full_size_image(u.split("?")[0])
            if u not in out:
                out.append(u)
    return out

def extract_color(soup):
    el = soup.select_one("#variation_color_name .selection")
    if el and el.get_text(strip=True):
        return el.get_text(strip=True)
    el = soup.select_one("tr.po-color td.po-break-word")
    if el and el.get_text(strip=True):
        return el.get_text(strip=True)
    for row in soup.select("#productDetails_techSpec_section_1 tr, #productDetails_detailBullets_sections1 tr"):
        th = row.find("th")
        td = row.find("td")
        if th and td and "couleur" in th.get_text(strip=True).lower():
            return td.get_text(strip=True)
    return None

def find_subcategories(driver, category_url):
    if not safe_get(driver, category_url):
        return []

    soup = BeautifulSoup(driver.page_source, "lxml")
    subs = []

    links = soup.select("a[href*='/s?']")

    for a in links:
        href = a.get("href")
        name = a.get_text(strip=True)

        if href and name and "ordinateur" in name.lower():
            link = urljoin(BASE_URL, href)
            subs.append((name, link))

    if not subs:
        subs.append(("Ordinateurs portables", category_url))

    return subs

def extract_product_links_from_search(driver):
    soup = BeautifulSoup(driver.page_source, "lxml")
    links = []
    for a in soup.select("a[href*='/dp/'], a[href*='/gp/product/']"):
        clean, _ = clean_product_url(a.get("href"))
        if clean:
            links.append(clean)
    next_link = None
    next_btn = soup.select_one("li.a-last a, a.s-pagination-next")
    if next_btn and next_btn.get("href"):
        next_link = urljoin(BASE_URL, next_btn["href"])
    return list(dict.fromkeys(links)), next_link
    
def scrape_subcategory(driver, name, url):
    safe_name = "".join(c for c in name if c.isalnum() or c in " _-")[:60]
    subfolder = os.path.join(OUTPUT_DIR, safe_name)
    os.makedirs(subfolder, exist_ok=True)
    products = []
    page_url = url
    page_count = 0

    while page_url and page_count < MAX_PAGES and len(products) < MAX_PRODUCTS:
        page_count += 1
        print(f"Page {page_count} : {page_url}", flush=True)

        if not safe_get(driver, page_url):
            break

        links, next_link = extract_product_links_from_search(driver)
        print(f"{len(links)} liens produits trouvÃ©s", flush=True)

        for link in links:
            if len(products) >= MAX_PRODUCTS:
                break

            try:
                product = parse_product(driver, link, subfolder)
                if product:
                    products.append(product)
                    summary["products_extracted"] += 1
                    print(f"[{len(products)}] {product.title}", flush=True)
            except Exception:
                errors.append(f"Erreur produit {link}: {traceback.format_exc()}")

        page_url = next_link

    Saver.save_products(products, subfolder, safe_name)
    summary["subcategories_processed"] += 1


def parse_product(driver, url, subfolder):
    if not safe_get(driver, url):
        return None

    time.sleep(random.uniform(1.5, 3.0))
    soup = BeautifulSoup(driver.page_source, "lxml")

    title_element = soup.select_one("#productTitle")
    title = title_element.get_text(strip=True) if title_element else None

    price_element = soup.select_one(".a-price .a-offscreen")
    price = price_element.get_text(strip=True) if price_element else None

    bullets = [
        li.get_text(strip=True)
        for li in soup.select("#feature-bullets li")
        if li.get_text(strip=True)
    ]

    description_element = soup.select_one("#productDescription")
    description = (
        description_element.get_text(" ", strip=True)
        if description_element else None
    )

    if not description:
        aplus = soup.select_one("#aplus")
        if aplus:
            description = aplus.get_text(" ", strip=True)[:1500] or None

    if not description and bullets:
        description = " ".join(bullets)

    _, asin = clean_product_url(url)
    color = extract_color(soup)
    images = extract_images(soup)

    img_folder = os.path.join(subfolder, "images")
    os.makedirs(img_folder, exist_ok=True)

    for i, img_url in enumerate(images[:3]):
        try:
            response = requests.get(img_url, timeout=15)
            if response.status_code == 200:
                filename = f"{asin}_{i + 1}.jpg" if asin else f"img_{i + 1}.jpg"
                with open(os.path.join(img_folder, filename), "wb") as file:
                    file.write(response.content)
                summary["images_downloaded"] += 1
        except Exception as e:
            errors.append(f"Erreur image {img_url}: {e}")

    return Product(url, asin, title, price, None, color, description, bullets, images)


