# scripts/convert_product_slugs.py
import os
import django
from utils.slugify_fa import slugify_fa  # مطمئن شو مسیر درست است

# تنظیم محیط Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Product

def convert_all_product_slugs():
    products = Product.objects.all()

    for product in products:
        old_slug = product.slug
        new_slug = slugify_fa(product.name)  # فقط از عنوان استفاده می‌کنیم

        # چک یکتا بودن اسلاگ
        tmp_slug = new_slug
        counter = 1
        while Product.objects.filter(slug=tmp_slug).exclude(id=product.id).exists():
            tmp_slug = f"{new_slug}-{counter}"
            counter += 1

        product.slug = tmp_slug
        product.save()
        print(f"{old_slug} → {product.slug}")

if __name__ == "__main__":
    convert_all_product_slugs()
    print("✅ تمام اسلاگ‌ها بروزرسانی شدند.")
