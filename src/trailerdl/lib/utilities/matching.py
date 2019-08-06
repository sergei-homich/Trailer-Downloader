import html.parser
import os
import unicodedata

class Matching:
    # Find Existing
    @staticmethod
    def find(formatting, extra, title, year, directory):
        count = 1
        limit = 50
        names = []
        while count <= limit:
            if year:
                names.append(formatting.replace('%title%', title.replace(':', '-')).replace('%year%', str(year)).replace(' %number%', '%number%').replace('%number%', (' '+str(count) if count > 1 else '')).replace('()', '').replace('  ', ' ').strip())
            else:
                names.append(formatting.replace('%title%', title.replace(':', '-')).replace('%year%', '').replace(' %number%', '%number%').replace('%number%', (' '+str(count) if count > 1 else '')).replace('()', '').replace('  ', ' ').strip())
            count += 1
        results = []
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.strip()[:-4] in names:
                    results.append(file)
        return results

    # Get Filename
    @staticmethod
    def filename(formatting, extra, title, year, downloaded):
        count = 1
        response = None
        while response is None or response in downloaded:
            if year:
                response = formatting[extra].replace('%title%', title.replace(':', '-')).replace('%year%', str(year)).replace(' %number%', '%number%').replace('%number%', (' '+str(count) if count > 1 else '')).replace('()', '').replace('  ', ' ').strip()+'.mp4'
            else:
                response = formatting[extra].replace('%title%', title.replace(':', '-')).replace('%year%', '').replace(' %number%', '%number%').replace('%number%', (' '+str(count) if count > 1 else '')).replace('()', '').replace('  ', ' ').strip()+'.mp4'
            count += 1
        return response

    # Remove Special Characters
    @staticmethod
    def removeSpecialChars(query):
        return ''.join([ch for ch in query if ch.isalnum() or ch.isspace()])

    # Normalize
    @staticmethod
    def normalize(query):
        return unicodedata.normalize('NFKD', Matching.removeSpecialChars(html.unescape(query.strip())).replace('/', '').replace('\\', '').replace('-', '').replace(':', '').replace('*', '').replace('?', '').replace(''', '').replace(''', '').replace('<', '').replace('>', '').replace('|', '').replace('.', '').replace('+', '').replace(' ', '').lower()).encode('ASCII', 'ignore')

    # Match Title
    @staticmethod
    def title(a, b):
        return str(Matching.normalize(a)) == str(Matching.normalize(b))

    # Match Year
    @staticmethod
    def year(a, b):
        return str(a).lower() in str(b).lower() if a else True