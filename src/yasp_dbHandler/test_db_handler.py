
""" Unit Test for db_handler.py """
# example_usage.py
import sys
from db_handler import DbHandler

def db_init():
    """ Initialize DbHandler with the database file, database config, and field mapping config
    """
    db_handle = DbHandler("stocks.db", "db_config.json", "api_field_mapping.json")
    return db_handle

def db_add_entries(db_handle : DbHandler):
    """Test add entries

    Args:
        db_handle: instance of DbHandler
    """
    db_handle.add_isin("IE000S9YS762")

    # Retrieve all entries
    #all_entries = db_handle.get_all()
    #print("All entries:", all_entries)

# Set watchlist status
#db_handler.set_watchlist("US1234567890", True)

# Retrieve watchlist entries
#watchlist_entries = db_handler.get_watchlist()
#print("Watchlist entries:", watchlist_entries)

# Get a specific entry
#entry = db_handler.get_entry("US1234567890")
#print("Specific entry:", entry)

print ('### Start Test ###')
try:
    db = db_init()
except Exception as e:
    print('Error on database initialization: ', str(e))
    sys.exit(1)
try:
    db_add_entries(db)
except Exception as e:
    print('Error on insert isin: ', str(e))
    sys.exit(1)  
print('### Test done ###')
del db
