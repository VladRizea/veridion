import pandas as pd
import re
import phonenumbers


# Function that does basic cleaning on the datasets
def clean_data(df):
    # Remove duplicate entries
    df_clean = df.drop_duplicates()
    # Remove entries with invalid phone numbers(we allow only numbers and '+')
    df_clean = df_clean[df_clean['phone'].str.match(r'^\+?\d+$', na=False)]
    
    return df_clean
# Function that creates an adress for the website dataset
def create_address(row):
    parts = []
    if pd.notnull(row['main_city']):
        parts.append(row['main_city'].capitalize())
    if pd.notnull(row['main_region']):
        parts.append(row['main_region'].capitalize())
    if pd.notnull(row['main_country']):
        parts.append(row['main_country'].capitalize())
    return ', '.join(parts)


# Function that creates a standard phone number from the raw_phone field
def check_and_fix_phone(row):
    if pd.isnull(row['phone']) and pd.notnull(row['raw_phone']):
        # If 'raw_phone' starts with '+', parse it
        if row['raw_phone'][0] == '+':
            parsed_number = phonenumbers.parse(row['raw_phone'], None)
            # Check if the parsed number is valid
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    return row['phone']  # Return original phone if no changes made

def main():
    print("Reading the data...")
    #* Reading the data
    facebook_data = pd.read_csv('./datasets/facebook_dataset.csv', on_bad_lines='skip', dtype={"phone": str})
    google_data = pd.read_csv('./datasets/google_dataset.csv', on_bad_lines='skip', dtype={"phone": str})
    #! The website dataset has values separated by ";"
    website_data = pd.read_csv('./datasets/website_dataset.csv', on_bad_lines='skip',dtype={"phone": str}, sep=';')

    print("Initial rows:" , len(facebook_data) + len(google_data) + len(website_data))

    print("Cleaning the data...")
    # Parsing phone numbers from "raw_phone" field for the google dataset
    google_data['phone'] = google_data.apply(check_and_fix_phone, axis=1)

    # Cleaning data
    facebook_data_cleaned = clean_data(facebook_data)
    google_data_cleaned = clean_data(google_data)
    website_data_cleaned = clean_data(website_data)


    #* Extracting just the first category for the facebook dataset
    facebook_data_cleaned['category'] = facebook_data_cleaned['categories'].str.split('|').str[0]

    #* Creating an address parameter for the website dataset
    website_data_cleaned['address'] = website_data_cleaned.apply(create_address, axis=1)

    #* Renaming the 'name' and 's_category' columns in the third dataset
    website_data_cleaned.rename(columns={"legal_name": "name", 's_category': 'category'},  inplace=True)

    #* Saving the phone numbers from the website dataset in the E.164 format standard
    website_data_cleaned['phone'] = '+' + website_data_cleaned['phone']

        

    #* Creating a dataset with all the relevant data
    df1_subset = facebook_data_cleaned[['name', 'address', 'category', 'phone']]
    df2_subset = google_data_cleaned[['name', 'address', 'category', 'phone']]
    df3_subset = website_data_cleaned[['name', 'address', 'category', 'phone']]

    newDataSet = pd.concat([df1_subset, df2_subset, df3_subset], ignore_index=True)

    # Cleaning the duplicate values
    newDataSet= newDataSet.drop_duplicates()

    # Dropna values
    newDataSet = newDataSet.dropna()

    print("Final number of rows:", len(newDataSet))

    # Saving to a new csv file
    newDataSet.to_csv('combined_dataset.csv', index=False)

    

if __name__ == "__main__":
    main()
    print("Complete")