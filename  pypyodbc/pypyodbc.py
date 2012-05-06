#! /usr/bin/env python
#coding=utf-8


# Welcome to RealPyODBC
# Version 0.1 beta
# This class help you to connect your python script with ODBC engine.
#
# This class is not db-api 2.0 compatible. If you want to help me to do it
# please modify it and send me an e-mail with your work!
# All the comunity will thanks you.
#
#
# TO-DO
# Make compatibility with db-api 2.0, so add:
# apilevel, theadsafety, paramstyle, cursor, exceptions, ....
#
# This software if released with MIT Licence

import sys, os, ctypes, decimal, datetime

library = "/usr/lib/libodbc.so"
VERBOSE = 1

#Costants
SQL_FETCH_NEXT, SQL_FETCH_FIRST, SQL_FETCH_LAST = 0x01, 0x02, 0x04

SQL_INVALID_HANDLE = -2
SQL_SUCCESS, SQL_SUCCESS_WITH_INFO = 0, 1
SQL_NO_DATA_FOUND = 100

SQL_NULL_HANDLE, SQL_HANDLE_ENV, SQL_HANDLE_DBC, SQL_HANDLE_STMT = 0, 1, 2, 3
SQL_HANDLE_DESCR = 4
SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2 = 200, 2

SQL_TABLE_NAMES = 3
SQL_C_CHAR = 1

def dttm_cvt(x):
    if x == '':
        return None
    else:
        return datetime.datetime(2012,1,1)
def tm_cvt(x):
    if x == '':
        return None
    else:
        return datetime.time(13)
    
def dt_cvt(x):
    if x == '':
        return None
    else:
        return datetime.date(2012,1,2)

#Types
SqlTypes = {0: ('TYPE_NULL', lambda x: None), 
1: ('CHAR', lambda x: str(x),'SQL_C_CHAR'),
2: ('NUMERIC', lambda x: decimal.Decimal(x)),
3: ('DECIMAL', lambda x: decimal.Decimal(x)),
4: ('INTEGER', lambda x: long(x)),
5: ('SMALLINT', lambda x: long(x)),
6: ('FLOAT', lambda x: float(x)),
7: ('REAL', lambda x: float(x)),
8: ('DOUBLE',lambda x: float(x)),
9: ('DATE', lambda x: dt_cvt(x)),
10: ('TIME', lambda x: tm_cvt(x)),
11: ('TIMESTAMP', lambda x: dttm_cvt(x)),
12: ('VARCHAR', lambda x: str(x),'SQL_C_CHAR'),
-1: ('LONGVARCHAR', lambda x: unicode(x,'mbcs'),'SQL_C_CHAR'),
-2: ('BINARY', lambda x: bytearray(x)),
-3: ('VARBINARY', lambda x: bytearray(x)),
-4: ('LONGVARBINARY', lambda x: bytearray(x)),
-5: ('BIGINT', lambda x: long(x)),
-6: ('TINYINT', lambda x: long(x)),
-7: ('BIT', lambda x: bool(x)),
-8: ('WCHAR', lambda x: unicode(x,'mbcs'),'SQL_C_WCHAR'),
-9: ('WVARCHAR', lambda x: unicode(x,'mbcs'),'SQL_C_WCHAR'),
-10:('WLONGVARCHAR', lambda x: unicode(x,'mbcs'),'SQL_C_WCHAR') \
  }




