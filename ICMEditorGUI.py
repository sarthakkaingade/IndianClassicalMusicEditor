#!/usr/bin/python

import wx, wx.html
import sys
from subprocess import call
import webbrowser
import MusicEditor as ME
import LatexHandler as LH

aboutText = """<p>This is a Google Docs based editor for Indian Classical Music.
See <a href="https://github.com/sarthakkaingade/IndianClassicalMusicEditor"> ICM Editor Github Repository</a>  for details.</p>"""

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About ICM Editor", style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
	displaySize= wx.DisplaySize()
        hwin = HtmlWindow(self, -1, size=(displaySize[0]/4, displaySize[1]/4))        
        hwin.SetPage(aboutText)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

class NewFileDialog(wx.Dialog):
    def __init__(self, parent):
        displaySize= wx.DisplaySize()
        wx.Dialog.__init__(self, parent, title='Enter New File Data', size=(displaySize[0]/4, displaySize[1]/6), style=wx.DEFAULT_DIALOG_STYLE)
        #panel = wx.Panel(self, -1) 
        self.fileNameLabel = wx.StaticText(self, -1, "File Name:")
        self.fileNameTextBox = wx.TextCtrl(self, -1, "", size=(displaySize[0]/6, -1))
        self.fileNameTextBox.SetInsertionPoint(0)
        self.taalNameLabel = wx.StaticText(self, -1, "Select Taal")
        taals = ['Tritaal', 'Ektaal', 'Jhaptaal', 'Rupak', 'Matta Taal'] 
        self.taalNameChoice = wx.Choice(self,choices = taals, size=(displaySize[0]/6, -1))
        self.taalNameChoice.SetSelection(0)

        txtSizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        txtSizer.AddMany([self.fileNameLabel, self.fileNameTextBox, self.taalNameLabel, self.taalNameChoice])

        dlgSizer = wx.BoxSizer(wx.VERTICAL)
        dlgSizer.Add(txtSizer, 1, wx.ALL, 4)

        okBtn = wx.Button(self, wx.ID_OK, "OK")
        okBtn.SetDefault()
        cancelBtn = wx.Button(self, wx.ID_CANCEL, "Cancel")    #TODO : Handle this
        #okBtn.Bind(wx.EVT_BUTTON, self.OnOk)
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnClose)
        
        btnSizer = wx.StdDialogButtonSizer()
        btnSizer.AddButton(okBtn)
        btnSizer.AddButton(cancelBtn)
        btnSizer.Realize()

        dlgSizer.Add(btnSizer, 0, wx.ALL|wx.ALIGN_CENTER, 4) 

        self.SetSizer(dlgSizer)
        #panel.SetFocus()
        self.Layout()
        self.Show()

    def OnClose(self, event):
        self.fileName = []
        self.taalName = []
        self.Destroy()
        #return

    #def OnOk(self, event):
        #self.fileName = self.fileNameTextBox.GetValue()
        #self.taalName = self.taalNameChoice.GetString( self.taalNameChoice.GetSelection() )
        
        #self.Destroy()
        
    def GetNewFileData(self):
        self.fileName = self.fileNameTextBox.GetValue()
        self.taalName = self.taalNameChoice.GetString( self.taalNameChoice.GetSelection() )
        return [self.fileName, self.taalName]

