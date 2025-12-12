import re

def slugify_fa(text):
    """
    تولید اسلاگ 100٪ فارسی بدون حذف یا تبدیل حروف.
    فقط فاصله → خط تیره
    فقط حذف کاراکترهای ممنوع در URL
    """

    # حذف کاراکترهای غیرمجاز مثل ! @ # % ^
    text = re.sub(r'[^\w\u0600-\u06FF\s-]', '', text)

    # تبدیل چند فاصله به یک فاصله
    text = re.sub(r'\s+', ' ', text).strip()

    # تبدیل فاصله به خط تیره
    text = text.replace(" ", "-")

    return text
