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
from decimal import *

DEBUG = 0
# Comment out all "if DEBUG:" statements like below for production
if DEBUG: print 'DEBUGGING'


# Set the library location on linux 
library = "/usr/lib/libodbc.so"


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


# Define ODBC constants. They are widly used in ODBC documents and programs
# They are defined in cpp header files: sql.h sqlext.h sqltypes.h sqlucode.h
# and you can get these files from the mingw32-runtime_3.13-1_all.deb package
SQL_ATTR_ODBC_VERSION, SQL_OV_ODBC2, SQL_OV_ODBC3 = 200, 2, 3
SQL_DRIVER_NOPROMPT = 0
SQL_FETCH_NEXT, SQL_FETCH_FIRST, SQL_FETCH_LAST = 0x01, 0x02, 0x04
SQL_NULL_HANDLE, SQL_HANDLE_ENV, SQL_HANDLE_DBC, SQL_HANDLE_STMT = 0, 1, 2, 3
SQL_SUCCESS, SQL_SUCCESS_WITH_INFO = 0, 1
SQL_ATTR_AUTOCOMMIT = 102
SQL_AUTOCOMMIT_OFF, SQL_AUTOCOMMIT_ON = 0, 1
SQL_IS_UINTEGER = -5
SQL_ATTR_LOGIN_TIMEOUT = 103
SQL_COMMIT, SQL_ROLLBACK = 0, 1

SQL_INDEX_UNIQUE,SQL_INDEX_ALL = 0,1
SQL_QUICK,SQL_ENSURE = 0,1
SQL_FETCH_NEXT = 1
SQL_COLUMN_DISPLAY_SIZE = 6
SQL_INVALID_HANDLE = -2
SQL_NO_DATA_FOUND = 100
SQL_NULL_DATA = -1
SQL_HANDLE_DESCR = 4
SQL_TABLE_NAMES = 3
SQL_PARAM_INPUT = 1
SQL_PARAM_INPUT_OUTPUT = 2
SQL_RESET_PARAMS = 3
SQL_UNBIND = 2
SQL_CLOSE = 0

SQL_TYPE_NULL = 0
SQL_DECIMAL = 3
SQL_FLOAT = 6
SQL_DATE = 9
SQL_TIME = 10
SQL_TIMESTAMP = 11
SQL_VARCHAR = 12
SQL_LONGVARCHAR = -1
SQL_VARBINARY = -3
SQL_LONGVARBINARY = -4
SQL_BIGINT = -5
SQL_WVARCHAR = -9
SQL_WLONGVARCHAR = -10
SQL_ALL_TYPES = 0

SQL_C_CHAR =            SQL_CHAR =          1
SQL_C_NUMERIC =         SQL_NUMERIC =       2
SQL_C_LONG =            SQL_INTEGER =       4
SQL_C_SHORT =           SQL_SMALLINT =      5
SQL_C_FLOAT =           SQL_REAL =          7
SQL_C_DOUBLE =          SQL_DOUBLE =        8
SQL_C_TYPE_DATE =       SQL_TYPE_DATE =     91
SQL_C_TYPE_TIME =       SQL_TYPE_TIME =     92
SQL_C_BINARY =          SQL_BINARY =        -2
SQL_C_TINYINT =         SQL_TINYINT =       -6
SQL_C_BIT =             SQL_BIT =           -7
SQL_C_WCHAR =           SQL_WCHAR =         -8
SQL_C_TYPE_TIMESTAMP =  SQL_TYPE_TIMESTAMP = 93

SQL_DESC_DISPLAY_SIZE = SQL_COLUMN_DISPLAY_SIZE

def dttm_cvt(x):
    if x == '': return None
    else: return datetime.datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]),int(x[10:13]),int(x[14:16]),int(x[17:19]))

def tm_cvt(x):
    if x == '': return None
    else: return datetime.time(int(x[0:2]),int(x[3:5]),int(x[6:8]))

def dt_cvt(x):
    if x == '': return None
    else: return datetime.datetime(int(x[0:4]),int(x[5:7]),int(x[8:10]))

def create_buffer_u(len):
    return ctypes.create_unicode_buffer(len)

def create_buffer(len):
    return ctypes.create_string_buffer(len)

