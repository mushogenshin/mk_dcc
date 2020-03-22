
Copyright 2017(c)purplepuppet AB. All Rights Reserved

spaceSwitchSetup tool - Python bytecode for Autodesk Maya
====================================================

Supported Maya versions
-----------------------
Maya 2014
Maya 2015
Maya 2016
Maya 2017

Updates
-----------------------
12-11-2017: The Marking menu triggers when cursor is not directly on the selected object.


Installation
---------------------------------------------------
1-Place the spaceSwitchTool folder in your user scripts folder. for example C:\Users\(user)\Documents\maya\<version>\scripts

2-In a python tab in the script editor add this line: 
from spaceSwitchTool import spaceSwitchSetup as switchSetup
switchSetup.show()

3-To automatically execute the marking menu command every time you start up Maya, add these lines to your userSetup.py file:

import maya.cmds as cmds
from spaceSwitchTool import spaceSwitchScripts
cmds.evalDeferred('''spaceSwitchScripts.spaceSwitch_MM()''')

4-If you want to import the marking menu script manually, in a python tab run these lines:
from spaceSwitchTool import spaceSwitchScripts
spaceSwitchScripts.spaceSwitch_MM()


To use the marking menu press CTRL + MMB on the target object you created the space switch setup on.

Full Documentation available on: http://www.rihamtoulan.com/space-switch-setup-tool/