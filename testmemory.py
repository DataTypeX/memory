import subprocess
import re
import logging
import time
import os
logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
# logger（setLevel）
fh = logging.FileHandler(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + '.txt')
# 输出到文件
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

package='com.***.***#应用名称

def getmem(package):
    cmd = r'adb shell dumpsys meminfo '+package+' | findstr "TOTAL"'  # % apk_file
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    pr.wait()  # 等待
    out = pr.stdout.readlines()  # out = pr.stdout.read().decode("UTF-8")
    str_out=map(str,out)
    number=[]
    for i in str_out:
         number.append(int( re.findall('\d+', i)[0]))#正则匹配出字符串中的数字列表，按选择列表[0]的数字大写排序
    return number[0]

def getCpu(package):
    li = os.popen("adb shell top -m 100 -n 1").readlines()
    name = package
    for line in li:
        if re.findall(name,line):
            cuplist = line.split(" ")
            if cuplist[-1].strip() == package:
                while '' in cuplist:       # 将元素删除
                    cuplist.remove('')
                cpu_apk=float(cuplist[2].strip('%'))
                return str(cpu_apk)+'%'  #去掉百分号，返回一个float

while True:
    try:
        mem = getmem(package)
    except :
        mem ='error'
    try:
        cpu = getCpu(package)
    except:
        cpu ='error'
    logger.info("mem: " + str(mem) + ' KB，cpu：' + str(cpu))
    time.sleep(1)
