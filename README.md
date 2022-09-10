# justCTF 2022

This repo contains sources for [justCTF 2022](https://2022.justctf.team) challenges hosted by [justCatTheFish](https://ctftime.org/team/33893).

TLDR: Run a challenge with `./run.sh` (requires Docker/docker-compose and might require `sudo` as we use `nsjail` extensively under the hood).

The [`challenges/`](./challenges/) contains challanges directories with the following structure:
* `README.md` - official challenge description used during CTF
* `run.sh` - shell script to run the challenge locally (uses Docker and sometimes docker-compose)
* `public/` - files that were public/to download
* `private/` - sources and other unlisted files
* `flag.txt`/`metadata.json` - the flag (don't look there?)
* `solv/` - scripts and files with raw solution (used by healthcheck, if exists)
* other files


### Challenges

| Category | Name | Points | Solves |
|----------|------|--------|--------|

### Write-ups
Write-ups can be found on [CTFTime](https://ctftime.org/event/1631/tasks/). You should also look at challenges solution directories, if they exist (`solv/`).

### CTF Platform
We wrote our own CTF platform which is available [here](https://github.com/justcatthefish/ctfplatform).

### justCTF 2022 was sponsored by


