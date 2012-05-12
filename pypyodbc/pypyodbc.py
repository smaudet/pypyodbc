#! /usr/bin/env python
# -*- coding: utf-8 -*-

# PyPyODBC is develped from RealPyODBC 0.1 beta released in 2004 by Michele Petrazzo. Thanks Michele.

# The MIT License (MIT)
# Copyright (c) 2012 Henry Zhou <jiangwen365@gmail.com>
# Copyright (c) 2004 Michele Petrazzo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions 
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO #EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import sys, os, datetime, ctypes
from decimal import Decimal

DEBUGGING = 1

# Set the library location on linux 
library = "/usr/lib/libodbc.so"
    
# Below ODBC constants are defined and widely used in ODBC related programs and documents
# They are defined in cpp header files: sql.h sqlext.h sqltypes.h sqlucode.h
# You can get these files from the mingw32-runtime_3.13-1_all.deb package

SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2, SQL_OV_ODBC3 = 200, 2, 3
SQL_FETCH_NEXT, SQL_FETCH_FIRST, SQL_FETCH_LAST = 0x01, 0x02, 0x04
SQL_INVALID_HANDLE = -2
SQL_SUCCESS, SQL_SUCCESS_WITH_INFO = 0, 1
SQL_NO_DATA_FOUND = 100
SQL_NULL_DATA = -1
SQL_NULL_HANDLE, SQL_HANDLE_ENV, SQL_HANDLE_DBC, SQL_HANDLE_STMT = 0, 1, 2, 3
SQL_HANDLE_DESCR = 4
SQL_TABLE_NAMES = 3
SQL_PARAM_INPUT = 1
SQL_PARAM_INPUT_OUTPUT = 2

SQL_TYPE_NULL = 0
SQL_CHAR = 1
SQL_NUMERIC = 2
SQL_DECIMAL = 3
SQL_INTEGER = 4
SQL_SMALLINT = 5
SQL_FLOAT = 6
SQL_REAL = 7
SQL_DOUBLE = 8
SQL_DATE = 9
SQL_TIME = 10
SQL_TIMESTAMP = 11
SQL_VARCHAR = 12
SQL_LONGVARCHAR = -1
SQL_BINARY = -2
SQL_VARBINARY = -3
SQL_LONGVARBINARY = -4
SQL_BIGINT = -5
SQL_TINYINT = -6
SQL_BIT = -7
SQL_WCHAR = -8
SQL_WVARCHAR = -9
SQL_WLONGVARCHAR = -10
SQL_TYPE_DATE = 91
SQL_TYPE_TIME = 92
SQL_TYPE_TIMESTAMP = 93

SQL_C_CHAR = SQL_CHAR
SQL_C_NUMERIC = SQL_NUMERIC
SQL_C_LONG = SQL_INTEGER
SQL_C_SHORT = SQL_SMALLINT
SQL_C_FLOAT = SQL_REAL
SQL_C_DOUBLE = SQL_DOUBLE
SQL_C_TYPE_DATE = SQL_TYPE_DATE
SQL_C_TYPE_TIME = SQL_TYPE_TIME
SQL_C_BINARY = SQL_BINARY
SQL_C_BINARY = SQL_BINARY
SQL_C_LONG = SQL_INTEGER
SQL_C_TINYINT = SQL_TINYINT
SQL_C_BIT = SQL_BIT
SQL_C_WCHAR = SQL_WCHAR
SQL_C_TYPE_TIMESTAMP = SQL_TYPE_TIMESTAMP
SQL_C_TYPE_TIME = SQL_TYPE_TIME
SQL_C_TYPE_DATE = SQL_TYPE_DATE


def dttm_cvt(x):
    if x == '': return None
    else: return datetime.datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]),int(x[10:13]),int(x[14:16]),int(x[17:19]))

def tm_cvt(x):
    if x == '': return None
    else: return datetime.time(int(x[0:2]),int(x[3:5]),int(x[6:8]))

def dt_cvt(x):
    if x == '': return None
    else: return datetime.datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]))

def create_buffer_u():
    return ctypes.create_unicode_buffer(1024)

def create_buffer():
    return ctypes.create_string_buffer(1024)

