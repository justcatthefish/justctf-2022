# Symple Unzipper Challenge

This repo contains a simple web server that accepts ZIP files, extracts them, and returns their contents.
It has a vulnerability that permits exfiltration of local files.

## Running the Server

It is highly recommended to run the server in Docker, since its behavior will be dependent on the specific
decompression tools installed on your system. The provided [Docker Compose script](docker-compose.yml)
expects an environment variable `FLAG` to be set, the contents of which will be written to `flag.txt` in the
same directory as the `server.py` script in the container. This is the flag that the attacker will attempt
to exfiltrate.

```console
$ env FLAG=ThisIsTheFlag docker-compose up --build
```

This will automatically run the server and bind it to port 8080 on the host. You can then connect to the 
server in your web browser, [here](http://localhost:8080/).

### Running the Server Locally

With the knowledge that it may behave slightly differently, the server _can_ be run locally (_e.g._, to make
debugging easier) by first installing the requirements:

```console
$ pip install -r requirements.txt
```

and then either executing it via Uvicorn

```console
$ uvicorn --port 8080 --host 0.0.0.0 server:app
```

or directly via Python

```console
$ python3 server.py
```

## Once the Server is Running

The web server's landing page, [`index.html`](index.html), has more information.

## Code Organization and Behavior

In the Docker container, all the files in this directory is copied to `/server/`. 

All the server code is in a single Python file: [/server/server.py](server.py). When started, it does two things:
1. If the `FLAG` environment variable is set, _and_ if  `/server/flag.txt` does not exist, then it saves the contents of
   the `FLAG` environmment variable to `/server/flag.txt`
2. Creates the directory `/server/uploads/`, if it does not already exist 

When a new ZIP extraction request is handled, the following steps occur:
1. A new temporary directory is created in `/server/uploads/`
2. The ZIP is saved to `/server/uploads/[TEMPDIR]/[ZIPFILE]`
3. The file is confirmed to be a ZIP by running 
   [`zipfile.is_zipfile`](https://docs.python.org/3/library/zipfile.html#zipfile.is_zipfile);
   if not, then an HTTP error 415 is returned
4. A new temporary directory is created: `/server/uploads/[TEMPDIR]/[SECOND_TEMPDIR]/`
5. The ZIP is extracted into `[SECOND_TEMPDIR]` using the [patool library's](https://wummel.github.io/patool/)
   [`extract_archive`](https://github.com/wummel/patool/blob/4928f3fc5083248ec83bbf6b02b5d9089c309100/patoolib/__init__.py#L760-L767)
   function
6. The server traverses all the extracted files and serializes their names and contents to a JSON dictionary; any files 
   that cannot be decoded in UTF-8 are Base64 encoded

## License and Acknowledgements

This code was created by [Evan Sultanik](https://www.sultanik.com/) and is licensed and distributed under the
[AGPLv3](LICENSE) license.
