'''
Author: yating.wang
Date: 2022-03-19 21:43:32
LastEditTime: 2022-03-20 11:55:59
LastEditors: yating.wang
Description: Vue2项目Vite改造脚本
'''
import os,fileinput
def vue2Vite(path):
  for filename in os.listdir(path):
    oldfilename=os.path.join(path,filename)
    fileArr=filename.split('.')
    if fileArr[-1]=='js':
      isJSX=False
      for line in fileinput.input(oldfilename,inplace = True):
        if "import" in line or "from" in line:
          if ".jsx\'" in line or '.jsx\"' in line:
            print(line.rstrip().replace('.jsx',''))
          elif ".js\'" in line or '.jsx\"' in line:
            print(line.rstrip().replace('.js',''))
          else:
            print(line.rstrip())
        else:
          print(line.rstrip())
        if not isJSX and ('/>' or '</') in line:
          isJSX=True
          pass
      if isJSX:
        newfilename=oldfilename+'x'
        os.rename(oldfilename,newfilename)
        print("文件%s重命名成功,新的文件名为%s" %(oldfilename, newfilename))
      print("文件%s修改完毕"%(oldfilename))
    elif fileArr[-1]=='vue':
      isJSX=False
      inScript=False
      for line in fileinput.input(oldfilename,inplace = True):
        if inScript:
          if not isJSX and "render" in line:
            isJSX=True
          if "</" in line and "script" in line:
            inScript=False
          if "import" in line or "from" in line:
            if ".jsx\'" in line or '.jsx\"' in line:
              line=line.rstrip().replace('.jsx','')
            elif ".js\'" in line or '.jsx\"' in line:
              line=line.rstrip().replace('.js','')
        elif "<script" in line:
          inScript=True
        print(line.rstrip())     
      if isJSX:
        for line in fileinput.input(oldfilename,inplace = True):
          if "<script" in line and "lang" not in line:
            print(line.rstrip().replace('<script','<script lang=\"jsx\"'))
          else:
            print(line.rstrip())
        print("文件%s修改完毕"%(oldfilename))
    elif fileArr[-1]==filename and os.path.isdir(oldfilename) and filename!="node_modules":
      newpath=oldfilename+'/'
      print("开始修改文件夹%s"%(newpath))
      vue2Vite(newpath)
# path指定开始改造的入口文件，例如: ./project_name/src/
path="./" 
vue2Vite(path)