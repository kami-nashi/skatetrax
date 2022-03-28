import pymysql
import configparser as conf
import smtplib
from email.message import EmailMessage


def baseConfig():
    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('appKey', 'secret')
    return appConfig


def moduleConfig():
    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    appConfig = configParser.get('modules', 'newUsers')
    return appConfig


# sanitize know problem makers from user input strings
def stripper(str):
    chars = [';', '#', '--', '//', '/', '.', '!', '\s', '\S', '*', '?', '\t', '\n', '\r', '@', '\\', '\\\\', '"', "'", 'drop']
    if any((c in chars) for c in str):
        return True
    else:
        return False


def dbconnect(sql, vTUP=None):
    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)

    host = configParser.get('dbconf', 'host')
    user = configParser.get('dbconf', 'user')
    password = configParser.get('dbconf', 'password')
    db = configParser.get('dbconf', 'db')

    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    cur = con.cursor()
    cur.execute(sql, vTUP)
    tables = cur.fetchall()
    cur.connection.commit()
    con.close()
    return tables


def dbinsert(sql, recordTuple):
    if not stripper(recordTuple):
        configParser = conf.RawConfigParser()
        configFilePath = r'/etc/skatetrax/settings.conf'
        configParser.read(configFilePath)
        host = configParser.get('dbconf', 'host')
        user = configParser.get('dbconf', 'user')
        password = configParser.get('dbconf', 'password')
        db = configParser.get('dbconf', 'db')
        con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        cur = con.cursor()
        cur.execute(sql, recordTuple)
        tables = cur.fetchall()
        cur.connection.commit()
        con.close()
        return tables


def notifyEmail(notifyTo, Subject, Body):
    '''
    Send email to user
    '''

    configParser = conf.RawConfigParser()
    configFilePath = r'/etc/skatetrax/settings.conf'
    configParser.read(configFilePath)
    mailLogin = configParser.get('notifier_email', 'login')
    mailPass = configParser.get('notifier_email', 'password')
    mailFrom = configParser.get('notifier_email', 'fromaddr')
    mailHost = configParser.get('notifier_email', 'SMTPServer')
    mailPort = configParser.get('notifier_email', 'port')

    msg = EmailMessage()
    msg.set_content(Body)
    msg['Subject'] = Subject
    msg['From'] = mailFrom
    msg['To'] = notifyTo

    server = smtplib.SMTP_SSL(mailHost, mailPort)
    server.login(mailLogin, mailPass)
    server.send_message(msg)
    server.quit()
    return
