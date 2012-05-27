# -*- coding: utf-8 -*-
import sys, os
import pypyodbc as pypyodbc
import ctypes
import time, datetime
from decimal import Decimal

def cur_file_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

c_Path = ctypes.create_string_buffer(u"CREATE_DB=.\\e.mdb General\0\0".encode('mbcs'))
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

    conxs = [\
        pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+cur_file_dir()+u'\\e.mdb', unicode_results = True),
        #pypyodbc.connect('DSN=PostgreSQL35W'),
        pypyodbc.connect('DSN=MSSQL')]
    
    for conn in conxs:
        cur = conn.cursor()
        has_table_data = cur.tables(table='data').fetchone()
        print has_table_data
        cur.close()
        
        
        cur = conn.cursor()
        if has_table_data:
            cur.execute('Drop table data')

            

        cur.execute(u"""create table data (编号 integer, 产品名 text, 数量 numeric, 价格 float, 日期 datetime, shijian datetime, riqi datetime, kong float)""")
        for row in cur.columns(table='data').fetchall():
            print row
        cur.close()
        cur = conn.cursor()
        
        cur.execute(u"insert into data values (1, 'pypyodbc好', 12.3, 1234.55, '2012-11-21','15:31:32','2012-12-23',NULL)")
        longtext = u''.join([u'北京天安门']*5)
        cur.execute("insert into data values (?,?,?,?,?,'15:31:32','2012-12-23',NULL)", (2, longtext.encode('mbcs'), Decimal('1233.4513'), 123.44, datetime.datetime.now()))
        print time.time()
        for i in xrange(3,34):
            cur.execute("insert into data values (?,?,12.3, 1234.55, '2012-11-21','15:31:32','2012-12-23',NULL)", (i, (u'X哦X'+unicode(i%10000)).encode('gbk')))
        
        print time.time()
        conn.commit()
        
        print time.time()

        cur.execute(u"""select * from data""".encode('mbcs'))
        print cur.description
        #Get results
        
        for row in cur.fetchmany(3):
            for field in row:
                print type(field),
                if isinstance(field, unicode):
                    print field.encode('mbcs'),
                else:
                    print field,
            print ('')
        
        #print (len(cur.fetchall()))
        
        cur.close()
        cur = conn.cursor()
        #cur.execute(u"delete from data ".encode('mbcs'))
        
        cur.execute(u"""select * from data""".encode('mbcs'))

        #Get results
        
        for row in cur.fetchmany(3):
            for field in row:
                if isinstance(field, unicode):
                    print len(field),
                    print field.encode('mbcs'),
                else:
                    print field,
                print '|',
            print ''
        
        cur.close()
        #conn.rollback()
        cur = conn.cursor()
        print time.time()
        cur.execute(u'update data set 数量 = ? where 数量 > 0 ',(time.time(),))
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
        import cProfile
        #cProfile.run('prof_func()')
        cur = conn.cursor()
        for row in (cur.get_type_info().fetchall()):
            i = 1
            for field in row:
                print i,
                print field
                i += 1
        conn.close()
    print ('End of testing')
    time.sleep(3)
    
