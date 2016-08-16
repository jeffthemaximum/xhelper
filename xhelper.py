import gspread
import pudb
from oauth2client.service_account import ServiceAccountCredentials

class Helpers:

    @classmethod
    def find_email(cls, worksheets_list):
        row_lowered = [cell.lower() for cell in worksheets_list]
        return row_lowered.index('email') if 'email' in row_lowered else None

    @classmethod
    def get_all_column_vals_as_row(cls, sheet, col_num):
        # get just elements at col_num index position
        return [el[col_num] for el in sheet.all_vals]


class Xhelper:
    def __init__(self, json_file_name, spread_sheet_name):
        self.json_file_name = json_file_name
        self.spread_sheet_name = spread_sheet_name
        self.errors = []
        self.gc = self.authorize()
        self.spread_sheet = self.open_spread_sheet()
        self.worksheets_list = self.get_all_worksheet_names()

    def get_all_worksheet_names(self):
        return self.spread_sheet.worksheets()

    def open_spread_sheet(self):
        return self.gc.open(self.spread_sheet_name)

    def authorize(self):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_file_name, scope)
        return gspread.authorize(credentials)


class Sheet:
    def __init__(self, xhelper, sheet):
        self.xhelper = xhelper
        self.sheet = sheet
        self.all_vals = sheet.get_all_values()


class Wiley:
    def __init__(self, xhelper, sheet):
        self.xhelper = xhelper
        self.sheet = Sheet(self.xhelper, sheet)
        self.email_col_num = self.get_email_column_number()

    def get_email_column_number(self):
        # get first row
        first_row_as_list = self.sheet.all_vals[0]
        # get column # of email
        return Helpers.find_email(first_row_as_list)

    def wiley(self):
        # return and print error if 
        if self.email_col_num == None:
            error = "ERROR WITH WILEY. MAKE SURE THERE'S A COLUMN NAMED 'email'"
            print(error)
            self.xhelper.errors.append(error)
            return None
        # else get list of all emails
        else:
            all_emails = Helpers.get_all_column_vals_as_row(self.sheet, self.email_col_num)
            print all_emails
            

    def run(self):
        return self.wiley()



def main():
    xhelper = Xhelper(json_file_name = 'microryza-jeff-e07a11b3dbc9.json', spread_sheet_name = 'Copy of Herpetology abstracts')
    for sheet in xhelper.worksheets_list:
        if 'wiley' in sheet.title.lower():
            wiley = Wiley(xhelper = xhelper, sheet = sheet)
            print wiley.run()

if __name__ == '__main__':
    main()
