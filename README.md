# dirb.py

**A minimal dir buster implementation**

## Run

```bash
git clone https://github.com/607011/dirb.git
cd dirb
pipenv install
pipenv run ./dirb.py "http://example.com" < path-list.txt
```

Where `http://example.com` is the root of the URL to scan for existent paths, and `path-list.txt` is a file containing paths to check, one per line.

