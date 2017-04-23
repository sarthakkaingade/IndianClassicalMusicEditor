#!/usr/bin/python

import wx, wx.html
import sys
import MusicEditor as ME

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

class Frame(wx.Frame):
    def __init__(self, title):
        displaySize= wx.DisplaySize()
        wx.Frame.__init__(self, None, title=title, size=(displaySize[0]/2, displaySize[1]/2))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_new = menu.Append(wx.ID_NEW, "New\tCtrl-N", "Create a new notation file.")
        m_open = menu.Append(wx.ID_OPEN, "Open\tCtrl-O", "Open an existing notation file.")
        m_exit = menu.Append(wx.ID_EXIT, "Exit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnNew, m_new)
        self.Bind(wx.EVT_MENU, self.OnOpen, m_open)
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)
        
        self.statusbar = self.CreateStatusBar()

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        
        m_text = wx.StaticText(panel, -1, "ICM Editor!")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)
        
        m_close = wx.Button(panel, wx.ID_CLOSE, "Close")
        m_close.Bind(wx.EVT_BUTTON, self.OnClose)
        box.Add(m_close, 0, wx.ALL, 10)
        
        self.ICME = ME.MusicEditor()

        panel.SetSizer(box)
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

    def OnOpen(self, event):
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

app = wx.App(redirect=True)   # Error messages go to popup window
top = Frame("ICM Editor")
top.Show()
app.MainLoop()
