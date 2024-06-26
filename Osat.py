import datetime
from colorama import Fore, Style
import colorama
import requests
import time
from dotenv import load_dotenv
import os
from Russian import RUSSIAN_SATELLITES
from rover import save_rover_images, fetch_rover_photos
from art import art
import csv

# Load environment variables from .env file
load_dotenv()
colorama.init()
# Constants for N2YO API
N2YO_API_KEY = os.getenv('N2YO_API_KEY', default='')
SAT_ID_ISS = 25544  # ISS satellite ID
LATITUDE = 41.702   # Replace with the latitude of the location
LONGITUDE = -76.014 # Replace with the longitude of the location
ALTITUDE = 0        # Replace with the altitude of the observer (in km)
NUM_POSITIONS = 2   # Number of position data points to fetch
CATEGORY = 24  # Satellite category for Navy Navigation Satellite System
RADIUS = 70  # Search radius from observer's location (in degrees)

# Constants for NASA API
NASA_API_KEY = os.getenv('NASA_API_KEY', default='')



def fetch_next_launches(launch_url):
    try:
        response = requests.get(launch_url)
        response.raise_for_status()  
        launches = response.json()

        if 'result' in launches:
            print_launches(launches['result'])  
            return launches['result']  
        else:
            print("Error: Unexpected response format")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def print_launches(launches):
    for launch in launches:
        name = launch.get('name', 'N/A')
        provider = launch.get('provider', {}).get('name', 'N/A')
        vehicle = launch.get('vehicle', {}).get('name', 'N/A')
        location = launch.get('pad', {}).get('location', {}).get('name', 'N/A')
        launch_time = launch.get('t0', 'N/A')
        launch_description = launch.get('launch_description', 'N/A')

        
        if launch_time != 'N/A' and launch_time is not None:
            try:
                launch_time = datetime.datetime.fromisoformat(launch_time.replace('Z', '+00:00'))
                launch_time = launch_time.strftime('%Y-%m-%d %H:%M:%S UTC')
            except ValueError:
                pass  

        print(f"Launch Name: {name}")
        print(f"Provider: {provider}")
        print(f"Vehicle: {vehicle}")
        print(f"Location: {location}")
        print(f"Launch Time: {launch_time}")
        print(f"Launch Description: {launch_description}")
        print("-" * 40)



def fetch_navy_satellites(api_key, latitude, longitude, altitude, radius, category):
    url = f'https://api.n2yo.com/rest/v1/satellite/above/{latitude}/{longitude}/{altitude}/{radius}/{category}/&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Navy Navigation Satellite System satellites information: {e}")
        return None


def display_navy_satellites_info(satellites_data):
    try:
        info = satellites_data['info']
        satellites = satellites_data['above']
        category = info['category']
        transactions_count = info['transactionscount']
        sat_count = info['satcount']
        
        print(f"Category: {category}")
        print(f"Transactions Count: {transactions_count}")
        print(f"Satellite Count: {sat_count}")
        print()

        for idx, sat_info in enumerate(satellites, start=1):
            sat_id = sat_info['satid']
            sat_name = sat_info['satname']
            int_designator = sat_info['intDesignator']
            launch_date = sat_info['launchDate']
            sat_latitude = sat_info['satlat']
            sat_longitude = sat_info['satlng']
            sat_altitude = sat_info['satalt']

            print(f"Satellite #{idx}:")
            print(f"  Satellite ID: {sat_id}")
            print(f"  Satellite Name: {sat_name}")
            print(f"  International Designator: {int_designator}")
            print(f"  Launch Date: {launch_date}")
            print(f"  Latitude: {sat_latitude}")
            print(f"  Longitude: {sat_longitude}")
            print(f"  Altitude (km): {sat_altitude}")
            print()

    except KeyError as e:
        print(f"Error accessing key in Navy Navigation Satellite System data: {e}")


