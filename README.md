# License Packer

Recursively find license files and export them to a browsable html page.<br/>
Used for https://doomhowl-interactive.com/license.

```

usage: license-packer.py [-h] [--ignore [IGNORE ...]] [--default-ignore]
                         [--verbose] [--warn-gpl]
                         input output

License Packer Tool

positional arguments:
  input                 Input path to check
  output                Path to export html to

options:
  -h, --help            show this help message and exit
  --ignore [IGNORE ...]
                        List of folders that should be ignored
  --default-ignore      Use default ignore list ['node_modules', 'tools',
                        'examples', '.cxx', 'docs', 'doc', 'test', 'tests']
  --verbose             Log more things
  --warn-gpl            Warn if detected viral GPL license
```
