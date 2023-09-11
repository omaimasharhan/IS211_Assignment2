import argparse
import urllib.request
import logging
import datetime

def downloadData(url):

    response = urllib.request.urlopen(url)
    data = response.read()
    response.close()
    return data

def processData(file_content):
    data_dict = {}
    logger = logging.getLogger('assignment2')
    lines = file_content.decode('utf-8').split('\n')
    for line_num, line in enumerate(lines, start=1):
        fields = line.split(',')
        if len(fields) >= 3:
            person_id = fields[0]
            name = fields[1]
            birthday_str = fields[2]
            try:
                birthday_date = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()
                data_dict[person_id] = (name, birthday_date)
            except ValueError:
                logger.error(f"Error processing line #{line_num} for ID #{person_id}")

    return data_dict

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        formatted_birthday = birthday.strftime("%Y-%m-%d")
        return f"Person #{id} is {name} with a birthday of {formatted_birthday}"
    else:
        return "No user found with that id"

def main():
    parser = argparse.ArgumentParser(description="Process a CSV file from a URL.")
    parser.add_argument("--url", required=True, help="URL to fetch CSV data")
    args = parser.parse_args()

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(message)s")
    logger = logging.getLogger('assignment2')

    personData = processData(csvData)
    while True:
        try:
            user_input = input("Enter an ID number: ")
            user_id = int(user_input)
            if user_id < 0:
                break
            result = displayPerson(user_id, personData)
            print(result)
        except ValueError:
            print("Invalid input. Please enter a valid ID.")

if __name__ == "__main__":
    main()