# Below Datatype mappings referenced the document at
# http://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.help.sdk_12.5.1.aseodbc/html/aseodbc/CACFDIGH.htm
SqlTypes = { \
SQL_TYPE_NULL       : (None,                lambda x: None,             SQL_C_CHAR,         create_buffer), 
SQL_CHAR            : (str,                 lambda x: x,                SQL_C_CHAR,         create_buffer),
SQL_NUMERIC         : (Decimal,             Decimal,                    SQL_C_CHAR,         create_buffer),
SQL_DECIMAL         : (Decimal,             Decimal,                    SQL_C_CHAR,         create_buffer),
SQL_INTEGER         : (int,                 long,                       SQL_C_LONG,         lambda x:ctypes.c_long()),
SQL_SMALLINT        : (int,                 long,                       SQL_C_SHORT,        lambda x:ctypes.c_short()),
SQL_FLOAT           : (float,               float,                      SQL_C_FLOAT,        lambda x:ctypes.c_float()),
SQL_REAL            : (float,               float,                      SQL_C_FLOAT,        lambda x:ctypes.c_float()),
SQL_DOUBLE          : (float,               float,                      SQL_C_DOUBLE,       lambda x:ctypes.c_double()),
SQL_DATE            : (datetime.date,       dt_cvt,                     SQL_C_CHAR ,        create_buffer),
SQL_TIME            : (datetime.time,       tm_cvt,                     SQL_C_CHAR,         create_buffer),
SQL_TIMESTAMP       : (datetime.datetime,   dttm_cvt,                   SQL_C_CHAR,         create_buffer),
SQL_VARCHAR         : (str,                 lambda x: x,                SQL_C_CHAR,         create_buffer),
SQL_LONGVARCHAR     : (str,                 lambda x: x,                SQL_C_CHAR,         create_buffer),
SQL_BINARY          : (bytearray,           lambda x: bytearray(x),     SQL_C_BINARY,       create_buffer),
SQL_VARBINARY       : (bytearray,           lambda x: bytearray(x),     SQL_C_BINARY,       create_buffer),
SQL_LONGVARBINARY   : (bytearray,           lambda x: bytearray(x),     SQL_C_BINARY,       create_buffer),
SQL_BIGINT          : (int,                 long,                       SQL_C_LONG,         lambda x:ctypes.c_long()),
SQL_TINYINT         : (int,                 long,                       SQL_C_TINYINT,      lambda x:ctypes.c_short()),
SQL_BIT             : (bool,                bool,                       SQL_C_BIT,          lambda x:ctypes.c_short()),
SQL_WCHAR           : (unicode,             lambda x: x,                SQL_C_WCHAR,        create_buffer_u),
SQL_WVARCHAR        : (unicode,             lambda x: x,                SQL_C_WCHAR,        create_buffer_u),
SQL_WLONGVARCHAR    : (unicode,             lambda x: x,                SQL_C_WCHAR,        create_buffer_u),
SQL_TYPE_DATE       : (datetime.date,       dt_cvt,                     SQL_C_CHAR,         create_buffer),
SQL_TYPE_TIME       : (datetime.time,       tm_cvt,                     SQL_C_CHAR,         create_buffer),
SQL_TYPE_TIMESTAMP  : (datetime.datetime,   dttm_cvt,                   SQL_C_CHAR,         create_buffer), 
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
class ProgrammingError(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)


class DataError(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)


class IntegrityError(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)

class NotSupportedError(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)


class DatabaseError(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)


class OperationalError(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)


class Error(Exception):
    def __init__(self, error_code, error_desc):
        self.value = (error_code, error_desc)
        self.args = (error_code, error_desc)




# Define the python return type for ODBC functions with ret result.
funcs_with_ret = ["SQLNumParams","SQLBindParameter","SQLExecute","SQLNumResultCols","SQLDescribeCol","SQLColAttribute",
        "SQLGetDiagRec","SQLAllocHandle","SQLSetEnvAttr","SQLExecDirect","SQLExecDirectW","SQLRowCount",
        "SQLFetch","SQLBindCol","SQLCloseCursor","SQLSetConnectAttr","SQLDriverConnect","SQLDriverConnectW",
        "SQLConnect","SQLTables","SQLStatistics","SQLFetchScroll",
        "SQLDataSources","SQLFreeHandle","SQLFreeStmt","SQLDisconnect","SQLEndTran","SQLPrepare","SQLPrepareW",
        "SQLDescribeParam","SQLGetTypeInfo","SQLPrimaryKeys","SQLForeignKeys","SQLProcedures"]
for func_name in funcs_with_ret: getattr(ODBC_API,func_name).restype = ctypes.c_short



# Set the alias for the ctypes functions for beter code readbility or performance.
ADDR = ctypes.byref
SQLFetch = ODBC_API.SQLFetch
SQLFetch.argtypes = [ctypes.c_int]
SQLExecute = ODBC_API.SQLExecute
SQLExecute.argtypes = [ctypes.c_int]
SQLBindParameter = ODBC_API.SQLBindParameter


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
            if DEBUG: print err_list[0][1]
            state = err_list[0][0]
            if state[:2] in ('24','25','42'):
                raise ProgrammingError(state,'['+state+'] '+err_list[0][1])
            elif state[:2] in ('22'):
                raise DataError(state,'['+state+'] '+err_list[0][1])
            elif state[:2] in ('23') or state == '40002':
                raise IntegrityError(state,'['+state+'] '+err_list[0][1])
            elif state == '0A000':
                raise NotSupportedError(state,'['+state+'] '+err_list[0][1])
            elif state in ('HYT00','HYT01'):
                raise OperationalError(state,'['+state+'] '+err_list[0][1])
            elif state[:2] in ('IM','HY'):
                raise Error(state,'['+state+'] '+err_list[0][1])
            else:
                raise DatabaseError(state,'['+state+'] '+err_list[0][1])
            break
        elif ret == SQL_INVALID_HANDLE:
            #The handle passed is an invalid handle
            raise OdbcInvalidHandle, 'SQL_INVALID_HANDLE'
        elif ret == SQL_SUCCESS:
            err_list.append((state.value, Message.value, NativeError.value))
            number_errors += 1

            
def validate(ret, handle_type, handle):
    """ Validate return value, if not success, raise exceptions based on the handle """
    if ret not in (SQL_SUCCESS, SQL_SUCCESS_WITH_INFO):
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


version = '0.50 alpha'

class ROW(list):
    pass
#
#The Cursor Class.
class Cursor:
    def __init__(self, conx):
        """ Initialize self._stmt_h, which is the handle of a statement
        A statement is actually the basis of a python"cursor" object
        """
        self.connection = conx
        self.statement = None
        self._last_param_types = None
        self._ParamBufferList = []
        self._ColBufferList = []
        self._buf_cvt_func = []
        self.rowcount = None
        self.description = None
        self.autocommit = None
        self._ColTypeCodeList = []
        self._outputsize = {}
        self._inputsizers = []
        self._stmt_h = ctypes.c_int()
        self.setoutputsize(512000) #512KB as the defalt buffer size for large column
        ret = ODBC_API.SQLAllocHandle(SQL_HANDLE_STMT, self.connection.dbc_h, ADDR(self._stmt_h))
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        self.closed = False
     
    
    def setoutputsize(self, size, column = None):
        self._outputsize[column] = size


    
    def _BindCols(self):
        '''Bind buffers for the record set columns'''
        NOC = self.NumOfCols()
        col_buffer_list = []
    
        for col_num in range(NOC):
            col_name = self.description[col_num][0]
            col_type_code = self._ColTypeCodeList[col_num]
            total_buf_len = self.description[col_num][2] + 1
            
            # if it's a long data col_num, we enlarge the buffer to predefined length.
            if total_buf_len > 1024000 or total_buf_len < 0: #1MB
                default_output_size = self._outputsize[None]
                total_buf_len = self._outputsize.get(col_num,default_output_size)
                

            
            alloc_buffer = SqlTypes[col_type_code][3](total_buf_len)
            used_buf_len = ctypes.c_long()
            
            target_type = SqlTypes[col_type_code][2]
            force_unicode = self.connection.unicode_results
    
            if force_unicode and col_type_code in (SQL_CHAR,SQL_VARCHAR,SQL_LONGVARCHAR):
                target_type = SQL_C_WCHAR
                alloc_buffer = create_buffer_u(total_buf_len)
            
            ret = ODBC_API.SQLBindCol(self._stmt_h, col_num + 1, target_type, ADDR(alloc_buffer), total_buf_len,\
                ADDR(used_buf_len))
            validate(ret, SQL_HANDLE_STMT, self._stmt_h)
            buf_cvt_func = SqlTypes[self._ColTypeCodeList[col_num]][1]
            col_buffer_list.append((col_name,alloc_buffer,used_buf_len,buf_cvt_func, target_type))
            #self.__bind(col_num + 1, col_buffer_list[col_num], buff_id)
        self._ColBufferList = col_buffer_list
        
    
    def _BindParams(self, param_types):
        """Create parameter buffers based on param types, and bind them to the statement"""
        # Get the number of query parameters judged by database.
        NumParams = ctypes.c_int()
        ret = ODBC_API.SQLNumParams(self._stmt_h, ADDR(NumParams))
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
        if len(param_types) != NumParams.value:
            # In case number of parameters provided do not same as number required
            error_desc = "The SQL contains %d parameter markers, but %d parameters were supplied" \
                        %(NumParams.value,len(param_types))
            raise ProgrammingError(error_desc,'HY000')
        
        
        # Every parameter needs to be binded to a buffer
        ParamBufferList = []
        for col_num in range(NumParams.value):
            '''
            DataType = ctypes.c_int()
            ParamSize = ctypes.c_long()
            DecimalDigits = ctypes.c_short()
            Nullable = ctypes.c_bool()                        
            ret = ODBC_API.SQLDescribeParam(self._stmt_h, col_num + 1, ADDR(DataType), ADDR(ParamSize), \
                ADDR(DecimalDigits), ADDR(Nullable))
            validate(ret, SQL_HANDLE_STMT, self._stmt_h)
            '''
            prec = 0
            buf_size = 512
        
            if param_types[col_num] == int:
                sql_c_type = SQL_C_LONG             
                sql_type = SQL_INTEGER
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.c_long()
                
                
            elif param_types[col_num] == float:
                sql_c_type = SQL_C_DOUBLE
                sql_type = SQL_DOUBLE
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.c_double()
                
                
            elif param_types[col_num] == Decimal:
                sql_c_type = SQL_C_DOUBLE
                sql_type = SQL_DOUBLE
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.c_double()
                
                
            elif param_types[col_num] == datetime.datetime:
                sql_c_type = SQL_C_CHAR
                sql_type = SQL_TYPE_TIMESTAMP
                buf_size = self.connection.type_size_dic[SQL_TYPE_TIMESTAMP][0]
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.create_string_buffer(buf_size)
                prec = self.connection.type_size_dic[SQL_TYPE_TIMESTAMP][1]
                
                
            elif param_types[col_num] == datetime.date:
                sql_c_type = SQL_C_CHAR
                if self.connection.type_size_dic.has_key(SQL_TYPE_DATE):
                    if DEBUG: print 'conx.type_size_dic.has_key(SQL_TYPE_DATE)'
                    sql_type = SQL_TYPE_DATE
                    buf_size = self.connection.type_size_dic[SQL_TYPE_DATE][0]
                    self._inputsizers.append(buf_size)
                    ParameterBuffer = ctypes.create_string_buffer(buf_size)
                    prec = self.connection.type_size_dic[SQL_TYPE_DATE][1]
                    
                else:
                    #SQL Sever use -9 to represent date, instead of SQL_TYPE_DATE
                    sql_type = SQL_TYPE_TIMESTAMP 
                    buf_size = 10
                    self._inputsizers.append(buf_size)
                    ParameterBuffer = ctypes.create_string_buffer(buf_size)
                    

            elif param_types[col_num] == datetime.time:
                sql_c_type = SQL_C_CHAR
                if self.connection.type_size_dic.has_key(SQL_TYPE_TIME):
                    sql_type = SQL_TYPE_TIME
                    buf_size = self.connection.type_size_dic[SQL_TYPE_TIME][0]
                    self._inputsizers.append(buf_size)
                    ParameterBuffer = ctypes.create_string_buffer(buf_size)
                    prec = self.connection.type_size_dic[SQL_TYPE_TIME][1]
                    
                    
                else:
                    sql_type = SQL_TYPE_TIMESTAMP #SQL Sever use -9 to represent date, instead of SQL_TYPE_DATE
                    buf_size = self.connection.type_size_dic[SQL_TYPE_TIMESTAMP][0]
                    self._inputsizers.append(buf_size)
                    ParameterBuffer = ctypes.create_string_buffer(buf_size)
                    prec = 3
                    
                    
            elif param_types[col_num] == unicode:
                sql_c_type = SQL_C_WCHAR
                sql_type = SQL_WLONGVARCHAR 
                buf_size = 102400 #100kB
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.create_unicode_buffer(buf_size)
                
                

            elif param_types[col_num] == bytearray:
                sql_c_type = SQL_C_BINARY
                sql_type = SQL_LONGVARBINARY 
                buf_size = 102400 #100kB
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.create_string_buffer(buf_size)
                
                
            else:
                sql_c_type = SQL_C_CHAR
                sql_type = SQL_LONGVARCHAR
                buf_size = 102400 #100kB
                self._inputsizers.append(buf_size)
                ParameterBuffer = ctypes.create_string_buffer(buf_size)
                
            BufferLen = ctypes.c_long(buf_size)
            LenOrIndBuf = ctypes.c_long()
                
            if param_types[col_num] in (unicode,str):
                ret = SQLBindParameter(self._stmt_h, col_num + 1, SQL_PARAM_INPUT, sql_c_type, sql_type, buf_size,\
                        prec, ADDR(ParameterBuffer), ADDR(BufferLen),None)
            else:
                ret = SQLBindParameter(self._stmt_h, col_num + 1, SQL_PARAM_INPUT, sql_c_type, sql_type, buf_size,\
                        prec, ADDR(ParameterBuffer), ADDR(BufferLen),ADDR(LenOrIndBuf))
            if ret != SQL_SUCCESS:    
                validate(ret, SQL_HANDLE_STMT, self._stmt_h)
            # Append the value buffer and the lenth buffer to the array
            ParamBufferList.append((ParameterBuffer,LenOrIndBuf))
                
        self._last_param_types = param_types
        self._ParamBufferList = ParamBufferList
    
            
            
            
            
    
    def execute(self, query_string, params = None, execute_many_mode = False):
        """ Execute the query string, with optional parameters.
        If parameters are provided, the query would first be prepared, then executed with parameters;
        If parameters are not provided, only th query sting, it would be executed directly 
        """
        if params != None:
            # If parameters exist, first prepare the query then executed with parameters
            if not type(params) in (tuple, list):
                raise TypeError("Params must be in a list, tuple, or Row")
            
            if not execute_many_mode:
                if query_string != self.statement:
                    # if the query is not same as last query, then it is not prepared
                    self.prepare(query_string)
                    
            param_types = [type(p) for p in params]
            if param_types != self._last_param_types:
                self._BindParams(param_types)
            
            # With query prepared, now put parameters into buffers
            col_num = 0
            for param_buffer, param_buffer_len in self._ParamBufferList:
                c_char_buf, c_buf_len = '', 0
                param_val = params[col_num]
                if param_val == None:
                    c_buf_len = -1
                elif type(param_val) == datetime.datetime:
                    c_buf_len = self.connection.type_size_dic[SQL_TYPE_TIMESTAMP][0]
                    datetime_str = param_val.isoformat().replace('T',' ') 
                    if len(datetime_str) == 19:
                        datetime_str += '.000'
                    c_char_buf = datetime_str[:c_buf_len]
                    if DEBUG: print c_buf_len, c_char_buf
                elif type(param_val) == datetime.date:
                    if self.connection.type_size_dic.has_key(SQL_TYPE_DATE):
                        c_buf_len = self.connection.type_size_dic[SQL_TYPE_DATE][0]
                    else:
                        c_buf_len = 10
                    c_char_buf = param_val.isoformat()[:c_buf_len]
                    if DEBUG: print c_char_buf
                elif type(param_val) == datetime.time:
                    if self.connection.type_size_dic.has_key(SQL_TYPE_TIME):
                        c_buf_len = self.connection.type_size_dic[SQL_TYPE_TIME][0]
                        c_char_buf = param_val.isoformat()[0:c_buf_len]
                    else:
                        c_buf_len = self.connection.type_size_dic[SQL_TYPE_TIMESTAMP][0]
                        time_str = param_val.isoformat()
                        if len(time_str) == 8:
                            time_str += '.000'
                        c_char_buf = '1900-01-01 '+time_str[0:c_buf_len - 11]
                    if DEBUG: print c_buf_len, c_char_buf
                elif type(param_val) == Decimal:
                    c_char_buf = float(param_val)
                    
                elif type(param_val) == str:
                    c_char_buf = param_val
                    
                elif type(param_val) == unicode:
                    c_char_buf = param_val
                    
                elif type(param_val) == bytearray:
                    c_char_buf = str(param_val)
                    c_buf_len = len(c_char_buf)
                    
                else:
                    c_char_buf = param_val
            

                if type(param_val) in (bytearray,):
                    param_buffer.raw = c_char_buf
                else:
                    param_buffer.value = c_char_buf
                    
                if type(param_val) not in (unicode,str):
                    #ODBC driver will find NUL in unicode and string to determine their length
                    param_buffer_len.value = c_buf_len

                col_num += 1

            self.SQLExecute()
            if not execute_many_mode:
                self.NumOfRows()
                self._UpdateDesc()
                self._BindCols()
            
        else:
            self.execdirect(query_string)
        return (self)
    
    def SQLExecute(self):
        ret = SQLExecute(self._stmt_h)
        if ret != SQL_SUCCESS:
            validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
    
    def executemany(self, query_string, params_list = [None]):
        self.prepare(query_string)
        for params in params_list:
            self.execute(query_string, params, execute_many_mode = True)
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        
            
            
    def prepare(self, query_string):
        """prepare a query"""
        if type(query_string) == unicode:
            ret = ODBC_API.SQLPrepareW(self._stmt_h, query_string, len(query_string))
        else:
            ret = ODBC_API.SQLPrepare(self._stmt_h, query_string, len(query_string))
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        self.statement = query_string
        
    
    def execdirect(self, query_string):
        """Execute a query directly"""
        if type(query_string) == unicode:
            ret = ODBC_API.SQLExecDirectW(self._stmt_h, query_string, len(query_string))
        else:
            ret = ODBC_API.SQLExecDirect(self._stmt_h, query_string, len(query_string))
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)
        
        
    
    def _UpdateDesc(self):
        "Get the information of (name, type_code, display_size, internal_size, precision, scale, null_ok)"  
        Cname = ctypes.create_string_buffer(1024)
        Cname_ptr = ctypes.c_int()
        Ctype_code = ctypes.c_short()
        Csize = ctypes.c_int()
        Cdisp_size = ctypes.c_int(0)
        Cprecision = ctypes.c_int()
        Cnull_ok = ctypes.c_int()
        ColDescr = []
        self._ColTypeCodeList = []
        NOC = self.NumOfCols()
        for col in range(1, NOC+1):
            ret = ODBC_API.SQLColAttribute(self._stmt_h, col, SQL_DESC_DISPLAY_SIZE, ADDR(ctypes.create_string_buffer(10)), 
                10, ADDR(ctypes.c_int()),ADDR(Cdisp_size))
            validate(ret, SQL_HANDLE_STMT, self._stmt_h)
            
            ret = ODBC_API.SQLDescribeCol(self._stmt_h, col, ADDR(Cname), len(Cname), ADDR(Cname_ptr),\
                ADDR(Ctype_code),ADDR(Csize),ADDR(Cprecision), ADDR(Cnull_ok))
            validate(ret, SQL_HANDLE_STMT, self._stmt_h)
            
            
            ColDescr.append((Cname.value, SqlTypes.get(Ctype_code.value,(Ctype_code.value))[0],Cdisp_size.value,\
                Csize.value,Cprecision.value, None,Cnull_ok.value == 1 and True or False))
            self._ColTypeCodeList.append(Ctype_code.value)
        self.description = ColDescr
        
    
    def NumOfRows(self):
        """Get the number of rows"""
        NOR = ctypes.c_int()
        ret = ODBC_API.SQLRowCount(self._stmt_h, ADDR(NOR))
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        self.rowcount = NOR.value
        return self.rowcount    

    
    def NumOfCols(self):
        """Get the number of cols"""
        NOC = ctypes.c_int()
        ret = ODBC_API.SQLNumResultCols(self._stmt_h, ADDR(NOC))
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        return NOC.value
    

    def fetchmany(self, num):
        return self.__fetch(num)


    def fetchone(self):
        ret = SQLFetch(self._stmt_h)
        if ret != SQL_SUCCESS:
            if ret == SQL_NO_DATA_FOUND:
                return (None)
            else:
                validate(ret, SQL_HANDLE_STMT, self._stmt_h)
            
        row = ROW()
        
        for col_name, buf_value, buf_len, cvt_func,target_type in self._ColBufferList:
            if buf_len.value != SQL_NULL_DATA:
                if target_type == SQL_C_BINARY:
                    row.append(cvt_func(buf_value.raw[:buf_len.value]))
                else:
                    row.append(cvt_func(buf_value.value))
                
            else:
                row.append(None)
            setattr(row,col_name,row[-1])

        return (row)
    
    
    def fetchall(self):
        return self.__fetch()


    def skip(self, count = 0):
        for i in xrange(count):
            ret = ODBC_API.SQLFetchScroll(self._stmt_h, SQL_FETCH_NEXT, 0)
            if ret != SQL_SUCCESS:
                validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        return None
    
    def __fetch(self, num = 0):
        rows = []
        row_num = 0
        # limit to num time loops, or loop until no data if num == 0
        while num == 0 or row_num < num:
            ret = SQLFetch(self._stmt_h)
            if ret != SQL_SUCCESS:
                if ret == SQL_NO_DATA_FOUND:
                    break
                else:
                    validate(ret, SQL_HANDLE_STMT, self._stmt_h)
                
            row = ROW()
            
            for col_name, buf_value, buf_len, cvt_func, target_type in self._ColBufferList:
                if buf_len.value != SQL_NULL_DATA:
                    if target_type == SQL_C_BINARY:
                        row.append(cvt_func(buf_value.raw[:buf_len.value]))
                    else:
                        row.append(cvt_func(buf_value.value))
    

                else:
                    row.append(None)
                setattr(row,col_name,row[-1])
            
                
            rows.append(row)
            row_num += 1
        return rows
    
        
    def close(self):
        """ Call SQLCloseCursor API to free the statement handle"""
        
        ret = ODBC_API.SQLCloseCursor(self._stmt_h)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
        ret = ODBC_API.SQLFreeStmt(self._stmt_h, SQL_CLOSE)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)

        ret = ODBC_API.SQLFreeStmt(self._stmt_h, SQL_UNBIND)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)

        ret = ODBC_API.SQLFreeStmt(self._stmt_h, SQL_RESET_PARAMS)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)

        ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_STMT, self._stmt_h)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
        self.closed = True
        return
    
    
    def __del__(self):  
        if not self.closed:
            if DEBUG: print 'auto closing cursor: ',
            try:
                self.close()
            except:
                if DEBUG: print 'failed'
                pass
            else:
                if DEBUG: print 'succeed'
                pass
    
    
    def getTypeInfo(self, sqlType = None):
        if sqlType == None:
            type = SQL_ALL_TYPES
        else:
            type = sqlType
        ret = ODBC_API.SQLGetTypeInfo(self._stmt_h, type)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
    
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)

    def statistics(self, table, catalog=None, schema=None, unique=False, quick=True):
        l_table = l_catalog = l_schema = 0

        if catalog != None: l_catalog = len(catalog)
        if schema != None: l_schema = len(schema)
        if table != None: l_table = len(table)
        if unique:
            Unique = SQL_INDEX_UNIQUE
        else:
            Unique = SQL_INDEX_ALL
        if quick:
            Reserved = SQL_QUICK
        else:
            Reserved = SQL_ENSURE

        ret = ODBC_API.SQLStatistics(self._stmt_h,
                                catalog, l_catalog,
                                schema, l_schema, 
                                table, l_table,
                                Unique, Reserved)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)

        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)


    
    def tables(self, table=None, catalog=None, schema=None, tableType=None):
        """Return a list with all tables""" 
        l_catalog = l_schema = l_table = l_tableType = 0
        
        if catalog != None: l_catalog = len(catalog)
        if schema != None: l_schema = len(schema)
        if table != None: l_table = len(table)
        if tableType != None: l_tableType = len(tableType)
        
        
        ret = ODBC_API.SQLTables(self._stmt_h,
                                catalog, l_catalog,
                                schema, l_schema, 
                                table, l_table,
                                tableType, l_tableType)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
    
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)
    
    
    def columns(self, table=None, catalog=None, schema=None, column=None):
        """Return a list with all columns"""        
        l_catalog = l_schema = l_table = l_column = 0
        if catalog != None: l_catalog = len(catalog)
        if schema != None: l_schema = len(schema)
        if table != None: l_table = len(table)
        if column != None: l_column = len(column)

        ret = ODBC_API.SQLColumns(self._stmt_h,
                            catalog, l_catalog,
                            schema, l_schema,
                            table, l_table,
                            column, l_column)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)

        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)
    
    def primaryKeys(self, table=None, catalog=None, schema=None):
        l_catalog = l_schema = l_table = 0
        if catalog != None: l_catalog = len(catalog)
        if schema != None: l_schema = len(schema)
        if table != None: l_table = len(table)
        
        ret = ODBC_API.SQLPrimaryKeys(self._stmt_h,
                            catalog, l_catalog,
                            schema, l_schema,
                            table, l_table)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)
        
    def foreignKeys(self, table=None, catalog=None, schema=None, foreignTable=None, foreignCatalog=None, foreignSchema=None):
        l_catalog = l_schema = l_table = l_foreignTable = l_foreignCatalog = l_foreignSchema = 0
        if catalog != None: l_catalog = len(catalog)
        if schema != None: l_schema = len(schema)
        if table != None: l_table = len(table)
        if foreignTable != None: l_foreignTable = len(foreignTable)
        if foreignCatalog != None: l_foreignCatalog = len(foreignCatalog)
        if foreignSchema != None: l_foreignSchema = len(foreignSchema)
        
        ret = ODBC_API.SQLForeignKeys(self._stmt_h,
                            catalog, l_catalog,
                            schema, l_schema,
                            table, l_table,
                            foreignCatalog, l_foreignCatalog,
                            foreignSchema, l_foreignSchema,
                            foreignTable, l_foreignTable)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)
    
    def procedures(self, procedure=None, catalog=None, schema=None):
        l_catalog = l_schema = l_procedure = 0
        if catalog != None: l_catalog = len(catalog)
        if schema != None: l_schema = len(schema)
        if procedure != None: l_procedure = len(procedure)
        
        ret = ODBC_API.SQLProcedures(self._stmt_h,
                            catalog, l_catalog,
                            schema, l_schema,
                            procedure, l_proceduree)
        validate(ret, SQL_HANDLE_STMT, self._stmt_h)
        
        self.NumOfRows()
        self._UpdateDesc()
        self._BindCols()
        return (self)
        
        
        

