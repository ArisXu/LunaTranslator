 
from PyQt5.QtWidgets import QWidget,QLabel,QStyle ,QPushButton,QGridLayout,QSpinBox,QComboBox,QScrollArea,QLineEdit,QApplication,QFileDialog
from PyQt5.QtGui import QColor 
from PyQt5.QtCore import Qt 
import functools,sqlite3
from utils.config import globalconfig ,translatorsetting
import os,json
import qtawesome,sys

import gui.switchbutton
import gui.attachprocessdialog  
from traceback import print_exc
import gui.selecthook 
import time
import importlib
import socket
from gui.inputdialog import autoinitdialog
def fanyiselect(self, who,checked ):
            if checked : 
                globalconfig['fanyi'][who]['use']=True
                self.object.prepare(who) 
            else:
                globalconfig['fanyi'][who]['use']=False 
def initsome11(self,l,label,grids): 
    grids.append(
        [(QLabel(label),4)]
    )
    i=0
    for fanyi in globalconfig['fanyi']:
        if i%3==0:
            line=[]
        if fanyi not in l:
            continue
        i+=1
        try:
            importlib.import_module('translator.'+fanyi)
        except:
            print_exc()
            continue
        
        
        if 'argsfile' in globalconfig['fanyi'][fanyi]:
             
            items=[] 
            for arg in translatorsetting[fanyi]['args']: 
                items.append({
                        't':'lineedit','l':arg,'d':translatorsetting[fanyi]['args'],'k':arg
                    })
                if arg=='json文件' or arg=='sqlite文件':
                    items[-1].update({
                        't':'file',
                        'dir':False,
                        'filter':"*.json" if arg=='json文件' else "*.sqlite"
                    }) 
                elif arg=='路径':
                    items[-1].update({
                        't':'file',
                        'dir':True 
                    }) 
            items.append({'t':'okcancel' })
            last=self.getcolorbutton(globalconfig,'',callback=functools.partial(autoinitdialog,self,globalconfig['fanyi'][fanyi]['name']+'设置',900,items),icon='fa.gear',constcolor="#FF69B4")
        else:
            last=''
        line+=[(QLabel(globalconfig['fanyi'][fanyi]['name']),5),
        self.getsimpleswitch(globalconfig['fanyi'][fanyi],'use',callback=functools.partial( fanyiselect,self,fanyi)),
        self.getcolorbutton(globalconfig['fanyi'][fanyi],'color',name="fanyicolor_"+fanyi,callback=functools.partial(self.ChangeTranslateColor,fanyi,None,self,"fanyicolor_"+fanyi)),last ] 


        if i%3==0 or i==len(l):
            grids.append(line)
        else:
            line+=['']
def initfanyiswitchs_auto11(self,grids):  
        lixians=set(('jb7','dreye','kingsoft'))
        alls=set(globalconfig['fanyi'].keys())
        mt=set(('rengong','premt'))
        online=alls-lixians-mt

        mianfei=set()
        for _ in online:
            if 'argsfile' not in globalconfig['fanyi'][_]:
                mianfei.add(_)
        
        shoufei=online-mianfei 
 
        initsome11(self, lixians,'离线翻译',grids)  
        grids.append([''])
        initsome11(self, mianfei,'在线翻译',grids)
        grids.append([''])
        initsome11(self, shoufei,'注册在线翻译',grids)
        grids.append([''])
        initsome11(self,mt,'预翻译',grids) 
def setTabTwo(self) :
        def __timeout(x):
    
            globalconfig.__setitem__('translatortimeout',x)
            socket.setdefaulttimeout(globalconfig['translatortimeout'])

        def _setproxy(x):
            globalconfig.__setitem__('useproxy',x)
            if x:
                os.environ['https_proxy']=globalconfig['proxy'] 
                os.environ['http_proxy']=globalconfig['proxy'] 
            else:
                os.environ['https_proxy']='' 
                os.environ['http_proxy']=''
        _setproxy(globalconfig['useproxy'])

        proxy=QLineEdit(globalconfig['proxy'])
        btn=QPushButton('确定' )
        def __resetproxy(x):
            globalconfig.__setitem__('proxy',proxy.text())
            if globalconfig['useproxy']:
                os.environ['https_proxy']=globalconfig['proxy'] 
                os.environ['http_proxy']=globalconfig['proxy'] 
        btn.clicked.connect(lambda x: __resetproxy(x))
        transkirokuuse =QComboBox( )  
        transkirokuuse.addItems([globalconfig['fanyi'][k]['name'] for k  in globalconfig['fanyi']])
        transkirokuuse.setCurrentIndex(list(globalconfig['fanyi'].keys()).index(globalconfig['transkirokuuse']))
        transkirokuuse.currentIndexChanged.connect(lambda x:globalconfig.__setitem__('transkirokuuse',list(globalconfig['fanyi'].keys())[x]))
        bt = QPushButton("导出sqlite文件为json文件")  

        def _sqlite2json():
                f=QFileDialog.getOpenFileName(filter="*.sqlite")
                if f[0]!='' :
                        try:
                                sql=sqlite3.connect(f[0],check_same_thread=False)
                                ret=sql.execute(f'SELECT * FROM artificialtrans  ').fetchall()
                                js={}
                                for _id,source,mt,ut  in ret:
                                        js[source]={'userTrans':ut,'machineTrans':mt}
                                with open(os.path.join(os.path.dirname(f[0]), os.path.basename(f[0]).replace('.'+os.path.basename(f[0]).split('.')[-1],'.json')),'w',encoding='utf8') as ff:
                                        ff.write(json.dumps(js,ensure_ascii=False,sort_keys=False, indent=4))
                        except:
                                print_exc()
        bt.clicked.connect(lambda x:_sqlite2json()) 
 
  

        grids=[
            [
                (QLabel("是否显示翻译器名称"),5),(self.getsimpleswitch(globalconfig  ,'showfanyisource'),1),'','','',
                (QLabel("源语言"),5),(self.getsimplecombobox(['日文','英文'],globalconfig,'srclang'),3),'',
                (QLabel("目标语言"),5),(self.getsimplecombobox(['中文','英文'],globalconfig,'tgtlang'),3) ,
            ],
            [
                (QLabel("最短翻译字数"),5),(self.getspinbox(0,500,globalconfig,'minlength'),3),'',
                (QLabel("最长翻译字数"),5),(self.getspinbox(0,500,globalconfig,'maxlength'),3),'',
                (QLabel("在线翻译超时(s)"),5),(self.getspinbox(1,20,globalconfig,'translatortimeout',callback=lambda x:__timeout(x)),3),

            ],
            [
                (QLabel("预翻译采用模糊匹配"),5),(self.getsimpleswitch(globalconfig  ,'premtsimiuse'),1),'','','',
                (QLabel("模糊匹配相似度限制"),5),(self.getspinbox(0,500,globalconfig,'premtsimi'),2),'', 
            ],[
                (QLabel("使用代理(ip:port)"),5),(self.getsimpleswitch(globalconfig  ,'useproxy',callback=lambda x: _setproxy(x)),1),
                (proxy,8),(btn,2),  
            ],
            
                [(QLabel('录制翻译文件'),5),(self.getsimpleswitch(globalconfig,'transkiroku'),1),
                 (QLabel('优先录制的翻译源'),6),(transkirokuuse,4),
                 
                 (bt,6) ,
                 ],
            ['']
        ] 
        initfanyiswitchs_auto11(self,grids)
         
        self.yitiaolong("翻译设置",grids)