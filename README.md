[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/crimack/lissandra/blob/master/LICENSE.txt)

# Lissandra

A Python adaptation of the Riot Games Teamfight Tactics API (https://developer.riotgames.com/).

Lissandra is a fork of Cassiopeia, a wrapper for the main League of Legends API. It provides a similar, user-friendly experience but focuses only on the TeamFight Tactics (TFT) APIs.

## Roadmap

*Note*: This library is currently a work in progress. Stuff might move around or never get finished.

- [x] Fork from Cassiopeia and rewrite the history
- [x] Support the summoner API
- [x] Support the leagues API
- [ ] Join summoner API to league (mr_wiggles = TFTSummoner(), mr_wiggles.league) type stuff
- [ ] Write a Cdragon data provider (DDragon has no static data for TFT)
- [ ] Model TFT items/stats
- [ ] Support the match history API
- [ ] Support the match API


## Documentation and Examples
TODO


## Installation
TODO

`pip install lissandra`


## Why use Lissandra?

* Works on on the Cassiopeia tech stack, which has been refined over the past few years by the [Meraki Analytics team](https://github.com/meraki-analytics).

* An excellent user interface that makes working with data from the Riot API easy and fun.

* "Perfect" rate limiting.

* Guaranteed optimal usage of your API key.

* Built in caching and (coming) the ability to easily hook into a database for offline storage of data.

* Dynamic settings so you can configure Liss for your specific use case.

## Questions/Contributions
Feel free to send pull requests, contact via GitHub or email.

## Bugs
If you find bugs please let us know via an issue or pull request.

## Disclaimer
Lissandra isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends or TeamFight Tactics. League of Legends TeamFight Tactics and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
