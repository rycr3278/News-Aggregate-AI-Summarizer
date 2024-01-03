
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from crawlers import *
from model import *

def drive_uploader():
	# Authentication
	gauth = GoogleAuth()
	gauth.LocalWebserverAuth()  # Creates local webserver for authentication
	drive = GoogleDrive(gauth)

	# Upload file
	file_path = base_directory / "NewsScrapes" / "Summaries" / f"Summaries_{date}.csv"
	gfile = drive.CreateFile({'title': file_path.name})
	gfile.SetContentFile(str(file_path))
	gfile.Upload()

	print("File uploaded to Google Drive successfully.")