def fetch_live_plane_locations():
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            states = data['states']
            return states
        else:
            print(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

def save_plane_locations_to_csv(states):
    if not states:
        return
    
    filename = 'plane_locations.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ICAO24', 'Callsign', 'Country', 'Latitude', 'Longitude'])
        for state in states:
            icao24 = state[0]
            callsign = state[1].strip()
            country = state[2].strip()
            latitude = state[6]
            longitude = state[5]
            writer.writerow([icao24, callsign, country, latitude, longitude])
    print(f"Saved live plane locations to {filename}")

def fetch_passes(api_key, sat_id, latitude, longitude):
    url = f'https://api.n2yo.com/rest/v1/satellite/radiopasses/{sat_id}/{latitude}/{longitude}/0/2/40/&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching passes information: {e}")
        return None

def display_passes_info(passes_data):
    try:
        passes = passes_data['passes']

        print(f"Number of passes: {len(passes)}")
        print()

        for idx, pass_info in enumerate(passes, start=1):
            start_az = pass_info['startAz']
            start_az_compass = pass_info['startAzCompass']
            start_utc = pass_info['startUTC']
            max_az = pass_info['maxAz']
            max_az_compass = pass_info['maxAzCompass']
            max_el = pass_info['maxEl']
            max_utc = pass_info['maxUTC']
            end_az = pass_info['endAz']
            end_az_compass = pass_info['endAzCompass']
            end_utc = pass_info['endUTC']

            print(f"Pass #{idx}:")
            print(f"  Start UTC: {start_utc}")
            print(f"  Start Azimuth: {start_az} ({start_az_compass})")
            print(f"  Maximum Elevation: {max_el} degrees")
            print(f"  Maximum UTC: {max_utc}")
            print(f"  Maximum Azimuth: {max_az} ({max_az_compass})")
            print(f"  End UTC: {end_utc}")
            print(f"  End Azimuth: {end_az} ({end_az_compass})")
            print()

    except KeyError as e:
        print(f"Error accessing key in passes data: {e}")


def display_apod(apod_data):
    if apod_data:
        print(f"Title: {apod_data['title']}")
        print(f"Date: {apod_data['date']}")
        print(f"Explanation: {apod_data['explanation']}")
        print(f"URL: {apod_data['url']}")
        print(f"Media type: {apod_data['media_type']}")
        
        # Check if 'hdurl' exists before printing
        if 'hdurl' in apod_data:
            print(f"HD URL: {apod_data['hdurl']}")
        else:
            print("HD URL not available for this media type.")

    else:
        print("Failed to fetch APOD data.")

def display_apod(apod_data):
    if apod_data:
        print(f"Title: {apod_data['title']}")
        print(f"Date: {apod_data['date']}")
        print(f"Explanation: {apod_data['explanation']}")
        print(f"HD URL: {apod_data['hdurl']}")
        print(f"URL: {apod_data['url']}")
        print(f"Media type: {apod_data['media_type']}")
    else:
        print("Failed to fetch APOD data.")

def fetch_military_satellites(api_key, latitude, longitude, altitude, radius, category):
    url = f'https://api.n2yo.com/rest/v1/satellite/above/{latitude}/{longitude}/{altitude}/{radius}/{category}/&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching military satellites information: {e}")
        return None


def display_military_satellites_info(satellites_data):
    try:
        info = satellites_data['info']
        satellites = satellites_data['above']
        category = info['category']
        transactions_count = info['transactionscount']
        sat_count = info['satcount']
        
        print(f"Category: {category}")
        print(f"Transactions Count: {transactions_count}")
        print(f"Satellite Count: {sat_count}")
        print()

        for idx, sat_info in enumerate(satellites, start=1):
            sat_id = sat_info['satid']
            sat_name = sat_info['satname']
            int_designator = sat_info['intDesignator']
            launch_date = sat_info['launchDate']
            sat_latitude = sat_info['satlat']
            sat_longitude = sat_info['satlng']
            sat_altitude = sat_info['satalt']

            print(f"Satellite #{idx}:")
            print(f"  Satellite ID: {sat_id}")
            print(f"  Satellite Name: {sat_name}")
            print(f"  International Designator: {int_designator}")
            print(f"  Launch Date: {launch_date}")
            print(f"  Latitude: {sat_latitude}")
            print(f"  Longitude: {sat_longitude}")
            print(f"  Altitude (km): {sat_altitude}")
            print()

    except KeyError as e:
        print(f"Error accessing key in military satellites data: {e}")


