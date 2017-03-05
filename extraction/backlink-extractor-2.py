import urllib
import json as simplejson
import sys
import time
import io
import os

"""
the wikipedia api url that is queried.
Note: This can change and therefore should be updated to the latest url 
%s defines the language eg. en for english, fr for french etc.
"""
api_url = 'https://%s.wikipedia.org/w/api.php'

def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode.
    Borrowed from pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])

def _run_query(args, language, retry=5, wait=5):
    """
    takes arguments and optional language argument and runs query on server
    if a socket error occurs, wait the specified seconds of time and retry for the specified number of times
    """
    url = api_url % (language)
    data = _unicode_urlencode(args)
    while True:
        try:
            search_results = urllib.urlopen(url, data=data)
            json = simplejson.loads(search_results.read())
        except Exception:
            if not retry:
                json = None
                break
            retry -= 1
            time.sleep(wait)
        else:
            break
    return json

"""
method used to query for raw article text
@param name:
    the name/title of the article
@param lang:
    the language being used for the article title and text
"""
def query_text_raw(title, language='en'):
    """
    action=query
    Fetches the article in wikimarkup form
    """
    query_args = {
        'action': 'query',
        'titles': title,
        'explaintext': True,
        'prop': 'extracts',
        'format': 'json',
        'redirects': ''
    }
    json = _run_query(query_args, language)
    if not json == None:
        for page_id in json['query']['pages']:
            if page_id != '-1' and 'missing' not in json['query']['pages'][page_id]:
                response = {
                    'text': json['query']['pages'][page_id]['extract']
                }
                return response
    return None

"""
method to generate a list of the languages queried from wikipedia
"""
def create_lang_list(filename):
    f = open(filename, "r")
    lang = f.readline().strip("\r\n").split("\t")
    f.close()
    return lang

"""
method to write given text to the file defined by filename
also takes care of creating a directory if it doesn't exist 
@param filename:
    string containing the name of the file where data needs to be stored
@param text:
    string containing the data that needs to be written to file
@param language:
    string denoting the language required to save the file in the appropriate language folder
@param datatype:
    string denoting the directory where the file needs to be saved
"""



"""
method responsible for reading the file one line at a time 
and then querying for the raw article data and backlinks linking to that data

Note: it is done this way because there is no way to maintain state of the file in an efficient manner 
without looping through the entire file every time

@param filename:
    string denoting the name of the file that needs to be read line by line
@param languages:
    a list of languages as retrieved from wikipedia
"""
def read_file_by_line(filename, languages):
    for index, language in enumerate(languages):
        filepath = "data/backlinks." + language
        if os.path.isfile(filepath):
            continue 
        d = os.path.dirname(filepath)
        if not os.path.exists(d):
            os.makedirs(d)
        output_f = open(filepath, "w")
        output_f.write(language)
        output_f.write("\n")

        f = open(filename, "r")
        for i, line in enumerate(f):
            if not i == 0:
                titles = line.strip("\r\n").split("\t")
                if not titles[index] == "":
                    backlink_resp = query_redirects(titles[index], language)
                    num_backlinks = 1
                    if not backlink_resp == None:
                        num_backlinks = num_backlinks + len(backlink_resp['backlinks'].split("\n"))
                    output_f.write(str(num_backlinks))
                    output_f.write("\t")
                    output_f.write(titles[index])

                    if not backlink_resp == None:
                        output_f.write("\t")
                        output_f.write(backlink_resp['backlinks'].replace("\n", "\t").encode('utf-8'))
                    output_f.write("\n")
                else:
                    output_f.write("0\n")

        f.close()
        output_f.close()


"""
method used to query for redirect backlinks
@param name:
    the name/title of the article for which backlinks are requested
@param lang:
    the language being used for the article title
"""
def query_redirects(name, lang):
    query_args = {
        'action': 'query',
        'bltitle': name,
        'list': 'backlinks',
        'blfilterredir': 'redirects',
        'format': 'json',
        'bllimit': 500
    }

    json = _run_query(query_args, lang)
    if not json == None:
        backlinks = []
        for page_id in json['query']['backlinks']:
            backlinks.append(page_id['title'])
        
        if backlinks:
            response = {
                'backlinks' : "\n".join(backlinks)
            }    
            return response
    return None

"""
method used to write backlinks to the file
@param filename:
    the name/title of the article for which backlinks are being written
@param language:
    the language being used for the article title
@param text:
    the data that needs to be written to the file
"""
def create_or_append_backlink(language, filename, text):
    filepath = "data/backlinks/%s/%s.txt" %(language, filename)
    d = os.path.dirname(filepath)

    if not os.path.exists(d):
        os.makedirs(d)

    f = open(filepath, "a")
    f.write(text.encode("utf-8"))
    f.close()



if __name__ == "__main__":
    filename = sys.argv[1]
    languages = create_lang_list(filename)
    read_file_by_line(filename, languages)

