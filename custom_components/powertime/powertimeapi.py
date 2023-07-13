
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta, date
import requests
import json
from functools import partial
import logging
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup
_LOGGER = logging.getLogger(__name__)
class powertime_api:
    def __init__(self, username, password,hass: HomeAssistant):
        self.username = username
        self.password = password
        self.session = ClientSession()

    async def authenticate(self):
        payload = {'name': self.username, 'pass': self.password}
        async with self.session.post('https://www.powertime.co.za/en/profile/login', data=payload) as response:
            return response

        return response
    async def get_viewhistory(self):
        async with self.session.get('https://www.powertime.co.za/en/electricity/viewhistory') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            table = soup.find('table')
            rows = table.find_all('tr')
            data = []
            for row in rows[1:]:
                cols = row.find_all('td')
                href = cols[4].find('a')['href']
                view = href.split('/receipt_id/')[1].split('/')[0]
                data.append(view)
            return data

    async def get_voucher(self, d):
        async with self.session.get(f'https://www.powertime.co.za/en/electricity/voucher/receipt_id/{d}/') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            table = soup.find('table')
            rows = table.find_all('tr')
            data_dict = {}
            units = None
            date = None
            meter_number = None
            total_electricity = None
            for row in rows:
                cols = row.find_all('td')
                key = cols[0].text.strip()
                if key == 'Electricity Units:':
                    units = cols[1].text.strip()
                elif key == 'Date:':
                    date = cols[1].text.strip()
                elif key == 'Meter Number:':
                    meter_number = cols[1].text.strip()
                elif key == 'Total Electricity:':
                    total_electricity = cols[1].text.strip()
                if units and date and meter_number and total_electricity:
                    units = units.replace("Kwh's", "")
                    data_dict[date] = {
                        'Electricity Units': units,
                        'Meter Number': meter_number,
                        'Total Electricity': total_electricity,
                        'Date': date,
                    }
                    break
            return data_dict
    async def get_all_data(self):
        all_data = {}

        # Get plant data
        await self.authenticate()
        viewhistory = await self.get_viewhistory()
        for history in viewhistory:
            voucher = await self.get_voucher(history)
            if voucher: # check if rr is not empty
                all_data.update(voucher) # add rr to all_data
        latest_date = max(all_data.keys())
        today = date.today().strftime("%Y-%m-%d")
        if latest_date == today:
            latest_units = all_data[latest_date]['Electricity Units']
        else:
            latest_units = 0

        all_data[latest_date]['Current Units'] = latest_units
        return all_data[latest_date]

