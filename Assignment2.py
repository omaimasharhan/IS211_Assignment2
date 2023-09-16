import argparse
import urllib.request
import logging
import datetime

def downloadData(url):

    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error downloading data: {str(e)}")
        exit(1)

def processData(file_content):

    result_dict = {}
    lines = file_content.split("\n")
    for i, record in enumerate(lines):
        items = record.split(",")
        if items[0] == "id":
            continue
        try:
            id = int(items[0])
            name = items[1]
            date_str = items[2]
            try:
                birthday = datetime.datetime.strptime(date_str, "%d/%m/%Y")
                result_dict[id] = (name, birthday)
            except ValueError as e:
                logging.error(f"Error parsing date on line #{i + 1}: {str(e)}")
        except (ValueError, IndexError) as e:
            logging.error(f"Error processing line #{i + 1}: {str(e)}")
    return result_dict


def displayPerson(id, personData):

    if id in personData:
        name, birthday = personData[id]
        print(f"{name} was born on {birthday:%Y-%m-%d}")
    else:
        print("No user found with that id")


def main(url):
    print(f"Running main with URL = {url}...")
    url_data = downloadData(url)
    data_dict = processData(url_data)

    while True:
        try:
            user_input = int(input("Enter an ID (<= 0 to exit): "))
            if user_input <= 0:
                break
            displayPerson(user_input, data_dict)
        except ValueError:
            print("Invalid input. Please enter a valid ID.")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    logging.basicConfig(filename="error.log", level=logging.ERROR)

    main(args.url)
