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

DEBUGGING = 0
version = '1.0 alpha'


# Set the library location on linux 
library = "/usr/lib/libodbc.so"
    
# Below ODBC constants are defined and widely used in ODBC related programs and documents
# They are defined in cpp header files: sql.h sqlext.h sqltypes.h sqlucode.h
# You can get these files from the mingw32-runtime_3.13-1_all.deb package

SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2, SQL_OV_ODBC3 = 200, 2, 3
SQL_FETCH_NEXT, SQL_FETCH_FIRST, SQL_FETCH_LAST = 0x01, 0x02, 0x04
SQL_NULL_HANDLE, SQL_HANDLE_ENV, SQL_HANDLE_DBC, SQL_HANDLE_STMT = 0, 1, 2, 3
SQL_SUCCESS, SQL_SUCCESS_WITH_INFO = 0, 1
SQL_INVALID_HANDLE = -2
SQL_NO_DATA_FOUND = 100
SQL_NULL_DATA = -1
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

# Below Datatype mappings ADDRenced the document at
# http://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.help.sdk_12.5.1.aseodbc/html/aseodbc/CACFDIGH.htm
SqlTypes = { \
SQL_TYPE_NULL       : ('SQL_TYPE_NULL',     lambda x: None,             SQL_C_CHAR,         create_buffer), 
SQL_CHAR            : ('SQL_CHAR',          lambda x: x,                SQL_C_CHAR,         create_buffer),
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
SQL_VARCHAR         : ('SQL_VARCHAR',       lambda x: x,                SQL_C_CHAR,         create_buffer),
SQL_LONGVARCHAR     : ('SQL_LONGVARCHAR',   lambda x: x,                SQL_C_CHAR,         create_buffer),
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



# Get the References of the platform's ODBC functions via ctypes 
if sys.platform == 'win32':
    ODBC_API = ctypes.windll.odbc32
else:
    if not os.path.exists(library):
        raise OdbcNoLibrary, 'Library %s not found' % library
    try:
        ODBC_API = ctypes.cdll.LoadLibrary(library)
    except:
        raise OdbcLibraryError, 'Error while loading %s' % library

# Define the return type for ODBC functions with ret result.

funcs_with_ret = ["SQLNumParams","SQLBindParameter","SQLExecute","SQLNumResultCols","SQLDescribeCol",
        "SQLGetDiagRec","SQLAllocHandle","SQLSetEnvAttr","SQLExecDirect","SQLExecDirectW","SQLRowCount",
        "SQLFetch","SQLBindCol","SQLCloseCursor","SQLSetConnectAttr","SQLDriverConnect","SQLConnect","SQLTables",
        "SQLDataSources","SQLFreeHandle","SQLDisconnect","SQLEndTran","SQLPrepare","SQLPrepareW","SQLDescribeParam"]
    
for func_name in funcs_with_ret:
    getattr(ODBC_API,func_name).restype = ctypes.c_short



# Set the alias for the ctypes get reference function for beter code readbility or performance.
ADDR = ctypes.byref
SQLFetch = ODBC_API.SQLFetch


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
            NativeError, Message, len(Message), ADDR(Buffer_len))
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
            dsn, len(dsn), ADDR(dsn_len), desc, len(desc), ADDR(desc_len))
        if ret == SQL_NO_DATA_FOUND:
            break
        elif not ret in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
            ctrl_err(SQL_HANDLE_ENV, shared_env_h, ret)
        else:
            dsn_list.append((dsn.value, desc.value))
    return dsn_list


