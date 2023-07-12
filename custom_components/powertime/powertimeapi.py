
from homeassistant.core import HomeAssistant
import requests
from functools import partial
import logging
from bs4 import BeautifulSoup
_LOGGER = logging.getLogger(__name__)
class powertime_api:
    def __init__(self, username, password, hass: HomeAssistant):
        self.hass = hass
        self.username = username
        self.password = password
        self.token = None

      
    async def get_all_data(self):
        pool_data = {
            "ame": self.username,
            "pass": self.password,
            }
        with requests.Session() as s:
            # Post login data
                p = s.post("https://www.powertime.co.za/en/profile/login", data=pool_data)
                r = s.get('https://www.powertime.co.za/en/electricity/viewhistory')
                # Given HTML
                html_content = r.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find the table in the HTML
                table = soup.find('table')

                # Get the table rows
                rows = table.find_all('tr')

                data = []

                # Loop through each row
                for row in rows[1:]:  # skip the header row
                    # Find each cell in the row
                    cols = row.find_all('td')
                    # Get the href attribute from the 'View' column (5th column, so index 4)
                    href = cols[4].find('a')['href']

                    # Extract the part of the URL after "/receipt_id/"
                    view = href.split('/receipt_id/')[1].split('/')[0]

                    # Add the amount and view to the data array
                    data.append(view)

                # Now 'data' is a 2D list containing the 'Amount' and 'View' data
                data_dict = {}
                for d in data:
                    rs = s.get(f'https://www.powertime.co.za/en/electricity/voucher/receipt_id/{d}/')
                    soup = BeautifulSoup(rs.text, 'html.parser')
                    # Find the table in the HTML
                    table = soup.find('table')

                    # Get the table rows
                    rows = table.find_all('tr')

                    # Initialize an empty dictionary
                    

                    # Initialize 'units', 'date', 'meter_number', and 'total_electricity' to None.
                    units = None
                    date = None
                    meter_number = None
                    total_electricity = None

                    # Loop through each row
                    for row in rows:
                        # Find each cell in the row
                        cols = row.find_all('td')

                        # Get the text from the first column
                        key = cols[0].text.strip()

                        if key == 'Electricity Units:':
                            # If the key is 'Electricity Units:', get the value from the second column
                            units = cols[1].text.strip()

                        if key == 'Date:':
                            # If the key is 'Date:', get the value from the second column
                            date = cols[1].text.strip()

                        if key == 'Meter Number:':
                            # If the key is 'Meter Number:', get the value from the second column
                            meter_number = cols[1].text.strip()

                        if key == 'Total Electricity:':
                            # If the key is 'Total Electricity:', get the value from the second column
                            total_electricity = cols[1].text.strip()

                        if units and date and meter_number and total_electricity:
                            # If we found all values, add them to the dictionary and break the loop
                            data_dict[date] = {
                                'Electricity Units': units,
                                'Meter Number': meter_number,
                                'Total Electricity': total_electricity,
                                'Date': date,
                            }   
                            break

                latest_date = max(data_dict.keys())
                # Print the latest date and associated data
                return data_dict[latest_date]

    def authenticate(self, username, password):
            pool_data = {
            "ame": username,
            "pass": password,
            }
            with requests.Session() as s:
            # Post login data
                p = s.post("https://www.powertime.co.za/en/profile/login", data=pool_data)
                return p.json()