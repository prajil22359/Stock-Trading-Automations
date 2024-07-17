from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import numpy as np


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import csv
import requests
import time
import telebot
import traceback
import subprocess



def time_sleep(t):
    for i in range(t):
        time.sleep(1)
        print(t-i)


def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_table_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='table__lg')
    if table:
        rows = table.find_all('tr')
        extracted_data = []
        for row in rows[1:]:  # Skip the first row as it contains headers
            cells = row.find_all('td')
            if len(cells) >= 8:  # Ensure that there are enough cells in the row
                sn = cells[0].text.strip()
                contract_no = int(cells[1].text.strip())
                stock_symbol = cells[2].text.strip()
                buyer = cells[3].text.strip()
                seller = cells[4].text.strip()
                quantity = float(cells[5].text.strip().replace(',', ''))
                rate_rs = float(cells[6].text.strip().replace(',', ''))
                amount_rs = float(cells[7].text.strip().replace(',', ''))
                title = cells[2].get('title', '')  # Fetch title attribute from the third cell
                extracted_data.append([sn, contract_no, stock_symbol, buyer, seller, quantity, rate_rs, amount_rs, title])
        return extracted_data
    else:
        print("Table not found in HTML content.")
        return None

def write_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['SN', 'Contract No.', 'Stock Symbol', 'Buyer', 'Seller', 'Quantity', 'Rate (Rs)', 'Amount (Rs)', 'Title'])
    df['Stock Symbol_Buyer'] = df['Stock Symbol'] + '_' + df['Buyer']
    df['Stock Symbol_Seller'] = df['Stock Symbol'] + '_' + df['Seller']
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename} with additional columns.")

    return df

def send_file_on_tg(filename,API_KEY, user ):
    files = {"document": open(filename, 'rb')}
    resp = requests.post("https://api.telegram.org/bot" + API_KEY +
                                "/sendDocument?chat_id=" + user,
                                files=files)
    return resp

# send_file_on_tg('report_table_data.pdf', API_KEY, "800851598" )



# def check_success(df):
#     symbol_buyer_freq = df['Stock Symbol'].value_counts()
#     # symbol_buyer_freq.to_csv("symbol_buyer_freq")
#     print("--------------------")
#     print("symbol_buyer_freq:", (symbol_buyer_freq))
#     # print("symbol_buyer_freq:", symbol_buyer_freq.iloc[1])

#     # Filter 'Stock Symbol' with frequency > 25
#     frequent_symbols = symbol_buyer_freq[symbol_buyer_freq > 25].index.tolist()
#     print("--------------------")
#     print("frequent_symbols:", frequent_symbols)
#     # Filter DataFrame to include only rows with 'Stock Symbol' in frequent_symbols
#     filtered_df = df[df['Stock Symbol'].isin(frequent_symbols)]

#     filtered_df.reset_index(drop=True, inplace=True)


#     # Group by 'Stock Symbol' and sum the 'Amount (Rs)'
#     total_amounts = filtered_df.groupby('Stock Symbol')['Amount (Rs)'].sum()

#     print("total_amounts:", total_amounts)
#     success_symbols = total_amounts[total_amounts > 5000000].index.tolist()

#     # If there are any success symbols, print "Success" along with those symbols
#     if success_symbols:
#         print("Success:")
#         for symbol in success_symbols:
#             print(symbol)
#         bot.send_message(
#             800851598, str(success_symbols))
#     else:
#         print("No success found.")


import pandas as pd
import numpy as np

# def check_success(df):

#     symbol_buyer_freq = df['Stock Symbol'].value_counts()
#     # print("--------------------")
#     # print("symbol_buyer_freq:", symbol_buyer_freq)

#     # Filter 'Stock Symbol' with frequency > 25
#     frequent_symbols = symbol_buyer_freq[symbol_buyer_freq > 25].index.tolist()
#     # print("--------------------")
#     # print("frequent_symbols:", frequent_symbols)

#     for symbol in frequent_symbols:
#         filtered_df = df[df['Stock Symbol'] == symbol]
#         # filtered_df = pd.read_csv("sshl.csv")


#         # Group by 'Stock Symbol' and sum the 'Amount (Rs)'
#         total_amount = filtered_df['Amount (Rs)'].sum()

#         if total_amount > 5000000:
#             string_to_return = ""
#             string_to_return += (f"Symbol {symbol} has total turnover {total_amount/100000:.2f} lacs.")

#             # Initialize trend column and val
#             filtered_df['trend'] = 0
#             val = 0

#             # Iterate over rows to calculate the trend
#             for i in range(1, len(filtered_df)):
#                 if filtered_df.iloc[i]['Rate (Rs)'] > filtered_df.iloc[i-1]['Rate (Rs)']:
#                     val = -1
#                 elif filtered_df.iloc[i]['Rate (Rs)'] < filtered_df.iloc[i-1]['Rate (Rs)']:
#                     val = +1
#                 # else, val remains the same
#                 filtered_df.at[filtered_df.index[i], 'trend'] = val

#             filtered_df.to_csv(f"filtered_df_{symbol}.csv", index=False)

#             # print("filtered_df with trend:", filtered_df[['Rate (Rs)', 'trend']])
            