''' 
Allocate an ODBC environment by initializing the handle shared_env_h
ODBC enviroment needed to be created, so connections can be created under it
connections pooling can be shared under one environment
'''
shared_env_h = ctypes.c_int()
ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, ADDR(shared_env_h))
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
        self.ParamBufferList = []
        self.ColBufferList = []
        self.buf_cvt_func = []
        self.rowcount = None
        self.description = None
        self.autocommit = None
        self.ColTypeCodeList = []
        self.stmt_h = ctypes.c_int()
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_STMT, self._conx.dbc_h, ADDR(self.stmt_h))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
    
    def execute(self, query_string, params = None):
        """ Execute the query string, with optional parameters.
        If parameters are provided, the query would first be prepared, then executed with parameters;
        If parameters are not provided, only th query sting, it would be executed directly 
        """
        if params != None:
            # If parameters are provided, then first prepare the query 
            # and then executed with parameters
            if not type(params) in (tuple, list):
                raise Exception
            if query_string != self.last_query:
                # if the query is not same as last query, then it is not prepared
                # and it needs to be prepared before excuting with parameters
                if type(query_string) == unicode:
                    ret = ODBC_API.SQLPrepareW(self.stmt_h, query_string, len(query_string))
                else:
                    ret = ODBC_API.SQLPrepare(self.stmt_h, query_string, len(query_string))
                validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                
                # Get the number of query parameters judged by database.
                NumParams = ctypes.c_int()
                ret = ODBC_API.SQLNumParams(self.stmt_h, ADDR(NumParams))
                validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                if DEBUGGING:
                    print ('DEBUGGING: Parameter numbers:' + str(NumParams.value))
                
                # Every parameter needs to be binded to a buffer
                ParamBufferList = []
                for i in range(NumParams.value):
                    '''
                    DataType = ctypes.c_int()
                    ParamSize = ctypes.c_long()
                    DecimalDigits = ctypes.c_short()
                    Nullable = ctypes.c_bool()                        
                    ret = ODBC_API.SQLDescribeParam(self.stmt_h, i + 1, ADDR(DataType), ADDR(ParamSize), \
                        ADDR(DecimalDigits), ADDR(Nullable))
                    validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                    '''
                    ParameterBuffer = ctypes.create_string_buffer(1024)
                    BufferLen = ctypes.c_long(1024)
                    LenOrIndBuf = ctypes.c_long()
                    ret = ODBC_API.SQLBindParameter(self.stmt_h, i + 1, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_VARCHAR, 255,\
                             0, ADDR(ParameterBuffer), ADDR(BufferLen),ADDR(LenOrIndBuf))
                    validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                    # Append the value buffer and the lenth buffer to the array
                    ParamBufferList.append((ParameterBuffer,LenOrIndBuf))
                        
                self.last_query = query_string
                self.ParamBufferList = ParamBufferList
            
            
            if len(params) != len(self.ParamBufferList):
                # Number of parameters provided do not same as number required
                raise Exception
            else:
                # With query prepared, now put parameters into buffers
                col_num = 0
                for buf_value, buf_len in self.ParamBufferList:
                    c_char_buf = ''
                    param_val = params[col_num]
                    if param_val == None:
                        pass
                    elif type(param_val) == datetime.datetime:
                        c_char_buf = param_val.isoformat().replace('T',' ')[:19]
                    elif type(param_val) == datetime.date:
                        c_char_buf = param_val.isoformat()
                    elif type(param_val) == datetime.time:
                        c_char_buf = param_val.isoformat()[0:8]
                    else:
                        c_char_buf = str(param_val)
                    buf_value.value, buf_len.value = c_char_buf, len(c_char_buf)
                    if param_val == None:
                        buf_len.value = -1
                    col_num += 1
                    #print c_char_buf
    
            ret = ODBC_API.SQLExecute(self.stmt_h)
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        else:
            """Execute a query directly"""
            if type(query_string) == unicode:
                ret = ODBC_API.SQLExecDirectW(self.stmt_h, query_string, len(query_string))
            else:
                ret = ODBC_API.SQLExecDirect(self.stmt_h, query_string, len(query_string))
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            
        self.NumOfRows()
        self._GetDesc()
        self._BindCols()
        return (self)
    
    def _GetDesc(self):
        "Get the tuple of (name, type_code, display_size, internal_size, precision, scale, null_ok)"  
        Cname = ctypes.create_string_buffer(1024)
        Cname_ptr = ctypes.c_int()
        Ctype_code = ctypes.c_short()
        Csize = ctypes.c_int()
        Cprecision = ctypes.c_int()
        Cnull_ok = ctypes.c_int()
        ColDescr = []
        self.ColTypeCodeList = []
        NOC = self.NumOfCols()
        for col in range(1, NOC+1):
            ret = ODBC_API.SQLDescribeCol(self.stmt_h, col, ADDR(Cname), len(Cname), ADDR(Cname_ptr),\
                ADDR(Ctype_code),ADDR(Csize),ADDR(Cprecision), ADDR(Cnull_ok))
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            
            ColDescr.append((Cname.value, SqlTypes.get(Ctype_code.value,(Ctype_code.value))[0],Csize.value,\
                Cprecision.value,Cnull_ok.value))
            self.ColTypeCodeList.append(Ctype_code.value)
        self.description = ColDescr
        

    
    def _BindCols(self):
        NOC = self.NumOfCols()
        col_buffer_list = []
        buf_cvt_func = []
        for col_num in range(NOC):
            col_type_code = self.ColTypeCodeList[col_num]
            
            a_buffer = SqlTypes[col_type_code][3]()
            buff_len = ctypes.c_long()
            
            target_type = SqlTypes[col_type_code][2]
            force_unicode = self._conx.unicode_results

            if force_unicode and col_type_code in (SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR):
                target_type = SQL_C_WCHAR
                a_buffer = create_buffer_u()
            
            ret = ODBC_API.SQLBindCol(self.stmt_h, col_num + 1, target_type, ADDR(a_buffer), 1024, ADDR(buff_len))
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
            col_buffer_list.append((a_buffer,buff_len))
            buf_cvt_func.append(SqlTypes[self.ColTypeCodeList[col_num]][1])
            #self.__bind(col_num + 1, col_buffer_list[col_num], buff_id)
        self.ColBufferList = col_buffer_list
        self.buf_cvt_func = buf_cvt_func
        
        
    def NumOfRows(self):
        """Get the number of rows"""
        NOR = ctypes.c_int()
        ret = ODBC_API.SQLRowCount(self.stmt_h, ADDR(NOR))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        self.rowcount = NOR.value
        return self.rowcount    
    
    def NumOfCols(self):
        """Get the number of cols"""
        NOC = ctypes.c_int()
        ret = ODBC_API.SQLNumResultCols(self.stmt_h, ADDR(NOC))
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)

        return NOC.value
    

    def fetchmany(self, num):
        return self.__fetch(num)

    def fetchone(self):
        records = self.__fetch(1)
        if records != []:
            return records[0]
        else:
            return None
    
    def fetchall(self):
        return self.__fetch()

    
    def __fetch(self, num = 0):
        rows = []
        row_num = 0
        # limit to num time loops, or loop until no data if num == 0
        while num == 0 or row_num < num:
            ret = SQLFetch(self.stmt_h)
            if ret != SQL_SUCCESS:
                if ret == SQL_NO_DATA_FOUND:
                    break
                else:
                    validate(ret, SQL_HANDLE_STMT, self.stmt_h)
                
            row = [None for colbuf in self.ColBufferList]
            
            col_num = 0
            for buf_value, buf_len in self.ColBufferList:
                try:
                    if buf_len.value != SQL_NULL_DATA:
                        row[col_num] = self.buf_cvt_func[col_num](buf_value.value)
                except:
                    print (colbuf[0].value)
                    print (SqlTypes[self.ColTypeCodeList[col_num]][0])
                    print type(colbuf[0].value)
                    x = colbuf[0].value
                    raise sys.exc_value
                col_num += 1
            rows.append(row)
            row_num += 1
        return rows
    
        
    def close(self):
        """ Call SQLCloseCursor API to free the statement handle"""
        ret = ODBC_API.SQLCloseCursor(self.stmt_h)
        validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        
        if self.stmt_h.value:
            if DEBUGGING: print 's'
            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_STMT, self.stmt_h)
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
        
        return
    
    def tables(self, table=None, catalog=None, schema=None, tableType=None):
        """Return a list with all tables"""
        v_catalog, l_catalog = None, 0
        if catalog:
            c_catalog = ctypes.create_string_buffer(catalog)
            v_catalog = ADDR(c_catalog)
            l_catalog = len(c_catalog)
            
        v_schema, l_schema = None, 0
        if schema:
            c_schema = ctypes.create_string_buffer(schema)
            v_schema = ADDR(c_schema)
            l_schema = len(c_schema)
            
        v_table, l_table = None, 0
        if table: 
            c_table = ctypes.create_string_buffer(table)
            v_table = ADDR(c_table)
            l_table = len(c_table)
            
        v_tabletype, l_tabletype = None, 0
        if tableType: 
            c_tabletype = ctypes.create_string_buffer(tableType)
            v_tabletype = ADDR(c_tabletype)
            l_tabletype = len(c_tabletype)
        
        
        ret = ODBC_API.SQLTables(self.stmt_h,
                                v_catalog, l_catalog,
                                v_schema, l_schema, 
                                v_table, l_table,
                                v_tabletype, l_tabletype)

        if not ret == SQL_SUCCESS:
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)
    
        self.NumOfRows()
        self._GetDesc()
        self._BindCols()
        return (self)
    
    
    def columns(self, table=None, catalog=None, schema=None, column=None):
        """Return a list with all columns"""        
        v_catalog, l_catalog = None, 0
        if catalog:
            c_catalog = ctypes.create_string_buffer(catalog)
            v_catalog = ADDR(c_catalog)
            l_catalog = len(c_catalog)
            
        v_schema, l_schema = None, 0
        if schema:
            c_schema = ctypes.create_string_buffer(schema)
            v_schema = ADDR(c_schema)
            l_schema = len(c_schema)
            
        v_table, l_table = None, 0
        if table: 
            c_table = ctypes.create_string_buffer(table)
            v_table = ADDR(c_table)
            l_table = len(c_table)
            
        v_column, l_column = None, 0
        if column: 
            c_column = ctypes.create_string_buffer(column)
            v_column = ADDR(c_column)
            l_column = len(c_column)
        
        
        



        ret = ODBC_API.SQLColumns(self.stmt_h,
                            v_catalog, l_catalog,
                            v_schema, l_schema,
                            v_table, l_table,
                            v_column, l_column)

        if not ret == SQL_SUCCESS:
            validate(ret, SQL_HANDLE_STMT, self.stmt_h)

        self.NumOfRows()
        self._GetDesc()
        self._BindCols()
        return (self)



class Connection:
    """This class implement a odbc connection. It use ctypes for work.
    """
    def __init__(self, connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
        """Init variables and connect to the engine"""
        self.connected = 0
        self.unicode_results = False
        self.dbc_h = ctypes.c_int()
        
        # Allocate an DBC handle self.dbc_h under the environment shared_env_h
        # This DBC handle is actually the basis of a "connection"
        # The handle of self.dbc_h will be used to connect to a certain source 
        # in the self.connect and self.ConnectByDSN method
        
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_DBC, shared_env_h, ADDR(self.dbc_h))
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
        
        self.unicode_results = unicode_results
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
        
        
odbc = Connection

def connect(connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
    conn = odbc(connectString, autocommit, ansi, timeout, unicode_results)
    return conn

