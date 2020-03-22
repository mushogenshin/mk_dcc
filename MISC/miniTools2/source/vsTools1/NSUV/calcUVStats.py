import maya.cmds as cmds
import maya.OpenMaya as openMaya
from math import sqrt

#-----------#
class vector:
	def __init__(self, data):
		self.data = data

	def __repr__(self):
		return repr(self.data)  

	def __add__(self, other):
		data = []
		for j in range(len(self.data)):
			data.append(self.data[j] + other.data[j])
			return vector(data)  

	def __sub__(self, other):
		data = []
		for j in range(len(self.data)):
			data.append(self.data[j] - other.data[j])
			return vector(data)  

	def __mul__(self, other):
		data = []
		for j in range(len(self.data)):
			data.append(self.data[j] * other.data[j])
			return vector(data)

	def __getitem__(self, data): 
		return vector(self.data[data])

	def length(self): 
		value = 0
		for j in range(len(self.data)):
			value += self.data[j] * self.data[j]
			return sqrt(value)

#----------#
class point:    
	def __init__(self, X, Y, Z, idx):  
		self.X = X   
		self.Y = Y   
		self.Z = Z
		self.idx = idx

#---------#
class line:    
	def __init__(self, pointA, pointB):    
		self.pointA = pointA    
		self.pointB = pointB    
		self.isIntersecting = 0    

	def intersect2D(self, line):    
		try:    
			Ua = ((line.pointB.X - line.pointA.X) * (self.pointA.Y - line.pointA.Y) - 
(line.pointB.Y - line.pointA.Y) * (self.pointA.X - line.pointA.X)) / ((line.pointB.Y - line.pointA.Y) * 
(self.pointB.X - self.pointA.X) - (line.pointB.X - line.pointA.X) * (self.pointB.Y - self.pointA.Y))
			Ub = ((self.pointB.X - self.pointA.X) * (self.pointA.Y - line.pointA.Y) - 
(self.pointB.Y - self.pointA.Y) * (self.pointA.X - line.pointA.X)) / ((line.pointB.Y - line.pointA.Y) * 
(self.pointB.X - self.pointA.X) - (line.pointB.X - line.pointA.X) * (self.pointB.Y - self.pointA.Y))
		except ZeroDivisionError:
			return 0

		if (0 < Ua < 1) and (0 < Ub < 1):    
			self.isIntersecting = 1    
			return 1
		else:
			return 0

#-------------#
class triangle:    
	def __init__(self, lines):    
		self.lines = lines    

	def intersect(self, triangle):    
		intersects = 0    
		for triA in range(0,3,1):    
			for triB in range(0,3,1):    
				intersects = self.lines[triA].intersect2D(triangle.lines[triB])    
				if intersects:    
					return 1