def fetch_iss_position(api_key, sat_id, latitude, longitude, altitude, num_positions):
    url = f'https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/{latitude}/{longitude}/{altitude}/{num_positions}/&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching ISS position information: {e}")
        return None

def display_iss_position_info(position_data):
    try:
        info = position_data['info']
        positions = position_data['positions']
        sat_name = info['satname']
        sat_id = info['satid']
        transactions_count = info['transactionscount']

        print(f"Satellite Name: {sat_name}")
        print(f"Satellite ID: {sat_id}")
        print(f"Transactions Count: {transactions_count}")
        print()

        for idx, pos_info in enumerate(positions, start=1):
            sat_latitude = pos_info['satlatitude']
            sat_longitude = pos_info['satlongitude']
            sat_altitude = pos_info['sataltitude']
            azimuth = pos_info['azimuth']
            elevation = pos_info['elevation']
            ra = pos_info['ra']
            dec = pos_info['dec']
            timestamp = pos_info['timestamp']
            eclipsed = pos_info['eclipsed']

            # Convert timestamp to human-readable format
            timestamp_utc = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))

            print(f"Position #{idx}:")
            print(f"  Time (UTC): {timestamp_utc}")
            print(f"  Latitude: {sat_latitude}")
            print(f"  Longitude: {sat_longitude}")
            print(f"  Altitude (km): {sat_altitude}")
            print(f"  Azimuth: {azimuth} degrees")
            print(f"  Elevation: {elevation} degrees")
            print(f"  Right Ascension (RA): {ra}")
            print(f"  Declination (DEC): {dec}")
            print(f"  Eclipsed: {eclipsed}")
            print()

    except KeyError as e:
        print(f"Error accessing key in ISS position data: {e}")


def fetch_satellite_position(api_key, norad_id, latitude, longitude, altitude, num_positions):
    url = f'https://api.n2yo.com/rest/v1/satellite/positions/{norad_id}/{latitude}/{longitude}/{altitude}/{num_positions}/&apiKey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status() 

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching satellite position information: {e}")
        return None

def display_satellite_position_info(position_data, satellite_name):
    try:
        info = position_data['info']
        positions = position_data['positions']
        sat_name = info['satname']
        sat_id = info['satid']
        transactions_count = info['transactionscount']

        print(f"Satellite Name: {sat_name} ({satellite_name})")
        print(f"Satellite NORAD ID: {sat_id}")
        print(f"Transactions Count: {transactions_count}")
        print()

        pos_info = positions[0]
        sat_latitude = pos_info['satlatitude']
        sat_longitude = pos_info['satlongitude']
        sat_altitude = pos_info['sataltitude']
        azimuth = pos_info['azimuth']
        elevation = pos_info['elevation']
        ra = pos_info['ra']
        dec = pos_info['dec']
        timestamp = pos_info['timestamp']
        eclipsed = pos_info['eclipsed']

        timestamp_utc = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))

        print(f"Position:")
        print(f"  Time (UTC): {timestamp_utc}")
        print(f"  Latitude: {sat_latitude}")
        print(f"  Longitude: {sat_longitude}")
        print(f"  Altitude (km): {sat_altitude}")
        print(f"  Azimuth: {azimuth} degrees")
        print(f"  Elevation: {elevation} degrees")
        print(f"  Right Ascension (RA): {ra}")
        print(f"  Declination (DEC): {dec}")
        print(f"  Eclipsed: {eclipsed}")
        print()

    except KeyError as e:
        print(f"Error accessing key in satellite position data: {e}")

