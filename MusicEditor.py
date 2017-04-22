import pygsheets
import webbrowser

class MusicEditor:
	def __init__(self):
		self.gc = pygsheets.authorize()
		print("ICM: Authorized Music Editor")
		self.templateSheets = {'Trital' : "https://docs.google.com/spreadsheets/d/1cN9ycjisj1KM2muyoCYUBs1oqpKCz80821GwUghzgrc/"}

	def NewSheet(self,fileName,taalName):
		targetSpreadSheet = self.gc.create(fileName)
		sourceSpreadSheet = self.gc.open_by_url(self.templateSheets[taalName])
		targetSpreadSheet.add_worksheet(taalName,src_worksheet=sourceSpreadSheet.sheet1)
		targetSpreadSheet.del_worksheet(targetSpreadSheet.sheet1)
		print("ICM: Created New Sheet")
		webbrowser.open("https://docs.google.com/spreadsheets/d/" + targetSpreadSheet.id + "/")

if __name__ == '__main__':
	ICME = MusicEditor()
	ICME.NewSheet(fileName="MyTaal",taalName="Trital")

