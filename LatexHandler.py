class LatexHandler:
    def __init__(self):
        self.taalTemplateDict ={
            'Tritaal' : [ "\t\\begin{longtabu} to \\textwidth{X X X X X X X X X X X}\n\n\t\tNOTATION\n\n\t\t\end{longtabu}",
                          [['']*10, [' ', '$\\boldsymbol\\times$', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' '], ['']*11, ['']*10, [' ','$\\boldsymbol\\circ$', ' ', ' ', ' ', ' ', '3', ' ', ' ', ' ', ' '], ['']*11] ]
        }

    def GenerateLatexScriptData(self, data, taalName):   #TODO : Generalize and move to Latex class
        taalTable = self.taalTemplateDict[taalName][0]
        taalTemplate = self.taalTemplateDict[taalName][1]
        taalLines = len(taalTemplate) / 3
        
	notation = []
	for (i,row) in enumerate(data):
	    if (i%taalLines == 0):
		notation = notation + taalTemplate
                
	    notation[3*i] = row
                
	dataNotationString = ""
	for (i,row) in enumerate(notation):        
	    dataNotationString += ' & '.join(row).encode('utf-8')   #TODO : Strip spaces?
	    dataNotationString += ' \\\ \n\t\t'
		    
	dataNotation = taalTable.replace("NOTATION", dataNotationString)
		
        with open('../docTemplate.tex', 'r') as myfile:
	    scriptData = myfile.read()
        
	scriptData = scriptData.replace("NOTATION", dataNotation)
    
	return scriptData

        