#------------------------------#
def checkOverlappingUVs(selObj, origObj):
	vtxFaces = cmds.select(cmds.polyListComponentConversion(selObj, tvf = 1))    
	vtxFaces = cmds.ls(selection = 1, fl = 1)    
	
	triangles = []
	lines = []
	intersects = 0
	intersectingFaces = 0
	
	for tri in range(0,(len(vtxFaces)/3),1):    
		points = []   #init
		for vtx in range(0,3,1):    
			cmds.select(vtxFaces[(tri * 3) + vtx])    
			cmds.select(cmds.polyListComponentConversion(tuv = 1))    
			coordList = cmds.polyEditUV(q = 1)    
			p = point(coordList[0], coordList[1], 0.0, vtxFaces[(tri * 3) + vtx])  
			points.append(p)    	
		line0 = line(points[0], points[1])    
		line1 = line(points[1], points[2])
		line2 = line(points[2], points[0])
		lines.append(line0)    
		lines.append(line1)
		lines.append(line2)
		templines = []
		templines.append(line0) 
		templines.append(line1)
		templines.append(line2)
		tri = triangle(templines)    
		triangles.append(tri)    

	barLength = len(triangles)
	wurst = progressWindow("Comparing Edges", barLength)

	
	isIntersecting = 0    

	for triA in triangles:    
		for triB in triangles:    
			if triA != triB:    
				intersects = triA.intersect(triB)    
				cmds.progressBar(wurst[1], edit=True, step=1)
				if intersects:   
					isIntersecting = 1    
	
	if isIntersecting:    
		cmds.select(cl=1)    
		
		failedUVs = []
		tempArray = []

		for curLine in lines:    
			if curLine.isIntersecting:    
				failedUVs.append(curLine.pointA.idx)    
				failedUVs.append(curLine.pointB.idx)
		
		cmds.select(failedUVs)    
		cmds.select(cmds.polyListComponentConversion(tuv = 1)) 
		failedUVs = cmds.ls(sl = 1)    
		
		for each in failedUVs:   
			each = each.replace(str(selObj[0]), str(origObj[0]))    
			tempArray.append(each)    
			
		failedUVs = tempArray    
		
		cmds.delete(selObj[0])    
		cmds.select(failedUVs)    
		openMaya.MGlobal.displayWarning((str(failedUVs) + "  belong to Overlapping Edges!"))
		cmds.confirmDialog( message='Failed UVs have been selected', title='Overlapping results')
		cmds.deleteUI(wurst[0])
		return 1    
	
	else:
		print "No Overlapping UV's found"
		cmds.deleteUI(wurst[0])


def progressWindow(titlename, barlength):
	
	progressWindow = cmds.window(titlename, width = 200, height = 50)
	cmds.columnLayout()
	progressControl = cmds.progressBar(maxValue = barlength * barlength, width = 200)
	cmds.showWindow(progressWindow)
	return progressWindow, progressControl


	


#_________________________________#
def removeListbyList(listA, listB):
	for each in listB:
		listA.remove(each)
	return listA

#_____________________________#
def checkUniqueUVSpace(selObj):
	uvs = cmds.select(cmds.polyListComponentConversion(selObj, tuv = 1))
	uvs = cmds.ls(sl=1, fl=1)

	failedUVs = []	
	
	selObjShape = cmds.listRelatives(selObj)[0]

	for each in cmds.getAttr(selObjShape + ".uvpt[*]"):
		if each[0] < 0 or each[1] < 0 or each[0] > 1 or each[1] > 1:
			for uv in uvs:
				uvPos = cmds.polyEditUV(uv , q = 1)
				if each[0] == uvPos[0] and each[1] == uvPos[1]:
					failedUVs.append(uv)

	if len(failedUVs) > 0:
		cmds.select(failedUVs)
		return failedUVs
	else:
		cmds.select(cl=1)