#             # Check if the trend is mixed, increasing or decreasing
#             # (filtered_df['trend'] >= 0).all():
#             #     print(f"Symbol {symbol} has an increasing price trend.")
#             # elif (filtered_df['trend'] <= 0).all():
#             #     print(f"Symbol {symbol} has a decreasing price trend.")
#             # else:                
#             # Calculate volumes for increasing and decreasing trends


#             increasing_volume = filtered_df[filtered_df['trend'] == 1]['Quantity'].sum()
#             decreasing_volume = filtered_df[filtered_df['trend'] == -1]['Quantity'].sum()
#             total_volume = filtered_df['Quantity'].sum()
            
#             # print("increasing_volume", increasing_volume)
#             # print("decreasing_volume", decreasing_volume)
#             string_to_return += (f"\nSymbol {symbol} has total volume ({total_volume}).")

#             if increasing_volume > decreasing_volume:
#                 string_to_return += (f"\nSymbol {symbol} has net volume ({increasing_volume}) in increasing trend.")
#             else:
#                 string_to_return += (f"\nSymbol {symbol} has net volume ({decreasing_volume}) in decreasing trend.")
        
#             # Send message to bot
#             bot.send_message(800851598, string_to_return)


import pandas as pd

def check_success(df):

    symbol_buyer_freq = df['Stock Symbol'].value_counts()
    # print("--------------------")
    # print("symbol_buyer_freq:", symbol_buyer_freq)

    # Filter 'Stock Symbol' with frequency > 25
    frequent_symbols = symbol_buyer_freq[symbol_buyer_freq > 25].index.tolist()
    # print("--------------------")
    # print("frequent_symbols:", frequent_symbols)

    for symbol in frequent_symbols:
        filtered_df = df[df['Stock Symbol'] == symbol]
        # filtered_df = pd.read_csv("sshl.csv")

        # Group by 'Stock Symbol' and sum the 'Amount (Rs)'
        total_amount = filtered_df['Amount (Rs)'].sum()

        if total_amount > 5000000:
            string_to_return = ""
            string_to_return += (f"Symbol {symbol} has total turnover {total_amount/100000:.2f} lacs.")

            # Initialize trend column and val
            filtered_df['trend'] = 0
            val = 0

            # Iterate over rows to calculate the trend from the bottom up
            for i in range(len(filtered_df) - 2, -1, -1):
                if filtered_df.iloc[i]['Rate (Rs)'] > filtered_df.iloc[i + 1]['Rate (Rs)']:
                    val = -1
                elif filtered_df.iloc[i]['Rate (Rs)'] < filtered_df.iloc[i + 1]['Rate (Rs)']:
                    val = +1
                # else, val remains the same
                filtered_df.at[filtered_df.index[i], 'trend'] = val

            filtered_df.to_csv(f"filtered_df_{symbol}.csv", index=False)

            # Calculate volumes for increasing and decreasing trends
            increasing_volume = filtered_df[filtered_df['trend'] == 1]['Quantity'].sum()
            decreasing_volume = filtered_df[filtered_df['trend'] == -1]['Quantity'].sum()
            total_volume = filtered_df['Quantity'].sum()
            
            string_to_return += (f"\nSymbol {symbol} has total volume ({total_volume}).")

            if increasing_volume > decreasing_volume:
                string_to_return += (f"\nSymbol {symbol} has net volume ({increasing_volume}) in increasing trend.")
            else:
                string_to_return += (f"\nSymbol {symbol} has net volume ({decreasing_volume}) in decreasing trend.")
        
            # Send message to bot
            bot.send_message(800851598, string_to_return)



# command = "pip install -r _req.txt"
# try:
#     # subprocess.check_call(command, shell=True)
#     print("Requirements installed successfully.")
# except subprocess.CalledProcessError:
#     print("Error installing requirements.")

API_KEY = "-----ADD API KEY------"
bot = telebot.TeleBot(API_KEY, parse_mode=None)
err = ""

wait_time = 4


if __name__ == '__main__':




    try:
        driver = webdriver.Chrome()

        # Open the URL in the Chrome browser
        class_link = "https://nepalstock.com/floor-sheet"

        driver.get(class_link)
        scroll_to_bottom()
        wait = WebDriverWait(driver, 10)
        table_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-striped")))

        # change option value
        # Locate the dropdown element
        dropdown_element = driver.find_element(By.CSS_SELECTOR, ".table__perpage select")

        # Use Select class to interact with dropdown
        dropdown = Select(dropdown_element)

        # Select the option with value "500"
        dropdown.select_by_value("500")

        # Locate the button element
        button_element = driver.find_element(By.CSS_SELECTOR, ".box__filter--search")

        while(True):

            print("Click the button")
            button_element.click()

            print("Wait until the page loads 500 rows")
            time.sleep(wait_time)

            html_content = driver.page_source

            extracted_data = extract_table_data(html_content=html_content)

            if extracted_data:
                df = write_to_csv(extracted_data, "extracted_table.csv")

                check_success(df)
                print("Data extracted and saved to extracted_table.csv.")
            else:
                print("No data extracted.") 

            print("Waiting for new page") 
            time_sleep(20)





    except Exception as e2:
        e2 = traceback.format_exc(limit=None, chain=True)
        bot.send_message(
            800851598, f"Phase2_bulk_download threw error!!\n```{e2}```")
        traceback.print_exc()
