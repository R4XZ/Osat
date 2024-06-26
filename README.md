# Osat - Satellite Data and NASA Rover Images Tool
Osat is a Python-based tool that fetches satellite data using NASA's and N2YO APIs, providing information about the International Space Station (ISS), Navy Navigation Satellite System, Russian LEO Navigation, and more. Additionally, it uses NASA API to retrieve images captured by NASA's rovers.

# Features
Satellite Data
Retrieves real-time data of satellites, including the ISS, Navy Navigation Satellite System, and Russian LEO Navigation.
Rover Images
Fetches images taken by NASA's rovers on Mars using NASA's API.
```
1. ISS passes info                             2. APOD (Astronomy picture of the day)
3. Military satellites info                    4. ISS position
5. Russian LEO nav info                        6. NASA Rovers (Any Rover and Camera)
7. Plane locations to CSV                      8. Navy Navigation satellites
```

# Installation
Replace ```YOUR_API_TOKEN_HERE ``` with both NASA and N2YO API keys in the ```.env``` file
```
N2YO_API_KEY=YOUR_API_TOKEN_HERE
NASA_API_KEY=YOUR_API_TOKEN_HERE
```

Open terminal in the Osat directory, then enter this below
```
pip install -r requirements.txt
```
Then run the program using this below or run the start.bat
```
python Osat.py
```
# API Information

To utilize the APIs for this tool, you'll need to sign up for API keys from both NASA and N2YO.

- **NASA API**: Visit [NASA API](https://api.nasa.gov/) to sign up for a free API key. With NASA's API, you can access a wide range of data, including satellite information, images from rovers, and more.
- **N2YO API**: Visit [N2YO API](https://www.n2yo.com/api/) to sign up for an API key. N2YO provides satellite tracking and related data.

Both APIs are free to use after signing up, and you can start exploring. Happy Tracking :)

# Updates and questions
1. Will there be updates? Yes
2. Will there be more implementations? yes 
3. Why use Osat?. Educational Purposes, Tracking Satellites
4. Benefits of this tool?. share and discuss satellite observations, space missions, also astronomical discoveries.

# Feedback
Feedback is invaluable to me as it helps me identify issues and weaknesses and enhances my understanding on projects and so on. Your input is greatly appreciated!

# Examples
![FRB_486265257EDR_F0481570FHAZ00323M_](https://github.com/R4XZ/Osat/assets/116701630/e81fb1aa-602e-46e8-84c6-83b6c195aa06)
![9721](https://github.com/R4XZ/Osat/assets/116701630/63ea70f9-f66f-4b77-a64d-f022bda5a039)
![9722](https://github.com/R4XZ/Osat/assets/116701630/52d0a765-8785-4510-bc49-ee7bfe9023d4)
![osat](https://github.com/R4XZ/Osat/assets/116701630/30893a39-f365-4e6e-825a-dd3d5356d776)
![iss](https://github.com/R4XZ/Osat/assets/116701630/6b765428-fbed-4dae-8f71-7545627be22b)
![russianSats](https://github.com/R4XZ/Osat/assets/116701630/4ac279f5-d413-4532-b190-9c3a7bacfc82)
![launches](https://github.com/R4XZ/Osat/assets/116701630/458b8e71-c77c-4b49-9133-3b09eb3648bd)
