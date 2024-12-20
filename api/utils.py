import csv


def parse_csv_file(file):
    """
    Parses the uploaded csv file
    convert to JSON like list of dictionaries.
    :param file: Uploaded file object
    :return: List of rows as dictionaries
    """
    try:
        file_data = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(file_data)
        return list(reader), None
    except Exception as e:
        return None, str(e)
