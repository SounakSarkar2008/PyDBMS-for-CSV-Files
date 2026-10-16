This one
#Command style DBMS with cprint,count,edit,add,delete,refresh,ERASE,view,highlight,Sum,evaluate,box,COLOURSS,show,scroll,delim,replace,THEME
from tkinter import *
from time import sleep as KNOCKOUT
from random import randint
import csv
class cmds:
    cmdlist=['cprint','count','edit','add','delete','refresh','ERASE','view','highlight','Sum','evaluate','box','COLOURSS','show','scroll','delim','replace','THEME']
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    def __init__(self,*prompt):
        pass
    def __str__(self):
        return 'All available commands'
    class cprint:
        def __init__(self,*prompt):
            if len(prompt)!=1:
                clist.insert(END,f'Argument Error: cmds.cprint(<prompt>) expected 1 Argument but got {len(prompt)}')
            else:
                clist.insert(END,prompt[0])
    class count:
        def __init__(self,*prompt):
            self.list=['rows','columns']
            if len(prompt)<1:
                clist.insert(END,f'There are {len(tdata)-len(read[0])} elements in the file.')
            elif len(prompt)>1:
                clist.insert(END,'Argument Error: cmds.count(<prompt>) expected 0 or 1 argument')
            elif prompt[0] not in self.list:
                clist.insert(END,f'Invalid Argument: prompt should be from {self.list} in cmds.count(<prompt>)')
            elif prompt[0]=='rows':
                clist.insert(END,f'There are {len(read)-1} rows in this File.')
            elif prompt[0]=='columns':
                clist.insert(END,f'There are {len(max(read,key=len))} columns in this File.')
    class edit:
        def __init__(self,*prompt):
            if len(prompt)!=3:
                clist.insert(END,f'Argument Error: cmds.edit(<row>,<column>,<entry>) expected 3 arguments but got {len(prompt)}')
                return
            r,c,IMP=prompt
            if str(type(r))=='<class \'str\'>':
                if not r.isdigit():
                    clist.insert(END,f'Type Error: cmds.edit(<row>,<column>,<entry>) expected an integer at <row> but got {r}')
                    return
                else:
                    r=int(r)
            if str(type(c))=='<class \'str\'>':
                if not r.isdigit():
                    clist.insert(END,f'Type Error: cmds.edit(<row>,<column>,<entry>) expected an integer at <column> but got {c}')
                    return
                else:
                    c=int(c)
            if str(type(r))!='<class \'int\'>' or str(type(c))!="<class 'int'>":
                clist.insert(END,f'Type Error: cmds.edit(<row>,<column>,<entry>) expected int but got {str(type(r))[-3:-1] if str(type(r))[-3:-1]!="str" else str(type(c))[-3:-1]}')
                return
            if c==0:
                clist.insert(END,'Index Error: Cannot edit column headers')
                return
            if r>len(read)-1:
                clist.insert(END,f'Index Error: row Index out of range')
            elif c>len(max(read,key=len)):
                clist.insert(END,f'Index Error: column Index out of range')
            else:
                read[r][c-1]=str(IMP)
                fh.seek(0)
                write.writerows(read)
                fh.flush()
                updater()
    class add:
        def __init__(self,*prompt):
            condition=1
            prompt=list(prompt)
            self.list=['row','column']
            if len(prompt)<1 or len(prompt)>3:
                clist.insert(END,f'Argument Error: cmds.add(<prompt> [,<positon> [,<value>]]) expected 1, 2 or 3 arguments but got {len(prompt)}')
                return
            elif prompt[0] not in ('row','column'):
                clist.insert(END,f'Invalid Argument: prompt should be from {self.list} in cmds.add(<prompt> [,<positon> [,<value>]])')
                return
            if len(prompt)==1:
                prompt+=[0,'']
            elif len(prompt)==2:
                prompt+=['']
            if prompt[1]==0:
                if prompt[0]=='row':
                    prompt[1]=len(read)
                else:
                    prompt[1]=len(max(read,key=len))
                    condition=0
            if prompt[0]=='row' and prompt[1]==0:
                clist.insert(END,'Index Error: Put <row> as 1 for adding row to top in cmds.add(row,<row>)')
                return
            if prompt[0]=='column' and prompt[1]==0:
                clist.insert(END,'Index Error: Put <column> as 1 for adding column to top in cmds.add(column,<column>)')
                return
            if prompt[0]=='row':
                read.insert(prompt[1],[str(prompt[2]) for x in range(len(max(read,key=len)))])
                fh.seek(0)
                write.writerows(read)
                fh.flush()
                updater()
            elif prompt[0]=='column':
                if condition:
                    prompt[1]-=1
                waste873249374=[x.insert(prompt[1],str(prompt[2])) for x in read]
                fh.seek(0)
                write.writerows(read)
                fh.flush()
                updater()
    class delete:
        def __init__(self,*prompt):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            self.list=['row','column']
            if len(prompt)!=2:
                clist.insert(END,f'Argument Error: cmds.delete(<prompt>,<number>) expected 2 arguments but got {len(prompt)}')
                return
            elif prompt[0] not in self.list:
                clist.insert(END,f'Invalid Argument: prompt should be from {self.list} in cmds.delete(<prompt>,<number>)')
                return
            v=prompt[1]
            if prompt[0]=='row' and v>len(read)-1:
                clist.insert(END,'Index Error: row Index out of range')
            elif prompt[0]=='column' and v>len(max(read,key=len)):
                clist.insert(END,'Index Error: column Index out of range')
            elif prompt[0]=='row' and v==0:
                clist.insert(END,'Index Error: Cannot delete row headers')
            elif prompt[0]=='column' and v==0:
                clist.insert(END,'Index Error: Cannot delete column headers')
            elif prompt[0]=='row':
                read.pop(v)
                ready=read.copy()
                fh.close()
                fh=open(flocation,'w+',newline='')
                write=csv.writer(fh,delimiter=delim)
                write.writerows(ready)
                fh.flush()
                fh.seek(0)
                read=list(csv.reader(fh,delimiter=delim))
                updater()
            else:
                waste2893490001=[x.pop(v-1) for x in read]
                ready=read.copy()
                fh.close()
                fh=open(flocation,'w+',newline='')
                write=csv.writer(fh,delimiter=delim)
                write.writerows(ready)
                fh.flush()
                fh.seek(0)
                read=list(csv.reader(fh,delimiter=delim))
                updater()
    class refresh:
        def __init__(self,*prompt):  
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            if len(prompt)!=0:
                clist.insert(END,f'Argument Error: cmds.refresh() expected 0 arguments but got {len(prompt)}')
            else:
                fh.seek(0)
                read=list(csv.reader(fh,delimiter=delim))
                write=csv.writer(fh,delimiter=delim)
                updater()
                clist.insert(END,'Refresh successful!')
    class ERASE:
        global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG,NUKE
        def __init__(self,*prompt):
            global NUKE
            def NUKE():
                global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
                confirm.destroy()
                fh.close()
                header=read[0]
                fh=open(flocation,'w+',newline='')
                write=csv.writer(fh,delimiter=delim)
                write.writerow(header)
                fh.flush()
                fh.seek(0)
                read=list(csv.reader(fh,delimiter=delim))
                updater()
            if len(prompt)!=0:
                clist.insert(END,f'Argument Error: cmds.ERASE() expected 0 arguments but got {len(prompt)}')
            else:
                confirm=Tk(className=' Confirmation Window')
                Label(confirm,text='Are you sure you want to clear this file?',font=('Milker',20,'underline')).pack(pady=5,padx=15)
                Button(confirm,text='yes',command=NUKE,font=('Times New RomaN',15)).pack(pady=5)
                Button(confirm,text='no',command=lambda :confirm.destroy(),font=('Times New RomaN',15)).pack(pady=2)
    class view:
        def __init__(self,*prompt):
            if len(prompt)!=2:
                clist.insert(END,f'Argument Error: cmds.view(<row>,<column>) expected 2 arguments but got {len(prompt)}')
                return
            r,c=prompt
            rt=str(type(r))[8:-2]
            ct=str(type(c))[8:-2]
            if not(rt==ct=='int'):
                clist.insert(END,f'Type Error: cmds.view(<row>,<column>) expected int but got {rt if rt!="int" else ct}')
            elif c==0:
                if r!=0:
                    clist.insert(END,r)
                elif r==0:
                    clist.insert(END,'Developer Button')
            elif r>len(read)-1:
                clist.insert(END,f'Index Error: row Index out of range')
            elif c>len(max(read,key=len)):
                clist.insert(END,f'Index Error: column Index out of range')
            else:
                clist.insert(END,read[r][c-1])
    class highlight:
        def __init__(self,*prompt):
            if len(prompt)!=1:
                clist.insert(END,f'Argument Error: cmds.highlight(<value>) expected 1 argument but got {len(prompt)}')
                return
            n=0
            v=str(prompt[0])
            for i in tdata:
                if i['text']==v:
                    n+=1
                    i['bg']=C_HIGH
            clist.insert(END,f'{n} entries with value \'{v}\' were found.')
    class SUM:
        def __init__(self,*prompt):
            if len(prompt)!=4:
                clist.insert(END,f'Argument Error: cmds.SUM(<cell 1 row>,<cell 1 column>,<cell 2 row>,<cell 2 column>) expected 4 arguments but got {len(prompt)}')
                return
            for i in prompt:
                if str(type(i))!="<class 'int'>":
                    clist.insert(END,f'Type Error: Expected int but got {str(type(i))[8:-2]}')
                    return
            r1,c1,r2,c2=prompt
            relv=[]
            if 0 in (c1,c2):
                clist.insert(END,'Index Error: Cannot operate on Column headers')
                return
            try:
                for i in range(len(read)):
                    for j in range(len(read[i])):
                        if i==0:
                            break
                        if (r1<=i<=r2 and c1-1<=j<=c2-1) or (r2<=i<=r1 and c2-1<=j<=c1-1):
                            relv.append(float(read[i][j]))
            except ValueError:
                clist.insert(END,'Type Error: Please ensure all data entries within specified range are numeric')
            else:
                clist.insert(END,f'The sum of all entries is {sum(relv)}')
    class evaluate:
        def __init__(self,prompt):
            p=str(prompt)
            res=''
            condit=0
            for i in p:
                if i=='[':
                    condit=1
                if condit:
                    res+=i
                if i==']':
                    #print(prompt,res)
                    condit=0
                    r=int(res[1:res.index(',')])
                    c=int(res[res.index(',')+1:-1])
                    if c==0:
                        clist.insert(END,'Index Error: Cannot Operate on column Headers')
                        return
                    prompt=prompt.replace(res,str(read[r][c-1]))
                    res=''
            clist.insert(END,f'The answer is {eval(prompt)}')
    class box:
        def __init__(self,*prompt,multiple=False):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            self.MultiList=(True,False,'True','False','true','row','column','Row','Column')
            if multiple not in self.MultiList:
                clist.insert(END,f'Argument Error: multiple parameter expected True or False but got {multiple}')
            elif multiple in (False,'False','false'):
                if len(prompt)!=4:
                    clist.insert(END,f'Argument Error: cmds.box(<cell 1 row>,<cell 1 column>,<cell 2 row>,<cell 2 column>) expected 4 arguments but got {len(prompt)}')
                    return
                for i in prompt:
                    if str(type(i))!="<class 'int'>":
                        clist.insert(END,f'Type Error: Expected int but got {str(type(i))[8:-2]}')
                        return
                r1,c1,r2,c2=prompt
                if 0 in (c1,c2):
                    clist.insert(END,'Index Error: Cannot box(multiple=False) Column Headers')
                    return
                for k in tdata:
                    for i in range(len(read)):
                        for j in range(len(read[i])):
                          #  if k['text']==read[i][j] and ((r1<=i<=r2 and c1-1<=j<=c2-1) or (r2<=i<=r1 and c2-1<=j<=c1-1)):
                            if tdata.index(k)==tposedata.index([i,j+1]) and ((r1<=i<=r2 and c1-1<=j<=c2-1) or (r2<=i<=r1 and c2-1<=j<=c1-1)):
                                if i==0:
                                    if unhigh:
                                        k['bg']=C_UI
                                    else:
                                        k['bg']=C_HEAD
                                else:
                                    if unhigh:
                                        k['bg']=C_BG
                                    else:
                                        k['bg']=C_HIGH
            elif multiple in (True,'True','true'):
                if len(prompt)%2!=0:
                    clist.insert(END,f'Argument Error: Invalid cell coordinates {prompt[-1]},None')
                    return
                for i,j in zip(list(range(0,len(prompt),2)),list(range(1,len(prompt),2))):
                    cmds.box(prompt[i],prompt[j],prompt[i],prompt[j])
            elif multiple in ('row','Row'):
                if len(prompt)!=1:
                    clist.insert(END,f'Argument Error: cmds.box(<row>,multiple=row) expected 2 Arguments but got {len(prompt)+1}')
                    return
                r=prompt[0]
                if r>len(read)-1:
                    clist.insert(END,'Index Error: Row range out of Index')
                else:
                    cmds.box(r,1,r,len(max(read,key=len)))
                    if not(unhigh):
                        tcolheads[r-1]['bg']=C_HEAD
                    else:
                        tcolheads[r-1]['bg']=C_UI
                    unhigh=False
            else:
                if len(prompt)!=1:
                    clist.insert(END,f'Argument Error: cmds.box(<column>,multiple=column) expected 2 Arguments but got {len(prompt)+1}')
                    return
                c=prompt[0]
                if c>len(max(read,key=len)):
                    clist.insert(END,'Index Error: Column range out of Index')
                else:
                    cmds.box(0,c,len(read)-1,c)
                    unhigh=False
    class COLOURSS:
        def __init__(self,*prompt):
            if DEVCOND:
                KNOCKOUT(0.5)
                for i in tdata+tcolheads:
                    n=str(hex(randint(0,int(0xFFFFFF))))[2:]
                    while len(n)<6:
                        n='0'+n
                    i['bg']='#'+n
            else:
                clist.insert(END,'Access Denied: You lack the necessary permission to access this command')
    class show:
        def __init__(self,*prompt,highlight=False,find_specific=False):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            if highlight and not find_specific:
                if len(prompt)==0:
                    clist.insert(END,f'Argument Error: cmds.show(<prompts>,highlight=True) expected multiple Arguments in <prompts> but got none')
                    return
                for i in prompt:
                    if i in read[0]:
                        cmds.box(read[0].index(i)+1,multiple='column')
                    else:
                        clist.insert(END,f'No row header named {i} found')
            if highlight and find_specific:
                if len(prompt)!=1:
                    clist.insert(END,f'Argument Error: cmds.show(<prompts>,highlight=True,find_specific=True) expected 1 Argument in <prompts> but got {len(prompt)}')
                    return
                inter=prompt[0]
                inter={str(k):str(v) for k,v in tuple(inter.items())}
                for k,v in inter.items():
                    if k not in read[0]:
                        clist.insert(END,f'Row Header {k} does not exist.')
                        return
                    elif v not in [x[read[0].index(k)] for x in read[1:]]:
                        clist.insert(END,'No intersection of such conditions found')
                        return
                rum=read[0].copy()
                for i in inter.keys():
                    if i in rum:
                        rum.remove(i)
                for i in rum:
                    inter[i]='\\n'
                dummy2=[list(x) for x in inter.items()]
                dummy3={}
                I_ran_out_of_ideas_for_this_counter=0
                for i in read[0]:
                    for j in dummy2:
                        if i==j[0]:
                            dummy3[j[0]]=j[1]
                for i in range(len(read)):
                    if i==0:
                        continue
                    hehe=tdata[i*len(max(read,key=len)):(i+1)*len(max(read,key=len))]
                    for k,j in zip(hehe,list(dummy3.values())):
                     #   print(k,j)
                        if j=='\\n':
                            continue
                        if k['text']!=j:
                            break
                    else:
                        I_ran_out_of_ideas_for_this_counter+=1
                        cmds.box(i,multiple='row')
                if not(I_ran_out_of_ideas_for_this_counter):
                    clist.insert(END,'No intersection of such conditions found.')
            if find_specific and not highlight:
                if len(prompt)!=1:
                    clist.insert(END,f'Argument Error: cmds.show(<prompts>,highlight=True,find_specific=True) expected 1 Argument in <prompts> but got {len(prompt)}')
                    return
                inter=prompt[0]
                inter={str(k):str(v) for k,v in tuple(inter.items())}
                for k,v in inter.items():
                    if k not in read[0]:
                        clist.insert(END,f'Row Header {k} does not exist.')
                        return
                    elif v not in [x[read[0].index(k)] for x in read[1:]]:
                        clist.insert(END,'No intersection of such conditions found')
                        return
                rum=read[0].copy()
                for i in inter.keys():
                    if i in rum:
                        rum.remove(i)
                for i in rum:
                    inter[i]='\\n'
                dummy2=[list(x) for x in inter.items()]
                dummy3={}
                rownum=1
                I_ran_out_of_ideas_for_this_counter=0
                for i in tdata[len(read[0]):]:
                    i.grid_forget()
                for i in tcolheads:
                    i.grid_forget()
                for i in read[0]:
                    for j in dummy2:
                        if i==j[0]:
                            dummy3[j[0]]=j[1]
                for i in range(len(read)):
                    if i==0:
                        continue
                    hehe=tdata[i*len(max(read,key=len)):(i+1)*len(max(read,key=len))]
                    for k,j in zip(hehe,list(dummy3.values())):
                     #   print(k,j)
                        if j=='\\n':
                            continue
                        if k['text']!=j:
                            break
                    else:
                        I_ran_out_of_ideas_for_this_counter+=1
                        tcolheads[i-1]['bg']=C_UI
                        tcolheads[i-1].grid(row=rownum,column=0,padx=1,pady=1)
                        for l in range(len(hehe)):
                            hehe[l].grid(row=rownum,column=l+1)
                        rownum+=1
                if not(I_ran_out_of_ideas_for_this_counter):
                    clist.insert(END,'No intersection of such conditions found.')
                    updater()
            if not(find_specific or highlight):
                if len(prompt)==0:
                    clist.insert(END,f'Argument Error: cmds.show(<prompts>) expected multiple Arguments in <prompts> but got none')
                    return
                prompt=list(prompt)
                num=1
                for i in prompt.copy():
                    if i not in read[0]:
                        clist.insert(END,f'No header named {i} found.')
                        prompt.remove(i)
                if prompt:
                    for i in tdata:
                        i.grid_forget()
                else:
                    clist.insert(END,'No showable columns found')
                for l in prompt:
                    for i in range(len(read)):
                        for j in range(len(read[i])):
                            if j==read[0].index(l):
                                for k in tdata:
                                    if k['text']==read[i][j]:
                                        k.grid(row=i,column=num,padx=1,pady=1)
                    num+=1
    class scroll:
        def __init__(self,*prompt,Set=None):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            self.plist=('row','column')
            self.slist=('Y','X',None)
            if Set==None:
                if len(prompt)!=2:
                    clist.insert(END,f'Argument Error: cmds.Scroll(<prompt>,<value>) expected 2 arguments but got {len(prompt)}')
                    return
                if prompt[0] not in ('row','column','Row','Column'):
                    clist.insert(END,f'Invalid Argument: prompt should be from {self.plist} in cmds.Scroll(<prompt>,<value>)')
                    return
                if str(type(prompt[1]))!="<class 'int'>":
                    clist.insert(END,f'Type Error: Expected int but got {str(type(prompt[1]))[8:-2]}')
                    return
                if prompt[0] in ('row','Row'):
                    r=prompt[1]
                    if r>len(read)-1 or r<1:
                        clist.insert(END,'Index Error: Row range out of Index')
                        return
                    if 0<r-srow<=23:
                        pass
                    elif r-srow>0:
                        num=r-srow-23
                        srow+=num
                        updater()
                    elif r-srow<=0:
                        num=srow-r+1
                        srow-=num
                        updater()
                if prompt[0] in ('Column','column'):
                    c=prompt[1]
                    if c>len(max(read,key=len)) or c<1:
                        clist.insert(END,'Index Error: Column range out of Index')
                        return
                    if 0<c-scolumn<=8:
                        return
                    elif c-scolumn>0:
                        num=c-scolumn-8
                        scolumn+=num
                        updater()
                    elif c-scolumn<=0:
                        num=scolumn-c+1
                        scolumn-=num
                        updater()
            elif Set=='X' or Set=='x':
                if len(prompt)!=1:
                    clist.insert(END,f'Argument Error: cmds.Scroll(<value>,Set=\'X\') expected 2 argument but got {len(prompt)}+1')
                    return
                if str(type(prompt[0]))!="<class 'int'>":
                    clist.insert(END,f'Type Error: Expected int but got {str(type(prompt[0]))[8:-2]}')
                    return
                num=prompt[0]
                if num<0:
                    clist.insert(END,'Type Error: Please Enter a non-negetive number.')
                else:
                    xScrollAmount=num
                    clist.insert(END,f'xScrollAmount has been updated to {xScrollAmount}.')
            elif Set=='Y' or Set=='y':
                if len(prompt)!=1:
                    clist.insert(END,f'Argument Error: cmds.Scroll(<value>,Set=\'Y\') expected 2 argument but got {len(prompt)}+1')
                    return
                if str(type(prompt[0]))!="<class 'int'>":
                    clist.insert(END,f'Type Error: Expected int but got {str(type(prompt[0]))[8:-2]}')
                    return
                num=prompt[0]
                if num<0:
                    clist.insert(END,'Type Error: Please Enter a non-negetive number.')
                else:
                    yScrollAmount=num
                    clist.insert(END,f'yScrollAmount has been updated to {yScrollAmount}.')
            else:
                 clist.insert(END,f"Argument Error: Set should be equal to one of {self.slist} in cmds.scroll(<value>,Set='Y'/'X'/None)")
    class delimit:
        def __init__(self,*prompt,change=False):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            if change not in (True,'True','False',False,'true','false'):
                clist.insert(END,f'Argument error: Invalid Parameter for change "{change}"')
                return
            if len(prompt)==0:
                clist.insert(END,f'The delimeter is \'{delim}\'')
                return
            if len(prompt)>1:
                clist.insert(END,f'Argument Error: cmds.delim([<delimiter> [,change=True]]) expected 1 or 2 argument but got {len(prompt)+1}')
                return
            if len(prompt[0])!=1:
                clist.insert(END,'Type Error: Delimiter must have only one character')
                return
            OLDY=delim
            delim=str(prompt[0])
            if change:
                fh.seek(0)
                a=fh.read().replace(OLDY,delim)
                fh.seek(0)
                fh.write(a)
                fh.flush()
                clist.insert(END,f'Delimeter changed from " {OLDY} " to " {delim} "')
            fh.seek(0)
            read=list(csv.reader(fh,delimiter=delim))
            write=csv.writer(fh,delimiter=delim)
            updater()
    class replace:
        def __init__(self,*prompt):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            if len(prompt)!=2:
                clist.insert(END,f'Argument Error: cmds.replace(<value>,<replacement>) expected 2 arguments but got {len(prompt)}')
                return
            fh.seek(0)
            a=[[x if x!=str(prompt[0]) else str(prompt[1]) for x in y] for y in read]
            write.writerows(a)
            fh.seek(0)
            read=list(csv.reader(fh,delimiter=delim))
            updater()
    class THEME:
        def __init__(self,*prompt,hackerman=False):
            global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
            self.list=('Light','Dark','True Darkness','Invisible','Green Valley')
            if DEVCOND:
                if len(prompt)!=1 and len(prompt)!=6:#THE 1000th LINE WOOOOOO
                    clist.insert(END,f'Argument Error: cmds.THEME(<theme> [,hackerman=True]) expected 1 or 6 arguments but got {len(prompt)}')
                    return
                t=prompt[0].title()
                if t not in self.list:
                    if len(t)==1:
                        clist.insert(END,f'Value Error: Invalid <theme> Preset {t}')
                        clist.insert(END,f'Presets include {self.list}')
                        return
                    if len(prompt)!=6:
                        clist.insert(END,f'Value Error: list should contain 6 colours not {len(prompt)}')
                        clist.insert(END,'List of colours should be structured as [<window background colour>,<Headers/UI colour>,<Entry/Cell colour>,<Header highlight colour>,<cell highlight colour>,<text colour>]')
                    elif not([str(type(x)) for x in prompt]==["<class 'str'>"]*6):
                        clist.insert(END,f'Type Error: expected str but got {sorted([str(type(x))[8:-2] if str(type(x))[8:-2]!="str" else "" for x in prompt])[-1]}')
                        return
                    else:
                        for i in prompt:
                            try:
                                Label(bg=i)
                            except TclError:
                                clist.insert(END,f'Value Error: Unknown colour {i}')
                                return
                        mw['bg'],C_UI,C_BG,C_HEAD,C_HIGH,C_FG=prompt
                        updater()
                elif t=='Light':
                    mw['bg'],C_UI,C_BG,C_HEAD,C_HIGH,C_FG='black','light blue','white','#E3C565','yellow','black'
                    console['bg']='white'
                    clist['bg']='white'
                    tw['bg']=enter_cmd_title['bg']='light green'
                    cmd['bg']='white'
                    helping_hand['bg']=BYEBYE['bg']=CmdsButton['bg']='SystemButtonFace'
                    helping_hand['activebackground']=BYEBYE['activebackground']=CmdsButton['activebackground']='SystemButtonFace'
                    clist['fg']=cmd['fg']=enter_cmd_title['fg']=helping_hand['fg']=CmdsButton['fg']=BYEBYE['bg']='black'
                    updater()
                elif t=='Dark':
                    mw['bg'],C_UI,C_BG,C_HEAD,C_HIGH,C_FG='black','#F06F33','#3f3f3f','orange','#FDC80B','white'
                    console['bg']='black'
                    clist['bg']='black'
                    tw['bg']=enter_cmd_title['bg']='green'
                    cmd['bg']='#3f3f3f'
                    helping_hand['bg']=BYEBYE['bg']=CmdsButton['bg']='#1069EC'
                    helping_hand['activebackground']=BYEBYE['activebackground']=CmdsButton['activebackground']='#5B9BFE'
                    clist['fg']=cmd['fg']=enter_cmd_title['fg']=helping_hand['fg']=CmdsButton['fg']=BYEBYE['fg']='white'
                    updater()
                elif t=='Green Valley':
                    mw['bg'],C_UI,C_BG,C_HEAD,C_HIGH,C_FG='black','#05B611','#AAFAB0','#1069EC','#5B9BFE','black'
                    console['bg']='white'
                    clist['bg']='white'
                    tw['bg']=enter_cmd_title['bg']='#F2E941'
                    cmd['bg']='white'
                    helping_hand['bg']=BYEBYE['bg']=CmdsButton['bg']='#FDC80B'
                    helping_hand['activebackground']=BYEBYE['activebackground']=CmdsButton['activebackground']='orange'
                    clist['fg']=cmd['fg']=enter_cmd_title['fg']=helping_hand['fg']=CmdsButton['fg']=BYEBYE['fg']='black'
                    updater()
                elif t=='True Darkness':
                    mw['bg'],C_UI,C_BG,C_HEAD,C_HIGH,C_FG='black','black','black','black','black','black'
                    console['bg']='black'
                    clist['bg']='black'
                    tw['bg']=enter_cmd_title['bg']='black'
                    cmd['bg']='black'
                    helping_hand['bg']=BYEBYE['bg']=CmdsButton['bg']='black'
                    helping_hand['activebackground']=BYEBYE['activebackground']=CmdsButton['activebackground']='black'
                    clist['fg']=cmd['fg']=enter_cmd_title['fg']=helping_hand['fg']=CmdsButton['fg']=BYEBYE['fg']='black'
                    updater()
                elif t=='Invisible':
                    mw['bg'],C_UI,C_BG,C_HEAD,C_HIGH,C_FG='white','white','white','white','white','white'
                    console['bg']='white'
                    clist['bg']='white'
                    tw['bg']=enter_cmd_title['bg']='white'
                    cmd['bg']='white'
                    helping_hand['bg']=BYEBYE['bg']=CmdsButton['bg']='white'
                    helping_hand['activebackground']=BYEBYE['activebackground']=CmdsButton['activebackground']='white'
                    clist['fg']=cmd['fg']=enter_cmd_title['fg']=helping_hand['fg']=CmdsButton['fg']=BYEBYE['fg']='white'
                    updater()
                if hackerman:
                    console['bg']='black'
                    clist['bg']='black'
                    clist['fg']='#08B31F'
            else:
                clist.insert(END,'Access Denied: You lack the necessary permission to access this command')
