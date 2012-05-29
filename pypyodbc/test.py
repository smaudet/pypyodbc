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
    cur.execute(u"""select * from pypyodbc_test_data""")

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
    pypyodbc.DEBUG = 0
    DSN_list = pypyodbc.dataSources()
    print (DSN_list)
    
    if sys.platform == "win32":
        dsn_test =  'mdb'
    else:
        dsn_test =  'pg'
    user = 'tutti'

    conxs = [\
        ('Access',
        pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ='+cur_file_dir()+u'\\e.mdb', unicode_results = True),
        u"""create table pypyodbc_test_data (编号 integer,产品名 text,数量 numeric,价格 float,日期 
                datetime,shijian time,riqi datetime, kong float)""",
        ),
        ('SQLServer',
        pypyodbc.connect('DSN=MSSQL'),
        u"""create table pypyodbc_test_data (编号 integer,产品名 text,数量 numeric,价格 float,日期 
                datetime,shijian time,riqi date, kong float)""",
        ),
        ('MySQL',
        pypyodbc.connect('DSN=MYSQL'),
        u"""create table pypyodbc_test_data (编号 integer,产品名 text,数量 numeric,价格 float,日期 
                datetime,shijian time,riqi date, kong float)""",
        
        ),
        ('PostgreSQL',
        pypyodbc.connect('DSN=PostgreSQL35W'),
        u"""create table pypyodbc_test_data (编号 integer,产品名 text,数量 numeric,价格 float,日期 
                        timestamp,shijian time,riqi date, kong float)""",
        ),
        ]
    
    for db_desc, conn, create_table_sql in conxs:
        '''
        cur = conn.cursor()
        for row in (cur.getTypeInfo().fetchall()):
            i = 1
            for field in row:
                print i,
                print field
                i += 1
        cur = None
        '''
        
        
        cur = conn.cursor()
        has_table_data = cur.tables(table='pypyodbc_test_data').fetchone()
        print 'has table "pypyodbc_test_data"?' + str(has_table_data)
        cur.close()
        
        
        cur = conn.cursor()
        try:
            cur.execute('Drop table pypyodbc_test_data;')
        except:
            pass

        print db_desc

        cur.execute(create_table_sql)
        conn.commit()
        for row in cur.columns(table='data').fetchall():
            print row
        cur.close()
        cur = conn.cursor()
        
        cur.execute(u"insert into pypyodbc_test_data values(1,'pypyodbc',12.3,1234.55,?,'17:31:32','2012-12-23',NULL)", (datetime.datetime.now(),))
        longtext = u''.join([u'我在马路边，捡到一分钱。']*2)
        cur.execute("insert into pypyodbc_test_data values (?,?,?,?,?,?,?,NULL)", \
                                (2, \
                                longtext,\
                                Decimal('1233.4513'), \
                                123.44, \
                                datetime.datetime.now(), \
                                datetime.datetime.now().time(),\
                                datetime.date.today(),\
                                ))
        print time.time()
        for i in xrange(3,190):
            cur.executemany(u"""insert into pypyodbc_test_data values 
            (?,?,12.3, 1234.55, ?,?,'2012-12-23',NULL)""", 
            [(i, "【巴黎圣母院】".decode('utf-8'), datetime.datetime.now(), datetime.datetime.now().time()),
            (i, u"《巴提斯图塔》", datetime.datetime.now(), datetime.datetime.now().time()),
            (i, "〖太极张三丰〗".decode('utf-8'), datetime.datetime.now(), datetime.datetime.now().time()),]
            )
        
        print time.time()
        conn.commit()
        
        print time.time()

        cur.execute(u"""select * from pypyodbc_test_data""")
        print cur.description
        #Get results
        
        for row in cur.fetchmany(6):
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
        #cur.execute(u"delete from pypyodbc_test_data ".encode('mbcs'))
        
        cur.execute(u"""select * from pypyodbc_test_data""")

        #Get results
        
        for row in cur.fetchmany(6):
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
        cur.execute(u'update pypyodbc_test_data set 数量 = ? where 数量 > 0 '.encode('mbcs'),(time.time(),))
        print cur.rowcount
        print time.time()
        conn.commit()
        for field in cur.execute(u"""select * from pypyodbc_test_data""").fetchone():
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

        #conn.close()
    print ('End of testing')
    time.sleep(3)
    
