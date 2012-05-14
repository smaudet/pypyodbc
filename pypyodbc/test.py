# -*- coding: utf-8 -*-
import sys, os
import pypyodbc as pypyodbc
import ctypes
import datetime


def cur_file_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

c_Path = ctypes.create_string_buffer(u"CREATE_DB=.\\e.mdb General\0".encode('mbcs'))
ODBC_ADD_SYS_DSN = 1
ctypes.windll.ODBCCP32.SQLConfigDataSource(None,ODBC_ADD_SYS_DSN,"Microsoft Access Driver (*.mdb)", c_Path)


def u8_enc(v, force_str = False):
    if v == None:
        return ('')
    elif isinstance(v,unicode):
        return (v.encode('utf_8','replace'))
    elif isinstance(v, buffer):
        return ('')
    else:
        if force_str:
            return (str(v))
        else:
            return (v)





def prof_func():
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+cur_file_dir()+u'\\e.mdb', unicode_results = True)

    cur = conn.cursor()


    cur.execute(u"""select * from data""")

    i = 0
    row = cur.fetchone()
    while row != None:
        for field in row:
            x = field
        i += 1
        if i % 5000 == 0:
            print i,
        
        row = cur.fetchone()
        
    #print conn.FetchAll()
    #Close before exit
    cur.close()
    conn.close()
    




if __name__ == "__main__":
    
    DSN_list = pypyodbc.dataSources()
    print (DSN_list)
    
    if sys.platform == "win32":
        dsn_test =  'mdb'
    else:
        dsn_test =  'pg'
    user = 'tutti'

    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+cur_file_dir()+u'\\e.mdb', unicode_results = True)
    #conn = pypyodbc.connect('DSN=PostgreSQL35W')
    #conn = pypyodbc.connect('DSN=MySQL')
    #Dsn list
    #print conn.info
    #Get tables list
    #cur = conn.cursor()
    #tables = cur.tables()
    #if sys.platform == "win32": t = tables[0][0]
    #else: t = "ttt"
    
    #cur.close()
    #cur = conn.cursor()
    #Get fields on the table
    #cols = cur.columns(t)
    #print cols
    #Make a query
    
    #cur.close()

    cur = conn.cursor()
    if cur.tables(table='data').fetchone():
        cur.close()
        cur = conn.cursor()
        cur.execute('Drop table data;')
        
    

    cur.execute(u"""create table data (编号 integer, 产品名 varchar(200), 价格 float, 数量 numeric, 
    日期 timestamp, shijian time, riqi date, kong float)""")
    for row in cur.columns(table='data').fetchall():
        print row
    cur.close()
    cur = conn.cursor()
    
    
    import time
    cur.execute(u"insert into data values (1, 'pypyodbc好', 12.3, 1234.55, '2012-11-21','15:31:32','2012-12-23',NULL)")
    
    cur.execute("insert into data values (?,?,?,?,?,?,?,NULL)", (2, u'X哦X'.encode('mbcs'),88.11119, 888.998798,datetime.datetime.now(),datetime.datetime.now().time(), datetime.datetime.now().date()))
    print time.time()
    for i in xrange(3,16000):
        cur.execute("insert into data values (?,?,?,?,?,?,?,?)", (i, (u'X哦X'+unicode(i%10000)).encode('gbk'),88.11119+i, 888.998798-i,None,datetime.datetime.now().time(), datetime.datetime.now().date(),i/10.0))
    
    print time.time()
    conn.commit()
    print time.time()

    cur.execute(u"""select * from data""".encode('mbcs'))
    print [(x[0], x[1]) for x in cur.description]
    #Get results
    
    for row in cur.fetchmany(5):
        for field in row:
            print type(field),
            if isinstance(field, unicode):
                print field.encode('mbcs'),
            else:
                print field,
        print ('')
    
    print (len(cur.fetchall()))
    
    cur.close()
    cur = conn.cursor()
    #cur.execute(u"delete from data ".encode('mbcs'))
    
    cur.execute(u"""select * from data""".encode('mbcs'))

    #Get results
    
    for row in cur.fetchmany(3):
        for field in row:
            if isinstance(field, unicode):
                print field.encode('mbcs'),
            else:
                print field,
            print '|',
        print ''
    
    cur.close
    #conn.rollback()
    cur = conn.cursor()
    print time.time()
    cur.execute(u'update data set 数量 = ? where 数量 > 0 ',(str(time.time()),))
    print cur.rowcount
    print time.time()
    conn.commit()
    for field in cur.execute(u"""select * from data""").fetchone():
        if isinstance(field, unicode):
            print field.encode('mbcs'),
        else:
            print field,
    print ('')
    print (cur.description)
    
    i = 1
    row = cur.fetchone()
    while row != None:
        for field in row:
            x = field
        i += 1
        if i % 5000 == 0:
            print i,
        
        row = cur.fetchone()
        
    #print conn.FetchAll()
    #Close before exit
    cur.close()
    conn.close()
    import cProfile
    cProfile.run('prof_func()')
    