def opener(*zz):
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG,mw,sw,tw,cmd,console,clist,sculk,xsculk,DownArrow,UpArrow,LeftArrow,RightArrow,Err,cmd,enter_cmd_title,helping_hand,CmdsButton,BYEBYE
    ercond=0
    NEWFILE=TheOnlyTkinterVariableInThisEntireCode.get()
    existance=0
    try:
        flocation=file.get().replace('/','\\')
        if file.get()[-3:]!='csv':
            ercond=1
        fh=open(flocation,'r+',newline='')
        if NEWFILE:
            fh.close()
            if not(ercond):
                existance=1
                raise FileNotFoundError
    except FileNotFoundError:
        if NEWFILE:
            if existance:
                try:
                    i=1
                    while True:
                        a=flocation[:-4]+f'({i})'+flocation[-4:]
                        fh=open(a,'r+',newline='')
                        fh.close()
                        i+=1
                except FileNotFoundError:
                    fh=open(a,'w+',newline='')
            else:
                a=flocation
                fh=open(flocation,'w+',newline='')
            fh.write('Head1,Head2\nCell1,Cell2')
            fh.close()
            file.delete(0,END)
            file.insert(0,a)
            newfile.deselect()
            opener(1)
        else:
            Err['text']='File Not Found'
            Err.grid(row=1,column=0,pady=2,padx=1)
            sw.geometry('600x80')
    else:
        if ercond:
            Err['text']='File Extension Should Be .csv'
            Err.grid(row=1,column=0,pady=2,padx=1)
            fh.close()
            sw.geometry('650x80')
        else:
            write=csv.writer(fh,delimiter=delim)
            read=list(csv.reader(fh,delimiter=delim))
            sw.destroy()
            mw=Tk(className=' '+flocation[flocation.rindex('\\'):flocation.rindex('.csv')]+'.csv')
            mw['bg']='black'
            tw=Tk(className=' Command Window')
            tw.geometry('650x100')
            tw['bg']='light green'
            mw.resizable(False,False)
            tw.resizable(False,False)
            enter_cmd_title=Label(tw,text='Enter a command:',font=('Milker',16,'underline'),bg='light green')
            enter_cmd_title.grid(row=0,column=0,pady=2,padx=5)
            cmd=Entry(tw,width=30,font=('Times New Roman',16))
            cmd.bind('<Return>',Executor)
            #cmd.bind('<)>',lambda x: cmd.insert(END,'('),add='+')
            cmd.grid(row=0,column=1,pady=2)
            helping_hand=Button(tw,text='Help',command=helper,font=('Calibri',15))
            helping_hand.grid(pady=2,column=0,row=1)
            BYEBYE=Button(tw,text='Exit',command=closer,font=('Calibri',15))
            BYEBYE.grid(pady=2,column=1,row=1)
            CmdsButton=Button(tw,text='Execute',command=Executor,font=('Calibri',15))
            CmdsButton.grid(pady=2,column=3,row=0,padx=3)
            UpArrow=Button(mw,text='/\\',font=('Milker',16),bg=C_UI,width=3,command=fly,fg=C_FG)
            DownArrow=Button(mw,text='\\/',font=('Milker',16),bg=C_UI,width=3,command=drown,fg=C_FG)
            LeftArrow=Button(mw,text='<',font=('Milker',16),bg=C_UI,width=3,command=rarefaction,fg=C_FG)
            RightArrow=Button(mw,text='>',font=('Milker',16),bg=C_UI,width=3,command=compression,fg=C_FG)
            updater()
            console=Tk(className=' Console')
            sculk=Scrollbar(console)
            xsculk=Scrollbar(console,orient='horizontal')
            sculk.pack(side=RIGHT,fill=Y)
            xsculk.pack(side=BOTTOM,fill=X)
            clist=Listbox(console,bg=C_BG,fg='black',font=('Times New Roman',14),width=91,yscrollcommand=sculk.set,xscrollcommand=xsculk.set)
            clist.insert(END,'This is a scrollable Console.')
            sculk['command']=clist.yview
            xsculk['command']=clist.xview
            clist.pack(fill=BOTH,expand=True)
            #console.geometry('600x200')
