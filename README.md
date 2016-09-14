# Clone the repo

# Install virtualenv (if you haven't yet)

- from the root of the repository, enter this in your terminal

```
pip install virtualenv
```

# make a new virtualenv (if you haven't yet)

- from the root of the repository, enter this in your terminal

```
virtualenv env
```

# activate the virtual environment

- from the root of the repository, enter this in your terminal

```
source env/bin/activate
```

# Install the dependencies (if you haven't yet)

- from the root of the repository, enter this in your terminal

```
pip install -r requirements.txt
```

# Setup your spreadsheet

- Make a Google Spreadsheet
- Make sure you have a sheet with wiley in it's sheet name
- Share your Google Spreadsheet with 123114053576-compute@developer.gserviceaccount.com
- Make a column titled pageUrl on the 'wiley' sheet
- Fill your Wiley url's in that column
- Change `spread_sheet_name` on line 389 of `xhelper.py` and save
- You're done. Enjoy the magic. Or maybe not, cuz it might not work, too.

# To run the Xhelper

- from the root of the repository, enter this in your terminal

```
python xhelper.py
```
