import pygsheets

class MusicEditor:
	def __init__(self):
		self.gc = pygsheets.authorize()
		print("ICM: Authorized Music Editor")

if __name__ == '__main__':
	ICME = MusicEditor()

