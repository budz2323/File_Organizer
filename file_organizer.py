import argparse
import logging
from pathlib import Path

#Argument parsing
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
    help = "show what would be moved without making changes"
)

args = parser.parse_args()
target_dir = Path(args.directory)

#Setting up logging logic
logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starting file organization")
logging.info(f"Target diretoy:{target_dir}")
logging.info(f"Dry run mode: {args.dry_run}")

if not target_dir.exists() or not target_dir.is_dir():
    print("Error: Directory does not exist")
    exit(1)

def get_safe_destination(dest_path: Path) -> Path:
    counter = 1 
    new_path = dest_path

    while new_path.exists():
        new_path= dest_path.with_stem(f"{dest_path.stem}_{counter}")
        counter +=1
    return new_path

#Main Script
for item in target_dir.iterdir():
    if not item.is_file():
        continue
    extension = item.suffix.lower()

    if extension:
        folder_name = extension[1:]
    else:
        folder_name = "no_extension"

    destination_dir = target_dir / folder_name
    destination_file = destination_dir/item.name
    
    if args.dry_run:
        message = f"[DRY RUN] Would move {item.name}-> {folder_name}/"
        print(message)
        logging.info(message)
        continue
        
    try:
        destination_dir.mkdir(exist_ok=True)
        safe_path = get_safe_destination(destination_file)
        item.rename(safe_path)

        if safe_path.name != item.name:
            message = f"Moved {item.name}->{folder_name}/{safe_path.name}(renamed)"
        else:
            message = f"Moved {item.name}->{folder_name}/"
        print(message)
        logging.info(message)

    except Exception as e:
        error_msg = f"Could Not move {item.name}: {e}"
        print(error_msg)
        logging.error(error_msg)
        
logging.info("File Organizer Finished")
