# File : src/extractor.py
import os
import datetime
import sys
import pandas as pd

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Execute program to retrieve all new data
def execute_program(dev_eui, beginning_date, ending_date):
    all_dev_eui = ""
    for dev in dev_eui:
        all_dev_eui += str(dev) + ","
    all_dev_eui = all_dev_eui[:-1]

    exe_path = resource_path("src/getDataFromIotSensors.exe")

    ret_value = os.system("""{0} {1} {2} {3}""".format(
        exe_path,
        all_dev_eui,
        '"' + str(beginning_date) + '"',
        '"' + str(ending_date) + '"'
    ))
    
    if ret_value == 1:
        raise Exception('Database is not reachable. Please verify that you are in a Virtual Machine (VM). Socotec Monitoring Wifi and Ethernet block the access...')
    elif ret_value == 2:
        raise Exception('Erreur, soit le devEUI est incorrect, soit vous êtes connecté à un réseau qui ne permet pas l\'accès à la base de données.(Cementys le bon)')

# Extract data from the database and save it to a text file.
def extract_data(result_list, debut_input, fin_input):
    print("Extracting data...")
    
    """
    Extract data from the database and save it to a text file.

    Args:
        config : The configuration dictionary.
        result_list : The list of DevEUIs.
        debut_input : The beginning date.
        fin_input : The ending date.
    
    Returns:
        result : The list of dataframes containing the raw data.
    """
    
    logs_file_name = "ErrorLogs_ReadDataSensorIoT.txt"
    DevEUIs = result_list
    beginning_date = datetime.datetime.strptime(debut_input, '%Y-%m-%d %H:%M:%S%z')
    ending_date = datetime.datetime.strptime(fin_input, '%Y-%m-%d %H:%M:%S%z')

    folder_path = resource_path(".tmp_files")
    result = []
    
    # Create folder for processed data
    print("\n> Extracting data from the database...")

    try:
        # Execute program to retrieve all new data
        execute_program(DevEUIs, beginning_date, ending_date)

        for device_id in DevEUIs:
            file_path = os.path.join(folder_path, f"output_{device_id}.txt")
            try:
                df = pd.read_csv(file_path)
                result.append(df)
            except FileNotFoundError:
                print(f"Fichier non trouvé : {file_path}")
            except Exception as e:
                print(f"Erreur pour {file_path} : {e}")
        
        return result
    
    except Exception as e:
        print(e)
        with open(logs_file_name, 'a', encoding="utf-8") as file:
            file.write(f"{datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')}, {DevEUIs}, {str(e)}\n")
    
    print("\n> Data extraction done")

def filter_excel_rows(
    file_path: str,
    sheet_name: str,
    column_name: str,
    condition_func
) -> pd.DataFrame:
    """
    Load an Excel file, select a sheet and filter rows where condition_func(column_value) returns True.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str): Sheet name to read.
        column_name (str): Column to apply the condition on.
        condition_func (function): A function that takes a single value and returns True or False.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows where condition is met.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
    except Exception as e:
        print(f"Error loading file: {e}")
        return pd.DataFrame()

    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in the sheet.")
        return pd.DataFrame()

    try:
        filtered_df = df[df[column_name].apply(condition_func)]
        return filtered_df
    except Exception as e:
        print(f"Error during filtering: {e}")
        return pd.DataFrame()
    
    