# Below Datatype mappings referenced the document at
# http://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.help.sdk_12.5.1.aseodbc/html/aseodbc/CACFDIGH.htm
SqlTypes = { \
SQL_TYPE_NULL       : ('SQL_TYPE_NULL',     lambda x: None,             SQL_C_CHAR,         create_buffer), 
SQL_CHAR            : ('SQL_CHAR',          lambda x: str(x),           SQL_C_CHAR,         create_buffer),
SQL_NUMERIC         : ('SQL_NUMERIC',       lambda x: Decimal(x),       SQL_C_CHAR,         create_buffer),
SQL_DECIMAL         : ('SQL_DECIMAL',       lambda x: Decimal(x),       SQL_C_CHAR,         create_buffer),
SQL_INTEGER         : ('SQL_INTEGER',       lambda x: long(x),          SQL_C_LONG,         lambda :ctypes.c_long()),
SQL_SMALLINT        : ('SQL_SMALLINT',      lambda x: long(x),          SQL_C_SHORT,        lambda :ctypes.c_short()),
SQL_FLOAT           : ('SQL_FLOAT',         lambda x: float(x),         SQL_C_FLOAT,        lambda :ctypes.c_float()),
SQL_REAL            : ('SQL_REAL',          lambda x: float(x),         SQL_C_FLOAT,        lambda :ctypes.c_float()),
SQL_DOUBLE          : ('SQL_DOUBLE',        lambda x: float(x),         SQL_C_DOUBLE,       lambda :ctypes.c_double()),
SQL_DATE            : ('SQL_DATE',          lambda x: dt_cvt(x),        SQL_C_CHAR ,        create_buffer),
SQL_TIME            : ('SQL_TIME',          lambda x: tm_cvt(x),        SQL_C_CHAR,         create_buffer),
SQL_TIMESTAMP       : ('SQL_TIMESTAMP',     lambda x: dttm_cvt(x),      SQL_C_CHAR,         create_buffer),
SQL_VARCHAR         : ('SQL_VARCHAR',       lambda x: str(x),           SQL_C_CHAR,         create_buffer),
SQL_LONGVARCHAR     : ('SQL_LONGVARCHAR',   lambda x: str(x),           SQL_C_CHAR,         create_buffer),
SQL_BINARY          : ('SQL_BINARY',        lambda x: bytearray(x),     SQL_C_BINARY,       lambda :ctypes.c_buffer()),
SQL_VARBINARY       : ('SQL_VARBINARY',     lambda x: bytearray(x),     SQL_C_BINARY,       lambda :ctypes.c_buffer()),
SQL_LONGVARBINARY   : ('SQL_LONGVARBINARY', lambda x: bytearray(x),     SQL_C_BINARY,       lambda :ctypes.c_buffer()),
SQL_BIGINT          : ('SQL_BIGINT',        lambda x: long(x),          SQL_C_LONG,         lambda :ctypes.c_long()),
SQL_TINYINT         : ('SQL_TINYINT',       lambda x: long(x),          SQL_C_TINYINT,      lambda :ctypes.c_short()),
SQL_BIT             : ('SQL_BIT',           lambda x: bool(x),          SQL_C_BIT,          lambda :ctypes.c_short()),
SQL_WCHAR           : ('SQL_WCHAR',         lambda x: x,                SQL_C_WCHAR,        create_buffer_u),
SQL_WVARCHAR        : ('SQL_WVARCHAR',      lambda x: x,                SQL_C_WCHAR,        create_buffer_u),
SQL_WLONGVARCHAR    : ('SQL_WLONGVARCHAR',  lambda x: x,                SQL_C_WCHAR,        create_buffer_u),
SQL_TYPE_DATE       : ('SQL_TYPE_DATE',     lambda x: dt_cvt(x),        SQL_C_CHAR,         create_buffer),
SQL_TYPE_TIME       : ('SQL_TYPE_TIME',     lambda x: tm_cvt(x),        SQL_C_CHAR,         create_buffer),
SQL_TYPE_TIMESTAMP  : ('SQL_TYPE_TIMESTAMP',lambda x: dttm_cvt(x),      SQL_C_CHAR,         create_buffer), 
}


#Define exceptions
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



# Get the references of the platform's ODBC functions via ctypes 
if sys.platform == 'win32':
    ODBC_API = ctypes.windll.odbc32
