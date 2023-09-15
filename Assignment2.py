import argparse
import urllib.request
import logging
import datetime


def downloadData(url):
    """
    Reads data from a URL and returns the data as a string

    :param url: The URL of the data file.
    :return: The content of the URL.
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error downloading data: {str(e)}")
        exit(1)


def processData(file_content):
    """
    Processes the data file and returns a dictionary mapping person's ID to (name, birthday).

    :param file_content: The content of the data file.
    :return: A dictionary containing person data.
    """
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
            birthday = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            result_dict[id] = (name, birthday)
        except (ValueError, IndexError, datetime.datetime.strptime) as e:
            logging.error(f"Error processing line #{i + 1}: {str(e)}")
    return result_dict


def displayPerson(id, personData):
    """
    Displays information about a person based on their ID.

    :param id: The ID of the person to display.
    :param personData: The dictionary containing person data.
    """
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
            user_input = int(input("Enter an ID to lookup (<= 0 to exit): "))
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
    main(args.url)
