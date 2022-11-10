import json 
import os ,importlib
from utils.defaultconfig import *
if os.path.exists('./userconfig')==False:
    os.mkdir('./userconfig')
if os.path.exists('./transkiroku')==False:
    os.mkdir('./transkiroku')
if os.path.exists('./ttscache/')==False:
    os.mkdir('./ttscache/')
if os.path.exists('./capture')==False:
    os.mkdir('./capture')

def tryreadconfig(path):
    if os.path.exists(os.path.join('./userconfig/',path)):
        path=os.path.join('./userconfig/',path)
        with open(path,'r',encoding='utf-8') as ff:
            x=json.load(ff)
    elif os.path.exists(os.path.join('./files/',path)):
        path=os.path.join('./files/',path)
        with open(path,'r',encoding='utf-8') as ff:
            x=json.load(ff)
    else:
        x={}
    return x 

globalconfig=tryreadconfig('config.json')
postprocessconfig=tryreadconfig('postprocessconfig.json')
noundictconfig=tryreadconfig('noundictconfig.json')
transerrorfixdictconfig=tryreadconfig('transerrorfixdictconfig.json')
savehook_new=tryreadconfig('savehook_new.json') 
savehook_new2=tryreadconfig('savehook_new3.json') 

translatorsetting=tryreadconfig('translatorsetting.json') 
ocrsetting=tryreadconfig('ocrsetting.json') 

def syncconfig(config,default,drop=False,deep=0):
    
    for key in default: 
        if key not in config: 
            config[key]=default[key] 
        elif key=='name': 
            config[key]=default[key]
        if type(default[key])!=type(config[key]) and (type(default[key])==dict or type(default[key])==list): 
            config[key]=default[key] 
        elif type(default[key])==dict:  
            syncconfig(config[key],default[key],drop,deep-1)
             
    if drop and deep>0:
        for key in list(config.keys()):
            if key not in default:
                config.pop(key) 
           
syncconfig(postprocessconfig,defaultpost ,True,3) 
syncconfig(globalconfig,defaultglobalconfig)
 
syncconfig(transerrorfixdictconfig,defaulterrorfix)

syncconfig(noundictconfig,defaultnoun)
syncconfig(translatorsetting,translatordfsetting)
syncconfig(ocrsetting,ocrdfsetting)

for name in translatorsetting: 
    try:
        configfile=globalconfig['fanyi'][name]['argsfile']
        if os.path.exists(configfile) : 
            with open(configfile,'r',encoding='utf8') as ff:
                js=json.load(ff)  
            for k in translatorsetting[name]['args']:
                if k in js['args']:
                    translatorsetting[name]['args'][k]=js['args'][k]  
            #os.remove(configfile)
            globalconfig['fanyi'][name]['argsfile']=''
    except:
        print('error',name)


for name in ocrsetting: 
    #try:
        configfile=globalconfig['ocr'][name]['argsfile']
        if os.path.exists(configfile) : 
            with open(configfile,'r',encoding='utf8') as ff:
                js=json.load(ff)  
            for k in ocrsetting[name]['args']:
                if k in js['args']:
                    ocrsetting[name]['args'][k]=js['args'][k]  
            #os.remove(configfile)
            globalconfig['ocr'][name]['argsfile']=''
    #except:
    #    print('error',name)
#0 ja  1 eng

language=globalconfig['languageuse']
with open(f'./files/lang/{language}.json','r',encoding='utf8') as ff:
    languageshow=json.load(ff)
def _TR(k):
    if language==0:
        return k
    if k not in languageshow:
        print(k)
        return k
    else:
        return languageshow[k]
def _TRL(kk):
    x=[]
    for k in kk:
        x.append(_TR(k))
    return x

def saveallconfig():
        
        with open('./userconfig/config.json','w',encoding='utf-8') as ff:
            ff.write(json.dumps(globalconfig,ensure_ascii=False,sort_keys=False, indent=4))
         
        with open('./userconfig/postprocessconfig.json','w',encoding='utf-8') as ff:
            ff.write(json.dumps(postprocessconfig,ensure_ascii=False,sort_keys=False, indent=4))
        with open('./userconfig/transerrorfixdictconfig.json','w',encoding='utf-8') as ff:
            ff.write(json.dumps(transerrorfixdictconfig,ensure_ascii=False,sort_keys=False, indent=4))
        with open('./userconfig/noundictconfig.json','w',encoding='utf-8') as ff:
            ff.write(json.dumps(noundictconfig,ensure_ascii=False,sort_keys=False, indent=4))
        with open('./userconfig/translatorsetting.json','w',encoding='utf-8') as ff:
            ff.write(json.dumps(translatorsetting,ensure_ascii=False,sort_keys=False, indent=4))
        with open('./userconfig/ocrsetting.json','w',encoding='utf-8') as ff:
            ff.write(json.dumps(ocrsetting,ensure_ascii=False,sort_keys=False, indent=4))

        with open('./userconfig/savehook_new.json','w',encoding='utf8') as ff:
                ff.write(json.dumps(savehook_new,ensure_ascii=False))
        with open('./userconfig/savehook_new3.json','w',encoding='utf8') as ff:
                ff.write(json.dumps(savehook_new2,ensure_ascii=False))