#Custom exceptions
class OdbcNoLibrary(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcLibraryError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcInvalidHandle(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
class OdbcGenericError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)





if sys.platform == 'win32':
    ODBC_API = ctypes.windll.odbc32
else:
    if not os.path.exists(library):
        raise OdbcNoLibrary, 'Library %s not found' % library
    try:
        ODBC_API = ctypes.cdll.LoadLibrary(library)
    except:
        raise OdbcLibraryError, 'Error while loading %s' % library

ODBC_API.SQLGetDiagRec.restype = ctypes.c_short
ODBC_API.SQLAllocHandle.restype = ctypes.c_short
ODBC_API.SQLSetEnvAttr.restype = ctypes.c_short
ODBC_API.SQLExecDirect.restype = ctypes.c_short
ODBC_API.SQLRowCount.restype = ctypes.c_short
ODBC_API.SQLNumResultCols.restype = ctypes.c_short
ODBC_API.SQLFetch.restype = ctypes.c_short
ODBC_API.SQLBindCol.restype = ctypes.c_short
ODBC_API.SQLCloseCursor.restype = ctypes.c_short
ODBC_API.SQLSetConnectAttr.restype = ctypes.c_short
ODBC_API.SQLDriverConnect.restype = ctypes.c_short
ODBC_API.SQLConnect.restype = ctypes.c_short
ODBC_API.SQLTables.restype = ctypes.c_short
ODBC_API.SQLDescribeCol.restype = ctypes.c_short
ODBC_API.SQLDataSources.restype = ctypes.c_short
ODBC_API.SQLFreeHandle.restype = ctypes.c_short
ODBC_API.SQLDisconnect.restype = ctypes.c_short
ODBC_API.SQLEndTran.restype = ctypes.c_short



def ctrl_err(ht, h, val_ret):
    """Method for make a control of the errors
    We get type of handle, handle, return value
    Return a raise with a list"""
    state = ctypes.create_string_buffer(5)
    NativeError = ctypes.c_int()
    Message = ctypes.create_string_buffer(1024*10)
    Buffer_len = ctypes.c_int()
    err_list = []
    number_errors = 1
    
    while 1:
        ret = ODBC_API.SQLGetDiagRec(ht, h, number_errors, state, \
            NativeError, Message, len(Message), ctypes.byref(Buffer_len))
        if ret == SQL_NO_DATA_FOUND:
            #No more data, I can raise
            raise OdbcGenericError, err_list
            break
        elif ret == SQL_INVALID_HANDLE:
            #The handle passed is an invalid handle
            raise OdbcInvalidHandle, 'SQL_INVALID_HANDLE'
        elif ret == SQL_SUCCESS:
            err_list.append((state.value, Message.value, NativeError.value))
            number_errors += 1

def dataSources():
    """Return a list with [name, descrition]"""
    dsn = ctypes.create_string_buffer(1024)
    desc = ctypes.create_string_buffer(1024)
    dsn_len = ctypes.c_int()
    desc_len = ctypes.c_int()
    dsn_list = []
    
    while 1:
        ret = ODBC_API.SQLDataSources(shared_env_h, SQL_FETCH_NEXT, \
            dsn, len(dsn), ctypes.byref(dsn_len), desc, len(desc), ctypes.byref(desc_len))
        if ret == SQL_NO_DATA_FOUND:
            break
        elif not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_ENV, shared_env_h, ret)
        else:
            dsn_list.append((dsn.value, desc.value))
    return dsn_list


''' 
Allocate an environment by initializing the handle shared_env_h
It's created so connections pooling can be shared under one environment
'''
shared_env_h = ctypes.c_int()
ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, ctypes.byref(shared_env_h))
if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
    ctrl_err(SQL_HANDLE_ENV, shared_env_h, ret)



# Set the environment's compatibil leve to ODBC 2.0

ret = ODBC_API.SQLSetEnvAttr(shared_env_h, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2, 0)
if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
    ctrl_err(SQL_HANDLE_ENV, shared_env_h, ret)