class Connection:
    """This class implement a odbc connection. It use ctypes for work."""
    def __init__(self, connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
        """Init variables and connect to the engine"""
        self.connected = 0
        self.type_size_dic = {}
        self.unicode_results = False
        self.dbc_h = ctypes.c_int()
        self.autocommit = False
        
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

        # Before we establish the connection by the connection string
        # Set the connection's attribute of "timeout" (Actully LOGIN_TIMEOUT)
        if timeout != 0:
            ret = ODBC_API.SQLSetConnectAttr(self.dbc_h, SQL_ATTR_LOGIN_TIMEOUT, timeout, SQL_IS_UINTEGER);
            validate(ret, SQL_HANDLE_DBC, self.dbc_h)


        # Create one connection with a connect string by calling SQLDriverConnect
        # and make self.dbc_h the handle of this connection


        # Convert the connetsytring to encoded string
        # so it can be converted to a ctypes c_char array object 
        self.connectString = connectString
        if type(self.connectString) == unicode:
            c_connectString = ctypes.create_unicode_buffer(self.connectString)
            ret = ODBC_API.SQLDriverConnectW(self.dbc_h, 0, c_connectString, len(c_connectString), 0, 0, 0, SQL_DRIVER_NOPROMPT)
        else:
            c_connectString = ctypes.create_string_buffer(self.connectString)
            ret = ODBC_API.SQLDriverConnect(self.dbc_h, 0, c_connectString, len(c_connectString), 0, 0, 0, SQL_DRIVER_NOPROMPT)
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
            
        
        # Set the connection's attribute of "autocommit" 
        #
        
        self.autocommit = autocommit
        
        ret = ODBC_API.SQLSetConnectAttr(self.dbc_h, SQL_ATTR_AUTOCOMMIT, self.autocommit and SQL_AUTOCOMMIT_ON or SQL_AUTOCOMMIT_OFF, SQL_IS_UINTEGER)
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        
        self.unicode_results = unicode_results
        self.update_type_size_info()
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

        self.update_type_size_info()
        self.connected = 1
        
    def cursor(self):
        return Cursor(self)   

    def update_type_size_info(self):
        #Get the scale information for SQL_TYPE_TIMESTAMP
        cur = Cursor(self)
        info_tuple = cur.getTypeInfo(SQL_TYPE_TIMESTAMP).fetchone()
        if info_tuple != None:
            self.type_size_dic[SQL_TYPE_TIMESTAMP] = info_tuple[2], info_tuple[13]
        cur.close()
        
        cur = Cursor(self)
        info_tuple = cur.getTypeInfo(SQL_TYPE_TIME).fetchone()
        if info_tuple != None:        
            self.type_size_dic[SQL_TYPE_TIME] = info_tuple[2], info_tuple[13]
        cur.close()
        
        
        cur = Cursor(self)
        if DEBUG: print 'SQL_TYPE_DATE:',
        info_tuple = cur.getTypeInfo(SQL_TYPE_DATE).fetchone()
        if info_tuple != None:        
            self.type_size_dic[SQL_TYPE_DATE] = info_tuple[2], info_tuple[13]
            
            if DEBUG: print info_tuple[2], info_tuple[13]
        cur.close()
        
        
        cur = Cursor(self)
        info_tuple = cur.getTypeInfo(SQL_TIME).fetchone()
        if info_tuple != None:        
            self.type_size_dic[SQL_TIME] = info_tuple[2], info_tuple[13]
        cur.close()

    
    def commit(self):
        ret = ODBC_API.SQLEndTran(SQL_HANDLE_DBC, self.dbc_h, SQL_COMMIT);
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)

    def rollback(self):
        ret = ODBC_API.SQLEndTran(SQL_HANDLE_DBC, self.dbc_h, SQL_ROLLBACK);
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)

    def __del__(self):
        if self.connected:
            self.close()
        
    def close(self):
        if self.connected:
            if DEBUG: print 'disconnect'
            if not self.autocommit:
                self.rollback()
            ret = ODBC_API.SQLDisconnect(self.dbc_h)
            validate(ret, SQL_HANDLE_DBC, self.dbc_h)
        if DEBUG: print 'free dbc'
        ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_DBC, self.dbc_h)
        validate(ret, SQL_HANDLE_DBC, self.dbc_h)
#        if shared_env_h.value:
#            if DEBUG: print 'env'
#            ret = ODBC_API.SQLFreeHandle(SQL_HANDLE_ENV, shared_env_h)
#            validate(ret, SQL_HANDLE_ENV, shared_env_h)
        self.connected = 0
        
odbc = Connection



def connect(connectString, autocommit = False, ansi = False, timeout = 0, unicode_results = False):
    return odbc(connectString, autocommit, ansi, timeout, unicode_results)


def win_create_mdb(mdb_path):
    c_Path = "CREATE_DB="+mdb_path+" General\0\0"
    ODBC_ADD_SYS_DSN = 1
    ctypes.windll.ODBCCP32.SQLConfigDataSource(None,ODBC_ADD_SYS_DSN,"Microsoft Access Driver (*.mdb)", c_Path)

