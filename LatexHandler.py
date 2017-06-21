class LatexHandler:
    def __init__(self):
        self.taalTemplateDict ={
            'Tritaal' :  "\t\\begin{longtabu} to \\textwidth{X X X X X X X X X X X}\n\n\t\tNOTATION\n\n\t\t\end{longtabu}",
                          
            'Ektaal' :  "\t\\begin{longtabu} to \\textwidth{X X X X X X X X X X}\n\n\t\tNOTATION\n\n\t\t\end{longtabu}",

            'Roopak' :  "\t\\begin{longtabu} to \\textwidth{X X X X X X X X X X X}\n\n\t\tNOTATION\n\n\t\t\end{longtabu}",

            'Jhaptaal' :  "\t\\begin{longtabu} to \\textwidth{X X X X X X X X}\n\n\t\tNOTATION\n\n\t\t\end{longtabu}",
        }

    def GenerateLatexScriptData(self, data, taalName):   #TODO : Generalize and move to Latex class
        taalTable = self.taalTemplateDict[taalName]
        #taalTemplate = self.taalTemplateDict[taalName][1]
        #taalLines = len(taalTemplate) / 3            

        #print data[0]
	dataNotationString = ""
	for (i,row) in enumerate(data):        
	    dataNotationString += ' & '.join(row).encode('utf-8')   #TODO : Strip spaces?
	    dataNotationString += ' \\\ \n\t\t'
		    
	dataNotation = taalTable.replace("NOTATION", dataNotationString)
		
        with open('../docTemplate.tex', 'r') as myfile:
	    scriptData = myfile.read()
        
	scriptData = scriptData.replace("NOTATION", dataNotation)
    
	return scriptData

        
