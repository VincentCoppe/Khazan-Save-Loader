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

def ImportSave(Name,Profile):
    if Profile == "":
        return False
    NewSavePath = AllSavePath +"/"+Profile+"/"+Name
    if os.path.exists(NewSavePath) :        
        os.chmod(NewSavePath,stat.S_IWUSR)
        shutil.rmtree(NewSavePath)
    shutil.copytree(CurrentSavePath,NewSavePath,dirs_exist_ok=True)
    return True

def DuplicateSave(Name,NameOfCopy,Profile):
    if Profile == "":
        return False
    OldSavePath = AllSavePath +"/"+Profile+"/"+Name
    NewSavePath = AllSavePath +"/"+Profile+"/"+NameOfCopy
    if os.path.exists(NewSavePath) :        
        os.chmod(NewSavePath,stat.S_IWUSR)
        shutil.rmtree(NewSavePath)
    shutil.copytree(OldSavePath,NewSavePath,dirs_exist_ok=True)
    return True

def RemoveSave(Name,Profile):
    if Profile == "":
        return False
    RemovedSavePath = AllSavePath +"/"+Profile+"/"+Name
    os.chmod(RemovedSavePath,stat.S_IWUSR)
    shutil.rmtree(RemovedSavePath)
    return True

def RenameSave(OldName,NewName,Profile):
    if Profile == "":
        return False
    OldNamePath = AllSavePath +"/"+Profile+"/"+OldName
    NewNamePath = AllSavePath +"/"+Profile+"/"+NewName
    os.rename(OldNamePath,NewNamePath)
    return True

def LoadSave(Name,Profile):
    if Profile == "":
        return False
    LoadedSavePath = AllSavePath +"/"+Profile+"/"+Name
    if os.path.exists(CurrentSavePath):
        for i in os.listdir(CurrentSavePath):
            os.remove(CurrentSavePath +"/"+i)
    shutil.copytree(LoadedSavePath,CurrentSavePath,dirs_exist_ok=True)
    return True

def GetListOfSave(Profile):
    return os.listdir(AllSavePath+"/"+Profile)

def GetListOfProfile():
    return os.listdir(AllSavePath)

def CreateProfile(Profile):
    if Profile == "":
        return False
    NewProfilePath = AllSavePath +"/"+Profile
    if os.path.exists(NewProfilePath) :
        return "Profile already exist"
    os.makedirs(NewProfilePath,exist_ok=True)
    return True

def DeleteProfile(Profile):
    if Profile == "":
        return False
    RemovedprofilePath = AllSavePath +"/"+Profile
    for root,dirs,files in os.walk(RemovedprofilePath):
        os.chmod(root,stat.S_IWUSR)
        for d in dirs:
            dirsPath = RemovedprofilePath + "/" + d
            os.chmod(dirsPath,stat.S_IWUSR)
    shutil.rmtree(RemovedprofilePath)
    return True

def DuplicateProfile(Profile, NameOfCopy):
    profilePath = AllSavePath +"/"+Profile
    CopyPath = AllSavePath +"/"+NameOfCopy
    shutil.copytree(profilePath,CopyPath,dirs_exist_ok=True)

def RenameProfile(Profile, NewName):
    OldProfilePath = AllSavePath +"/"+Profile
    NewProfilePath = AllSavePath +"/"+NewName
    os.rename(OldProfilePath,NewProfilePath)


