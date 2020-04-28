def str_remove_app(string: str):
    return string.replace('/app', '')


def str_add_app(string: str):
    return string.replace('/media/', '/app/media/')