def run_tool():
    while True:
        print(Fore.LIGHTCYAN_EX + art)

        print("Select an option:")
        print("{:<2}. {:<45}".format(0, "Exit"))
        print("{:<2}. {:<45} {:<2}. {}".format(1, "ISS passes info", 2, "APOD"))
        print("{:<2}. {:<45} {:<2}. {}".format(3, "Military satellites info", 4, "ISS position"))
        print("{:<2}. {:<45} {:<2}. {}".format(5, "Russian LEO nav info", 6, "NASA Rovers(Any Rover and Camera)"))
        print("{:<2}. {:<45} {:<2}. {}".format(7, "Plane locations to CSV", 8, "Navy Navigation satellites"))
        print("{:<2}. {:<45}".format(9,"Next 5 NASA Rocket Launches"))

        choice = input("Enter your choice (0-9): ")

        if choice == '1':
            print("Fetching passes information for ISS...\n")
            passes_data = fetch_passes(N2YO_API_KEY, SAT_ID_ISS, LATITUDE, LONGITUDE)
            if passes_data:
                print("Passes Information:\n")
                display_passes_info(passes_data)
            else:
                print("Failed to fetch passes information.\n")

        elif choice == '2':
            print("Fetching Astronomy Picture of the Day (APOD) from NASA API...\n")
            apod_data = fetch_apod(NASA_API_KEY)
            if apod_data:
                print("APOD Information:\n")
                display_apod(apod_data)
            else:
                print("Failed to fetch Astronomy Picture of the Day (APOD).\n")

        elif choice == '3':
            print("Fetching military satellites information from N2YO API...\n")
            military_satellites_data = fetch_military_satellites(N2YO_API_KEY, LATITUDE, LONGITUDE, ALTITUDE, 70, 30)
            if military_satellites_data:
                print("Military Satellites Information:\n")
                display_military_satellites_info(military_satellites_data)
            else:
                print("Failed to fetch military satellites information.\n")

        elif choice == '4':
            print("Fetching ISS position information from N2YO API...\n")
            iss_position_data = fetch_iss_position(N2YO_API_KEY, SAT_ID_ISS, LATITUDE, LONGITUDE, ALTITUDE, NUM_POSITIONS)
            if iss_position_data:
                print("ISS Position Information:\n")
                display_iss_position_info(iss_position_data)
            else:
                print("Failed to fetch ISS position information.\n")

        elif choice == '5':
            print("Fetching position information for Russian LEO navigation satellites...\n")
            for satellite in RUSSIAN_SATELLITES:
                satellite_name = satellite['name']
                norad_id = satellite['norad_id']
                satellite_position_data = fetch_satellite_position(N2YO_API_KEY, norad_id, LATITUDE, LONGITUDE, ALTITUDE, NUM_POSITIONS)
                if satellite_position_data:
                    display_satellite_position_info(satellite_position_data, satellite_name)
                else:
                    print(f"Failed to fetch satellite position information for {satellite_name} (NORAD ID: {norad_id}).")
        elif choice == '6':
            print("Fetching and saving Mars Rover photos...\n")
            rover_name = input('Enter the rover name (e.g., curiosity, opportunity, spirit): ')
            sol = input('Enter sol (e.g., 0-1000): ')
            camera = input('Enter camera abbreviation (e.g., FHAZ): ')
            save_folder = input('Enter folder name to save images (e.g., mars): ')
            photo_data = fetch_rover_photos(rover_name, sol, camera, NASA_API_KEY)
            if photo_data:
                save_rover_images(photo_data, save_folder)
            else:
                print("Failed to fetch Mars Rover photos.\n")

        elif choice == '7':
            print("Fetching and saving live plane locations...\n")
            states = fetch_live_plane_locations()
            if states:
                save_plane_locations_to_csv(states)
            else:
                print("Failed to fetch live plane locations.\n")

        elif choice == '8':
            print("Fetching Navy Navigation Satellite System satellites information...")
            navy_satellites_data = fetch_navy_satellites(N2YO_API_KEY, LATITUDE, LONGITUDE, ALTITUDE, RADIUS, CATEGORY)
            if navy_satellites_data:
                display_navy_satellites_info(navy_satellites_data)
            else:
                print("Failed to fetch Navy Navigation Satellite System satellites information.")
        elif choice == '9':
            launch_url = "https://fdo.rocketlaunch.live/json/launches/next/5"
            launches = fetch_next_launches(launch_url)

        elif choice == '0':
            print("Exiting the Satellite Information Tool. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 9.")

if __name__ == '__main__':
    run_tool()
