import lissandra as liss
from lissandra import LanguageStrings


def get_language_strings():
    language_strings = liss.get_language_strings(region="EUW")
    print(language_strings.strings)


if __name__ == "__main__":
    get_language_strings()
