import argparse
import shutil
from pathlib import Path

# System and temporary files that should never be moved
IGNORED_FILES = {"desktop.ini", "thumbs.db", ".ds_store"}
IGNORED_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}

# Define file categories and their corresponding extensions
FILE_CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".csv", ".md"},
    "Videos": {".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml", ".sh"},
    "Executables": {".exe", ".msi", ".msix", ".dmg", ".pkg", ".deb", ".iso", ".img"},
}

def get_category(extension: str) -> str:
    """Return the category folder name for a given file extension."""
    ext = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def get_unique_path(destination: Path) -> Path:
    """
    If destination file exists, append a counter (e.g., file_1.txt)
    to prevent overwriting existing files.
    """
    if not destination.exists():
        return destination
    
    counter = 1
    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_dest = destination.with_name(new_name)
        if not new_dest.exists():
            return new_dest
        counter += 1

def should_skip(item: Path) -> bool:
    """Check if a file or directory should be ignored during organization."""
    return (
        item.is_dir()
        or item.name.startswith(".")
        or item.name.lower() in IGNORED_FILES
        or item.suffix.lower() in IGNORED_EXTENSIONS
        or item.name == Path(__file__).name
    )

def organize_directory(target_dir: Path, dry_run: bool = False) -> None:
    """Scan target directory and move files into category subfolders."""
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    print(f"{'[DRY RUN] ' if dry_run else ''}Organizing: {target_dir.resolve()}\n" + "-" * 45)
    moved_count = 0

    for item in target_dir.iterdir():
        if should_skip(item):
            continue

        category = get_category(item.suffix)
        category_dir = target_dir / category
        dest_path = category_dir / item.name

        # Ensure we don't overwrite an existing file with the same name
        unique_dest = get_unique_path(dest_path)

        if dry_run:
            print(f"[Would Move] {item.name} -> {category}/{unique_dest.name}")
        else:
            category_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(unique_dest))
            print(f"[Moved] {item.name} -> {category}/{unique_dest.name}")
        
        moved_count += 1

    print("-" * 45)
    print(f"Done! {moved_count} file(s) {'would be ' if dry_run else ''}organized.")

def main():
    parser = argparse.ArgumentParser(description="Automatically organize files in a folder by type.")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the directory to organize (defaults to current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the organization without actually moving any files"
    )
    args = parser.parse_args()

    target_path = Path(args.path).expanduser()
    organize_directory(target_path, args.dry_run)

if __name__ == "__main__":
    main()