import xlrd
from tabeebi.directory.models import FlatTable

#read and throw in the flat table

network_files = {
    'DubaiCare-N2.xls' : 'Dubai Care',
    'DubaiCare-N1.xls' : 'Dubai Care',
    'DubaiCare-N3.xls' : 'Dubai Care',
    'DubaiCare-N4.xls' : 'Dubai Care',
    'MedNet-Gold.xls' : 'MedNet',
    'MedNet-Green.xls' : 'MedNet',
    'MedNet-Silver-Premium.xls' : 'MedNet',
    'NextCare-General.xls' : 'Next Care',
    'NextCare-RN.xls' : 'Next Care',
    'NextCare-RN2.xls' : 'Next Care',
    'Now-Health-Network.xls' : 'Now Health',
}


field_names = {
    'provider' : 'provider',
    'type' : 'type',
    'network' : 'network',
    'country' : 'country',
    'city' : 'city',
    'pobox' : 'pobox',
    'p.o.box' : 'pobox',
    'p.o. box' : 'pobox',
    'p.o box' : 'pobox',
    'telephone' : 'telephone',
    'tel' : 'telephone',
    'fax' : 'fax',
    'location' : 'location1',
    'location1' : 'location2',
    'location 1' : 'location2',
}


for network_file in network_files.keys():

    wb = xlrd.open_workbook('tabeebi/networks_excel/%s'%network_file)

    wb.sheet_names()

    for sh in wb.sheets():

        headers = sh.row_values(0)
        print headers
        index_headers = {}
        for index,header in enumerate(headers):
            index_headers.update({ index : field_names[header.lower().strip()] })


        for rownum in range(6,sh.nrows):
            row_values = sh.row_values(rownum)

            kwargs = { 'insurance_name' : network_files[network_file] }

            for cell_index,item in enumerate(row_values):
                kwargs.update({  index_headers[cell_index] : row_values[cell_index] })

            print kwargs

            ft = FlatTable( **kwargs )
            ft.save()
            print ">>>>>>>>>> "
