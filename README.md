# justCTF 2022

This repo contains sources for [justCTF 2022](https://2022.justctf.team) challenges hosted by [justCatTheFish](https://ctftime.org/team/33893) as well as summary of winners and sponsors of the event.

TLDR: Run a challenge with `./run.sh` (requires Docker/docker-compose and might require `sudo` as we use `nsjail` extensively under the hood).

The [`challenges/`](./challenges/) contains challanges directories with the following structure:
* `README.md` - official challenge description used during CTF
* `run.sh` - shell script to run the challenge locally (uses Docker and sometimes docker-compose)
* `public/` - files that were public/to download
* `private/` - sources and other unlisted files
* `flag.txt`/`metadata.json` - the flag (don't look there?)
* `solv/` - scripts and files with raw solution (used by healthcheck, if exists)
* other files


### Winners & Prizes
* 1st place - [C4T BuT S4D](https://ctftime.org/team/83435) - $3200 + 1x Binary Ninja Personal
* 2nd place - [Never Stop Exploiting](https://ctftime.org/team/13575) $1500 + 1x Binary Ninja Personal
* 3rd place - [0ops](https://ctftime.org/team/4419) - $1000 + 1x Binary Ninja Personal
* 4-8th place - [DiceGang](https://ctftime.org/team/109452), [r3kapig](https://ctftime.org/team/58979), [Water Paddler](https://ctftime.org/team/155019), [idek](https://ctftime.org/team/157039) - 1x Binary Ninja Personal

* We also give a 1x Binary Ninja Personal license for the best writeup that uses Binary Ninja
* We also provided  $50 for each of the two unsolved challenges to the first winners

### justCTF 2022 sponsors:
* Sumo Logic - https://www.sumologic.com/
* Trail of Bits - https://www.trailofbits.com/
* Vector35 (Binary Ninja) - https://vector35.com/

Thanks again to all the sponsors who made this event possible!

### Challenges

(Sorted from most solved to least solved)

| Category | Name | Points | Solves |
|----------|------|--------|--------|
| Misc | Sanity Check | 50 | 316 |
| Misc | Bifurcation (ppc) | 103 | 121 |
| Web | Symple Unzipper | 225 | 40 |
| Crypto | Frosty | 228 | 39 |
| Pwn | Notes | 256 | 30 |
| Crypto | Simply Powered | 260 | 29 |
| Pwn | arm | 267 | 27 |
| Crypto | fROSty's Second Signature Scheme | 275 | 25 |
| Misc | Hardware Screen | 279 | 24 |
| Re | I'm slow | 283 | 23 |
| Web | Velociraptor | 288 | 22 |
| Misc | Radio Ga Ga | 288 | 22 |
| Web | GoBucket | 308 | 18 | 
| Misc, Pwn | dumpme | 333 | 14 |
| Pwn | Skilltest | 340 | 13 | 
| Web, Misc | gitara | 347 | 12 |
| Pwn | League of Lamports | 373 | 9 |
| Web | Baby XSLeak | 394 | 7 |
| Re | AMXX | 406 | 6 |
| Re, Pwn | Monsters | 406 | 6 |
| Web | Foreigner | 420 | 5 |
| Pwn | herpetology | 435 | 4 |
| Web, Misc | Web API intended | 435 | 4 |
| Re, Misc | Fancy Device | 453 | 3 |
| Web | Ninja | 500 | 1 |
| Pwn | Dark SOLs | 500 | 0 |
| Web | Dank Shark | 500 | 0 |


### Write-ups
Write-ups can be found on [CTFTime](https://ctftime.org/event/1631/tasks/). You should also look at challenges solution directories, if they exist (`solv/`).

### CTF Platform
We wrote our own CTF platform which is available [here](https://github.com/justcatthefish/ctfplatform).

