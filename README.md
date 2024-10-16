# Challenge #3

👋 Hi! I'm Vlad and this is my attempt for the third challenge regarding the Veridion Deeptech Engineer intern position.

🎯My goal is to extract as much data as i can from the 3 files, whiles preserving continuity and ensuring data integrity

🔧I used python for solving this problem, specifically the pandas library

🔄To recreate and run the program add the 3 data sets to a folder called "datasets" in root

🚀How i approached the solution?
The first step i took was opening the datasets to see what kind of data i was dealing with, and what kind of separator did each file have.
After that I looked at the columns of each data set in the search for the Category, Address , Phone and Company names:
 - **NAME** The Facebook and Google datasets all ready had a name field, while the Website data set had a 'legal name" field, which i renamed to "name".
 ``` python
 website_data_cleaned.rename(columns={"legal_name": "name", 's_category': 'category'}, inplace=True)
 ```
 - **Category** The Google dataset has a "category" field, the Website has a "s_category" that means the same thing, while the Facebook "category" had 3 types of fields, I assumed that the first of the 3 was the main one, to preserve a continuity among the data.
  ``` python
facebook_data_cleaned['category'] =  facebook_data_cleaned['categories'].str.split('|').str[0]
 ```
 -   **Address** Only the Website dataset did not contain an address field, so I had to create it by merging and capitalizing the "main_city", "main_region" and "main_country". Process for which i created a function for ease of use.
  ``` python
website_data_cleaned['address'] =  website_data_cleaned.apply(create_address, axis=1)
 ```
 -  **Phone** Each data set has a "phone" field, that was all ready in the E.164 formal, but i observed that the Google set also had a "raw phone" column, so if an entry had an invalid phone number, we try to extract one from the raw_phone field, process for which i used the "phonenumbers" library. While reading the documentation for this library, I noticed that there is a function that uses "region codes", for which i had a field in the Google dataset, but after continuous trial and error there was no data to be extracted by using this method.
  ``` python
google_data['phone'] =  google_data.apply(check_and_fix_phone, axis=1)
 ```
 
   ``` python
df_clean  =  df_clean[df_clean['phone'].str.match(r'^\+?\d+$', na=False)]
 ```


For cleaning the data I removed the entries that do not have a valid phone number using a regex, and i removed duplicates. I also did this again for the combined dataset, whiles also removing the n/a fields (I chose to do this by the end of the project to be sure that i can get the most data out of the sets)

💡While doing this project I learned quite a bit of things about standards and data cleaning, this being my first such project. It got me hooked for the 5 to 6 hours or so, and even more interested in data and how beautiful it is. I am eager to learn even more, in a professional environment.


	

