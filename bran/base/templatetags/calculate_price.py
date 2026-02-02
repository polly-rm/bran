from django import template

register = template.Library()

VEHICLE_PRICING = {
    'small_van': {
        'fixed_ranges': [
            (20, 50),
            (30, 65),
            (40, 80),
            (50, 90),
            (60, 100),
        ],
        'per_mile_ranges': [
            (70, 1.65),
            (80, 1.55),
            (90, 1.45),
            (100, 1.35),
            (150, 1.25),
            (249, 1.15),
            (float('inf'), 1.10),
        ]
    },
    'swb': {
        'fixed_ranges': [
            (20, 60),
            (30, 75),
            (40, 90),
            (50, 100),
            (60, 110),
        ],
        'per_mile_ranges': [
            (70, 1.80),
            (80, 1.70),
            (90, 1.55),
            (100, 1.45),
            (150, 1.35),
            (249, 1.25),
            (float('inf'), 1.20),
        ]
    },
    'mwb': {
        'fixed_ranges': [
            (20, 70),
            (30, 85),
            (40, 100),
            (50, 110),
            (60, 120),
        ],
        'per_mile_ranges': [
            (70, 2.00),
            (80, 1.90),
            (90, 1.80),
            (100, 1.70),
            (150, 1.60),
            (249, 1.45),
            (float('inf'), 1.35),
        ]
    },
    'lwb': {
        'fixed_ranges': [
            (20, 80),
            (30, 95),
            (40, 110),
            (50, 120),
            (60, 130),
        ],
        'per_mile_ranges': [
            (70, 2.20),
            (80, 2.05),
            (90, 1.90),
            (100, 1.75),
            (150, 1.65),
            (249, 1.55),
            (float('inf'), 1.50),
        ]
    },
    'xlwb': {
        'fixed_ranges': [
            (20, 90),
            (30, 105),
            (40, 120),
            (50, 130),
            (60, 140),
        ],
        'per_mile_ranges': [
            (70, 2.30),
            (80, 2.20),
            (90, 2.10),
            (100, 2.00),
            (150, 1.90),
            (249, 1.80),
            (float('inf'), 1.70),
        ]
    },
    'luton_van': {
        'fixed_ranges': [
            (20, 100),
            (30, 120),
            (40, 140),
            (50, 150),
            (60, 160),
        ],
        'per_mile_ranges': [
            (70, 2.65),
            (80, 2.55),
            (90, 2.45),
            (100, 2.35),
            (150, 2.25),
            (249, 2.15),
            (float('inf'), 2.10),
        ]
    },
}


@register.filter
def calculate_price(distance, vehicle_type):
    try:
        distance = float(distance)
    except (TypeError, ValueError):
        return 0

    if distance <= 0:
        return 0

    config = VEHICLE_PRICING.get(vehicle_type)
    if not config:
        return 0

    # 1️⃣ Fixed price ranges
    for max_distance, fixed_price in config['fixed_ranges']:
        if distance <= max_distance:
            return fixed_price

    # 2️⃣ Per-mile ranges (61+)
    for max_distance, price_per_mile in config['per_mile_ranges']:
        if distance <= max_distance:
            return round(distance * price_per_mile, 2)

    return 0


@register.filter
def calculate_price_with_vat(distance, vehicle_type):
    net_price = calculate_price(distance, vehicle_type)
    vat_price = net_price * 1.20
    return round(vat_price, 2)
