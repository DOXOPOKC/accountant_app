KLASS_TYPES = [
        (0, 'Пусто'),
        (1, 'Юридическое лицо без договора'),
        (2, 'Юридическое лицо с договором'),
        (3, 'ИЖС без договора'),
        (4, 'ИЖС с договором'),
        (5, 'Физическое лицо'),
    ]


DOC_TYPE = [
    (0, 'Доверенность'),
    (1, 'Пасспорт'),
]


def str_remove_app(string: str):
    return string.replace('/app', '')


def str_add_app(string: str):
    return string.replace('/media/', '/app/media/')
