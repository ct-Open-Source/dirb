# dirb.py

**An improved dir buster implementation in Python.**

This software scans a web server for accessible paths. Paths to check are read from text files, one path per line.

Thanks to massive parallelization using asynchronous I/O, this implementation works very fast.

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
  -n 10
  -f \
  --csv \
  -o scan-result.csv
```

Where `http://example.com` is the root of the URL to scan for existent paths, and `path-list[1..n].txt` are files containing paths to check. 
`-n` determines the number of workers being spawned, i.e. how many checks can run concurrently (default: 20).
`--csv` produces CSV output, suitable e.g. for spreadsheet programs.
With option `-f` the HTTP client follows redirects.
`-o` directs output to a file.

See `dirb.py -h` for more options.


## License

See [LICENSE](LICENSE)
