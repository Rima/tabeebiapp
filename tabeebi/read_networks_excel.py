import xlrd
from tabeebi.directory.models import Provider, Location

wb = xlrd.open_workbook('networks_excel/network1.xls')

wb.sheet_names()

for sh in wb.sheets():
    for rownum in range(6,sh.nrows):
        row_values = sh.row_values(rownum)

        name = row_values[0]
        address = row_values[1]
        pobox = row_values[2]
        telephone = row_values[3]
        fax = row_values[4]


        Location(  )

        print ">>>>>>>>>> "
        print  ",".join( [name , address,str(pobox),str(telephone), str(fax)] )