def drown():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    srow+=yScrollAmount
    updater()
def fly():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    srow-=yScrollAmount
    updater()
def compression():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    scolumn+=xScrollAmount
    updater()
def rarefaction():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    scolumn-=xScrollAmount
    updater()
def helper():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    hallo=Tk(className=' hallo')
    hallo['bg']=C_BG
    skull=Scrollbar(hallo)
    xskull=Scrollbar(hallo,orient='horizontal')
    skull.pack(side=RIGHT,fill=Y)
    xskull.pack(side=BOTTOM,fill=X)
    hlist=Listbox(hallo,bg=C_BG,fg=C_FG,font=('Times New Roman',14),width=91,yscrollcommand=skull.set,xscrollcommand=xskull.set)
    skull['command']=hlist.yview
    xskull['command']=hlist.xview
    hlist.pack(fill=BOTH,expand=True)
    a="""This is a scrollable guide:
(Please keep in mind python convention for writing literals of all datatypes and arguments while writing commands and case-sestivity)

SOME PRIOR INFORMATION-
1) Column headers are not considered as cells or entries while row headers are.
2) Tables where number of rows exceed 23 or number of columns exceed 8 will become scrollable via buttons in respective direction.
3) All indexing starts from 1, however 0 may be used to refer to row headers
4) New File Checkbox creates a file slightly different from provided name when file with that name already exists.

COMMANDS-
1) cprint(<prompt>)- Prints <prompt> in the console
eg.- cprint('Hello')

2)count(<prompt>)- rows/columns/nothing may be written into prompt
a)count()- cprints the total number of entries in the file.
eg-count()

b)count(rows)- cprints the total number of rows in the file.
eg.-count(rows)

c)count(columns)- cprint the total number of columns in the file.
eg.-count(columns)

3)edit(<row>,<column>,<entry>)- replaces the entry at the specified row and column with <entry>
eg- edit(1,1,'Hello')
    edit(4,3,12)
    
4)add(<prompt>, [,<position> [,<value>]])- add a row or column at a specified position(default is last) with a specified common value(optional)
a)add(row)- adds row at end
eg. add(row)

b)add(row,<position>)- adds a row at given position <position>
eg.-add(row,2)

c)add(row,<position>,<value>)- adds a row at given position <position> with a common value <value>
eg.-add(row,3,'Hi')
    add(row,5,9)
    
d)add(column)- adds column at end
eg.-add(column)

e)add(column,<position>)- adds a column at given position <position>
eg.-add(column,2)

f)add(column,<position>,<value>)- adds a column at given position <position> with a common value <value>
eg.-add(column,3,'Hi')
    add(column,5,9)

5)delete(<prompt>,<number>)- delete a row or column at a specified position
a)delete(row,<number>)- deletes the row at position <number>
eg-delete(row,2)

b)delete(column,<number>)- deletes the column at position <number>
eg.-delete(column,3)

6)refresh()- updates and refreshes the table, resetting modifications like highlight and show (takes no arguments)
eg.-refresh()

7)ERASE()- asks confirmation and erases the table, leaving only 2 blank entries in its place (takes no arguments)
eg.-ERASE()

8)view(<row>,<column>)- cprints the value of the entry at row <row> and column <column>
eg.-view(2,1)
    view(0,2)

9)highlight(<value>)- highlights every entry with specified value
eg.-highlight('hello')
    highlight('123')
Refresh to return to original state

10)SUM(<cell 1 row>,<cell 1 column>,<cell 2 row>,<cell 2 column>)-Finds the sum of all entries in box formed by the rectangle created by taking the entries at specified positions as opposite corners.
IMPORTANT- all entries must be numeric in the specified range.
eg.-SUM(1,1,2,3)
    SUM(5,5,6,2)
    
11)evaluate(<prompt>)- evaluate takes <prompt> and performs the necessary calculations before cprinting the result
It takes individual cell coordinates inside <prompt> in square brackets in the form [<row>,<column>] and gets the number from that cell for operations
Regular numbers may also be used.
IMPORTANT- ensure all data fetched from cell coordinates is numeric
eg.-evaluate(1/[1,2])
    evaluate(2+[1,4]/5-[3,2]+[1,1])
    evaluate(-[7,8]*[0,1])

12)box(<many arguments>)- box has a parameter called multiple that can be set to 4 values - False,True,row,column (Default is False)
a)box(<cell 1 row>,<cell 1 column>,<cell 2 row>,<cell 2 column>)- multiple is False here
Highlights all entries in box formed by the rectangle created by taking the entries at specified positions as opposite corners
(to highlight a single entry, one may write the cell coordinates of the entry twice)
eg.-box(1,1,2,3)
    box(1,2,2,1)
    box(3,3,5,5)
    box(2,1,2,1)

b)box(<prompts>,multiple=True)- multiple is set to True here
Highlights individual cells/entries whose coordinates are mentioned
<prompts> must be in the form of <cell 1 row>,<cell 1 column>,<cell 2 row>,<cell 2 column>,<cell 3 row>,<cell 3 column>...
(To highlight a single entry, one may also write the cell coordinates of that entry here)
eg.-box(1,1,2,3,2,1,5,4,multiple=True)
    box(1,1,multiple=True)
    box(3,2,2,2,1,1,8,7,multiple=True)

c)box(<row number>,multiple=row)- multiple is set to row here
highlights the row whose row number is given
eg.-box(1,multiple=row)
    box(2,multiple=row)

d)box(<row number>,multiple=column)- multiple is set to column here
highlights the column whose column number is given
eg.-box(1,multiple=column)
    box(2,multiple=column)

Refresh to return to original state

13)show(<many arguments>)- show has 2 conditions highlight and find_specific which are set to False by default
Broadly highlight dictates whether only satisfying rows/columns fill be shown and rest hidden or all rows/columns shown but satisfying rows/columns highlighted
find_specific dictates whether a row satisfying the conditions given should be found or all columns with given column headers should be found.
a)show(<prompts>)- Both highlight and find_specific are False here
column headers must be input here and only those columns will be shown. Rest all columns will be hidden.
eg.-show('Head1','Head3')
    show('Username','Address')

b)show(<prompts>,highlight=True)- Only find_specific is False here
column headers must be input here and only those columns will be highlighted. Rest all columns will still be visible but will be remain in their original state.
eg.-show('Head1','Head3',highlight=True)
    show('Username','Address',highlight=True)

c)show(<dictionary>,find_specific=True)- Only highlight is False here
put a dictionary in the form of {<row header1>:<value1>,<row header3>:<value3> ...} and all rows where <row Header n>'s value is <value n> will be showed, rest will be hidden.
IMPORTANT- for a row to be shown, all conditions specified in  <dictionary> must be satisfied by that row.
           so if <dictionary> is {'Head1':'Hello','Head2','hi','Head5','blue'}; then only those rows will be shown whose 'Head1' value is 'Hello', 'Head2' value is 'hi' and 'Head5' value is 'blue'
eg.-show({'Head1':3,'Head4':'hi'},find_specific=True)
    show({'username':'Andy'},find_specific=True)

d)show(<dictionary>,find_specific=True,highlight=True)- Both highlight and find_specific are True here
put a dictionary in the form of {<row header1>:<value1>,<row header3>:<value3> ...} and all rows where <row Header n>'s value is <value n> will be highlighted, rest will remain in their original state.
IMPORTANT- for a row to be highlighted, all conditions specified in  <dictionary> must be satisfied by that row.
           so if <dictionary> is {'Head1':'Hello','Head2','hi','Head5','blue'}; then only those rows will be highlighted whose 'Head1' value is 'Hello', 'Head2' value is 'hi' and 'Head5' value is 'blue'
eg.-show({'Head1':3,'Head4':'hi'},find_specific=True,highlight=True)
    show({'username':'Andy'},find_specific=True,highlight=True)

Refresh to return to original state

14)scroll(<many arguments>)- This command is useful only when table content exceeds viewing capacity.
It is used to either scroll to a particular row/column or adjust how many rows are scrolled by the scroll buttons.
scroll has a parameter called Set whose value can be 'Y','X' or None (Default is None)
a)scroll(row,<row number>)- Set's value is None here.
Scrolls to the point so that the row <row number> becomes visible
eg.-scroll(row,24)
    scroll(row,40)

b)scroll(column,<column number>)- Set's value is None here.
Scrolls to the point so that the column <column number> becomes visible
eg.-scroll(column,9)
    scroll(column,11)

c)scroll(<number>,Set='X')- Set's value is 'X' here
Sets the number of lines scrolled when clicking the down arrow to <number>
eg.-scroll(2,Set='X')
    scroll(4,Set='X')

d)scroll(<number>,Set='Y')- Set's value is 'Y' here
Sets the number of lines scrolled when clicking the down arrow to <number>
eg.-scroll(2,Set='Y')
    scroll(4,Set='Y')

14)delimit([<delimiter> [,change=True]])- View the delimiter or change it to <delimiter>.
The change parameter decides whether the new delimiter should be reflected in the file also. It can be True or False.(Default is False)
a)delimit()- cprints the current delimiter
eg.-delimit()

b)delimit(<delimiter>)- changes it so that the program now reads the delimiter as <delimiter> instead of the old delimiter
The value of change is False here
eg.-delimit(';')
    delimit(':')
    delimit('\\t')

c)delimit(<delimiter>,change=True)- Changes it so that not only the program now recognizes <delimiter> as the delimiter but also all instances of the old delimiter are now replaced with <delimiter> in the file.
The value of change is True here
eg.-delimit(';',change=True)
    delimit('\\t',change=True)
    delimit(':',change=True)

15)replace(<value>,<replacement>)- replaces all instances of <value> with <replacement>
eg.-replace('yello','hello')
    replace(2,1)
    replace('bad','good')

GENERAL UI AND INFORMATION-
1) Each entry is represented in the form of a cell in the table
2) For proper functioning of program, please ensure that all rows contain the same number of entries in the file.
3) For proper functioning of program, please also ensure that file has atleast 2 entries
4) Cells highlighted by blue are row headers
5) The first column displayed in blue with numbering are column headers
6) Right-Click an unhighlighted row or column header to highlight that row/column
7) Right-Click a highlighted row or column header to unhighlight that row/column
8) Right-Click the top-left most empty square (at intersection of row and column headers) to refresh table
9) Do not middle-click the top-left most empty square.
10)Cells can only display ~15 characters at once of that entry, however the data is still stored in full
11)Double-Click a cell to view its entire content in a separate window or use view()
12)When table exceeds scroll capacity, buttons will appear to scroll the list. These button's scroll distance can be set to any number using scroll()
13)Default delimiter is comma (',')
14)Triple Right-Click a cell to display its position in the console.
"""
    for i in a.split('\n'):
        hlist.insert(END,' '+i)
