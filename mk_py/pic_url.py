import requests
import xlrd

#读取excl文件的url地址并下载图片
wb = xlrd.open_workbook("url.xlsx","r")  #以只读方式读取列表数据
sh = wb.sheet_by_index(0)  #获取表格的第一张表内容
cv = sh.col_values(1)   #获取整列的值
i = 0
while i < len(cv):
    print(cv[i])
    re = requests.get(cv[i]).content  #下载图片
    with open("./picture/"+str(i)+".jpg","wb") as f:
        f.write(re)
    i += 1






