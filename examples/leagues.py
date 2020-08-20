import lissandra as liss
from lissandra.data import Queue, Position
from lissandra.core import Summoner


def print_leagues(summoner_name: str, region: str):
    summoner = Summoner(name=summoner_name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)

    entries = summoner.league_entries

    print("Name of leagues this summoner is in:")
    for entry in entries:
        print(entry.league.name)
    print()

    print(f"Listing all summoners in this league:")
    for position, entry in enumerate(entries.fives.league.entries):
        print(entry.summoner.name, entry.league_points, entry.tier, entry.division, position)

    print()
    print("Master's League name:")
    masters = liss.get_master_league(region=region)
    print(masters.name)


if __name__ == "__main__":
    print_leagues("Poltsc2", "NA")