def Executor(*zz):
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    rows,columns,row,column='rows','columns','row','column'
    comad=cmd.get()
    if comad[:8]=='evaluate':
        cmds.evaluate(comad[9:-1])
    else:
        try:
            waste278323492=eval('cmds.'+str(comad))
        except AttributeError:
            clist.insert(END,f'Invalid command \'{comad}\'. Please choose a command from the command list.')
            clist.insert(END,f'COMMAND LIST- {cmds.cmdlist}')
        except NameError:
            clist.insert(END,'Please follow proper python convention for strings, integers and booleans as your input may have been considered an undefined variable')
def closer():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    tw.destroy()
    console.destroy()
    mw.destroy()
    fh.close()
def updater():
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    def headhigh(Indian_Space_Research_Organization,zz):
        global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
        if zz.widget['bg']==C_HEAD:
            unhigh=True
        if Indian_Space_Research_Organization:
            cmds.box(int(zz.widget['text']),multiple='row')
        else:
            cmds.box(tposedata[tdata.index(zz.widget)][1],multiple='column')
    UpArrow['bg']=C_UI
    UpArrow['fg']=C_FG
    DownArrow['bg']=C_UI
    DownArrow['fg']=C_FG
    LeftArrow['bg']=C_UI
    LeftArrow['fg']=C_FG
    RightArrow['bg']=C_UI
    RightArrow['fg']=C_FG
    for i in tdata:
        i.grid_forget()
    for i in tcolheads:
        i.grid_forget()
    wsate,tdata,tcolheads,tposedata=[],[],[],[]
    for i in read:
        wsate+=i
    wide=len(max(wsate,key=len))+1
    if wide>12:
        wide=12
    for i in range(len(read)):
        for j in range(len(read[i])):
            waste2=Label(mw,text=read[i][j],bg=C_BG,font=('Milker',16),width=wide,fg=C_FG)
            if i==0:
                waste2['bg']=C_UI
                waste2.bind('<Button-3>',lambda zz: headhigh(0,zz),add='+')
            waste2.bind('<Double-Button-1>',viewer)
            waste2.bind('<Double-Button-3>',finder)
            tdata.append(waste2)
            tposedata.append([i,j+1])
            if i==0 and 0<j+1-scolumn<=8:
                waste2.grid(row=i,column=j+1-scolumn,padx=1,pady=1)
                continue
            if i-1<srow or 0<=j<scolumn:
                continue
            if i-srow<=23 and 0<j+1-scolumn<=8:
                waste2.grid(row=i-srow,column=j+1-scolumn,padx=1,pady=1)
    if srow>0:
        if srow+23!=len(read):
            UpArrow.grid(row=i+1,column=1,pady=3)
            DownArrow.grid(row=i+1,column=2,pady=3)
        else:
            UpArrow.grid(row=i+1,column=1,pady=3)
            DownArrow.grid_forget()
    elif i>23:
        DownArrow.grid(row=i+1,column=2,pady=3)
        UpArrow.grid_forget()
    elif srow==0:
        if len(read)<=23:
            UpArrow.grid_forget()
            DownArrow.grid_forget()
    if scolumn>0:
        if scolumn+8!=len(max(read,key=len)):
            LeftArrow.grid(row=i+1,column=3,pady=3)
            RightArrow.grid(row=i+1,column=4,pady=3)
        else:
            LeftArrow.grid(row=i+1,column=3,pady=3)
            RightArrow.grid_forget()
    elif j>8:
        RightArrow.grid(row=i+1,column=4,pady=3)
        LeftArrow.grid_forget()
    elif scolumn==0:
        if len(max(read,key=len))<=8:
            LeftArrow.grid_forget()
            RightArrow.grid_forget()
    for i in range(len(read)):
        if i==0:
            waste4=Label(mw,text=' ',bg=C_UI,font=('Milker',16),width=3,fg=C_FG)
            waste4.bind('<Triple-Button-2>',the_reveal)
            waste4.bind('<Button-3>',lambda x: cmds.refresh())
            waste4.grid(row=i,column=0,padx=1,pady=1)
            continue
        if i-1<srow:
            continue
        waste3=Label(mw,text=i,bg=C_UI,font=('Milker',16),width=3,fg=C_FG)
        waste3.bind('<Button-3>',lambda zz: headhigh(1,zz))
        if i-srow<=23:
            waste3.grid(row=i-srow,column=0,padx=1,pady=1)
        tcolheads.append(waste3)
