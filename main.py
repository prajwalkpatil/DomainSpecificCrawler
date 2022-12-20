import sys
from create_files import create_files
from preprocess import preprocess
from logger import Logger
from fetch_links import fetch_links
from fetch_data import fetch_data
start_id = 1000
item_ids = []


def main():
    global item_ids
    Logger.start_log()
    create_files(start_id)

    item_ids = sys.argv[1:]
    if len(item_ids) < 1:
        Logger.write_error("No ID specified")
        Logger.end_log()
        sys.exit(1)
    else:
        Logger.write_info("ID(s): " + str(item_ids))

    preprocess(item_ids)
    fetch_links(10)
    fetch_data()
    Logger.end_log()


if __name__ == "__main__":
    main()
