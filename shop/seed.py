from shop.models import Category, Product

# Создаём категорию, если её нет
rolls, _ = Category.objects.get_or_create(
    name="Роллы",
    slug="rolls"
)

items = [
    ("Филадельфия", "philadelphia", 450, "products/philadelphia.jpg"),
    ("Калифорния", "california", 390, "products/california.jpg"),
    ("Дракон", "dragon", 520, "products/dragon.jpg"),
    ("Спайси ролл", "spicy", 410, "products/spicy.jpg"),
    ("Сяке маки", "syake-maki", 320, "products/syake.jpg"),
    ("Текка маки", "tekka-maki", 330, "products/tekka.jpg"),
    ("Унаги ролл", "unagi", 550, "products/unagi.jpg"),
]

for name, slug, price, img in items:
    Product.objects.get_or_create(
        slug=slug,
        defaults={
            "category": rolls,
            "name": name,
            "description": f"Вкусный ролл {name}.",
            "price": price,
            "weight": 250,
            "image": img
        }
    )

print("Готово! Товары добавлены.")