class Cursor:
    def __init__(self, conx):
        """ Initialize self.stmt_h, which is an handle of a statement
        A statement is actually the basis of a "cursor"
        """
        self._conx = conx
        self.stmt_h = ctypes.c_int()
        
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_STMT, self._conx.dbc_h, ctypes.byref(self.stmt_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            
        self.rowcount = None
        self.description = None
        self.autocommit = None
        self._ColType = None
    
    def execute(self, query):
        return self.Query(query)
        
        
    def Query(self, q):
        """Make a query"""
        ret = ODBC_API.SQLExecDirect(self.stmt_h, q, len(q))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            
        NOC = self.NumOfCols()
        "same as pyodbc's tuple (name, type_code, display_size, internal_size, precision, scale, null_ok)"
        CName = ctypes.create_string_buffer(1024)
        Cname_ptr = ctypes.c_int()
        Ctype_code = ctypes.c_short()
        Csize = ctypes.c_int()
        Cprecision = ctypes.c_int()
        Cnull_ok = ctypes.c_int()
        ColDescr = []
        self._ColType = []
        for col in range(1, NOC+1):
            ret = ODBC_API.SQLDescribeCol(self.stmt_h, col, ctypes.byref(CName), len(CName), ctypes.byref(Cname_ptr),\
                ctypes.byref(Ctype_code),ctypes.byref(Csize),ctypes.byref(Cprecision), ctypes.byref(Cnull_ok))
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            if SqlTypes.has_key(Ctype_code.value):
                ColDescr.append((CName.value, SqlTypes[Ctype_code.value][0],Csize.value,Cprecision.value,Cnull_ok.value))
            else:
                ColDescr.append((CName.value, Ctype_code.value,Csize.value,Cprecision.value,Cnull_ok.value))
            self._ColType.append(Ctype_code.value)
        self.description = ColDescr
        return self

        
    def NumOfRows(self):
        """Get the number of rows"""
        NOR = ctypes.c_int()
        ret = ODBC_API.SQLRowCount(self.stmt_h, ctypes.byref(NOR))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
        self.rowcount = NOR.value
        return self.rowcount    
    
    def NumOfCols(self):
        """Get the number of cols"""
        NOC = ctypes.c_int()
        
        ret = ODBC_API.SQLNumResultCols(self.stmt_h, ctypes.byref(NOC))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
        self.rowcount = NOC.value
        return NOC.value
    

    def fetchmany(self, num):
        return self._fetch(num)

    def fetchone(self):
        return self._fetch(1)
    
    def fetchall(self):
        return self._fetch()
    
    def _fetch(self, num = 0):
        NOC = self.NumOfCols()
        col_buffs = [ctypes.create_string_buffer(1024) for c in range(NOC)]
        buff_id = ctypes.c_int()
        for col_num in range(NOC):
            ret = ODBC_API.SQLBindCol(self.stmt_h, col_num + 1, SQL_C_CHAR, \
            ctypes.byref(col_buffs[col_num]), len(col_buffs[col_num]), ctypes.byref(buff_id))
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            
            #self.__bind(col_num + 1, col_buffs[col_num], buff_id)
        return self.__fetch(col_buffs, num)
    
    def __fetch(self, cols, num = 0):
        i_row = 0
        rows = []
        while num == 0 or i_row < num:
            row = []
            ret = ODBC_API.SQLFetch(self.stmt_h)
            if ret == SQL_NO_DATA_FOUND:
                break
            elif not ret == SQL_SUCCESS:
                ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
            i_col = 0
            for col in cols:
                f = SqlTypes[self._ColType[i_col]][1]
                try:
                    row.append(f(col.value))
                    print (col.value)
                except:
                    print (col.value)
                    print (len(col.value))
                    print (SqlTypes[self._ColType[i_col]][0])
                    print type(col.value)
                    print (unicode(col.value,'mbcs'))
                    sys.exit()
                i_col += 1
            rows.append(row)
            i_row += 1
        return rows
    
    def __bind(self, col_num, data, buff_indicator):
        
        ret = ODBC_API.SQLBindCol(self.stmt_h, col_num, SQL_C_CHAR, ctypes.byref(data), \
          len(data), ctypes.byref(buff_indicator))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
    
        
    def close(self):
        self.__CloseCursor()
    
    def __CloseCursor(self):
        """ Call SQLCloseCursor API to free the statement handle"""
        ret = ODBC_API.SQLCloseCursor(self.stmt_h)
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_ENV, self.stmt_h, ret)
        
        if self.stmt_h.value:
            if VERBOSE: print 's'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_STMT, self.stmt_h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_ENV, self.stmt_h, ret)
        
        return
    
    def tables(self):
        """Return a list with all tables"""
        #We want only tables
        t_type = ctypes.create_string_buffer('TABLE')
        ret = ODBC_API.SQLTables(self.stmt_h, None, 0, None, 0, None, 0, \
            ctypes.byref(t_type), len(t_type))
        if not ret == SQL_SUCCESS:
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)
        data = ctypes.create_string_buffer(1024)
        buff = ctypes.c_int()
        self.__bind(SQL_TABLE_NAMES, data, buff)
        return self.__fetch([data])
    
    
    def columns(self, table):
        """We return a list with a tuple for every col:
        field, type, number of digits, allow null"""
        self.Query("SELECT * FROM " + table)

    





