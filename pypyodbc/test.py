# -*- coding: utf-8 -*-
import sys, os
import pypyodbc as pypyodbc
import ctypes
import time, datetime
from decimal import Decimal
import base64

binary_data = base64.b64decode('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')

ba = bytearray(binary_data)
mv = bytearray(binary_data)


def cur_file_dir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

#c_Path = ctypes.create_string_buffer(u"CREATE_DB=.\\e.mdb General\0\0".encode('mbcs'))
#ODBC_ADD_SYS_DSN = 1
#ctypes.windll.ODBCCP32.SQLConfigDataSource(None,ODBC_ADD_SYS_DSN,"Microsoft Access Driver (*.mdb)", c_Path)


def u8_enc(v, force_str = False):
    if v == None: return ('')
    elif isinstance(v,unicode): return (v.encode('utf_8','replace'))
    elif isinstance(v, buffer): return ('')
    else:
        if force_str: return (str(v))
        else: return (v)





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
    
    
    mdb_path = cur_file_dir()+u'\\e.mdb'
    
    #pypyodbc.win_create_mdb(mdb_path.encode('mbcs'))
    try:
        conxs = [\
            ('Access',
            pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=ss'+mdb_path, unicode_results = True),
            u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,product_name text,数量 numeric,价格 float,日期 
                    datetime,shijian time,riqi datetime, kong float, bin LONGBINARY)""",
            ),
            ('SQLServer',
            pypyodbc.connect('DSN=MSSQL', unicode_results = True),
            u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,product_name text,数量 numeric(14,4),价格 float,日期 
                    datetime,shijian time,riqi date, kong float, bin varbinary(MAX))""",
            ),
            ('MySQL',
            pypyodbc.connect('DSN=MYSQL', unicode_results = True),
            u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,product_name text,数量 numeric(14,4),价格 float,日期 
                    datetime,shijian time,riqi date, kong float, bin BLOB)""",
            
            ),
            ('PostgreSQL',
            pypyodbc.connect('DSN=PostgreSQL35W', unicode_results = True),
            u"""create table pypyodbc_test_data (编号 integer PRIMARY KEY,product_name text,数量 numeric(14,4),价格 float,日期 
                            timestamp,shijian time,riqi date, kong float, bin bytea)""",
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

            print ' *'.join(['' for i in range(80)])

            print db_desc 
            print ' *'.join(['' for i in range(80)])
            cur = conn.cursor()
            
            
            has_table_data = cur.tables(table='pypyodbc_test_data').fetchone()
            print 'has table "pypyodbc_test_data"?' + str(has_table_data)
            
            cur.close()
            
            
            cur = conn.cursor()
            if has_table_data:
                cur.execute('Drop table pypyodbc_test_data;')

            
            cur.execute(create_table_sql)
            conn.commit()
            for row in cur.columns(table='pypyodbc_test_data').fetchall():
                print row
            cur.close()
            
            print 'inserting...',
            start_time = time.time()
            cur = conn.cursor()
            cur.execute(u"insert into pypyodbc_test_data values(1,'这是pypyodbc模块 :)',12.3,1234.55,'2012-11-11','17:31:32','2012-11-11',NULL, ?)", (ba,))
            longtext = u''.join([u'我在马路边，捡到一分钱。']*2)
            cur.execute("insert into pypyodbc_test_data values (?,?,?,?,NULL,NULL,NULL,NULL,?)", \
                                    (2, \
                                    longtext,\
                                    Decimal('1233.4513'), \
                                    123.44, \
    #                                datetime.datetime.now(), \
    #                                datetime.datetime.now().time(),\
    #                                datetime.date.today(),\
                                    mv))



            for i in xrange(3,103):
                cur.executemany(u"""insert into pypyodbc_test_data values 
                (?,?,12.32311, 1234.55, NULL,NULL,'2012-12-23',NULL,NULL)""", 
                [(i+500000, "【巴黎圣母院】".decode('utf-8')),
                (i+100000, u"《普罗米修斯》"),
                (i+200000, "〖太极张三丰〗".decode('utf-8')),
                (i+300000, '〖!@#$$%"^&%&〗'.decode('utf-8')),
                (i+400000, "〖querty-','〗".decode('utf-8'))]\
                )
            
            print 'insert complete, total time ',
            end_time = time.time()
            print end_time-start_time
            conn.commit()
            print 'commit comlete, commit time ',
            print time.time() - end_time


            cur.execute(u"""select * from pypyodbc_test_data""")
            print cur.description
            #Get results
            field = cur.fetchone().bin
            file(cur_file_dir()+'\\logo_'+db_desc+'.gif','wb').write(field)
            
            
            field = cur.fetchone().bin
            file(cur_file_dir()+'\\logo2_'+db_desc+'.gif','wb').write(field)


            
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
            start_time =  time.time()
            print 'updating one column...',
            cur.execute(u'update pypyodbc_test_data set 数量 = ? where 数量 > 0 '.encode('mbcs'),(time.time(),))
            print 'updated: '+str(cur.rowcount),
            print ' total time: '+ str(time.time()-start_time)
            conn.commit()
            for field in cur.execute(u"""select * from pypyodbc_test_data""").fetchone():
                if isinstance(field, unicode):
                    print field.encode('mbcs'),
                else:
                    print field,
            print ('')
            print (cur.description)
            
            start_time = time.time()
            i = 1
            row = cur.fetchone()
            while row != None:
                for field in row:
                    x = field
                i += 1
                if i % 1000 == 0:
                    print i,
                
                row = cur.fetchone()
            print '\n Total records retrive time:',
            print time.time() - start_time
            #print conn.FetchAll()
            #Close before exit
            cur.close()
            import cProfile
            #cProfile.run('prof_func()')

            #conn.close()
        print ('End of testing')
        time.sleep(3)
        
    except Exception, e:
        print e
        print type(e)
        print e[0]
        print e[1]
        