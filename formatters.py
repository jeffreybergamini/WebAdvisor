import re
import crypt 

def extract_name( student ) :
    rval = dict()
    n = student['name'];
    comma = n.index(',');
    rval['family'] = n[0:comma]
    dot = n.find('.')
    if dot > 0:
        rval['given'] = n[comma+2:dot-2]
    else:
        rval['given'] = n[comma+2:]

    return rval

def gen_login( class_name, student ) :
    rval = extract_name(student)
    m = re.search('^(cs|cis)(\d+).*$', class_name)
    classnumber = m.group(2)
    rval['login'] = rval['family'][0:3].lower() + rval['given'][0:3].lower() + classnumber
    rval['password'] = rval['given'][0:2] + rval['family'][0:2] + student['id'][-4:]
    return rval


def gen_netlab ( rosters ) :
    for cl in rosters :
        class_name = cl[0:-3]
        filename = class_name + '-netlab.csv'
        print ('Writing: ' + filename)
        f = open(filename, 'w')
        f.write('User ID, Given/First Name, Family/Last Name, Display Name, Email\n')
        for q in rosters[cl]:
            login = gen_login(class_name, q)
            f.write(login['login'] + ',' + login['given'] + ',' + login['family'] + ',' + login['given'] + ' ' + login['family'] + ',' + q['email'] + '\n')
        f.close()

def gen_maillist ( rosters ) :
    for cl in rosters :
        class_name = cl[0:-3]
        filename = class_name + '-email-list.txt'
        print ('Writing: ' + filename)
        f = open(filename, 'w')
        for q in rosters[cl]:
            f.write('"' + q['name'] + '" <' + q['email'] + ">\n")
        f.close()

def gen_unix ( rosters ) :
    for cl in rosters :
        class_name = cl[0:-3]
        m = re.search('^(cs|cis)(\d+).*$', class_name)
        unixclass = m.group(1) + m.group(2)
        filename = class_name + '-unix.sh'
        print ('Writing: ' + filename)
        f = open(filename, 'w')
        for q in rosters[cl]:
            login = gen_login(class_name, q)
            f.write('useradd -g ' + unixclass +\
                     ' -d /home/' + unixclass + '/' + login['login'] +\
                     ' -m -p \'' + crypt.crypt(login['password'], '$6$af9$') + '\'' +\
                     ' -c "' + login['given'] + ' ' + login['family'] + '"' +\
                     ' -g users ' + login['login'] + '\n')
        f.close()

def gen_vlab ( rosters ) :
    for cl in rosters :
        class_name = cl[0:-3]
        m = re.search('^(cs|cis)(\d+).*$', class_name)
        unixclass = m.group(1) + m.group(2)
        ou = unixclass.upper()
        filename = class_name + '-vlab.bat'
        print ('Writing: ' + filename)
        f = open(filename, 'w')
        for q in rosters[cl]:
            login = gen_login(class_name, q)
            f.write('dsadd user "CN='+login['given']+' '+login['family']+',OU='+ou+',DC=cislab,DC=net"'+\
                    ' -samid ' + login['login'] +\
                    ' -upn ' + login['login'] + '@cislab.net' +\
                    ' -fn ' + login['given'] +\
                    ' -ln ' + login['family'] +\
                    ' -pwd ' + login['password'] +\
                    ' -desc "' + unixclass + ' student"' +\
                    ' -memberof "CN='+unixclass+',CN=users,DC=cislab,DC=net"' +\
                    ' "CN=students,CN=users,DC=cislab,DC=net"' +\
                    ' -canchpwd yes -pwdneverexpires yes -acctexpires never -disabled no\n')
        f.close()

def gen_netacad ( rosters ) :
    for cl in rosters :
        class_name = cl[0:-3]
        filename = class_name + '-netacad.csv'
        print ('Writing: ' + filename)
        f = open(filename, 'w')
        f.write('First Name, Last Name, Email Address, Institution Student ID\n')
        for q in rosters[cl]:
            login = gen_login(class_name, q)
            f.write(login['given'] + ',' + login['family'] + ',' + q['email'] + ',' + q['id'] + '\n')
        f.close()

def gen_csv ( rosters ) : 
    for cl in rosters :
        class_name = cl[0:-3]
        filename = class_name + '-full.csv'
        print ('Writing: ' + filename)
        f = open(filename, 'w')
        f.write('Username, First Name, Last Name, Student ID, Email, Phone Number\n')
        for q in rosters[cl]:
            login = gen_login(class_name, q)
            f.write(q['username'] + ',' +\
                    login['given'] + ',' +\
                    login['family'] + ',' +\
                    q['id'] + ',' +\
                    q['email'] + ',' +\
                    q['phone'] + '\n')
        f.close()
