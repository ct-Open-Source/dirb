# dirb.py

**A minimal dir buster implementation.**

This software scans a web server for accessible paths. Paths to check are read from text files, one path per line.

## Prepare

```bash
git clone https://github.com/607011/dirb.git
cd dirb
pipenv install
```

## Run

For example:

```
pipenv run ./dirb.py "http://example.com" \
  -w path-list1.txt -w path-list2.txt \
  --csv \
  -f \
  -o scan-result.csv
```

Where `http://example.com` is the root of the URL to scan for existent paths, and `path-list[1..n].txt` are files containing paths to check. `--csv` produces CSV output, suitable for spreadsheet programs. With option `-f` the HTTP client follows redirects. `-o` directs output to a file.

See `dirb.py -h` for more options.


## License

See [LICENSE](LICENSE)
