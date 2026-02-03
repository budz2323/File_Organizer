import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Organize files in a directory by file extenstion"
)

parser.add_argument(
    "directory",
    help = "Target directory to organize"
)

parser.add_argument(
    "--dry-run",
    action = "store_true",
    help = "show what would be moved withour making changes"
)

args = parser.parse_args()
target_dir = Path(args.directory)

if not target_dir.exists() or not target_dir.is_dir():
    print("Error: Directory does not exist")
    exit(1)

for item in target_dir.iterdir():
        if not item.is_file():
            continue
        extension = item.suffix.lower()

        if extension:
            folder_name = extension[1:]
        else:
            folder_name = "no_extension"

        destination = target_dir / folder_name
        
        if args.dry_run:
            print(f"[DRY RUN] Would move {item.name}-> {folder_name}/")
        else:
            destination.mkdir(exist_ok=True)
            try:
                item.rename(destination / item.name)
                print(f"Moved {item.name}->{folder_name}/")
            except Exception as e:
                print(f"Could Not move {item.name}: {e}")
