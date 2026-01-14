# gitscanner

gitscanner is a Python script that scans a list of URLs to check for exposed Git repositories.

## Usage

To use gitscanner, you need a JSON file containing a list of URLs to scan.

```bash
python3 src/gitscanner/gitscanner.py urls.json
```

### Options

- `-v`, `--verbose`: Enable verbose logging.
- `-t`, `--timeout`: Set a custom timeout in seconds for HTTP requests. Default is 5 seconds.

## JSON File Format

The JSON file should contain a single list of strings, where each string is a URL to be scanned. 

### Example `urls.json`

```json
[
    "http://example.com/",
    "http://another-example.com/"
]
```
