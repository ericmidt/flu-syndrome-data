import requests
from datetime import datetime, timedelta
import calendar
import json
import boto3
import os
from dotenv import load_dotenv

class NotificationsProcessor:

    def __init__(self):
        # API credentials
        self.url = "https://elasticsearch-saps.saude.gov.br/desc-esus-notifica-estado-pr/_search"
        self.username = "user-public-notificacoes"
        self.password = "Za4qNXdyQNSa9YaA" # standard password for the API
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def fetch_and_processs_data(self, start_date, end_date):

        # Define the date range
        start_date = datetime(2022, 11, 1)
        end_date = datetime.now()

        # Define the array that will hold all the records
        all_records = []

        # Loop through each year and month
        current_date = start_date
        while current_date <= end_date:
            # Calculate the last day of the current month
            last_day = calendar.monthrange(current_date.year, current_date.month)[1]

            # Define the query parameters for the search
            query_params = {
                "q": f"@timestamp:[{current_date.strftime('%Y-%m-%dT00:00:00.000Z')} TO {current_date.replace(day=last_day).strftime('%Y-%m-%dT23:59:59.999Z')}]",
                "size": 10000  # Specify the batch size
            }

            # Make a GET request to the API URL with query parameters
            response = self.session.get(self.url, params=query_params)

            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                # Process the hits as needed
                hits = data.get("hits", {}).get("hits", [])
                for hit in hits:
                    source = hit.get("_source", {})
                    keys_to_retrieve = ["id", "@timestamp", "sexo", "idade", "racaCor",
                                        "sintomas", "dataInicioSintomas",
                                        "municipio", "estado", "dataPrimeiraDose", "dataSegundaDose",
                                        "dataNotificacao", "municipioNotificacao", "estadoNotificacao",
                                        "recebeuAntiviral", "profissionalSaude", "profissionalSeguranca"]
                    selected_data = {}
                    for key in keys_to_retrieve:
                        value = source.get(key)
                        selected_data[key] = value

                    # Append selected data to all records list
                    all_records.append(selected_data)

                print(f"Processed {len(hits)} hits for {current_date}")

            else:
                print(f"Error in request for {current_date}: {response.status_code}")

            # Move to the next month
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)


        # Insert all records into json file
        with open("flu_data.json", "a", encoding="utf-8") as json_file:
            # Load existing data from json file
            json.dump(all_records, json_file, indent=2, ensure_ascii=False)

        print("Data insertion complete.")

if __name__ == "__main__":

    processor = NotificationsProcessor()

    start_date = datetime(2022, 11, 1)
    end_date = datetime.now()

    processor.fetch_and_processs_data(start_date, end_date)

    # Load environment variables from .env file
    load_dotenv()
    
    # Access the environment variables
    aws_access_key_id = os.getenv("aws_access_key")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    aws_flu_data_bucket = os.getenv("aws_flu_data_bucket")

    s3 = boto3.client('s3')
    s3.meta.client.upload_file()
    