import lissandra as liss


def get_versions():
    versions = liss.get_versions(region="NA")
    print(versions[0])
    print(versions.region)

    versions = liss.get_versions(region="NA")
    print(versions[0])

    realms = liss.get_realms(region="NA")
    print(realms.latest_versions)


if __name__ == "__main__":
    get_versions()
