# Import modules
import yaml
import bonobo
from chapter_08.etl.extract import extract_data
from chapter_08.etl.transform import (
    transform_crash_data,
    transform_vehicle_data,
    transform_people_data
)
from chapter_08.tools.bonobo.load import load_data

# Import file configuration
with open('../../config.yaml', 'r') as file:
    config_data = yaml.safe_load(file)

# Step 1: Extract data
def extract_all_data() -> list:
    crashes_df = extract_data(filepath=config_data['crash_filepath'],
                              select_cols=config_data['crash_columns_list'],
                              rename_cols=config_data['crash_columns_rename_dict'])
    vehicle_df = extract_data(filepath=config_data['vehicle_filepath'],
                              select_cols=config_data['vehicle_columns_list'],
                              rename_cols=config_data['vehicle_columns_rename_dict'])
    people_df = extract_data(filepath=config_data['people_filepath'],
                              select_cols=config_data['crash_columns_list'],
                              rename_cols=config_data['crash_columns_rename_dict'])
    return [crashes_df, vehicle_df, people_df]

# Step 2: Transform Data
def transform_all_data(data: list) -> list:
    transformed_crashes_df = transform_crash_data(data[0])
    transformed_vehicle_df = transform_vehicle_data(data[1])
    transformed_people_df = transform_people_data(data[2])
    return [transformed_crashes_df, transformed_vehicle_df, transformed_people_df]

# Step 3: Load Data
# - import new bonobo load_data() in bonobo directory

# Define the Bonobo pipeline
def get_graph(**options):
    graph = bonobo.Graph()
    graph.add_chain(extract_all_data, transform_all_data, load_data)
    return graph

# Define the main function to run the Bonobo pipeline
def main():
    # Set the options for the Bonobo pipeline
    options = {
        'services': [],
        'plugins': [],
        'log_level': 'INFO',
        'log_handlers': [bonobo.logging.StreamHandler()],
        'use_colors': True,
        'graph': get_graph()
    }
    # Run the Bonobo pipeline
    bonobo.run(**options)

if __name__ == '__main__':
    main()
