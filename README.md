# Automatic File Organizer

A lightweight, zero-dependency Python CLI tool that automatically sorts cluttered directories (like your `Downloads` folder) into neat categories such as **Images**, **Documents**, **Videos**, **Audio**, and **Archives**.

## Features
- **Cross-Platform**: Built with Python's `pathlib` to work seamlessly on Windows, macOS, and Linux.
- **Overwrite Protection**: Automatically renames duplicate files (e.g., `image_1.png`) so you never lose data.
- **Dry-Run Mode**: Preview exactly where files will go before moving anything.
- **Zero Dependencies**: Uses only the Python Standard Library.

## Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/auto-file-organizer.git](https://github.com/YOUR-USERNAME/auto-file-organizer.git)
   cd auto-file-organizer
   ```

2. Run a **Dry Run** first to preview changes:
   ```bash
   python organizer.py /path/to/your/folder --dry-run
   ```

3. Organize the folder:
   ```bash
   python organizer.py /path/to/your/folder
   ```