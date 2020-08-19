import lissandra as liss
from lissandra import Locales


def get_locales():
    locales = liss.get_locales(region="NA")
    print(locales)
    for locale in locales:
        print(locale)
    print(locales)


if __name__ == "__main__":
    get_locales()
