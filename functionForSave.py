import os
import shutil
import stat
folderLocation = os.getenv('LOCALAPPDATA') + "/The First Berserker Khazan/Saved/SaveGames"
AllSavePath = folderLocation + "/Save"
os.makedirs(AllSavePath,exist_ok=True)
for i in os.listdir(folderLocation) :
    if i.isdigit():
        CurrentSavePath = folderLocation+"/"+i
        break

def importSave(Name):
    NewSavePath = AllSavePath +"/"+Name
    if os.path.exists(NewSavePath) :        
        os.chmod(NewSavePath,stat.S_IWUSR)
        shutil.rmtree(NewSavePath)
    shutil.copytree(CurrentSavePath,NewSavePath,dirs_exist_ok=True)

def RemoveSave(Name):
    RemovedSavePath = AllSavePath +"/"+Name
    os.chmod(RemovedSavePath,stat.S_IWUSR)
    shutil.rmtree(RemovedSavePath)

def RenameSave(OldName,NewName):
    OldNamePath = AllSavePath +"/"+OldName
    NewNamePath = AllSavePath +"/"+NewName
    os.rename(OldNamePath,NewNamePath)

def LoadSave(Name):
    LoadedSavePath = AllSavePath +"/"+Name
    if os.path.exists(CurrentSavePath):
        for i in os.listdir(CurrentSavePath):
            os.remove(CurrentSavePath +"/"+i)
    shutil.copytree(LoadedSavePath,CurrentSavePath,dirs_exist_ok=True)

def GetListOfSave():
    return os.listdir(AllSavePath)