class ICME_GUI(wx.Frame):
    def __init__(self, title):
        displaySize= wx.DisplaySize()
        wx.Frame.__init__(self, None, title=title, size=(displaySize[0]/2, displaySize[1]/2))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        itemNew = menuFile.Append(wx.ID_NEW, "New\tCtrl-N", "Create a new notation file.")
        itemOpen = menuFile.Append(wx.ID_OPEN, "Open\tCtrl-O", "Open an existing notation file.")
        itemExit = menuFile.Append(wx.ID_EXIT, "Exit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnNew, itemNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, itemOpen)
        self.Bind(wx.EVT_MENU, self.OnClose, itemExit)
        menuBar.Append(menuFile, "&File")
        menuHelp = wx.Menu()
        itemAbout = menuHelp.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, itemAbout)
        menuBar.Append(menuHelp, "&Help")
        self.SetMenuBar(menuBar)
        
        self.statusbar = self.CreateStatusBar()

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        itemText = wx.StaticText(panel, -1, "ICM Editor!")
        itemText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        itemText.SetSize(itemText.GetBestSize())
        vbox1.Add(itemText, 0, wx.ALL, 10)
        
        buttonClose = wx.Button(panel, wx.ID_CLOSE, "Close")
        buttonClose.Bind(wx.EVT_BUTTON, self.OnClose)
        vbox1.Add(buttonClose, 0, wx.ALL, 10)

        buttonGeneratePDF = wx.Button(panel, -1, "Generate PDF")
        buttonGeneratePDF.Bind(wx.EVT_BUTTON, self.OnGeneratePDF)
        vbox1.Add(buttonGeneratePDF, 0, wx.ALL, 10)

        self.listCtrlFiles = wx.ListCtrl(panel, size=(100,-1), style = wx.LC_REPORT)
        self.listCtrlFiles.InsertColumn(0, "File Name", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.listCtrlIndex = 0
        vbox2.Add(self.listCtrlFiles, 1, wx.EXPAND)

        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND)
        
        self.ICME = ME.MusicEditor()
        self.UpdateListCtrl()
        self.LatexHandler = LH.LatexHandler()
        
        panel.SetSizer(hbox)
        #panel.SetSizerAndFit(hbox)
        panel.Layout()

    def OnNew(self, event):
        dlg = NewFileDialog(self)
        result = dlg.ShowModal()
        if (result == wx.ID_OK):
            [fileName, taalName] = dlg.GetNewFileData()
            print fileName
            print taalName
            self.ICME.NewSheet(fileName,taalName)
        dlg.Destroy()
        self.UpdateListCtrl()
        
    def OnOpen(self, event):
        webbrowser.open("https://drive.google.com/drive/folders/" + self.ICME.folderID + "/")
        return

    def OnClose(self, event):
        dlg = wx.MessageDialog(self, 
            "Do you really want to close this application?",
                               "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()  

    def UpdateListCtrl(self):
        fileNames = self.ICME.GetSheets(self.ICME.folderID)
        self.listCtrlFiles.DeleteAllItems()
        for name in fileNames:
            #print name
            self.listCtrlFiles.InsertStringItem(self.listCtrlIndex, name)
            self.listCtrlIndex += 1
        self.listCtrlFiles.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)        
        
    def OnGeneratePDF(self, event):
        if(self.listCtrlFiles.GetFirstSelected() == -1):
            d= wx.MessageDialog( self, "Please select the files for PDF generation from the list.", "Error", wx.ICON_INFORMATION|wx.OK)
            d.ShowModal()
            d.Destroy()
            return

        dlg = wx.DirDialog (None, "Choose the directory to store PDF files", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return

        selected_items = [self.listCtrlFiles.GetFirstSelected()]
        index = self.listCtrlFiles.GetNextSelected(selected_items[0])
        while(index != -1):
            selected_items.append(index)
            index = self.listCtrlFiles.GetNextSelected(index)

        for index in selected_items:
            data, taalName = self.ICME.GetDataFromSheet(self.listCtrlFiles.GetItemText(index))
            print taalName
            latexScriptData = self.LatexHandler.GenerateLatexScriptData(data, taalName)
            with open('../testFile.tex', 'w') as file:
                file.write(latexScriptData)
        call("xelatex -synctex=1 -interaction=nonstopmode -output-directory=" + dlg.GetPath() + " ../testFile.tex")
        
app = wx.App(redirect=True)   # Error messages go to popup window
top = ICME_GUI("ICM Editor")
top.Show()
app.MainLoop()
