MONTHS_IN_YEAR = 12
WEEKS_IN_MONTH = 4

SUBUNIT_CURRENCY = 100

SUBSCRIBERS_FEATURES = {
    'free': {
        'max_billboards_upload': 3,
        'max_billboards_sale': 2,
        'analytics': False,
    },

    'basic': {
        'max_billboards_upload': 5,
        'max_billboards_sale': 3,
        'analytics': False,
    },

    'pro': {
        'max_billboards_upload': float('inf'),
        'max_billboards_sale': float('inf'),
        'analytics': True,
    }
}