def the_reveal(zz):
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    if not(DEVCOND):
        clist.insert(END,'Developer options Enabled!')
        DEVCOND=True
    else:
        clist.insert(END,'Developer options Disabled!')
        DEVCOND=False
def viewer(zz):
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    newwin=Tk(className=' CELL')
    myguy=list(zz.widget['text'])
    n=0
    IMP=''
    for i in myguy:
        n+=1
        IMP+=i
        if n>=60 and i==' ':
            n=0
            IMP+='\n'
    Label(newwin,text=IMP,font=('Calibri',15)).pack(padx=1,pady=5)
def finder(zzz):
    global fh,write,read,wide,tdata,flocation,tcolheads,DEVCOND,tposedata,srow,scolumn,xScrollAmount,yScrollAmount,delim,unhigh,C_UI,C_BG,C_HIGH,C_HEAD,C_FG
    me=zzz.widget
    clist.insert(END,f'The position of this cell is {tposedata[tdata.index(me)]}')
wide=5
C_UI,C_BG,C_HIGH,C_HEAD,C_FG='light blue','white','yellow','#E3C565','black'
tdata=[]
tcolheads=[]
tposedata=[]
sw=Tk(className=' Filer')
sw['bg']=C_UI
sw.geometry('600x80')
sw.resizable(False,False)
Label(sw,text='Enter File Location:',font=('Milker',16,'underline'),bg=C_UI).grid(row=0,column=0,padx=5,pady=2)
file=Entry(sw,width=30,font=('Times New Roman',16))
file.bind('<Return>',opener)
file.grid(row=0,column=1,pady=2,columnspan=2)
Button(sw,text='Open',command=opener,font=('Calibri',15,'bold')).grid(pady=2,column=1,row=1)
Err=Label(sw,font=('Milker',16,'bold'),bg=C_UI)
DEVCOND=False
srow=scolumn=0
xScrollAmount=yScrollAmount=1
delim=','
unhigh=False
TheOnlyTkinterVariableInThisEntireCode=BooleanVar(sw,value=0)
newfile=Checkbutton(sw,variable=TheOnlyTkinterVariableInThisEntireCode,bg='light blue',activebackground='light blue',text='Create New File',font=('Times New Roman',12))
newfile.grid(pady=2,column=2,row=1)
sw.mainloop()
#f0f0f0 for windows is colour of plain window background or SystemButtonFace
#SystemWindow is default colour of listbox or white for windows

try:
    fh.close()
except NameError:
    pass
