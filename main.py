import csv
import xml.etree.cElementTree as ET


def convert_date(d):
    return d.replace('.', '-')


if __name__ == '__main__':
    COL_AMOUNT = 6
    COL_CURRENCY = 1
    COL_DATE = 2
    COL_REF = 3
    COL_DESC = 4
    COL_PARTY = 5

    in_file = 'un.csv'
    with open(in_file, newline='') as csvfile:
        un = csv.reader(csvfile, delimiter=';', quotechar='"')
        un = list(un)

        balance = un[1][COL_AMOUNT]

        root = ET.Element("FIDAVISTA", xmlns="http://www.bankasoc.lv/fidavista/fidavista0101.xsd")

        # header
        header = ET.SubElement(root, "Header")
        ET.SubElement(header, "From").text = "Unlimnt"

        statement = ET.SubElement(root, "Statement")
        ET.SubElement(statement, "StartDate").text = convert_date(un[1][COL_DATE])
        ET.SubElement(statement, "EndDate").text = convert_date(un[-1][COL_DATE])
        ET.SubElement(statement, "PrepDate").text = convert_date(un[-1][COL_DATE])

        account_set = ET.SubElement(statement, "AccountSet")
        ET.SubElement(account_set, "IBAN").text = un[2][0]
        ET.SubElement(account_set, "AccNo").text = un[2][0]


        for u in un[1:]:
            # new currency
            if u[4] == 'Opening balance':
                ccystmt = ET.SubElement(account_set, "CcyStmt")
                ET.SubElement(ccystmt, "Ccy").text = u[COL_CURRENCY]
                ET.SubElement(ccystmt, "OpenBal").text = u[COL_AMOUNT]
            elif u[4] == 'Closing balance':
                ET.SubElement(ccystmt, "CloseBal").text = u[COL_AMOUNT]
            else:
                trxset = ET.SubElement(ccystmt, "TrxSet")
                ET.SubElement(trxset, "RegDate").text = u[COL_DATE]
                ET.SubElement(trxset, "BankRef").text = u[COL_REF]
                ET.SubElement(trxset, "PmtInfo").text = u[COL_DESC]
                ET.SubElement(trxset, "Amt").text = u[COL_AMOUNT]

                CPartySet = ET.SubElement(trxset, "CPartySet")

                AccHolder = ET.SubElement(CPartySet, "AccHolder")
                ET.SubElement(AccHolder, "Name").text = u[COL_PARTY]

        tree = ET.ElementTree(root)
        tree.write("breakpoint-unlimnt-fidavista-2021.01.xml")

        print(un)
