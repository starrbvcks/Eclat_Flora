from django.db.models import Case, IntegerField, Value, When

from .models import Category


def category_list(request):
    category_order = Case(
        When(name='دسته گل', then=Value(0)),
        When(name='کالکشن', then=Value(1)),
        When(name='جانبی', then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )

    categories = Category.objects.filter(parent__isnull=True).order_by(category_order, 'name')
    return {'categories': categories}
