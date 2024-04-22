from pathlib import Path
import pandas as pd
from flask_caching import Cache
import base64
import os
import zipfile

DATA_DIR = Path(Path.cwd(), 'data')

def load_and_combine_data(data_dir, folder='8451_sample'):
    """
    Load household, product, and transaction data from Parquet files, merge them,
    and process date columns.

    Args:
    - data_dir (str or Path): The base directory where data is stored.
    - sample_folder (str): The folder name containing the sample data.
    - households_file (str): Filename of the households data.
    - products_file (str): Filename of the products data.
    - transactions_file (str): Filename of the transactions data.

    Returns:
    - DataFrame: A combined dataframe with processed data.
    """
    base_path = Path(data_dir, folder)
    # Build file names
    all_files = os.listdir(base_path)
    hhd_filename = [f for f in all_files if f.endswith("parquet") and "household" in f][0]
    pd_filename = [f for f in all_files if f.endswith("parquet") and "product" in f][0]
    tr_filename = [f for f in all_files if f.endswith("parquet") and "transaction" in f][0]
    print(hhd_filename)
    # Build file paths
    hhd_path = Path(base_path, hhd_filename)
    pd_path = Path(base_path, pd_filename)
    tr_path = Path(base_path, tr_filename)
    print(hhd_path)

    # Load dataframes with trimmed column names
    hhd_df = pd.read_parquet(hhd_path).rename(columns=lambda x: x.strip())
    pd_df = pd.read_parquet(pd_path).rename(columns=lambda x: x.strip())
    tr_df = pd.read_parquet(tr_path).rename(columns=lambda x: x.strip())

    # Merge dataframes
    combined_df = tr_df.merge(pd_df, on='PRODUCT_NUM').merge(hhd_df, on='HSHD_NUM')

    # Process date columns
    combined_df['MONTH'] = pd.to_datetime(combined_df['PURCHASE_'], format='%d-%b-%y').dt.month_name()
    combined_df['DATE'] = pd.to_datetime(combined_df['PURCHASE_'], format='%d-%b-%y')

    return combined_df

def get_data(folder='8451_sample'):
    return load_and_combine_data(data_dir=DATA_DIR, folder=folder)


import os
import base64
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import pandas as pd

def save_zip(contents, filename, username):
    try:
        # Decode the content and save the zip file
        content_type, content_string = contents.split(',')
        file_data = base64.b64decode(content_string)

        # Create the directory for storing uploaded and processed files
        print(username)
        data_dir = Path('data', 'my_data')
        data_dir.mkdir(parents=True, exist_ok=True)
        zip_path = data_dir

        with open(zip_path, 'wb') as f:
            f.write(file_data)

        # Attempt to extract the zip file
        try:
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
        except BadZipFile:
            return "Error: The uploaded file is not a valid ZIP file."

        # Find CSV files
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        if len(csv_files) < 3:
            print(len(csv_files))
            return "Error: The zip file must contain at least three CSV files with names contain products, transactions, households."

        # Convert CSV files to Parquet
        for csv_file in csv_files:
            csv_path = data_dir / csv_file
            df = pd.read_csv(csv_path)
            parquet_path = csv_path.with_suffix('.parquet')
            df.to_parquet(parquet_path, engine='pyarrow')

        all_files = set(os.listdir(data_dir))
        parquet_files = {f for f in all_files if f.endswith('.parquet')}
        for file in all_files - parquet_files:
            os.remove(data_dir / file)
        return "All files are saved successfully."

    except Exception as e:
        return f"An error occurred: {str(e)}"
