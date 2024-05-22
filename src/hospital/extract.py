import os
import requests
import json
import logging
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import utils

load_dotenv()
local_directory = os.environ['LOCAL_DIRECTORY']

def run():
    cms_metastore = requests.get('https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items')
    logging.info('Retrieved metadata')
    cms_metastore_list = json.loads(cms_metastore.content)
    url_list = utils.retrieve_urls(cms_metastore_list)

    # Retrieve current time, add as metadata column
    extract_time = datetime.now()

    for item in url_list:
        extract = pd.read_csv(item, index_col=None, header=0)
        extract_time = datetime.now()
        extract['run_id'] = extract_time
        new_columns = []
        for col in extract.columns:
            new_col = utils.snake_case(col)
            new_columns.append(new_col)
        
        extract.columns = new_columns

        # Set name for csv file
        csv_name = item.split('/')[-1]
        # Check if csv exists
        if os.path.isfile(f'{local_directory}{csv_name}'):
            current_file = pd.read_csv(f'{local_directory}{csv_name}', header=0)
            if extract['run_id'].max() == current_file['run_id'].max():
                logging.info(f'{local_directory}{csv_name} already has data from previous run.')
                break
            else:
                extract = pd.concat([extract, current_file])
                extract.to_csv(f'{local_directory}{csv_name}', index=False)
                logging.info(f'{local_directory}{csv_name} has had data inserted at {extract_time}.')
        else:
            extract.to_csv(f'{local_directory}{csv_name}', index=False)
            logging.info(f'{local_directory}{csv_name} has been created at {extract_time}.')
