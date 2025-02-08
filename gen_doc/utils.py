import qrcode


class GenDoc:
    def __init__(self, id=None, docx=None):
        self.id = id
        self.docx = docx

    def display_info(self):
        return print("GenDoc class info")

    def gen_qrcode(self):
        return print("QRCODE")

    def gen_docx(self):
        return print(self.docx)

    def gen_pdf(self):
        return print(self.docx)


my_doc = GenDoc(docx='HH')
my_doc.display_info()
my_doc.gen_qrcode()
my_doc.gen_docx()
my_doc.gen_pdf()


# EXCELdan ma'lumotlarni o'qish
# def extract_excel(self):
#     xlsx = self.report_obj.xlsx
#     wb = load_workbook(filename=xlsx, read_only=True, data_only=True)
#     ws = wb['График']
#
#     # Cheklangan qatordan o'qish
#     data = []
#     obj = {
#         "id": None,
#         "date": None,
#         "total_payment": None,
#         "principal_balance": None,
#         "interest_payment": None,
#         "principal_payment": None,
#     }
#
#     for row in ws.iter_rows(min_row=9, max_row=100, min_col=1, max_col=6, values_only=True):
#         if obj["date"] != None:
#             obj = {
#                 "id": row[0],
#                 "date": row[1].strftime('%d.%m.%Y') if type(row[1]) is datetime else row[1],
#                 "total_payment": '{:,.2f}'.format(row[2]) if type(row[2]) is float else row[2],
#                 "principal_balance": '{:,.2f}'.format(row[3]),
#                 "interest_payment": '{:,.2f}'.format(row[4]),
#                 "principal_payment": '{:,.2f}'.format(row[5]),
#             }
#             data.append(obj)
#         elif obj["date"] is None:
#             print(obj)
#             # Pustoy polyalarni o'tkazib yuboramiz
#         elif obj["date"] == 'JAMI':
#             obj = {
#                 "id": "",
#                 "date": row[1].strftime('%d.%m.%Y') if type(row[1]) is datetime else row[1],
#                 "total_payment": '{:,.2f}'.format(row[2]) if type(row[2]) is float else row[2],
#                 "principal_balance": '{:,.2f}'.format(row[3]) if type(row[2]) is float else row[3],
#                 "interest_payment": '{:,.2f}'.format(row[4]) if type(row[4]) is float else row[4],
#                 "principal_payment": '{:,.2f}'.format(row[5]) if type(row[5]) is float else row[5],
#             }
#             data.append(obj)
#             break
#     wb.close()
#     return data
