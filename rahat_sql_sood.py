import pyodbc

server = "rahat-database.database.windows.net,1433"
database = 'RahatDatabase'
username = 'akash@rahat-database'
password = 'Yashikens.1'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = cnxn.cursor()

def add_new_victim(id, number, lat_val, long_val, food, water, med, shelter, info, status):
    sql_vq = "INSERT INTO Victims (VictimID, Number, Latitude, Longitude, Food, Water, Medicine, Shelter, ExtraInformation, Status) VALUES ("+id+", "+number+", "+lat_val+", "+long_val+", "+food+", "+water+", "+med+", "+shelter+", "+info+", "+status+");"
    cursor.execute(sql_vq)
    cnxn.commit()

def show_all_victims():
    cursor.execute("SELECT * FROM Victims;")
    row = cursor.fetchone()
    while row:
        for attribute in row:
            print(attribute, end=" ")
        print()
        row = cursor.fetchone()

def dashboard_show_all_victims():
    cursor.execute("SELECT * FROM Victims;")
    rows = []
    row = cursor.fetchone()
    while row:
        rows.append(row)
        row = cursor.fetchone()
    return rows
    
def add_new_help(id, number, lat_val, long_val, info):
    sql_hq = "INSERT INTO Help (HelpID, Number, Latitude, Longitude, ExtraInformation) VALUES ("+id+", "+number+", "+lat_val+", "+long_val+", "+info+");"
    cursor.execute(sql_hq)
    cnxn.commit()

def show_all_help():
    cursor.execute("SELECT * FROM Help;")
    row = cursor.fetchone()
    while row:
        for attribute in row:
            print(attribute, end=" ")
        print()
        row = cursor.fetchone()

def add_new_shelters(id, number, lat_val, long_val, people, info):
    sql_hq = "INSERT INTO Shelters (ShelterID, Latitude, Longitude, People, ExtraInformation) VALUES ("+id+", "+number+", "+lat_val+", "+long_val+", "+people+", "+info+");"
    cursor.execute(sql_hq)
    cnxn.commit()

def show_all_shelters():
    cursor.execute("SELECT * FROM Shelters;")
    row = cursor.fetchone()
    while row:
        for attribute in row:
            print(attribute, end=" ")
        print()
        row = cursor.fetchone()

def dashboard_show_all_shelters():
    cursor.execute("SELECT * FROM Shelters;")
    rows = []
    row = cursor.fetchone()
    while row:
        rows.append(row)
        row = cursor.fetchone()
    return rows