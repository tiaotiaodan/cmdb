import xlrd
import mysql_tools
def insertFromExcel( excelPath ):
    book = xlrd.open_workbook(excelPath )
    sheet = book.sheet_by_index(0)
    rowsnumber = sheet.nrows
    colsnumber = sheet.ncols
    for i in range(0, rowsnumber):
        value = []
        for j in range(0, colsnumber):
            value.append(sheet.cell(i, j).value)
        if i != 0:
            sql = 'replace into servers (server_name, server_ip, server_port, server_user, server_passwd) VALUES( %s, %s, %s, %s, %s);'
            mysql_tools.updateByParameters( sql, (value[0], value[1], value[2], value[3], value[4]) )

if __name__ == "__main__":
    insertFromExcel('/tmp/servers.xlsx')