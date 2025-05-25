from products.models import Category


# def category_menu(request):
#     return {'categories': Category.objects.all()}

def category_menu(request):
    categories = Category.objects.root_nodes()  # فقط دسته‌های سطح اول
    return {'category_menu': categories}
# def category_menu(request):
#     return {
#         'categories': Category.objects.filter(parent__isnull=True)
#     }