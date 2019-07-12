
import datetime, os, shutil

"""detect hidden file"""
def isHiddenFile(path):
    base = os.path.basename(path)
    return (len(base) > 0
    and base[0] == '.'
    and base != '.'
    and base != '..')


"""get all the dates of files in a given directory in a sorted order
    return a sorted list of datetimes
"""
def getDateListFromDir(directory):
    dateList = [each for each in os.listdir(directory) if not isHiddenFile(each)]
    dateList = [d.strip('.json') for d in dateList]
    return sorted(dateList, key=lambda x: datetime.datetime.strptime(x, '%Y-%m-%d-%I%p'))

def getQueryListFromDir(directory):
    querylist = [each for each in os.listdir(directory) if not isHiddenFile(each)]
    querylist = sorted(querylist)
    querylist = [d.replace('.html','') for d in querylist]
    return querylist

def get_only_12pm(datelist):
    noons = []
    for date in datelist:
        if '12pm' in date:
            noons.append(date)
    return noons

all_dates = getDateListFromDir('/Users/yueyang/Downloads/2019-processed-json')
datelist = get_only_12pm(all_dates)
datelist2 = getDateListFromDir('/Users/yueyang/Downloads/June26-July5')
querylist = getQueryListFromDir('/Users/yueyang/Downloads/June26-July5/2019-06-26-9am')
querylist = ['are hijabs oppressive', 'arizona redneck', 'black feminism', 'black women hair stigma', 'can you be gay and christian', 'can you choose to be gay', 'christianity and lgbt', 'detransitioning', 'do you decide your sexuality', 'effeminacy', 'fake feminism', 'feminine men', 'feminism and religion cannot coexist', 'feminism is problematic', 'feminists hate men', 'feminists kill babies', 'gender fluidity', 'gender transitioning', 'hijab and feminism', 'Hijab oppresion',"how do you know if you're gay", 'indophobia', 'islam and sexism', 'Islamic feminism', 'mental illness in college students', 'muslim feminism', 'muslim women', 'Religion brainwashing','republicans on a liberal campus', 'sexual transitioning', 'white feminism', "why black people don't shower", "women's rights in islam"]