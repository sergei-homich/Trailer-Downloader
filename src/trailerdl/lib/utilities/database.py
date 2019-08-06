import os
import sqlite3

class Database:
    # Initialize
    def __init__(self):
        self.db = os.path.split(os.path.abspath(__file__))[0]+'/../../db.sqlite'
        if not os.path.exists(self.db):
            self.create()

    # Create
    def create(self):
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute('CREATE TABLE downloads (title TEXT, year INTEGER, type TEXT, extra TEXT, original_name TEXT, filename TEXT, directory TEXT, scraper TEXT)')
        db.commit()
        db.close()

    # Store
    def store(self, title, year, type, extra, original_name, filename, directory, scraper):
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute('INSERT INTO downloads (title, year, type, extra, original_name, filename, directory, scraper) VALUES ("'+title.replace('"', '')+'", '+str(year)+', "'+type+'", "'+extra+'", "'+original_name.replace('"', '')+'", "'+filename[:-4].replace('"', '')+'", "'+directory.replace('"', '')+'", "'+scraper+'")')
        db.commit()
        db.close()

    # Delete
    def delete(self, title, year, type, extra, original_name, directory, scraper):
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute('DELETE FROM downloads WHERE (title="'+title.replace('"', '')+'" AND year='+str(year)+' AND type="'+type+'" AND extra="'+extra+'" AND original_name="'+original_name.replace('"', '')+'" AND directory="'+directory.replace('"', '')+'" AND scraper="'+scraper+'")')
        db.commit()
        db.close()

    # Search
    def search(self, title, year, type, extra, original_name, directory, scraper):
        db = sqlite3.connect(self.db)
        c = db.cursor()
        c.execute('SELECT * FROM downloads WHERE (title="'+title.replace('"', '')+'" AND year='+str(year)+' AND type="'+type+'" AND extra="'+extra+'" AND original_name="'+original_name.replace('"', '')+'" AND directory="'+directory.replace('"', '')+'" AND scraper="'+scraper+'")')
        response = c.fetchone()
        db.close()

        if response is not None and os.path.exists(directory):
            matched = False
            for file in os.listdir(directory):
                if file.strip()[:-4].replace('"', '') == response[5]:
                    matched = True
            if not matched:
                self.delete(title, year, type, extra, original_name, directory, scraper)
            return matched
        else:
            return False