else:
    if not os.path.exists(library):
        raise OdbcNoLibrary, 'Library %s not found' % library
    try:
        ODBC_API = ctypes.cdll.LoadLibrary(library)
    except:
        raise OdbcLibraryError, 'Error while loading %s' % library

# Set the return type for ODBC functions with ret result.
funcs_with_ret = ["SQLNumParams","SQLBindParameter","SQLExecute",
"SQLGetDiagRec","SQLAllocHandle","SQLSetEnvAttr","SQLExecDirect","SQLExecDirectW","SQLRowCount","SQLNumResultCols",
"SQLFetch","SQLBindCol","SQLCloseCursor","SQLSetConnectAttr","SQLDriverConnect","SQLConnect","SQLTables","SQLDescribeCol",
"SQLDataSources","SQLFreeHandle","SQLDisconnect","SQLEndTran","SQLPrepare","SQLPrepareW","SQLDescribeParam"]
for func_name in funcs_with_ret:
    getattr(ODBC_API,func_name).restype = ctypes.c_short

# Set the alias for the ctypes get reference function for beter code readbility.
Refer = ctypes.byref




def ctrl_err(ht, h, val_ret):
    """Classify type of ODBC error from (type of handle, handle, return value)
    , and raise with a list"""
    state = ctypes.create_string_buffer(5)
    NativeError = ctypes.c_int()
    Message = ctypes.create_string_buffer(1024*10)
    Buffer_len = ctypes.c_int()
    err_list = []
    number_errors = 1
    
    while 1:
        ret = ODBC_API.SQLGetDiagRec(ht, h, number_errors, state, \
            NativeError, Message, len(Message), Refer(Buffer_len))
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
            
def validate(ret, handle_type, handle):
    """ Validate return value, if not success, raise exceptions based on the handle """
    if ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
        return
    else:
        ctrl_err(handle_type, handle, ret)

            

def dataSources():
    """Return a list with [name, descrition]"""
    dsn = ctypes.create_string_buffer(1024)
    desc = ctypes.create_string_buffer(1024)
    dsn_len = ctypes.c_int()
    desc_len = ctypes.c_int()
    dsn_list = []
    
    while 1:
        ret = ODBC_API.SQLDataSources(shared_env_h, SQL_FETCH_NEXT, \
            dsn, len(dsn), Refer(dsn_len), desc, len(desc), Refer(desc_len))
        if ret == SQL_NO_DATA_FOUND:
            break
        elif not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_ENV, shared_env_h, ret)
        else:
            dsn_list.append((dsn.value, desc.value))
    return dsn_list


''' 
Allocate an environment by initializing the handle shared_env_h
It's created so connections can be created under it
connections pooling can be shared under one environment
'''
shared_env_h = ctypes.c_int()
ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, Refer(shared_env_h))
validate(ret, SQL_HANDLE_ENV, shared_env_h)

# Set the ODBC environment's compatibil leve to ODBC 3.0
ret = ODBC_API.SQLSetEnvAttr(shared_env_h, SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC3, 0)
validate(ret, SQL_HANDLE_ENV, shared_env_h)


