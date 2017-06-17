import pygsheets
import webbrowser

class MusicEditor:
	def __init__(self):
		self.gc = pygsheets.authorize()
		print("ICM: Authorized Music Editor")
		self.templateSheets = {'Tritaal' : "https://docs.google.com/spreadsheets/d/1cN9ycjisj1KM2muyoCYUBs1oqpKCz80821GwUghzgrc/"}
		folders = self.gc.driveService.files().list(q="mimeType='application/vnd.google-apps.folder'",fields="files(id,name)").execute()
		foldersList = folders.get('files',[])
		self.folderID = ''
		if len(foldersList) != 0:
			folderID = [x['id'] for x in foldersList if x['name'] == "ICME"]
			if len(folderID) != 0:
				self.folderID = folderID[0]
		if len(self.folderID) == 0:
			folder = self.gc.driveService.files().create(body={'name' : 'ICME','mimeType' : 'application/vnd.google-apps.folder'},fields='id').execute()
			self.folderID = folder.get('id')
		files = self.gc.driveService.files().list(q = "'" + self.folderID + "'" + " in parents",fields="files(id,name)").execute()
		self.filesICME = files.get('files',[])

	def NewSheet(self,fileName,taalName):
		targetSpreadSheet = self.gc.create(fileName)
		sourceSpreadSheet = self.gc.open_by_url(self.templateSheets[taalName])
		targetSpreadSheet.add_worksheet(taalName,src_worksheet=sourceSpreadSheet.sheet1)
		targetSpreadSheet.del_worksheet(targetSpreadSheet.sheet1)
		file = self.gc.driveService.files().get(fileId=targetSpreadSheet.id,fields='parents').execute()
		previous_parents = ",".join(file.get('parents'))
		file = self.gc.driveService.files().update(fileId=targetSpreadSheet.id,addParents=self.folderID,removeParents=previous_parents,fields='id, parents').execute()
		print("ICM: Created New Sheet")
		webbrowser.open("https://docs.google.com/spreadsheets/d/" + targetSpreadSheet.id + "/")

	def GetSheets(self,folderID):
		files = self.gc.driveService.files().list(q = "'" + folderID + "'" + " in parents",fields="files(id,name)").execute()
		self.filesICME = files.get('files',[])
		return [x['name'] for x in self.filesICME]

	def GetDataFromSheet(self,sheetName):
		fileIDList = [x['id'] for x in self.filesICME if x['name'] == sheetName]
		if len(fileIDList) != 0:
			fileID = fileIDList[0]
		sh = self.gc.open_by_key(fileID)
		wks = sh.worksheet('index',0)
		return wks.get_all_values(), wks.title

if __name__ == '__main__':
	ICME = MusicEditor()
	#ICME.NewSheet(fileName="MyTaal",taalName="Tritaal")
	print(ICME.GetSheets(ICME.folderID))

