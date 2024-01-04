import json
import os
from datetime import datetime

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image


class LanguageSelectionScreen(ctk.CTk):
	"""
	Class representing loading screen (screen to choose a language) of the program
	"""

	def __init__(self) -> None:
		super().__init__()
		self.title("")
		self.geometry("500x300")

		languages = ["English", "Polski"]
		self.language = ctk.CTkOptionMenu(self, values=languages)
		self.language.pack(pady=10)

		self.confirm_button = ctk.CTkButton(self, text='✓', command=self.confirm)
		self.confirm_button.pack()

	def confirm(self) -> None:
		"""
		Function to confirm selection of the language
		"""
		global localisation_data

		language = self.language.get()
		with open(f'localisation/{language.lower()}.json', encoding='utf8') as f:
			localisation_data = json.load(f)

		self.destroy()


class MainScreen(ctk.CTk):
	"""
	Main screen of the program
	"""

	def __init__(self) -> None:
		super().__init__()
		self.title(localisation_data['title'])
		self.geometry("500x300")

		self.path_box = ctk.CTkEntry(self, width=400, placeholder_text=localisation_data["entry_box_placeholder"])
		self.path_box.pack()

		self.browse_button = ctk.CTkButton(self, text=localisation_data["browse_files_button"], command=self.browse)
		self.browse_button.pack(pady=10)

		self.accept_button = ctk.CTkButton(self, text=localisation_data["accept_button"], command=self.accept, fg_color='green', hover_color='darkgreen')
		self.accept_button.pack(pady=10)

	def accept(self) -> None:
		"""
		Function to accept the path
		"""
		directory = self.path_box.get()

		os.chdir(directory)

		files = [f for f in os.listdir() if os.path.isfile(f) and os.path.splitext(f)[1] == '.jpg']

		for f in files:
			new_name = get_date_taken(f).strftime("%Y%m%d_%H%M%S")
			os.rename(f'{directory}/{f}', f'{new_name}.jpg')

		CTkMessagebox(message=localisation_data["messagebox_text"], icon='check', title='')

	def browse(self) -> None:
		"""
		Function to open file dialog to choose a directory
		"""
		directory = ctk.filedialog.askdirectory(initialdir=os.getcwd(), title=localisation_data["filedialog_title"])
		self.path_box.insert(0, directory)


def get_date_taken(path: str = os.getcwd()) -> datetime:
	"""
	Function to get date taken from the image
	:param path: path to the image
	:return: datetime object representing date taken
	"""
	exif = Image.open(path).getexif()
	if not exif:
		raise Exception('Image {0} does not have EXIF data.'.format(path))
	return datetime.strptime(exif[36867], "%Y:%m:%d %H:%M:%S")


def main() -> None:
	"""
	Main function of the script
	"""
	language_selection_screen = LanguageSelectionScreen()
	language_selection_screen.mainloop()

	main_screen = MainScreen()
	main_screen.mainloop()


if __name__ == '__main__':
	main()
