import lissandra as liss
from lissandra import ProfileIcons


def get_items():
    profile_icons = liss.get_profile_icons(region="NA")
    for pi in profile_icons:
        print(pi.name)
    print(profile_icons[10].name)


if __name__ == "__main__":
    get_items()
