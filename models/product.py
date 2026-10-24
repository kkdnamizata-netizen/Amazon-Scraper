class Product:
    def __init__(self, url, asin, title, price, label, color, description, bullets, images):
        self.url = url
        self.asin = asin
        self.title = title
        self.price = price
        self.label = label
        self.color = color
        self.description = description
        self.bullets = bullets
        self.images = images

    def to_dict(self):
        return {
            "url": self.url,
            "asin": self.asin,
            "title": self.title,
            "price": self.price,
            "label": self.label,
            "color": self.color,
            "description": self.description,
            "bullets": "; ".join(self.bullets) if self.bullets else None,
            "images_count": len(self.images)
        }
