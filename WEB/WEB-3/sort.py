import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread


parser = argparse.ArgumentParser(description="Folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="sorted")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []


def grab_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grab_folder(el)


def copy_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            new_path = output / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as error:
                print(f"Error: {error}")


if __name__ == "__main__":
    print(source, output)
    folders.append(source)
    grab_folder(source)
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join for th in threads]
    print("Sorting is complete")
