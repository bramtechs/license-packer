import sys
import argparse
import os
import json
from pathlib import Path

DEFAULT_IGNORED = ["node_modules","tools","examples", ".cxx", "docs", "doc", "test", "tests"]
LICENSE_FILE_NAMES = ["license","licenses", "copying", "copyright"]

def add_to_set(s: set, x):
  return len(s) != (s.add(x) or len(s))

def no_print(*args):
    pass

def should_include(path):
    for name in LICENSE_FILE_NAMES:
        parents = list(map(lambda p: os.path.basename(p).lower(), path.parents))
        if name in parents:
           return True 
        if path.name.lower().startswith(name):
            return True
    return False

def lib_name_from_path(path):
    for path in Path(path).parents:
       if not any(child in path.name.lower() for child in LICENSE_FILE_NAMES):
            return path.name.replace(' ',"-")
    raise f"Unable to tell name from path {path}"

def html_content(content):
    return f"""
    <main>
        {content} 
    </main>
    """

def html_content_item(content, path, hash):
    display_name = lib_name_from_path(path).replace('-',' ')
    target = f"license-{lib_name_from_path(path)}-{hash}"
    return f"""
    <article id={target}>
        <h2>{display_name}</h2>
        <pre>{content}</pre>
    </article>
    """

def html_nav(navbar_items):
   return f"""
   <nav>
        <ul>
            {navbar_items} 
        </ul>
    </nav>
    """ 

def html_nav_item(path, hash):
    display_name = lib_name_from_path(path).replace('-',' ')
    target = f"#license-{lib_name_from_path(path)}-{hash}"
    return f"""
        <li>
            <a href="{target}">{display_name}</a>
        </li>
    """

def find_licenses(folder, output_file, ignored, warn_gpl, export_json, print=no_print, vprint=no_print):
    licenses = set() 
    navbar = ""
    license_html = ""
    json_libs = {}

    vprint(f"Checking for licenses in folder {folder}")
    warnings = []
    for path in Path(folder).rglob('*'):
        if not should_include(path):
            continue
        if os.path.isdir(path):
            continue

        parents = list(map(lambda p: os.path.basename(p), path.parents))

        should_ignore = any(ign in parents for ign in ignored)
        if should_ignore:
            vprint(f"Ignoring {path}...")
            continue

        with open(path, encoding="utf8") as file:
            text = file.read()
            if add_to_set(licenses, text):
                vprint(f"Found unique license file at: {path}")

                if warn_gpl:
                    text_lower = text.lower()
                    if any(word in text_lower for word in ["gpl"]):
                        warnings.append(f"! Found GPL license at {path} !")

                salt = hash(path)
                json_libs[lib_name_from_path(path).replace('-',' ')] = text
                navbar += html_nav_item(path, salt)
                license_html += html_content_item(text, path, salt)

                print(path)
            
    for warn in warnings:
        print(warn)
    
    with open(output_file, "wt") as out:
        if export_json:
            output = json.dump(json_libs, out, indent=4)
        else:
            output = html_nav(navbar) + html_content(license_html)
            out.write(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='License Packer Tool')
    parser.add_argument('input', type=str, help='Input path to check')
    parser.add_argument('output', type=str, help='Path to export html to')
    parser.add_argument('--ignore', nargs='*', help="List of folders that should be ignored", default=[])
    parser.add_argument('--default-ignore', action="store_true", help=f"Use default ignore list {str(DEFAULT_IGNORED)}")
    parser.add_argument("--verbose", action="store_true", help=f"Log more things")
    parser.add_argument("--warn-gpl", action="store_true", help="Warn if detected viral GPL license")
    parser.add_argument("--export-json", action="store_true", help="Write json to the output file instead of html")

    args = parser.parse_args()
    if (args.default_ignore):
        args.ignore = set(args.ignore)
        args.ignore.update(DEFAULT_IGNORED)

    vprint = print if args.verbose else no_print
    vprint(f"Set ignored folders to {str(args.ignore)}")
    find_licenses(folder=args.input, export_json=args.export_json, output_file=args.output, ignored=args.ignore, warn_gpl=args.warn_gpl, print=print, vprint=vprint)
    sys.exit(0)