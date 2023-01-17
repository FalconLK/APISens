from re import finditer
import codecs, os, ast, json, csv, shutil, hashlib, datetime, re, pickle, sys
import pandas as pd
from emoji import UNICODE_EMOJI
import matplotlib.pyplot as plt

sys.path.append('')
sys.path.append('..')

'''
Requirements
pip install langdetect
pip install emoji==1.7.0

'''


def getTime():
    return datetime.datetime.now()
def getDate():
    return datetime.date.today()
def getTimeString():
    current_time = getTime
    return current_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

def hashString(target_string):
    ''' Compute the SHA-256 hash of the string 'hello' '''
    hash_value = hashlib.sha256(target_string.encode('utf-8')).hexdigest()
    return hash_value


def readFile(file_path):
    with codecs.open(file_path, "r", encoding='utf-8') as file:
        return file.read()

def writeText(file_name, method, text):
    """
    write text to file
    method: 'a'-append, 'w'-overwrite
    """
    with open(file_name, method, encoding='utf-8') as f:
        f.write(text + '\n')

def convertStrToDict(file_cont):
    return ast.literal_eval(file_cont)

def convertDictToStr(src_dict):
    return json.dumps(src_dict)

def removeFileIfExists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
def camel_case_split(identifier):
    matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0).lower() for m in matches]

def getPickleData(pickle_load_path):
    """
    Load a pickle file as a Pandas dataframe object (usually dict).
    """
    obj = pd.read_pickle(pickle_load_path)
    return obj

def saveDictToPickle(target_dict, pickle_save_path):
    with open(pickle_save_path, 'wb') as handle:
        pickle.dump(target_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def saveDataFrameToPickle(target_object, pickle_save_path):
    """
    Save Pandas dataframe object as a pickle file.
    """
    df = pd.DataFrame(target_object)
    df.to_pickle(pickle_save_path)

def savePickleDataWithPD(dst_path, target_object, columns):
    """
    Save a dictionary with pandas dataframe object to a pickle file.
        target_dict = dict()
        target_dict['a'] = [1,2,3]
        savePickleDataWithPD('test.pkl', target_dict)
    """
    df = pd.DataFrame(data=target_object, columns=columns)
    df.to_pickle(dst_path)
    # df = df.append(target_object)

    # df.DataFrame(target_object).to_pickle(dst_path)
    # pd.DataFrame(target_object).to



def cleanPickleWithIndex(src_obj, index_list):
    """
    Cleaning a pickle object with a list of index.
    The indices from the list will be deleted but the existing indices still remain as they are.
    For example, [1, 2, 3, 4, 5, 6, 7] - [2, 3, 5, 6] = [1, 4, 7]
    """
    dst_obj = src_obj.drop(labels=index_list, axis=0)
    return dst_obj

def listIntersection(list_1, list_2):
    """
    Input: two lists
    Output: an intersected list
    """
    set1 = set(list_1)
    set2 = set(list_2)
    newList = list(set1.intersection(set2))
    print("Intersection of the lists is:", newList)
    return newList

def clearDirectory(folder):
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    else:
        os.makedirs(folder)

def csvReader(file_path):
    '''Read a csv file and return a list'''

    target_list = list()
    # with open(file_path, 'r', encoding='latin-1') as file:
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            target_list.append(row)

    '''
    Reader usage: 
    for idx, row in enumerate(reader):
        row[0]
    '''
    return target_list

def csvListWriter(file_path, target_list):
    ''' Open a file to write a list '''
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        # Write the rows of data to the CSV file
        writer.writerow(target_list)

def csvDictWriter(file_path, field_names, target_dict):
    ''' Open a file to write a dict '''
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        # Write the headers to the CSV file
        writer.writeheader()
        # Write the rows of data to the CSV file
        writer.writerow(target_dict)

def jsonWriteWithDict(file_path, target_dict):
    with open(file_path, "w") as outfile:
        json.dump(target_dict, outfile, indent=4)

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" # emoticons
                           u"\U0001F300-\U0001F5FF" # symbols & pictographs
                           u"\U0001F680-\U0001F6FF" # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def is_inappropriate_tweet(string):
    '''
    Distinguish the non-english tweets
    '''
    twitter_specific_list = ['#', '@', '?', '!', '\n', '\'', '/', ':', '[', ']', '(', ')', '_', ';', '"', '…', ' ', '.', ',', '&', '^', '*', '$', '%', '+', '-', '~', '`']
    emoji_list = ['💕', '🍑']
    for character in string:
        if not character.isalpha() or ord(character) > 128:
            if character in twitter_specific_list or is_emoji(character) or is_number(character) or character in emoji_list:
                continue    # No problem
            return True     # It may have problems like non-English as the language.
    return False

def is_emoji(s):
    count = 0
    for emoji in UNICODE_EMOJI:
        count += s.count(emoji)
        if count > 1:
            return False
    return bool(count)

def is_number(value):
    return value.isnumeric()

# a = '@txtnso Aber nicht nach 22 Uhr denn das ist verboten 😉\n(Bezug auf Schild an örtlichem Container)'
# print(is_inappropriate_tweet(a))
# b = 'せっかくn=strlenを用意してるならとIntStackにしました😃'
# print(b)
# c = remove_emoji(b)
# print(c)


def convert_emojis_to_word(text, Emoji_Dict):
    for emot in Emoji_Dict:
        text = re.sub(r'('+emot+')', "_".join(Emoji_Dict[emot].replace(",","").replace(":","").split()), text)
    return text

def duplication_score(str1, str2):
    from difflib import SequenceMatcher
    matcher = SequenceMatcher(None, str1, str2)
    score = matcher.ratio()
    return score

def getEnglishScoreFor1Sentence(target_string):
    from langdetect import detect_langs
    languages = detect_langs(target_string)
    confidence_score = None
    for lang in languages:
        actual_language = lang.lang
        confidence_score = lang.prob
        if actual_language == 'en':
            return confidence_score
    return confidence_score

def duplication_score_between_two_strings(str1, str2):
    # Import the SequenceMatcher class
    from difflib import SequenceMatcher
    # Create a SequenceMatcher object
    matcher = SequenceMatcher(None, str1, str2)
    # Calculate the duplication score
    score = matcher.ratio()
    return score

# list_ = [[1,2], [3,4], [5,6]]
# columns = ['sentence', 'label']
# savePickleDataWithPD('test.pkl', target_object=list_, columns=columns)
# te = getPickleData('test.pkl')
# print(1)

def get1stQuartile(target_list):
    df = pd.DataFrame(target_list)
    return df.quantile(0.25)

def get2ndQuartile(target_list):
    df = pd.DataFrame(target_list)
    return df.quantile(0.5)

def get3rdQuartile(target_list):
    df = pd.DataFrame(target_list)
    return df.quantile(0.75)

def saveNshowBoxPlotWithList(dst_path, target_list):
    fig, ax = plt.subplots()
    ax.boxplot(target_list)
    plt.show()
    fig.savefig(dst_path)

def saveNshowBoxPlotWithDict(dst_path, target_dict):
    fig, ax = plt.subplots()
    ax.boxplot(target_dict.values(), labels=target_dict.keys())
    plt.show()
    fig.savefig(dst_path)

def getMedianValue(target_dict, target_key):
    df = pd.DataFrame(target_dict)
    return df[target_key].median()