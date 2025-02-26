import requests
import string
from PyQt6.QtCore import QObject, pyqtSignal as Signal, pyqtSlot as Slot

class toAPI():

    #@Slot(string)
    def upload_musicxml_to_api(file_path, api_url):
        try:
            # Open the MusicXML file to send as binary
            with open(file_path, 'rb') as file:
                # Prepare the files dictionary for the request
                files = {'file': (file_path, file, 'application/octet-stream')}
                
                # Send the POST request to the API
                response = requests.post(api_url, files=files)
                
                # Check the response status
                if response.status_code == 200:
                    print("MusicXML successfully uploaded and converted!")
                    sheet_music_url = response.json().get('sheet_music_url', '')
                    print(f"Your sheet music is available at: {sheet_music_url}")
                else:
                    print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
api_url = "https://example.com/upload_musicxml"
toAPI().upload_musicxml_to_api('testMusic.musicxml', api_url)