#________________#
def calcUVStats():
	
	oldTool = cmds.currentCtx()
	cmds.setToolTo("selectSuperContext")
	selObj = ""
	selObj = cmds.ls(selection = 1)
	
	if len(selObj) != 0:
		
		selObj = cmds.ls(selection = 1)
		cmds.duplicate(selObj)
		dupeObj = cmds.ls(selection = 1)
		cmds.select (dupeObj)
		cmds.polyTriangulate(dupeObj)
		cmds.select(dupeObj)

		str1 = "cmds.select("
		str2 = ".f["
		str3 = "]\")"
		area = 0
		areaPercent = 0
		warningRange = 0
		warningOverlapping = 0
		edgeLengthSum = 0
		uvShells = 0
		
		#Calc UV Area
		for tri in range(0, cmds.polyEvaluate(t = 1), 1):
			exec(str1 + "\"" + dupeObj[0] + str2 + str(tri) + str3)
			coords = cmds.polyEditUV(cmds.filterExpand(cmds.polyListComponentConversion(ff = 1, 
fuv = 1, fvf = 1, tuv = 1), sm = 35), query = 1)
			for coord in coords:
				if (coord > 1.0 or coord < 0.0):
					warningRange = 1
			face = abs(((coords[0]*coords[3] - coords[1]*coords[2]) + (coords[2]*coords[5] - 
coords[3]*coords[4]) + (coords[4]*coords[1] - coords[5]*coords[0]))/2)
			area += face
		
		if warningRange:
			button = cmds.confirmDialog(title = "!!!  UV's  out of Range  !!!", message = "Stop and show failed UV's ?", button = ["Yes","No"], defaultButton = "No", cancelButton = 

"No", dismissString = "No")
			failedUVs = checkUniqueUVSpace(selObj)
			openMaya.MGlobal.displayWarning((str(failedUVs) + "  Out of Range!"))

			if button == "Yes":
				cmds.delete(dupeObj)
				cmds.setToolTo(oldTool)
				cmds.confirmDialog( message='Failed UVs have been selected', title='Overlapping results')
				return
				
		button = cmds.confirmDialog(title = "Do an Overlapping Test?", message = "Warning: This can be really Slow !!!", button = ["Yes","No"], defaultButton = "No", cancelButton = "No", 

dismissString = "No")

		if button == "Yes":
			check4Overlapping = checkOverlappingUVs(dupeObj, selObj)
			if check4Overlapping:
				return
			
		#Calc BorderEdgeLenght
		cmds.select(dupeObj)
		cmds.select(cmds.polyListComponentConversion(ff = 1, tuv = 1)) #Convert to UVs
		cmds.polySelectConstraint(t = 0x0010 ,sh = 0, bo = 1, m = 2) #Convert to ShellBorder
		cmds.select(cmds.polyListComponentConversion(fv = 1, ff = 1, fuv = 1, fvf = 1, te = 1, 
internal = 1)) #Convert to contained Edges
		containedBoarderEdges = cmds.filterExpand(cmds.ls(selection = 1), sm = 32)
		
		for boarder in containedBoarderEdges:
			cmds.select(cmds.polyListComponentConversion(boarder, ff = 1, fuv = 1, fvf = 1, fe = 
1, tv = 1))
			allPnts = cmds.xform(q = 1, ws = 1, t = 1)
			pntA = [allPnts[0], allPnts[1], allPnts[2]] #x,y,z coords
			pntB = [allPnts[3], allPnts[4], allPnts[5]]
			edgeLen = vector(pntA) - vector(pntB)
			edgeLen = edgeLen.length()
			edgeLengthSum += edgeLen
		
		#Calc UV Shells
		cmds.select(dupeObj)
		cmds.select(cmds.polyListComponentConversion(ff = 1, tuv = 1)) #Convert to UVs
		allUVs = []
		allUVs = cmds.filterExpand(cmds.ls(selection = 1), sm = 35) #Expand all selected UVs
		
		while len(allUVs) > 0:
			cmds.polySelectConstraint(disable = 1)
			cmds.select(allUVs[0])
			cmds.polySelectConstraint(t = 0x0010 ,sh = 1, bo = 0, m = 2) #Convert to Shell
			shell = cmds.ls(selection = 1)
			shell = cmds.filterExpand(cmds.ls(selection = 1), sm = 35) #Expand all selected UVs
			allUVs = removeListbyList(allUVs, shell)
			uvShells = uvShells + 1
			
		message = "UV coverage: %s%% percent \n\nBorder edge length: %s units \n\nNumber of UV shells: %s" %((round(area*100,2)), round(edgeLengthSum,2), uvShells)
		
		cmds.delete(dupeObj)
		cmds.polySelectConstraint(disable = 1)
		cmds.setToolTo(oldTool)
		cmds.confirmDialog( message=message, title='UV statistics', button='Close')

	else:

		cmds.confirmDialog( message='You need to select a mesh', title='Error!', button = ["Ok"], defaultButton = "Ok", cancelButton = "Ok", dismissString = "No")
		openMaya.MGlobal.displayError("Select a Object!")