class Cursor:
    def __init__(self, conx):
        """ Initialize self.stmt_h, which is the handle of a statement
        A statement is actually the basis of a python"cursor" object
        """
        self._conx = conx
        self.last_query = None
        self.last_ParamBufferList = None
        self.rowcount = None
        self.description = None
        self.autocommit = None
        self._ColType = None
        self.stmt_h = ctypes.c_int()
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_STMT, self._conx.dbc_h, Refer(self.stmt_h))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
    
    def execute(self, query_string, params = None):
        """ Execute the query string, with optional parameters.
        If parameters are provided, the query would be first prepared, then executed with parameters;
        If parameters are not provided, only th query sting, it would be executed directly 
        """
        if params != None:
            # If parameters are provided, then first prepare the query 
            # and then executed with parameters
            if not type(params) in (tuple, list):
                raise Exception
            if query_string != self.last_query:
                if type(query_string) == unicode:
                    ret = ODBC_API.SQLPrepareW(self.stmt_h, query_string, len(query_string))
                else:
                    ret = ODBC_API.SQLPrepare(self.stmt_h, query_string, len(query_string))
                validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                
                # Get the number of query parameters judged by database.
                NumParams = ctypes.c_int()
                ret = ODBC_API.SQLNumParams(self.stmt_h, Refer(NumParams))
                validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                if DEBUGGING:
                    print ('DEBUGGING: Parameter numbers:' + str(NumParams.value))
                
                if NumParams.value > 0:
                    # Every parameter needs to be binded to a buffer
                    ParamBufferList = []
                    for i in range(NumParams.value):
                        '''
                        DataType = ctypes.c_int()
                        ParamSize = ctypes.c_long()
                        DecimalDigits = ctypes.c_short()
                        Nullable = ctypes.c_bool()                        
                        ret = ODBC_API.SQLDescribeParam(self.stmt_h, i + 1, Refer(DataType), Refer(ParamSize), \
                            Refer(DecimalDigits), Refer(Nullable))
                        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                        '''
                        ParameterBuffer = ctypes.create_string_buffer(1024)
                        BufferLen = ctypes.c_long(1024)
                        LenOrIndBuf = ctypes.c_long()
                        ret = ODBC_API.SQLBindParameter(self.stmt_h, i + 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 255,\
                                 0, Refer(ParameterBuffer), Refer(BufferLen),Refer(LenOrIndBuf))
                        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                        # Append the value buffer and the lenth buffer to the array
                        ParamBufferList.append((ParameterBuffer,LenOrIndBuf))
                        
                self.last_query = query_string
                self.last_ParamBufferList = ParamBufferList
                
            if len(params) == len(self.last_ParamBufferList):
                for i in range(len(params)):
                    c_char_buf = ''
                    if type(params[i]) == datetime.datetime:
                        c_char_buf = params[i].isoformat().replace('T',' ')[:19]
                    elif type(params[i]) == datetime.date:
                        c_char_buf = params[i].isoformat()
                    elif type(params[i]) == datetime.time:
                        c_char_buf = params[i].isoformat()[0:8]
                    else:
                        c_char_buf = str(params[i])
                    self.last_ParamBufferList[i][0].value = c_char_buf
                    self.last_ParamBufferList[i][1].value = len(c_char_buf)
                    #print c_char_buf
            else:
                raise Exception
    
            ret = ODBC_API.SQLExecute(self.stmt_h)
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        else:
            """Make a query"""
            if type(query_string) == unicode:
                ret = ODBC_API.SQLExecDirectW(self.stmt_h, query_string, len(query_string))
            else:
                ret = ODBC_API.SQLExecDirect(self.stmt_h, query_string, len(query_string))
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            
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
            ret = ODBC_API.SQLDescribeCol(self.stmt_h, col, Refer(CName), len(CName), Refer(Cname_ptr),\
                Refer(Ctype_code),Refer(Csize),Refer(Cprecision), Refer(Cnull_ok))
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            ColDescr.append((CName.value, SqlTypes.get(Ctype_code.value,(Ctype_code.value))[0],Csize.value,Cprecision.value,Cnull_ok.value))
            self._ColType.append(Ctype_code.value)
        self.description = ColDescr
        self.NumOfRows()
        return (self)

        
    def NumOfRows(self):
        """Get the number of rows"""
        NOR = ctypes.c_int()
        ret = ODBC_API.SQLRowCount(self.stmt_h, Refer(NOR))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        self.rowcount = NOR.value
        return self.rowcount    
    
    def NumOfCols(self):
        """Get the number of cols"""
        NOC = ctypes.c_int()
        
        ret = ODBC_API.SQLNumResultCols(self.stmt_h, Refer(NOC))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
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
        col_buffs = []
        
        for col_num in range(NOC):
            col_sql_type = self._ColType[col_num]
            try:
                a_buffer = SqlTypes[col_sql_type][3]()
                buff_len = ctypes.c_long()
            except:
                print SqlTypes[col_sql_type]
                raise sys.exc_value
            ret = ODBC_API.SQLBindCol(self.stmt_h, col_num + 1, SqlTypes[col_sql_type][2], Refer(a_buffer), 1024, Refer(buff_len))
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            col_buffs.append((a_buffer,buff_len))
            #self.__bind(col_num + 1, col_buffs[col_num], buff_id)
        return self.__fetch(col_buffs, num)
    
    def __fetch(self, col_buffs, num = 0):
        i_row = 0
        rows = []
        while num == 0 or i_row < num:
            row = []
            ret = ODBC_API.SQLFetch(self.stmt_h)
            if ret == SQL_NO_DATA_FOUND:
                break
            elif not ret == SQL_SUCCESS:
                validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            i_col = 0
            for col in col_buffs:
                constructor = SqlTypes[self._ColType[i_col]][1]
                try:
                    if col[1].value == SQL_NULL_DATA:
                        row.append(None)
                    else:
                        row.append(constructor(col[0].value))
                except:
                    print (col[0].value)
                    print (len(col[0].value))
                    print (SqlTypes[self._ColType[i_col]][0])
                    print type(col[0].value)
                    x = col[0].value
                    print (int(x[0:3]),int(x[5:6]),int(x[8:9]))
                    raise sys.exc_value
                i_col += 1
            rows.append(row)
            i_row += 1
        return rows
    
    def __bind(self, col_num, data, buff_indicator):
        
        ret = ODBC_API.SQLBindCol(self.stmt_h, col_num, SQL_C_CHAR, Refer(data), \
          len(data), Refer(buff_indicator))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
    
        
    def close(self):
        """ Call SQLCloseCursor API to free the statement handle"""
        ret = ODBC_API.SQLCloseCursor(self.stmt_h)
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        
        if self.stmt_h.value:
            if DEBUGGING: print 's'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_STMT, self.stmt_h)
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        
        return
    
    def tables(self):
        """Return a list with all tables"""
        #We want only tables
        t_type = ctypes.create_string_buffer('TABLE')
        ret = ODBC_API.SQLTables(self.stmt_h, None, 0, None, 0, None, 0, \
            Refer(t_type), len(t_type))
        if not ret == SQL_SUCCESS:
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
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
        
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_DBC, shared_env_h, Refer(self.dbc_h))
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        
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
            validate(ret, SQL_HANDLE_DBC, self.dbc_h)


        # Create one connection with a connect string by calling SQLDriverConnect
        # and make self.dbc_h the handle of this connection
        c_connectString = ctypes.create_string_buffer(self.connectString)
        SQL_DRIVER_NOPROMPT = 0
        
        ret = ODBC_API.SQLDriverConnect(self.dbc_h, 0, c_connectString, len(c_connectString), 0, 0, 0, SQL_DRIVER_NOPROMPT)
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        
        # Set the connection's attribute of "autocommit" 
        #
        
        SQL_ATTR_AUTOCOMMIT = 102
        SQL_AUTOCOMMIT_OFF, SQL_AUTOCOMMIT_ON = 0, 1
        self.autocommit = autocommit
        
        ret = ODBC_API.SQLSetConnectAttr(self.dbc_h, SQL_ATTR_AUTOCOMMIT, self.autocommit and SQL_AUTOCOMMIT_ON or SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER)
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        
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
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        # Intinalize self.stmt_h, which is the basis of a "cursor"
        self.__set_stmt_h()
        self.connected = 1
        
    def cursor(self):
        return Cursor(self)   
    
    def commit(self):
        SQL_COMMIT = 0
        ret = ODBC_API.SQLEndTran(SQL_HANDLE_DBC, self.dbc_h, SQL_COMMIT);
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)

    def rollback(self):
        SQL_ROLLBACK = 1
        ret = ODBC_API.SQLEndTran(SQL_HANDLE_DBC, self.dbc_h, SQL_ROLLBACK);
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)

    def close(self):
        """Call me before exit, please"""
        self.__CloseHandle()

    def __CloseHandle(self, ht='', h=0):
        if ht:
            if not h.value: return
            ret = ODBC_API.SQLFreeHandle(ht, h)
            validate(SQL_HANDLE_ENV, self.stmt_h, ret)
            return
        
        if self.dbc_h.value:
            if self.connected:
                if DEBUGGING: print 'disc'
                if not self.autocommit:
                    self.rollback()
                ret = ODBC_API.SQLDisconnect(self.dbc_h)
                validate(ret, SQL_HANDLE_DBC, self.dbc_h)
            if DEBUGGING: print 'dbc'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_DBC, self.dbc_h)
            validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        '''
        if shared_env_h.value:
            if DEBUGGING: print 'env'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_ENV, shared_env_h)
            validate(ret, SQL_HANDLE_ENV, shared_env_h)
        '''


def connect(connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
    od = Connection(connectString, autocommit, ansi, timeout, unicode_results)
    return od