class Connection:
    """This class implement a odbc connection. It use ctypes for work.
    """
    def __init__(self, connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
        """Init variables and connect to the engine"""
        self.connected = 0
        self.dbc_h = ctypes.c_int()
        
        # Allocate an DBC handle self.dbc_h under the environment shared_env_h
        # This DBC handle is actually the basis of a "connection"
        # The handle of self.dbc_h will be used to connect to a certain source 
        # in the self.connect and self.ConnectByDSN method
        
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_DBC, shared_env_h, ctypes.byref(self.dbc_h))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        
        self.connect(connectString, autocommit, ansi, timeout, unicode_results)
            
            
            
    def connect(self, connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
        """Connect to odbc, using connect strings
        and set the connection's attributes like autocommit and timeout
        by calling SQLSetConnectAttr
        """ 
        # Convert the connetsytring to encoded string
        # so it can be converted to a ctypes c_char array object 
        self.connectString = connectString
        if isinstance(self.connectString,unicode):
            self.connectString = self.connectString.encode('mbcs')


        # Before we establish the connection by the connection string
        # Set the connection's attribute of "timeout" (Actully LOGIN_TIMEOUT)
        SQL_IS_UINTEGER = -5
        SQL_ATTR_LOGIN_TIMEOUT = 103
        
        if timeout != 0:
            ret = ODBC_API.SQLSetConnectAttr(self.dbc_h, SQL_ATTR_LOGIN_TIMEOUT, timeout, SQL_IS_UINTEGER);
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)


        # Create one connection with a connect string by calling SQLDriverConnect
        # and make self.dbc_h the handle of this connection
        c_connectString = ctypes.create_string_buffer(self.connectString)
        SQL_DRIVER_NOPROMPT = 0
        
        ret = ODBC_API.SQLDriverConnect(self.dbc_h, 0, c_connectString, len(c_connectString), 0, 0, 0, SQL_DRIVER_NOPROMPT)
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        
        # Set the connection's attribute of "autocommit" 
        #
        
        SQL_ATTR_AUTOCOMMIT = 102
        SQL_AUTOCOMMIT_OFF, SQL_AUTOCOMMIT_ON = 0, 1
        self.autocommit = autocommit
        if self.autocommit == True:
            ret = ODBC_API.SQLSetConnectAttr(self.dbc_h, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_ON, SQL_IS_UINTEGER)
        else:
            ret = ODBC_API.SQLSetConnectAttr(self.dbc_h, SQL_ATTR_AUTOCOMMIT, SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER)
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        
        self.connected = 1
        

    def ConnectByDSN(self, dsn, user, passwd = ''):
        """Connect to odbc, we need dsn, user and optionally password"""
        self.dsn = dsn
        self.user = user
        self.passwd = passwd

        sn = ctypes.create_string_buffer(dsn)
        un = ctypes.create_string_buffer(user)        
        pw = ctypes.create_string_buffer(passwd)
        
        ret = ODBC_API.SQLConnect(self.dbc_h, sn, len(sn), un, len(un), pw, len(pw))
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        # Intinalize self.stmt_h, which is the basis of a "cursor"
        self.__set_stmt_h()
        self.connected = 1
        
    def cursor(self):
        return Cursor(self)   
    
    def commit(self):
        SQL_COMMIT = 0
        ret = ODBC_API.SQLEndTran(SQL_HANDLE_DBC, self.dbc_h, SQL_COMMIT);
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)

    def rollback(self):
        SQL_ROLLBACK = 1
        ret = ODBC_API.SQLEndTran(SQL_HANDLE_DBC, self.dbc_h, SQL_ROLLBACK);
        if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_STMT, self.stmt_h, ret)

    def close(self):
        """Call me before exit, please"""
        self.__CloseHandle()

    def __CloseHandle(self, ht='', h=0):
        if ht:
            if not h.value: return
            ret = ODBC_API.SQLFreeHandle(ht, h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_ENV, self.stmt_h, ret)
            return
        
        if self.dbc_h.value:
            if self.connected:
                if VERBOSE: print 'disc'
                if not self.autocommit:
                    self.rollback()
                ret = ODBC_API.SQLDisconnect(self.dbc_h)
                if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                    ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
            if VERBOSE: print 'dbc'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_DBC, self.dbc_h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_DBC, self.dbc_h, ret)
        if shared_env_h.value:
            if VERBOSE: print 'env'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_ENV, shared_env_h)
            if not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
                ctrl_err(SQL_HANDLE_ENV, shared_env_h, ret)





def connect(connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
    od = Connection(connectString, autocommit, ansi, timeout, unicode_results)
    return od




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




if __name__ == "__main__":
    
    DSN_list = dataSources()
    print (DSN_list)
    
    if sys.platform == "win32":
        dsn_test =  'mdb'
    else:
        dsn_test =  'pg'
    user = 'tutti'
    
    #conn = connect('Driver={Microsoft Access Driver (*.mdb)};DBQ=C:\\cnzzz.mdb')
    conn = connect('DSN=PostgreSQL35W')
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
    
    cur.execute(u"""select * from yesoulchenyu where 日期时间 IS NOT NULL""".encode('mbcs'))
    print [(x[0], x[1]) for x in cur.description]
    #Get results
    import time
    
    for row in cur.fetchmany(15):
        for field in row:
            print type(field),
            
            if isinstance(field, unicode):
                print (field.encode('mbcs'))
            else:
                print (field)
            
            time.sleep(0.2)
    
    
    print (len(cur.fetchall()))
    
    cur.close()
    cur = conn.cursor()
    cur.execute(u"delete from yesoulchenyu ".encode('mbcs'))
    
    cur.execute(u"""select * from yesoulchenyu""".encode('mbcs'))

    #Get results
    
    for row in cur.fetchmany(8):
            print (u' '.join([field for field in row]).encode('mbcs'))
    
    cur.close
    conn.rollback()
    cur = conn.cursor()
    import time
    cur.execute('update yesoulchenyu set Num = '+str(time.time()))
    conn.commit()
    for row in cur.execute(u"""select * from yesoulchenyu""".encode('mbcs')).fetchone():
        for field in row:
            if isinstance(field, unicode):
                print (field.encode('mbcs'))
            else:
                print (field)
        print ('')
        print (cur.description)
    
    i = 1
    row = cur.fetchone()
    while row != []:
        row = cur.fetchone()
        i += 1
        if i%2500 == 0:
            print (i)
    #print conn.FetchAll()
    #Close before exit
    cur.close()
    conn.close()
