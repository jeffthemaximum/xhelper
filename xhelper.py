import gspread
import requests
import bs4
import pudb
from oauth2client.service_account import ServiceAccountCredentials

class Scraper:
    def __init__(self, url):
        self.url = url
        self.soup = self.cook_soup(self.url)

    def cook_soup(self, link):
        """
        takes a link as a string
        returns a bs soup object
        """
        response = requests.get(self.url)
        return bs4.BeautifulSoup(response.text)

class Helpers:

    @classmethod
    def get_all_column_vals_as_row(cls, sheet, col_num):
        # get just elements at col_num index position
        col_as_list = [el[col_num] for el in sheet.all_vals]
        col_as_list.pop(0)
        return col_as_list

    @classmethod
    def get_column_number(cls, sheet, column_keyword):
        '''
        takes a sheet object
        and a column keyword as string, such as 'email'
        and returns the column number who's column title contains that string
        else none if no column contains that string
        '''
        column_keyword = column_keyword.lower()
        first_row_as_list = sheet.all_vals[0]
        row_lowered = [cell.lower() for cell in first_row_as_list]
        return row_lowered.index(column_keyword) if column_keyword in row_lowered else None


class Xhelper:
    def __init__(self, json_file_name, spread_sheet_name):
        self.json_file_name = json_file_name
        self.spread_sheet_name = spread_sheet_name
        self.errors = []
        self.gc = self.authorize()
        self.spread_sheet = self.open_spread_sheet()
        self.worksheets_list = self.get_all_worksheet_names()
        print "done xhelper init"

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
        self.email_col_num = Helpers.get_column_number(self.sheet, 'email')
        print('77')
        self.url_col_num = Helpers.get_column_number(self.sheet, 'pageUrl')
        self.author_col_num = Helpers.get_column_number(self.sheet, 'author')
        print('80')
        self.all_emails = Helpers.get_all_column_vals_as_row(self.sheet, self.email_col_num)
        print('82')
        self.all_urls = Helpers.get_all_column_vals_as_row(self.sheet, self.url_col_num)
        self.all_authors = Helpers.get_all_column_vals_as_row(self.sheet, self.author_col_num)
        print('85')
        print "done wiley init"

    def get_first_names(self):
        for url in self.all_urls:
            pu.db
            scraped = Scraper(url)
            authors_as_list = scraped.soup.find("ol", {"id": "authors"}).find_all('li')
            authors_as_text_list = [el.text for el in authors_as_list]
            for author in authors_as_text_list:
                if '*' in author:
                    return author
            error = "ERROR WITH WILEY. COULDN'T FIND FIRST NAME FOR " + url
            print(error)
            self.xhelper.errors.append(error)
            return ''

    def wiley(self):
        # return and print error if 
        if self.email_col_num == None:
            error = "ERROR WITH WILEY. MAKE SURE THERE'S A COLUMN NAMED 'email'"
            print(error)
            self.xhelper.errors.append(error)
            return None
        # else get list of all emails
        else:
            # TODO get first name
            first_name = self.get_first_name()
            # TODO get email
            print self.all_emails

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
