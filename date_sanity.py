from datetime import datetime
import re

def is_date(string):
    string = re.sub('[a-z]', '', string)
    try:
        datetime.strptime(string, "%d/%b/%Y")
        return True
    except ValueError:
        return False

def invalid(date):
    '''checks for the validity of a date string,verifies if the string represents a date or not
    input the date string
    output boolean representing the validity of date,True if invalid,False if valid
    '''

    # print(dhinkachika)

    try:
        if any([int(x) == 0 for x in date.split('/')]) or int(date.split('/')[0]) > 31 or len(date.split('/')[-1]) == 3:
            return True
        else:
            return False
    except ValueError:
        try:
            date = datetime.strftime(datetime.strptime(date, "%d/%b/%Y"), "%d/%m/%Y")
            if any([int(x) == 0 for x in date.split('/')]) or int(date.split('/')[0]) > 31 or len(date.split('/')[-1]) == 3:
                return True
            else:
                return False
        except ValueError:
            print('olayolay')
            return True


def min_date(date1, date2):
    try:
        if datetime.toordinal(datetime.strptime(date1, "%d/%m/%Y")) - datetime.toordinal(
                datetime.strptime(date2, "%d/%m/%Y")) <= 0:
            return date1
        else:
            return date2
    except Exception as e:
        return str()

def max_date(date1, date2):
    try:
        if datetime.toordinal(datetime.strptime(date1, "%d/%m/%Y")) - datetime.toordinal(
                datetime.strptime(date2, "%d/%m/%Y")) <= 0:
            return date2
        else:
            return date1
    except Exception as e:
        return str()

def difference(date1, date2=''):
    '''calculates difference between two dates
    input date1,date2(optional),if only one date is given,calculates difference from real today
    output difference in terms of number of days
    '''
    if not date2:
        return datetime.toordinal(datetime.today()) - datetime.toordinal(datetime.strptime(date1, "%d/%m/%Y"))
    else:
        return datetime.toordinal(datetime.strptime(date1, "%d/%m/%Y")) - datetime.toordinal(
            datetime.strptime(date2, "%d/%m/%Y"))
def check_dates(date):
    mdates=[]
    i=date
    # for i in fdates:
    i = i.replace('.', '/').replace('-', '/').replace(' ','')
    poss=["%d/%b/%Y","%d%b%Y","%d/%B/%Y","%d%B%Y"]
    for j in poss:
        try:
            i = datetime.strftime(datetime.strptime(i, j), "%d/%m/%Y")

        except:
            continue
    # print(i,'*******************************')
    if not invalid(i):

        # print(i)
        if len(i.split('/')[-1]) == 2:
            try:
                i = datetime.strftime(datetime.strptime(i, "%d/%m/%y"), "%d/%m/%Y")
            except Exception as e:
                i = datetime.strftime(datetime.strptime(i, "%m/%d/%y"), "%d/%m/%Y")
        elif len(i.split('/')[-1]) == 3:
            i=''
    else:
        i=''
    return i

