
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


def get_only_12pm(datelist):
    noons = []
    for date in datelist:
        if '12pm' in date:
            noons.append(date)
    return noons

all_dates = getDateListFromDir('/Users/yueyang/Downloads/2019-processed-json')
datelist = get_only_12pm(all_dates)
datelist2 = getDateListFromDir('/Users/yueyang/Downloads/June26-July5')
print(datelist)
