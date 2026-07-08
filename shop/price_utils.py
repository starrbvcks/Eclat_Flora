from decimal import Decimal, InvalidOperation


PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
PERSIAN_SEPARATOR = '٬'
PERSIAN_DECIMAL_SEPARATOR = '٫'


def normalize_price(value):
    if value in (None, ''):
        return None

    try:
        decimal_value = Decimal(str(value).replace(',', '').replace('٬', '').strip())
    except (InvalidOperation, AttributeError, ValueError):
        return None

    return decimal_value


def format_price_value(value):
    normalized = normalize_price(value)
    if normalized is None:
        return ''

    sign = '-' if normalized < 0 else ''
    normalized = abs(normalized)
    integer_part = int(normalized)
    fraction_part = normalized - integer_part

    formatted = f'{integer_part:,}'.replace(',', PERSIAN_SEPARATOR)
    if fraction_part:
        fraction = format(fraction_part.normalize(), 'f').split('.', 1)[1]
        formatted = f'{formatted}{PERSIAN_DECIMAL_SEPARATOR}{fraction}'

    formatted = f'{sign}{formatted}'
    return formatted.translate(PERSIAN_DIGITS)