def checkfirst(out1: dict):
    while '' in out1['dob']:
        out1['dob'].remove('')
    while '' in out1['issueDate']:
        out1['issueDate'].remove('')
    while '' in out1['expiryDate']:
        out1['expiryDate'].remove('')
    for idx,i in enumerate(out1['dob']):
        out1['dob'][idx]=check_dates(i)
    for idx, i in enumerate(out1['issueDate']):
        out1['issueDate'][idx] = check_dates(i)
    for idx,i in enumerate(out1['expiryDate']):
        out1['expiryDate'][idx]=check_dates(i)

    notInformat = list()
    for d in out1['dob']+out1['issueDate']+out1['expiryDate']:
        try:
            notInformat.append(int(d.split('/')[1])>12)
        except Exception as e:
            print (d, " is ignored")

    if any(notInformat):
        for idx,i in enumerate(out1['dob']):
            try:
                out1['dob'][idx] = datetime.strftime(datetime.strptime(i, "%m/%d/%Y"), "%d/%m/%Y")
            except Exception as e:
                out1['dob'][idx] = str()
        for idx,i in enumerate(out1['issueDate']):
            try:
                out1['issueDate'][idx] = datetime.strftime(datetime.strptime(i, "%m/%d/%Y"), "%d/%m/%Y")
            except Exception as e:
                out1['issueDate'][idx] = str()
        for idx,i in enumerate(out1['expiryDate']):
            try:
                out1['expiryDate'][idx] = datetime.strftime(datetime.strptime(i, "%m/%d/%Y"), "%d/%m/%Y")
            except Exception as e:
                out1['expiryDate'][idx] = str()
            
    if len(out1['dob']) == 2:
        out1['dob'] = sorted(out1['dob'], key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
        if len(out1['issueDate']) == 0 and len(out1['expiryDate']) > 0:
            out1['issueDate'].append(out1['dob'][1])
            out1['dob'].remove(out1['dob'][1])
        elif len(out1['expiryDate']) == 0 and len(out1['issueDate']) > 0:
            out1['expiryDate'].append(out1['dob'][1])
            out1['dob'].remove(out1['dob'][1])
        elif len(out1['expiryDate']) == 0 and len(out1['issueDate']) == 0:
            if difference(out1['dob'][1]) <= 0:
                out1['expiryDate'].append(out1['dob'][1])
                out1['dob'].remove(out1['dob'][1])
            else:
                out1['issueDate'].append(out1['dob'][1])
                out1['dob'].remove(out1['dob'][1])
        else:
            out1['dob'].remove(out1['dob'][1])
    if len(out1['issueDate']) == 2:
        out1['issueDate'] = sorted(out1['issueDate'], key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
        if len(out1['dob']) == 0 and len(out1['expiryDate']) > 0:
            out1['dob'].append(out1['issueDate'][0])
            out1['issueDate'].remove(out1['issueDate'][0])
        elif len(out1['expiryDate']) == 0 and len(out1['dob']) > 0:
            out1['expiryDate'].append(out1['issueDate'][1])
            out1['issueDate'].remove(out1['issueDate'][1])
        elif len(out1['expiryDate']) == 0 and len(out1['dob']) == 0:
            if difference(out1['issueDate'][1]) <= 0:
                out1['expiryDate'].append(out1['issueDate'][1])
                out1['issueDate'].remove(out1['issueDate'][1])
            else:
                out1['dob'].append(out1['issueDate'][0])
                out1['issueDate'].remove(out1['issueDate'][0])
        else:
            if difference(out1['issueDate'][0]) / 365 >= 15:
                out1['issueDate'].remove(out1['issueDate'][0])
            else:
                out1['issueDate'].remove(out1['issueDate'][1])
    if len(out1['expiryDate']) == 2:
        out1['issueDate'] = sorted(out1['issueDate'], key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
        if len(out1['dob']) == 0 and len(out1['issueDate']) > 0:
            out1['dob'].append(out1['expiryDate'][0])
            out1['expiryDate'].remove(out1['expiryDate'][0])
        elif len(out1['issueDate']) == 0 and len(out1['dob']) > 0:
            out1['issueDate'].append(out1['expiryDate'][0])
            out1['expiryDate'].remove(out1['expiryDate'][0])
        elif len(out1['expiryDate']) == 0 and len(out1['dob']) == 0:
            if difference(out1['expiryDate'][0]) / 365 >= 15:
                out1['dob'].append(out1['expiryDate'][0])
                out1['expiryDate'].remove(out1['expiryDate'][0])
            else:
                out1['issueDate'].append(out1['expiryDate'][0])
                out1['expiryDate'].remove(out1['expiryDate'][0])
        else:
            out1['expiryDate'].remove(out1['expiryDate'][0])
    return out1


def check_all(dob: list,doi : list,doe :list):
    print('******',dob,doi,doe)
    mega_list=dob+doi+doe
    dob_tmp,doi_tmp,doe_tmp=str(),str(),str()
    if len(dob)==1:
        dob_tmp=dob[0]
    if len(doi)==1:
        doi_tmp=doi[0]
    if len(doe)==1:
        doe_tmp=doe[0]
    if len(mega_list)==3:

        if max_date(dob_tmp,doi_tmp)==dob_tmp:
            a=doi_tmp
            doi_tmp=dob_tmp
            dob_tmp= a
        if max_date(dob_tmp,doe_tmp)==dob_tmp:
            a = doe_tmp
            doe_tmp = dob_tmp
            dob_tmp = a
        if max_date(doi_tmp, doe_tmp) == doi_tmp:
            a = doe_tmp
            doe_tmp = doi_tmp
            doi_tmp = a
    if len(mega_list)==2:
        if not dob_tmp:
            if max_date(doi_tmp, doe_tmp) == doi_tmp:
                a = doe_tmp
                doe_tmp = doi_tmp
                doi_tmp = a
            if difference(doi_tmp) / 365 >= 18:
                dob_tmp=doi_tmp
                doi_tmp=""
        if not doi_tmp:
            if max_date(dob_tmp, doe_tmp) == dob_tmp:
                a = doe_tmp
                doe_tmp = dob_tmp
                dob_tmp = a
            if difference(dob_tmp) / 365 <15:
                doi_tmp=dob_tmp
                dob_tmp=''
        if not doe_tmp:
            if max_date(dob_tmp, doi_tmp) == dob_tmp:
                a = doi_tmp
                doi_tmp = dob_tmp
                dob_tmp = a
            if difference(doi_tmp)<=0:
                doe_tmp=doi_tmp
                if difference(dob_tmp) / 365 >= 18:
                    doi_tmp=''
                else:
                    doi_tmp=dob_tmp
                    dob_tmp=''
    if len(mega_list) == 1:
        if dob_tmp:
            if 0<=difference(dob_tmp) / 365 <15:
                doi_tmp=dob_tmp
                dob_tmp=''
            elif difference(dob_tmp)<=0:
                doe_tmp=dob_tmp
                dob_tmp=''
        elif doi_tmp:
            if difference(doi_tmp) / 365 >= 18:
                dob_tmp=doi_tmp
                doi_tmp=''
            elif difference(doi_tmp)<=0:
                doe_tmp=doi_tmp
                doi_tmp=''
        elif doe_tmp:
            if difference(doe_tmp) / 365 >= 18:
                dob_tmp=doe_tmp
                doe_tmp=''
    dob[0]=dob_tmp
    doi[0]=doi_tmp
    doe[0]=doe_tmp
    return dob,doi,doe