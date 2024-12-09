import os
import sys
import maya.cmds as cmds
import maya.mel as mel

'''
v 1.1
import easyExport
easyExport.startEasyExport()
'''


class easyExport():
    
    def __init__(self):
        self.window = cmds.window( title="easyExport")
        cmds.rowColumnLayout( adjustableColumn=1, numberOfColumns=1, columnAttach=(1, 'right', 0), columnWidth=[(1, 400), (2, 200)] )
        self.folder = cmds.textFieldGrp( label='Folder',tx = 'C:\\Users\\mukhamadiyarov\\Desktop', ed=True)
        self.anim = cmds.textFieldGrp( label='Animation Name', ed=True)
        self.rootJointName = cmds.textFieldGrp( label='Root Joint Name', tx='global_C0_0_jnt', ed=True)
        cmds.separator(h=10)
        cmds.button( label='GO', command=self.go)
        cmds.separator(h=10)
        cmds.button( label='Close', command=('cmds.deleteUI(\"' + self.window + '\", window=True)') )
        cmds.setParent( '..' )
        cmds.showWindow( self.window )
        
        self.fromField = cmds.playbackOptions(q=True, min=True)
        self.toField = cmds.playbackOptions(q=True, max=True)
        
    def getFolder(self):
        finalName = cmds.textFieldGrp( self.folder, q=True, tx=True)
        return finalName
        
    def getAnimationName(self):
        animName = cmds.textFieldGrp( self.anim, q=True, tx=True)
        return animName
        
    def getRootJointName(self):
        rootJointName = cmds.textFieldGrp( self.rootJointName, q=True, tx=True)
        return rootJointName     
    
    def go(self, *arg):
        folder = self.getFolder()
        anim = self.getAnimationName()
        rootJoint = self.getRootJointName()
        mainpath = "{0}\\{1}.fbx".format(folder, anim)
        finmainpath = mainpath.replace(os.sep, '/')
      
        sel = cmds.ls(sl=True)
        
        if sel:
            sel=sel[0]
            if cmds.referenceQuery(sel, isNodeReferenced=True):
                node = cmds.referenceQuery(sel, referenceNode=True)
                filename = cmds.referenceQuery(sel, filename=True)
                cmds.file(filename, importReference=True)
            getNameSpace = sel.split(':')[0]
            cmds.namespace(removeNamespace = getNameSpace, mnr=True)
            selRoot = cmds.ls(rootJoint)
            cmds.parent(selRoot, w=True)
            cmds.select(rootJoint, hi=True)
            selExportJoints = cmds.ls(sl=True)
            cmds.select(cl=True)
            for i in selExportJoints:
            	cmds.setAttr( i + '.tx', l = False, k = True )
            	cmds.setAttr( i + '.ty', l = False, k = True )
            	cmds.setAttr( i + '.tz', l = False, k = True )
            	cmds.setAttr( i + '.rx', l = False, k = True )
            	cmds.setAttr( i + '.ry', l = False, k = True )
            	cmds.setAttr( i + '.rz', l = False, k = True )
            	cmds.setAttr( i + '.sx', l = False, k = True )
            	cmds.setAttr( i + '.sy', l = False, k = True )
            	cmds.setAttr( i + '.sz', l = False, k = True )			
            	cmds.setAttr( i + '.v', l = False, k = True )
            	
            cmds.bakeResults(selExportJoints, simulation=True, t=(self.fromField, self.toField))
           
            for e in selExportJoints:
                cmds.filterCurve(e)
                cmds.selectKey(clear=True)
                cmds.selectKey(e, add=True, k=True)
               
            cmds.select(rootJoint, hi=True)    
            mel.eval('FBXResetExport')
            #mel.eval('FBXExportSmoothingGroups -v false')
            #mel.eval('FBXExportSmoothMesh -v false')
            mel.eval('FBXExportAnimationOnly -v false')
            mel.eval('FBXExportInputConnections -v false')
            mel.eval('FBXExportUpAxis y')
            mel.eval('FBXExport -f "{0}" -s'.format(finmainpath))
            mel.eval("FBXExportInAscii -v false")

def startEasyExport():
    easyExport()

