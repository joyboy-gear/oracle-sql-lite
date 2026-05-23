#!/usr/bin/env python3
"""
Oracle SQL*Lite
A dummy Oracle DBMS simulator with tkinter GUI.
Light theme with classic Oracle editor style, worksheet panels.
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font as tkfont
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict, Any
import random
import time


# ── Constants ──────────────────────────────────────────────────────

FONT_FAMILY = "Courier New"
FONT_SIZE = 10
FONT = (FONT_FAMILY, FONT_SIZE)
FONT_BOLD = (FONT_FAMILY, FONT_SIZE, "bold")
FONT_ITALIC = (FONT_FAMILY, FONT_SIZE, "italic")

COLOR_BG = "#F5F5F5"
COLOR_EDITOR_BG = "#FFFFFF"
COLOR_OUTPUT_BG = "#FCFCFC"
COLOR_LINE_NUM_BG = "#F8F8F8"
COLOR_LINE_NUM_FG = "#999999"
COLOR_KEYWORD = "#1A1AE8"
COLOR_STRING = "#228B22"
COLOR_NUMBER = "#B22222"
COLOR_COMMENT = "#5F9EA0"
COLOR_PROMPT = "#C74634"
COLOR_ERROR = "#D32F2F"
COLOR_SUCCESS = "#2E7D32"
COLOR_TAB_BG = "#ECECEC"
COLOR_TAB_ACTIVE = "#FFFFFF"
COLOR_STATUS_BG = "#E8E8E8"
COLOR_ACCENT = "#C74634"
COLOR_BORDER = "#D0D0D0"

SQL_KEYWORDS = {
    'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET',
    'DELETE', 'CREATE', 'TABLE', 'DROP', 'ALTER', 'VIEW', 'SEQUENCE',
    'PROCEDURE', 'FUNCTION', 'TRIGGER', 'PACKAGE', 'BODY', 'DECLARE',
    'BEGIN', 'END', 'EXCEPTION', 'IF', 'THEN', 'ELSE', 'ELSIF', 'END IF',
    'LOOP', 'FOR', 'WHILE', 'EXIT', 'CONTINUE', 'RETURN', 'CURSOR',
    'OPEN', 'FETCH', 'CLOSE', 'INTO', 'OF', 'IS', 'AS', 'LANGUAGE',
    'NOT', 'AND', 'OR', 'IN', 'LIKE', 'BETWEEN', 'IS', 'NULL', 'EXISTS',
    'ALL', 'ANY', 'SOME', 'UNION', 'INTERSECT', 'MINUS', 'DISTINCT',
    'ORDER', 'BY', 'ASC', 'DESC', 'GROUP', 'HAVING', 'COUNT', 'SUM',
    'AVG', 'MIN', 'MAX', 'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES',
    'CONSTRAINT', 'UNIQUE', 'CHECK', 'DEFAULT', 'INDEX', 'GRANT',
    'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT', 'TRUNCATE', 'RENAME',
    'EXECUTE', 'EXEC', 'WHEN', 'THEN', 'ELSE', 'CASE', 'NVL', 'COALESCE',
    'DECODE', 'SUBSTR', 'INSTR', 'LENGTH', 'TRIM', 'TO_DATE', 'TO_CHAR',
    'TO_NUMBER', 'SYSDATE', 'SYSTIMESTAMP', 'USER', 'DUAL', 'ROWNUM',
    'ROWID', 'LEVEL', 'CONNECT', 'PRIOR', 'START', 'WITH', 'MATERIALIZED',
    'TABLESPACE', 'STORAGE', 'NEXTVAL', 'CURRVAL',
    'AUTONOMOUS_TRANSACTION', 'SERIALIZABLE', 'COMMIT', 'WORK',
    'DBMS_OUTPUT', 'PUT_LINE', 'PUT', 'NEW_LINE',
    'VARCHAR2', 'VARCHAR', 'CHAR', 'NCHAR', 'NVARCHAR2', 'NUMBER',
    'INTEGER', 'INT', 'SMALLINT', 'DECIMAL', 'FLOAT', 'DOUBLE',
    'DATE', 'TIMESTAMP', 'CLOB', 'BLOB', 'BFILE', 'LONG', 'RAW',
    'PLS_INTEGER', 'BINARY_INTEGER', 'BOOLEAN', 'SYS_REFCURSOR',
    'TYPE', 'RECORD', 'VARRAY', 'OBJECT', 'REF', 'XMLTYPE',
    'REPLACE', 'OR', 'BEFORE', 'AFTER', 'ON', 'EACH', 'ROW', 'STATEMENT',
    'REFERENCING', 'OLD', 'NEW', 'FOR', 'COMPOUND', 'INSTEAD',
    'ENABLE', 'DISABLE', 'VALIDATE', 'RELY', 'NORELY',
    'OUTER', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'NATURAL',
    'USING', 'CROSS', 'HAVING', 'CONNECT', 'PRIOR', 'START',
    'MERGE', 'MATCHED', 'WHEN', 'THEN', 'SYNONYM', 'PUBLIC',
    'GRANT', 'REVOKE', 'ROLE', 'IDENTIFIED', 'PASSWORD',
    'COLUMN', 'MODIFY', 'ADD', 'RENAME', 'CONSTRAINT',
    'PRIMARY', 'UNIQUE', 'FOREIGN', 'CHECK', 'REFERENCES', 'CASCADE',
    'RESTRICT', 'NO', 'ACTION', 'SET', 'NULL', 'DEFAULT',
    'INCREMENT', 'MINVALUE', 'MAXVALUE', 'CYCLE', 'NOCYCLE',
    'CACHE', 'NEXTVAL', 'CURRVAL', 'START', 'WITH',
    'TRIGGER', 'BEFORE', 'AFTER', 'INSTEAD', 'OF', 'EACH', 'ROW',
    'STATEMENT', 'WHEN', 'BEGIN', 'END', 'DECLARE',
    'VARIABLE', 'REF', 'OUT', 'IN', 'OUT', 'NOCOPY',
    'PRAGMA', 'AUTONOMOUS_TRANSACTION', 'EXCEPTION', 'INIT',
    'RAISE', 'RAISE_APPLICATION_ERROR', 'SQLERRM', 'SQLCODE',
    'DENSE_RANK', 'RANK', 'ROW_NUMBER', 'LAG', 'LEAD', 'FIRST_VALUE',
    'LAST_VALUE', 'OVER', 'PARTITION', 'ANALYTIC',
    'LATERAL', 'PIVOT', 'UNPIVOT',
}

# Dummy data pools
PRODUCT_NAMES = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Printer', 'Scanner',
                 'Speaker', 'Webcam', 'Tablet', 'Smartphone', 'Router', 'Cable',
                 'Hard Drive', 'SSD', 'RAM', 'Motherboard', 'GPU', 'CPU', 'Fan', 'Pendrive']
CUSTOMER_NAMES = ['John', 'Mathew', 'Leena', 'Singh', 'Raj', 'Kumar', 'Smith',
                  'David', 'Sarah', 'Emma', 'James', 'Robert', 'Maria', 'Alice',
                  'Bob', 'Charlie', 'Diana', 'Edward', 'Fiona', 'George']
SUPPLIER_NAMES = ['ABC', 'XYZ', 'PQR', 'LMN', 'DEF', 'GHI', 'JKL', 'MNO', 'STU', 'VWX']
BOAT_NAMES = ['Sea Breeze', 'Ocean Star', 'Wave Rider', 'Blue Lagoon', 'Sunset',
              'Mariner', 'Coral Reef', 'Triton', 'Neptune', 'Aquarius']
COLORS_LIST = ['Red', 'Blue', 'Green', 'White', 'Black', 'Yellow', 'Silver', 'Gold', 'Purple']
DESIGNATIONS = ['Manager', 'Analyst', 'Developer', 'Designer', 'Tester',
                'Architect', 'Consultant', 'Engineer', 'Lead', 'Director']
MALE_NAMES = ['Raju', 'Sam', 'John', 'David', 'James', 'Robert', 'Michael', 'William', 'Joseph', 'Richard']
FEMALE_NAMES = ['Sarah', 'Emma', 'Leena', 'Maria', 'Alice', 'Diana', 'Fiona', 'Helen', 'Grace', 'Irene']
BOAT_TYPES = ['D', 'S']
RATINGS = ['FAIR', 'GOOD', 'EXCELLENT']


# ── Enums and Data Classes ─────────────────────────────────────────

class StatementType(Enum):
    CREATE_TABLE = "CREATE TABLE"
    CREATE_VIEW = "CREATE VIEW"
    CREATE_PROCEDURE = "CREATE PROCEDURE"
    CREATE_FUNCTION = "CREATE FUNCTION"
    CREATE_TRIGGER = "CREATE TRIGGER"
    CREATE_SEQUENCE = "CREATE SEQUENCE"
    INSERT = "INSERT"
    SELECT = "SELECT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ALTER_TABLE = "ALTER TABLE"
    DROP_TABLE = "DROP TABLE"
    DROP_VIEW = "DROP VIEW"
    DROP_SEQUENCE = "DROP SEQUENCE"
    TRUNCATE = "TRUNCATE"
    RENAME_OBJECT = "RENAME"
    EXEC = "EXEC"
    COMMIT = "COMMIT"
    ROLLBACK = "ROLLBACK"
    SAVEPOINT = "SAVEPOINT"
    ANONYMOUS_BLOCK = "ANONYMOUS_BLOCK"
    GRANT = "GRANT"
    REVOKE = "REVOKE"
    DESCRIBE = "DESCRIBE"
    UNKNOWN = "UNKNOWN"


@dataclass
class ColumnDef:
    name: str
    dtype: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references: Optional[Tuple[str, str]] = None
    is_unique: bool = False
    is_not_null: bool = False
    default: Optional[str] = None
    check_expr: Optional[str] = None


@dataclass
class TableInfo:
    name: str
    columns: List[ColumnDef]
    constraints: List[str] = field(default_factory=list)


@dataclass
class ViewInfo:
    name: str
    query: str
    columns: List[str]


@dataclass
class ProcedureInfo:
    name: str
    params: List[Tuple[str, str, str]]
    body: str
    output_lines: List[str] = field(default_factory=list)


@dataclass
class FunctionInfo:
    name: str
    params: List[Tuple[str, str, str]]
    return_type: str
    body: str
    output_lines: List[str] = field(default_factory=list)


@dataclass
class TriggerInfo:
    name: str
    timing: str
    event: str
    table: str
    level: str
    body: str


@dataclass
class SequenceInfo:
    name: str
    current_val: int = 1
    increment: int = 1
    min_val: int = 1
    max_val: int = 999999999
    cycle: bool = False


@dataclass
class ParsedStatement:
    type: StatementType = StatementType.UNKNOWN
    text: str = ""
    table_name: str = ""
    columns: List[ColumnDef] = field(default_factory=list)
    insert_table: str = ""
    insert_columns: List[str] = field(default_factory=list)
    insert_values: List[str] = field(default_factory=list)
    select_columns: List[str] = field(default_factory=list)
    from_tables: List[str] = field(default_factory=list)
    from_subqueries: Dict[str, str] = field(default_factory=dict)  # placeholder_name -> subquery_sql
    where_clause: str = ""
    group_by: List[str] = field(default_factory=list)
    having_clause: str = ""
    order_by: List[str] = field(default_factory=list)
    is_select_into: bool = False
    into_variables: List[str] = field(default_factory=list)
    update_table: str = ""
    set_clause: List[Tuple[str, str]] = field(default_factory=list)
    delete_table: str = ""
    alter_table: str = ""
    alter_action: str = ""
    alter_column: str = ""
    alter_dtype: str = ""
    drop_name: str = ""
    view_name: str = ""
    view_query: str = ""
    proc_name: str = ""
    proc_params: List[Tuple[str, str, str]] = field(default_factory=list)
    proc_body: str = ""
    return_type: str = ""
    trigger_name: str = ""
    trigger_event: str = ""
    trigger_table: str = ""
    trigger_timing: str = ""
    trigger_level: str = ""
    trigger_body: str = ""
    sequence_name: str = ""
    sequence_start: int = 1
    sequence_increment: int = 1
    exec_name: str = ""
    exec_args: List[str] = field(default_factory=list)
    anonymous_declare: str = ""
    anonymous_body: str = ""
    dbms_output_lines: List[str] = field(default_factory=list)
    describe_name: str = ""
    sub_statements: List['ParsedStatement'] = field(default_factory=list)
    joins: List[Tuple[str, str, str]] = field(default_factory=list)
    table_aliases: Dict[str, str] = field(default_factory=dict)


# ── SQL Parser ─────────────────────────────────────────────────────

class PLSQLError(Exception):
    """Custom exception for PL/SQL runtime errors (e.g., RAISE_APPLICATION_ERROR)."""
    def __init__(self, errno: int, message: str):
        self.errno = errno
        self.message = message
        super().__init__(f"ORA-{errno}: {message}")


class SQLParser:
    @staticmethod
    def clean_sql(text: str) -> str:
        text = re.sub(r'--.*?(\n|$)', '\n', text)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        return text.strip()

    @staticmethod
    def parse(text: str) -> ParsedStatement:
        text = SQLParser.clean_sql(text)
        if not text:
            return ParsedStatement(type=StatementType.UNKNOWN, text=text)
        statements = SQLParser._split_statements(text)
        if len(statements) == 1:
            return SQLParser._parse_single(statements[0])
        combined = ParsedStatement(type=StatementType.UNKNOWN, text=text)
        for stmt_text in statements:
            if stmt_text.strip():
                combined.sub_statements.append(SQLParser._parse_single(stmt_text))
        return combined

    @staticmethod
    def _split_statements(text: str) -> List[str]:
        """Split text into individual SQL/PL/SQL statements.
        Handles semicolons inside strings and keeps PL/SQL blocks intact."""
        if not text.strip():
            return []

        # Pattern to match a complete PL/SQL block from start keyword to END[/;]
        plsql_pattern = re.compile(
            r'(?:DECLARE|BEGIN|'
            r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:PROCEDURE|FUNCTION|TRIGGER|PACKAGE)\b'
            r').*?\bEND(?!\s+(?:IF|LOOP|CASE|WHILE|FOR)\b)\s*;?\s*/?\s*',
            re.IGNORECASE | re.DOTALL
        )

        # Find all PL/SQL blocks and their positions
        blocks = []
        for m in plsql_pattern.finditer(text):
            blocks.append((m.start(), m.end(), m.group(0).strip()))

        if not blocks:
            # No PL/SQL blocks — simple semicolon split
            return SQLParser._split_by_semicolons(text)

        statements = []
        last_end = 0
        for start, end, block_text in blocks:
            # Emit non-PL/SQL text before this block
            if start > last_end:
                prefix = text[last_end:start].strip()
                if prefix:
                    stmts = SQLParser._split_by_semicolons(prefix)
                    statements.extend(stmts)
            # Emit the PL/SQL block as a single statement
            statements.append(block_text)
            last_end = end
        # Emit remaining text after last block
        if last_end < len(text):
            suffix = text[last_end:].strip()
            if suffix:
                stmts = SQLParser._split_by_semicolons(suffix)
                statements.extend(stmts)

        return [s for s in statements if s]

    @staticmethod
    def _split_by_semicolons(text: str) -> List[str]:
        """Split text on semicolons outside string literals."""
        stmts = []
        current = ""
        in_string = False
        string_char = None
        for ch in text:
            if ch in ("'", '"'):
                if not in_string:
                    in_string = True
                    string_char = ch
                elif ch == string_char:
                    in_string = False
                current += ch
            elif ch == ';' and not in_string:
                stmt = current.strip()
                if stmt:
                    stmts.append(stmt)
                current = ""
            else:
                current += ch
        stmt = current.strip()
        if stmt:
            stmts.append(stmt)
        return stmts

    @staticmethod
    def _parse_single(text: str) -> ParsedStatement:
        text = text.strip()
        if not text:
            return ParsedStatement(type=StatementType.UNKNOWN, text=text)
        upper = text.upper().strip()

        # SET SERVEROUTPUT ON/OFF — no-op
        if re.match(r'SET\s+SERVEROUTPUT\s+(ON|OFF)\s*', upper):
            stmt = ParsedStatement(type=StatementType.UNKNOWN, text=text)
            stmt.is_noop = True
            return stmt

        # SQL*Plus slash command — no-op
        if upper in ('/', 'RUN'):
            stmt = ParsedStatement(type=StatementType.UNKNOWN, text=text)
            stmt.is_noop = True
            return stmt

        # Anonymous PL/SQL block
        if upper.startswith('DECLARE') or (upper.startswith('BEGIN') and 'END;' in upper):
            return SQLParser._parse_anonymous_block(text)

        # CREATE OR REPLACE VIEW
        m = re.match(r'CREATE\s+OR\s+REPLACE\s+VIEW\s+(\w+)\s+AS\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_view(m.group(1), m.group(2), is_replace=True)
        # CREATE VIEW
        m = re.match(r'CREATE\s+VIEW\s+(\w+)\s+AS\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_view(m.group(1), m.group(2))

        # CREATE OR REPLACE FUNCTION (with or without params)
        m = re.match(r'CREATE\s+OR\s+REPLACE\s+FUNCTION\s+(\w+)\s*(?:\(([^)]*)\))?\s*RETURN\s+(\w+(?:\([^)]*\))?)\s+(?:IS|AS)\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_function(m.group(1), m.group(2) or '', m.group(3), m.group(4))
        # CREATE FUNCTION (with or without params)
        m = re.match(r'CREATE\s+FUNCTION\s+(\w+)\s*(?:\(([^)]*)\))?\s*RETURN\s+(\w+(?:\([^)]*\))?)\s+(?:IS|AS)\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_function(m.group(1), m.group(2) or '', m.group(3), m.group(4))

        # CREATE OR REPLACE PROCEDURE (with or without params)
        m = re.match(r'CREATE\s+OR\s+REPLACE\s+PROCEDURE\s+(\w+)\s*(?:\(([^)]*)\))?\s+(?:IS|AS)\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_procedure(m.group(1), m.group(2) or '', m.group(3))
        # CREATE PROCEDURE (with or without params)
        m = re.match(r'CREATE\s+PROCEDURE\s+(\w+)\s*(?:\(([^)]*)\))?\s+(?:IS|AS)\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_procedure(m.group(1), m.group(2) or '', m.group(3))

        # CREATE OR REPLACE TRIGGER
        m = re.match(
            r'CREATE\s+OR\s+REPLACE\s+TRIGGER\s+(\w+)\s+'
            r'(BEFORE|AFTER|INSTEAD\s+OF)\s+'
            r'((?:INSERT|UPDATE|DELETE)(?:\s+OR\s+(?:INSERT|UPDATE|DELETE))*)'
            r'(?:\s+OF\s+\w+(?:\s*,\s*\w+)*\s*)?\s*ON\s+(\w+)'
            r'(?:\s+FOR\s+EACH\s+(ROW|STATEMENT))?\s*(.*)',
            text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_trigger(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or 'STATEMENT', m.group(6))
        # CREATE TRIGGER
        m = re.match(r'CREATE\s+TRIGGER\s+(\w+)\s+'
                     r'(BEFORE|AFTER|INSTEAD\s+OF)\s+'
                     r'((?:INSERT|UPDATE|DELETE)(?:\s+OR\s+(?:INSERT|UPDATE|DELETE))*)'
                     r'(?:\s+OF\s+\w+(?:\s*,\s*\w+)*\s*)?\s*ON\s+(\w+)'
                     r'(?:\s+FOR\s+EACH\s+(ROW|STATEMENT))?\s*(.*)',
                     text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_trigger(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or 'STATEMENT', m.group(6))

        # CREATE SEQUENCE
        m = re.match(r'CREATE\s+SEQUENCE\s+(\w+)(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_sequence(m.group(1), m.group(2))

        # CREATE TABLE
        m = re.match(r'CREATE\s+TABLE\s+(\w+)\s*\((.*)\)\s*$', text, re.IGNORECASE | re.DOTALL)
        if m:
            return SQLParser._parse_create_table(m.group(1), m.group(2))

        # ALTER TABLE
        # ALTER TABLE ... ADD CONSTRAINT ... CHECK/FOREIGN KEY
        constraint_m = re.match(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', text, re.IGNORECASE | re.DOTALL)
        if constraint_m:
            stmt = ParsedStatement(type=StatementType.ALTER_TABLE, text=text)
            stmt.alter_table = constraint_m.group(1).upper()
            stmt.alter_action = 'ADD CONSTRAINT'
            stmt.alter_column = constraint_m.group(2).upper()
            constraint_def = constraint_m.group(3).upper().strip()
            stmt.alter_dtype = constraint_def
            return stmt

        m = re.match(r'ALTER\s+TABLE\s+(\w+)\s+(ADD|MODIFY|DROP(?:\s+COLUMN)?\s+|RENAME\s+COLUMN\s+TO\s+)(.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            stmt = ParsedStatement(type=StatementType.ALTER_TABLE, text=text)
            stmt.alter_table = m.group(1).upper()
            action = m.group(2).upper().strip()
            rest = m.group(3).strip()
            stmt.alter_action = action
            if action.startswith('ADD') or action.startswith('MODIFY'):
                col_match = re.match(r'(\w+)\s+(\w+(?:\([^)]*\))?)', rest, re.IGNORECASE)
                if col_match:
                    stmt.alter_column = col_match.group(1).upper()
                    stmt.alter_dtype = col_match.group(2).upper()
            elif 'DROP' in action:
                stmt.alter_column = rest.upper().strip()
            return stmt

        # DROP TABLE
        m = re.match(r'DROP\s+TABLE\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.DROP_TABLE, text=text)
            stmt.drop_name = m.group(1).upper()
            return stmt
        # DROP VIEW
        m = re.match(r'DROP\s+VIEW\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.DROP_VIEW, text=text)
            stmt.drop_name = m.group(1).upper()
            return stmt
        # DROP SEQUENCE
        m = re.match(r'DROP\s+SEQUENCE\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.DROP_SEQUENCE, text=text)
            stmt.drop_name = m.group(1).upper()
            return stmt
        # TRUNCATE
        m = re.match(r'TRUNCATE\s+TABLE\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.TRUNCATE, text=text)
            stmt.drop_name = m.group(1).upper()
            return stmt
        # RENAME
        m = re.match(r'RENAME\s+(\w+)\s+TO\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.RENAME_OBJECT, text=text)
            stmt.drop_name = m.group(1).upper()
            stmt.sequence_name = m.group(2).upper()
            return stmt

        # INSERT INTO ... VALUES
        m = re.match(r'INSERT\s+(?:INTO\s+)?(\w+)\s*(?:\(([^)]*)\))?\s*VALUES\s*\(([^)]*)\)', text, re.IGNORECASE | re.DOTALL)
        if m:
            stmt = ParsedStatement(type=StatementType.INSERT, text=text)
            stmt.insert_table = m.group(1).upper()
            if m.group(2):
                stmt.insert_columns = [c.strip().upper() for c in m.group(2).split(',')]
            stmt.insert_values = SQLParser._parse_values(m.group(3))
            return stmt
        # INSERT ... SELECT
        m = re.match(r'INSERT\s+(?:INTO\s+)?(\w+)\s*(?:\(([^)]*)\))?\s*(SELECT\s+.*)', text, re.IGNORECASE | re.DOTALL)
        if m:
            stmt = ParsedStatement(type=StatementType.INSERT, text=text)
            stmt.insert_table = m.group(1).upper()
            if m.group(2):
                stmt.insert_columns = [c.strip().upper() for c in m.group(2).split(',')]
            stmt.sub_statements.append(SQLParser._parse_single(m.group(3)))
            return stmt

        # UPDATE
        m = re.match(r'UPDATE\s+(\w+)\s+SET\s+(.*?)(?:\s+WHERE\s+(.*))?$', text, re.IGNORECASE | re.DOTALL)
        if m:
            stmt = ParsedStatement(type=StatementType.UPDATE, text=text)
            stmt.update_table = m.group(1).upper()
            set_str = m.group(2)
            stmt.where_clause = (m.group(3) or "").strip()
            pairs = re.findall(r'(\w+)\s*=\s*([^,]+)', set_str)
            stmt.set_clause = [(p[0].upper(), p[1].strip()) for p in pairs]
            return stmt

        # DELETE
        m = re.match(r'DELETE\s+FROM\s+(\w+)(?:\s+WHERE\s+(.*))?$', text, re.IGNORECASE | re.DOTALL)
        if m:
            stmt = ParsedStatement(type=StatementType.DELETE, text=text)
            stmt.delete_table = m.group(1).upper()
            stmt.where_clause = (m.group(2) or "").strip()
            return stmt

        # EXEC (allow leading / that ended a PL/SQL block)
        exec_clean = re.sub(r'^[\s/]+', '', text)
        m = re.match(r'EXEC(?:UTE)?\s+(\w+)\s*\(([^)]*)\)', exec_clean, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.EXEC, text=text)
            stmt.exec_name = m.group(1).upper()
            stmt.exec_args = [a.strip().strip("'\"") for a in m.group(2).split(',') if a.strip()]
            return stmt
        m = re.match(r'EXEC(?:UTE)?\s+(\w+)', exec_clean, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.EXEC, text=text)
            stmt.exec_name = m.group(1).upper()
            return stmt

        # COMMIT
        if re.match(r'COMMIT\s*(WORK)?\s*$', text, re.IGNORECASE):
            return ParsedStatement(type=StatementType.COMMIT, text=text)
        # ROLLBACK
        if re.match(r'ROLLBACK\s*(WORK)?\s*(TO\s+SAVEPOINT\s+\w+)?\s*$', text, re.IGNORECASE):
            stmt = ParsedStatement(type=StatementType.ROLLBACK, text=text)
            m = re.search(r'TO\s+SAVEPOINT\s+(\w+)', text, re.IGNORECASE)
            if m:
                stmt.drop_name = m.group(1).upper()
            return stmt
        # SAVEPOINT
        m = re.match(r'SAVEPOINT\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.SAVEPOINT, text=text)
            stmt.drop_name = m.group(1).upper()
            return stmt

        # DESCRIBE
        m = re.match(r'(?:DESCRIBE|DESC)\s+(\w+)', text, re.IGNORECASE)
        if m:
            stmt = ParsedStatement(type=StatementType.DESCRIBE, text=text)
            stmt.describe_name = m.group(1).upper()
            return stmt

        # GRANT
        m = re.match(r'GRANT\s+(.*?)\s+ON\s+(\w+)\s+TO\s+(\w+)', text, re.IGNORECASE)
        if m:
            return ParsedStatement(type=StatementType.GRANT, text=text)
        # REVOKE
        m = re.match(r'REVOKE\s+(.*?)\s+ON\s+(\w+)\s+FROM\s+(\w+)', text, re.IGNORECASE)
        if m:
            return ParsedStatement(type=StatementType.REVOKE, text=text)

        # SELECT
        if re.match(r'\s*SELECT\b', text, re.IGNORECASE):
            return SQLParser._parse_select(text)

        return ParsedStatement(type=StatementType.UNKNOWN, text=text)

    @staticmethod
    def _parse_values(values_str: str) -> List[str]:
        values = []
        current = ""
        in_string = False
        string_char = None
        for ch in values_str:
            if ch in ("'", '"') and not in_string:
                in_string = True
                string_char = ch
                current += ch
            elif in_string and ch == string_char:
                in_string = False
                current += ch
            elif ch == ',' and not in_string:
                values.append(current.strip())
                current = ""
            else:
                current += ch
        if current.strip():
            values.append(current.strip())
        return values

    @staticmethod
    def _parse_create_table(name: str, columns_str: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.CREATE_TABLE)
        stmt.table_name = name.upper()
        stmt.columns = SQLParser._parse_column_defs(columns_str)
        return stmt

    @staticmethod
    def _parse_column_defs(columns_str: str) -> List[ColumnDef]:
        columns = []
        parts = []
        current = ""
        depth = 0
        for ch in columns_str:
            if ch == '(':
                depth += 1
                current += ch
            elif ch == ')':
                depth -= 1
                current += ch
            elif ch == ',' and depth == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += ch
        if current.strip():
            parts.append(current.strip())
        for part in parts:
            upper = part.upper().strip()
            if upper.startswith('PRIMARY KEY') or upper.startswith('FOREIGN KEY') or \
               upper.startswith('UNIQUE') or upper.startswith('CHECK') or \
               upper.startswith('CONSTRAINT') or upper.startswith('INDEX'):
                continue
            m = re.match(r'(\w+)\s+(\w+(?:\([^)]*\))?(?:\s+WITH\s+(?:LOCAL\s+)?TIME\s+ZONE)?)\s*(.*)', part, re.IGNORECASE)
            if m:
                col = ColumnDef(name=m.group(1).upper(), dtype=m.group(2).upper())
                constraints = m.group(3).upper().strip() if m.group(3) else ""
                col.is_primary_key = 'PRIMARY KEY' in constraints
                col.is_not_null = 'NOT NULL' in constraints or col.is_primary_key
                col.is_unique = 'UNIQUE' in constraints
                ref_m = re.search(r'REFERENCES\s+(\w+)\s*\((\w+)\)', constraints, re.IGNORECASE)
                if ref_m:
                    col.is_foreign_key = True
                    col.references = (ref_m.group(1).upper(), ref_m.group(2).upper())
                default_m = re.search(r'DEFAULT\s+(\S+)', constraints, re.IGNORECASE)
                if default_m:
                    col.default = default_m.group(1)
                check_m = re.search(r'CHECK\s*\(([^)]+)\)', constraints, re.IGNORECASE)
                if check_m:
                    col.check_expr = check_m.group(1)
                columns.append(col)
        pk_match = re.search(r'PRIMARY\s+KEY\s*\(([^)]+)\)', columns_str, re.IGNORECASE)
        if pk_match:
            pk_cols = [c.strip().upper() for c in pk_match.group(1).split(',')]
            for col in columns:
                if col.name in pk_cols:
                    col.is_primary_key = True
                    col.is_not_null = True
        fk_matches = re.finditer(r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)', columns_str, re.IGNORECASE)
        for fk in fk_matches:
            fk_cols = [c.strip().upper() for c in fk.group(1).split(',')]
            ref_table = fk.group(2).upper()
            ref_cols = [c.strip().upper() for c in fk.group(3).split(',')]
            for col in columns:
                if col.name in fk_cols:
                    col.is_foreign_key = True
                    idx = fk_cols.index(col.name)
                    col.references = (ref_table, ref_cols[idx] if idx < len(ref_cols) else ref_cols[0])
        return columns

    @staticmethod
    def _parse_select(text: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.SELECT, text=text)
        into_match = re.search(r'SELECT\s+(.*?)\s+INTO\s+(.*?)\s+FROM\s+', text, re.IGNORECASE | re.DOTALL)
        if into_match:
            stmt.is_select_into = True
            stmt.select_columns = [c.strip() for c in SQLParser._split_columns(into_match.group(1))]
            stmt.into_variables = [v.strip() for v in into_match.group(2).split(',')]
            remainder = text[into_match.end():]
        else:
            m = re.match(r'SELECT\s+(.*?)\s+FROM\s+', text, re.IGNORECASE | re.DOTALL)
            if m:
                stmt.select_columns = [c.strip() for c in SQLParser._split_columns(m.group(1))]
                remainder = text[m.end():]
            else:
                return stmt
        sql_keywords = {'WHERE', 'GROUP', 'HAVING', 'ORDER', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'JOIN', 'ON', 'CROSS', 'NATURAL'}
        # Replace subqueries in FROM portion only (not in WHERE/HAVING/ORDER BY)
        _subq_idx = [0]
        def _replace_from_subqueries(text: str) -> str:
            result = []
            i = 0
            while i < len(text):
                if text[i] == '(' and i + 7 < len(text) and text[i+1:i+7].upper() == 'SELECT':
                    depth = 1
                    j = i + 1
                    while j < len(text) and depth > 0:
                        if text[j] == '(': depth += 1
                        elif text[j] == ')': depth -= 1
                        j += 1
                    if depth == 0:
                        subq_sql = text[i+1:j-1].strip()
                        placeholder = f"__SUBQ_{_subq_idx[0]}"
                        _subq_idx[0] += 1
                        stmt.from_subqueries[placeholder] = subq_sql
                        result.append(placeholder)
                        i = j
                        alias_match = re.match(r'\s+(?:AS\s+)?(\w+)', text[i:])
                        if alias_match and alias_match.group(1).upper() not in sql_keywords:
                            alias = alias_match.group(1).upper()
                            stmt.table_aliases[placeholder] = alias
                            i += alias_match.end()
                        else:
                            stmt.table_aliases[placeholder] = placeholder
                        continue
                result.append(text[i])
                i += 1
            return ''.join(result)
        # Find the boundary of the FROM clause: everything up to WHERE/GROUP/HAVING/ORDER
        from_end = len(remainder)
        for kw_pos in re.finditer(r'\b(?:WHERE|GROUP|HAVING|ORDER)\b', remainder, re.IGNORECASE):
            # Only stop at top-level keywords, not inside subqueries
            prefix = remainder[:kw_pos.start()]
            if prefix.count('(') == prefix.count(')'):
                from_end = kw_pos.start()
                break
        from_portion = remainder[:from_end]
        rest_portion = remainder[from_end:]
        from_portion = _replace_from_subqueries(from_portion)
        remainder = from_portion + rest_portion
        from_match = re.match(r'(\w+(?:\s+\w+)?(?:\s*,\s*\w+(?:\s+\w+)?)*)\s*', remainder, re.IGNORECASE | re.DOTALL)
        if from_match:
            raw_tables = from_match.group(1).strip()
            # Validate: the last word before a keyword must not be a keyword
            # Re-extract: take tokens until we hit a keyword
            table_names = []
            table_aliases = {}
            parts = raw_tables.split(',')
            valid_parts = []
            for part in parts:
                part = part.strip()
                tokens = part.split()
                # Only take tokens that aren't SQL keywords
                valid_tokens = []
                for t in tokens:
                    if t.upper() not in sql_keywords:
                        valid_tokens.append(t)
                    else:
                        break
                if valid_tokens:
                    valid_parts.append(' '.join(valid_tokens))
            cleaned_raw = ','.join(valid_parts)
            from_match2 = re.match(re.escape(cleaned_raw), remainder, re.IGNORECASE)
            if from_match2:
                remainder = remainder[from_match2.end():]
            for part in valid_parts:
                part = part.strip()
                tokens = part.split()
                tname = tokens[0].upper()
                table_names.append(tname)
                if len(tokens) > 1:
                    table_aliases[tname] = tokens[1].upper()
                else:
                    table_aliases[tname] = tname
            stmt.from_tables = table_names
            stmt.table_aliases = table_aliases
        join_pattern = re.compile(
            r'((?:INNER\s+|LEFT\s+(?:OUTER\s+)?|RIGHT\s+(?:OUTER\s+)?|FULL\s+(?:OUTER\s+)?)?JOIN)\s+(\w+)(?:\s+\w+)?(?:\s+ON\s+(.*?))?(?=\s+(?:INNER|LEFT|RIGHT|FULL|JOIN|WHERE|GROUP|HAVING|ORDER|$)|$)',
            re.IGNORECASE)
        on_conditions = []
        for match in join_pattern.finditer(remainder):
            tname = match.group(2).upper()
            join_type = (match.group(1) or 'JOIN').upper().strip()
            if tname not in stmt.from_tables:
                stmt.from_tables.append(tname)
            # Capture alias after table name in JOIN
            full_join_part = match.group(0)
            after_tname = full_join_part[match.end(2) - match.start(0):].strip()
            alias_m2 = re.match(r'(\w+)(?:\s+ON\s+|$)', after_tname, re.IGNORECASE)
            if alias_m2:
                stmt.table_aliases[tname] = alias_m2.group(1).upper()
            else:
                if tname not in stmt.table_aliases:
                    stmt.table_aliases[tname] = tname
            on_clause = match.group(3)
            if on_clause:
                on_conditions.append(on_clause.strip())
            stmt.joins.append((join_type, tname, on_clause.strip() if on_clause else ''))
        remainder = re.sub(
            r'(?:INNER\s+|LEFT\s+(?:OUTER\s+)?|RIGHT\s+(?:OUTER\s+)?|FULL\s+(?:OUTER\s+)?)?JOIN\s+\w+(?:\s+\w+)?(?:\s+ON\s+.*?)?(?=\s+(?:WHERE|GROUP|HAVING|ORDER|$)|$)',
            '', remainder, flags=re.IGNORECASE)
        where_parts = []
        where_m = re.search(r'WHERE\s+', remainder, re.IGNORECASE)
        if where_m:
            start = where_m.end()
            depth = 0
            i = start
            while i < len(remainder):
                c = remainder[i]
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                elif depth == 0:
                    suffix = remainder[i:]
                    if re.match(r'\s+GROUP\s+BY\s+', suffix, re.IGNORECASE):
                        break
                    if re.match(r'\s+HAVING\s+', suffix, re.IGNORECASE):
                        break
                    if re.match(r'\s+ORDER\s+BY\s+', suffix, re.IGNORECASE):
                        break
                i += 1
            where_parts.append(remainder[start:i].strip())
            remainder = remainder[:where_m.start()] + remainder[i:]
        if where_parts:
            stmt.where_clause = ' AND '.join(where_parts)
        group_match = re.search(r'GROUP\s+BY\s+(.*?)(?=\s+HAVING\s+|\s+ORDER\s+BY\s+|$)', remainder, re.IGNORECASE | re.DOTALL)
        if group_match:
            stmt.group_by = [g.strip() for g in group_match.group(1).split(',')]
            remainder = remainder[group_match.end():]
        having_match = re.search(r'HAVING\s+(.*?)(?=\s+ORDER\s+BY\s+|$)', remainder, re.IGNORECASE | re.DOTALL)
        if having_match:
            stmt.having_clause = having_match.group(1).strip()
            remainder = remainder[having_match.end():]
        order_match = re.search(r'ORDER\s+BY\s+(.*?)$', remainder, re.IGNORECASE | re.DOTALL)
        if order_match:
            stmt.order_by = [o.strip() for o in order_match.group(1).split(',')]
        return stmt

    @staticmethod
    def _split_columns(columns_str: str) -> List[str]:
        cols = []
        current = ""
        depth = 0
        for ch in columns_str:
            if ch == '(':
                depth += 1
                current += ch
            elif ch == ')':
                depth -= 1
                current += ch
            elif ch == ',' and depth == 0:
                cols.append(current.strip())
                current = ""
            else:
                current += ch
        if current.strip():
            cols.append(current.strip())
        return cols

    @staticmethod
    def _parse_create_view(name: str, query: str, is_replace: bool = False) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.CREATE_VIEW)
        stmt.view_name = name.upper()
        stmt.view_query = re.sub(r'[\s;\/]+$', '', query.strip())
        select_match = re.match(r'SELECT\s+(.*?)\s+FROM\s+', query, re.IGNORECASE | re.DOTALL)
        if select_match:
            stmt.select_columns = [c.strip() for c in SQLParser._split_columns(select_match.group(1))]
        return stmt

    @staticmethod
    def _parse_create_procedure(name: str, params_str: str, body: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.CREATE_PROCEDURE)
        stmt.proc_name = name.upper()
        stmt.proc_params = SQLParser._parse_params(params_str)
        stmt.proc_body = body.strip()
        stmt.dbms_output_lines = SQLParser._extract_dbms_output(body)
        return stmt

    @staticmethod
    def _parse_create_function(name: str, params_str: str, return_type: str, body: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.CREATE_FUNCTION)
        stmt.proc_name = name.upper()
        stmt.proc_params = SQLParser._parse_params(params_str)
        stmt.return_type = return_type.upper()
        stmt.proc_body = body.strip()
        stmt.dbms_output_lines = SQLParser._extract_dbms_output(body)
        return stmt

    @staticmethod
    def _parse_params(params_str: str) -> List[Tuple[str, str, str]]:
        params = []
        if not params_str.strip():
            return params
        parts = SQLParser._split_columns(params_str)
        for part in parts:
            part = part.strip()
            m = re.match(r'(\w+)\s+(IN|OUT|IN\s+OUT)?\s*(\w+(?:\([^)]*\))?)', part, re.IGNORECASE)
            if m:
                name = m.group(1).upper()
                direction = (m.group(2) or 'IN').upper().strip()
                dtype = m.group(3).upper()
                params.append((name, direction, dtype))
        return params

    @staticmethod
    def _parse_create_trigger(name: str, timing: str, event: str, table: str, level: str, body: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.CREATE_TRIGGER)
        stmt.trigger_name = name.upper()
        stmt.trigger_timing = timing.upper().strip()
        stmt.trigger_event = event.upper().strip()
        stmt.trigger_table = table.upper()
        stmt.trigger_level = level.upper().strip()
        stmt.trigger_body = body.strip()
        return stmt

    @staticmethod
    def _parse_create_sequence(name: str, options: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.CREATE_SEQUENCE)
        stmt.sequence_name = name.upper()
        stmt.sequence_start = 1
        stmt.sequence_increment = 1
        start_match = re.search(r'START\s+WITH\s+(\d+)', options, re.IGNORECASE)
        if start_match:
            stmt.sequence_start = int(start_match.group(1))
        inc_match = re.search(r'INCREMENT\s+(?:BY\s+)?(\d+)', options, re.IGNORECASE)
        if inc_match:
            stmt.sequence_increment = int(inc_match.group(1))
        return stmt

    @staticmethod
    def _parse_anonymous_block(text: str) -> ParsedStatement:
        stmt = ParsedStatement(type=StatementType.ANONYMOUS_BLOCK, text=text)
        if text.upper().strip().startswith('DECLARE'):
            m = re.match(r'DECLARE\s+(.*?)BEGIN\s+', text, re.IGNORECASE | re.DOTALL)
            if m:
                stmt.anonymous_declare = m.group(1).strip()
                body_start = m.end()
                end_match = re.search(r'END\s*;', text[body_start:], re.IGNORECASE)
                if end_match:
                    stmt.anonymous_body = text[body_start:body_start + end_match.start()].strip()
        else:
            m = re.match(r'BEGIN\s+(.*?)END\s*;', text, re.IGNORECASE | re.DOTALL)
            if m:
                stmt.anonymous_body = m.group(1).strip()
        stmt.dbms_output_lines = SQLParser._extract_dbms_output(text)
        return stmt

    @staticmethod
    def _extract_dbms_output(text: str) -> List[str]:
        lines = []
        for m in re.finditer(r'DBMS_OUTPUT\s*\.\s*PUT_LINE\s*\(\s*([^)]+)\s*\)', text, re.IGNORECASE):
            arg = m.group(1).strip()
            if (arg.startswith("'") and arg.endswith("'")) or \
               (arg.startswith('"') and arg.endswith('"')):
                lines.append(arg[1:-1])
            else:
                parts = re.split(r'\s*\|\|\s*', arg)
                resolved = []
                for part in parts:
                    part = part.strip()
                    if (part.startswith("'") and part.endswith("'")) or \
                       (part.startswith('"') and part.endswith('"')):
                        resolved.append(part[1:-1])
                    else:
                        resolved.append(f'[{part}]')
                lines.append(''.join(resolved))
        return lines


# ── Mock Database Engine ───────────────────────────────────────────

class MockDatabase:
    def __init__(self):
        self.tables: Dict[str, TableInfo] = {}
        self.rows: Dict[str, List[List[str]]] = {}
        self.views: Dict[str, ViewInfo] = {}
        self.procedures: Dict[str, ProcedureInfo] = {}
        self.functions: Dict[str, FunctionInfo] = {}
        self.triggers: Dict[str, TriggerInfo] = {}
        self.sequences: Dict[str, SequenceInfo] = {}
        self._last_sequence_nextvals: Dict[str, Optional[str]] = {}
        self.rownum_counter: int = 0
        self._undo_log: List[Tuple[str, str, int, List[str]]] = []

    # ── PL/SQL Body Executor ────────────────────────────────────

    def _evaluate_plsql_expr(self, expr: str, variables: Dict[str, str]) -> str:
        """Evaluate a PL/SQL expression with variable substitution."""
        expr = expr.strip()
        if not expr:
            return ''

        # Handle single-quoted string literals
        if expr.startswith("'") and expr.endswith("'"):
            return expr[1:-1]

        # Handle concatenation with ||
        if '||' in expr:
            parts = re.split(r'\|\|', expr)
            result = ''
            for part in parts:
                result += self._evaluate_plsql_expr(part.strip(), variables)
            return result

        # Handle simple arithmetic: var + num, var - num, var * num, var / num
        for op in ['+', '-', '*', '/']:
            if op in expr and not (expr.startswith("'") or expr.startswith('-')):
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self._evaluate_plsql_expr(parts[0].strip(), variables)
                    right = self._evaluate_plsql_expr(parts[1].strip(), variables)
                    try:
                        nl = float(left)
                        nr = float(right)
                        if op == '+': return str(int(nl + nr))
                        elif op == '-': return str(int(nl - nr))
                        elif op == '*': return str(int(nl * nr))
                        elif op == '/' and nr != 0: return str(round(nl / nr, 2))
                    except ValueError:
                        pass
            if op in expr:
                break  # Only try first operator found

        # Variable reference or numeric literal
        if expr.lstrip('-').replace('.', '', 1).isdigit():
            return expr

        # Trim semicolons
        clean = expr.rstrip(';').strip()
        # Check variable
        var_upper = clean.upper()
        for vname, vval in variables.items():
            if vname.upper() == var_upper:
                return vval

        # Unknown - return as-is (without quotes)
        return clean.strip("'\"")

    def _split_plsql_statements(self, block: str) -> List[str]:
        """Split a PL/SQL block into statements on semicolons, handling strings."""
        stmts = []
        current = ''
        in_string = False
        string_char = ''
        i = 0
        while i < len(block):
            ch = block[i]
            if ch in ("'", '"'):
                if not in_string:
                    in_string = True
                    string_char = ch
                elif ch == string_char:
                    if i == 0 or block[i-1] != '\\':
                        in_string = False
                current += ch
            elif ch == ';' and not in_string:
                s = current.strip()
                if s:
                    stmts.append(s)
                current = ''
            else:
                current += ch
            i += 1
        s = current.strip()
        if s:
            stmts.append(s)
        return stmts

    def _execute_plsql_block(self, block_text: str, variables: Dict[str, str],
                              output_lines: List[str], return_val: List[Optional[str]]) -> None:
        """Execute a series of PL/SQL statements."""
        # Normalize: remove outer BEGIN/END if present
        text = block_text.strip()
        if text.upper().startswith('BEGIN'):
            text = text[5:].strip()
        if text.upper().endswith('END;'):
            text = text[:-4].strip()
        elif text.upper().endswith('END'):
            text = text[:-3].strip()

        # Split into individual statements
        stmts = self._split_plsql_statements(text)
        i = 0
        while i < len(stmts):
            stmt = stmts[i].strip()
            if not stmt or stmt.upper() == 'NULL':
                i += 1
                continue

            upper = stmt.upper()

            # IF statement
            if upper.startswith('IF '):
                # Find matching END IF;
                if_block = stmt
                j = i + 1
                while j < len(stmts) and 'END IF' not in stmts[j].upper() and 'ENDIF' not in stmts[j].upper():
                    if_block += '; ' + stmts[j]
                    j += 1
                if j < len(stmts):
                    if_block += '; ' + stmts[j]
                i = j

                # Parse IF condition
                if_match = re.match(r'IF\s+(.*?)\s+THEN\s+(.*?)(?:\s+ELSE\s+(.*?))?\s+END\s+IF\s*;?',
                                    if_block, re.IGNORECASE | re.DOTALL)
                if if_match:
                    cond = if_match.group(1).strip()
                    then_body = if_match.group(2).strip()
                    else_body = (if_match.group(3) or '').strip()
                    # Evaluate condition
                    cond_result = self._evaluate_if_condition(cond, variables)
                    if cond_result:
                        self._execute_plsql_block(then_body, variables, output_lines, return_val)
                    elif else_body:
                        self._execute_plsql_block(else_body, variables, output_lines, return_val)
                i += 1
                continue

            # LOOP
            if upper.startswith('FOR ') or (upper.startswith('WHILE ')):
                i += 1
                continue

            # RETURN
            ret_match = re.match(r'RETURN\s+(.*)', stmt, re.IGNORECASE)
            if ret_match:
                val = self._evaluate_plsql_expr(ret_match.group(1), variables)
                return_val[0] = val
                i += 1
                continue

            # RAISE_APPLICATION_ERROR
            raise_match = re.match(r'RAISE_APPLICATION_ERROR\s*\(\s*(-?\d+)\s*,\s*(.+?)\s*\)', stmt, re.IGNORECASE)
            if raise_match:
                errno = int(raise_match.group(1))
                msg = raise_match.group(2).strip().strip("'\"")
                raise PLSQLError(errno, msg)

            # DBMS_OUTPUT.PUT_LINE
            put_match = re.search(r'DBMS_OUTPUT\s*\.\s*PUT_LINE\s*\(\s*([^)]+)\s*\)', stmt, re.IGNORECASE)
            if put_match:
                arg = put_match.group(1).strip()
                val = self._evaluate_plsql_expr(arg, variables)
                output_lines.append(val)
                i += 1
                continue

            # SELECT ... INTO ... FROM ...
            into_match = re.match(r'SELECT\s+(.*?)\s+INTO\s+(.*?)\s+FROM\s+(.*)', stmt, re.IGNORECASE | re.DOTALL)
            if into_match:
                sel_cols_str = into_match.group(1).strip()
                into_vars = [v.strip() for v in into_match.group(2).split(',')]
                from_rest = into_match.group(3).strip().rstrip(';')

                # Extract all table names from FROM (including JOINs)
                all_tables = []
                from_upper = from_rest.upper()
                # Get primary table (first word)
                primary_m = re.match(r'(\w+)', from_rest, re.IGNORECASE)
                if primary_m:
                    all_tables.append(primary_m.group(1).upper())
                # Find all JOIN table names
                for m in re.finditer(r'\bJOIN\s+(\w+)', from_rest, re.IGNORECASE):
                    tname = m.group(1).upper()
                    if tname not in all_tables:
                        all_tables.append(tname)
                # Find all comma-separated table names
                if ',' in from_rest:
                    parts = re.split(r'\s*,\s*', from_rest)
                    for part in parts:
                        tm = re.match(r'(\w+)', part.strip(), re.IGNORECASE)
                        if tm:
                            tname = tm.group(1).upper()
                            if tname not in ('NATURAL', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'CROSS', 'JOIN', 'ON', 'WHERE', 'AND', 'OR', 'AS') and tname not in all_tables:
                                all_tables.append(tname)

                where_part = ''
                where_m = re.search(r'WHERE\s+(.*)', from_rest, re.IGNORECASE | re.DOTALL)
                if where_m:
                    where_part = where_m.group(1).strip()

                # Get the first real table as primary (preserve order!)
                from_table = all_tables[0] if all_tables else ''
                all_tables_unique = []
                for t in all_tables:
                    if t not in all_tables_unique:
                        all_tables_unique.append(t)
                all_tables = all_tables_unique

                if from_table and from_table in self.tables:
                    tcols = self.get_column_names(from_table)
                    trows = list(self.rows.get(from_table, []))

                    # Gather column-to-table mapping from all joined tables
                    col_table_map = {}
                    for tname in all_tables:
                        if tname in self.tables:
                            for c in self.get_column_names(tname):
                                col_table_map[c.upper()] = tname

                    # Build combined row from first matching primary row + joined table rows
                    joined_rows = []
                    for primary_row in trows:
                        combined = dict(zip([c.upper() for c in tcols], primary_row))
                        # Add data from joined tables
                        for tname in all_tables[1:]:
                            if tname in self.tables:
                                jcols = self.get_column_names(tname)
                                jrows = list(self.rows.get(tname, []))
                                # Find matching rows (simple: same values in common columns)
                                common_cols = [c for c in combined if c in [jc.upper() for jc in jcols]]
                                for jrow in jrows:
                                    match_found = True
                                    if common_cols:
                                        for cc in common_cols:
                                            jci = -1
                                            for ci, jc in enumerate(jcols):
                                                if jc.upper() == cc:
                                                    jci = ci
                                                    break
                                            if jci >= 0 and combined.get(cc) != jrow[jci]:
                                                match_found = False
                                                break
                                    if match_found:
                                        for ci, jc in enumerate(jcols):
                                            if jc.upper() not in combined:
                                                combined[jc.upper()] = jrow[ci] if ci < len(jrow) else ''
                                        break
                        joined_rows.append(combined)

                    # Apply WHERE with variable substitution
                    if where_part and joined_rows:
                        substituted_where = where_part
                        self._plsql_vars = variables
                        filtered = []
                        for crow in joined_rows:
                            # Evaluate WHERE against combined dict
                            all_cols_list = list(crow.keys())
                            all_vals_list = list(crow.values())
                            if self._evaluate_simple(all_vals_list, all_cols_list, from_table, substituted_where):
                                filtered.append(crow)
                        joined_rows = filtered
                        self._plsql_vars = None

                    if joined_rows:
                        sel_cols = [c.strip() for c in SQLParser._split_columns(sel_cols_str)]
                        for sci, sc in enumerate(sel_cols):
                            sc_upper = sc.upper().strip()
                            # Handle aggregate functions: SUM(Qty) -> extract Qty
                            agg_match = re.match(r'(SUM|COUNT|AVG|MIN|MAX)\((.+?)\)', sc_upper, re.IGNORECASE)
                            if agg_match:
                                agg_func = agg_match.group(1).upper()
                                agg_col = agg_match.group(2).strip()
                                vals = []
                                is_star = agg_col == '*'
                                for crow in joined_rows:
                                    if is_star:
                                        vals.append(1)
                                    elif agg_col in crow:
                                        try:
                                            vals.append(int(crow[agg_col]))
                                        except ValueError:
                                            pass
                                if sci < len(into_vars):
                                    var_name = into_vars[sci].strip().upper()
                                    if agg_func == 'SUM':
                                        variables[var_name] = str(sum(vals)) if vals else '0'
                                    elif agg_func == 'COUNT':
                                        variables[var_name] = str(len(joined_rows))
                                    elif agg_func == 'AVG':
                                        variables[var_name] = str(round(sum(vals) / len(vals), 2)) if vals else '0'
                                    elif agg_func == 'MIN':
                                        variables[var_name] = str(min(vals)) if vals else '0'
                                    elif agg_func == 'MAX':
                                        variables[var_name] = str(max(vals)) if vals else '0'
                                continue
                            if sci < len(into_vars):
                                var_name = into_vars[sci].strip().upper()
                                lookup_key = sc_upper
                                if '.' in lookup_key:
                                    lookup_key = lookup_key.split('.')[-1]
                                if lookup_key in joined_rows[0]:
                                    variables[var_name] = joined_rows[0][lookup_key]
                                elif sc_upper in joined_rows[0]:
                                    variables[var_name] = joined_rows[0][sc_upper]
                                else:
                                    variables[var_name] = ''
                i += 1
                continue

            # Assignment: var := expr
            assign_match = re.match(r'(\w+)\s*:=\s*(.*)', stmt, re.IGNORECASE | re.DOTALL)
            if assign_match:
                var_name = assign_match.group(1).strip().upper()
                expr = assign_match.group(2).strip().rstrip(';')
                val = self._evaluate_plsql_expr(expr, variables)
                variables[var_name] = val
                i += 1
                continue

            # DML: INSERT, UPDATE, DELETE (e.g. trigger body)
            dml_match = re.match(r'(INSERT|UPDATE|DELETE)\b', stmt, re.IGNORECASE)
            if dml_match:
                # Substitute :NEW/:OLD references and PL/SQL variables with actual values
                subst = stmt
                for var_key in sorted(variables.keys(), key=len, reverse=True):
                    var_val = variables[var_key]
                    if var_val.lstrip('-').replace('.', '', 1).isdigit():
                        replacement = var_val
                    else:
                        replacement = "'" + var_val.replace("'", "''") + "'"
                    if var_key.startswith(':'):
                        subst = re.sub(re.escape(var_key), replacement, subst, flags=re.IGNORECASE)
                    else:
                        subst = re.sub(r'\b' + re.escape(var_key) + r'\b', replacement, subst, flags=re.IGNORECASE)
                try:
                    dml_parsed = SQLParser.parse(subst)
                    if dml_parsed:
                        dml_result = self.process_statement(dml_parsed)
                        for line in dml_result:
                            stripped = line.strip()
                            if stripped:
                                output_lines.append(stripped)
                except Exception:
                    pass
                i += 1
                continue

            # Unknown statement - skip
            i += 1

    def _evaluate_if_condition(self, cond: str, variables: Dict[str, str]) -> bool:
        """Evaluate a PL/SQL IF condition with variable substitution."""
        substituted = cond

        # Substitute regular variables with word boundaries
        for vname, vval in variables.items():
            if not vname.startswith(':'):
                substituted = re.sub(r'\b' + re.escape(vname) + r'\b', vval, substituted, flags=re.IGNORECASE)

        # Handle NOT
        not_flag = False
        if substituted.upper().startswith('NOT '):
            not_flag = True
            substituted = substituted[4:].strip()

        # IS NULL / IS NOT NULL
        null_m = re.match(r'((?::NEW|:OLD)?\.?\w+)\s+IS\s+(NOT\s+)?NULL', substituted, re.IGNORECASE)
        if null_m:
            val = variables.get(null_m.group(1).upper(), '')
            is_null = val == '' or val.upper() == 'NULL'
            is_not = null_m.group(2) is not None
            result = is_null
            if is_not:
                result = not result
            return not result if not_flag else result

        # LIKE
        like_m = re.match(r"((?::NEW|:OLD)?\.?\w+)\s+LIKE\s+'([^']*)'", substituted, re.IGNORECASE)
        if like_m:
            val = variables.get(like_m.group(1).upper(), '')
            pat = like_m.group(2).upper()
            val_upper = val.upper()
            if pat.startswith('%') and pat.endswith('%'):
                return (pat[1:-1] in val_upper) != not_flag
            elif pat.startswith('%'):
                return val_upper.endswith(pat[1:]) != not_flag
            elif pat.endswith('%'):
                return val_upper.startswith(pat[:-1]) != not_flag
            return (val_upper == pat) != not_flag

        # IN
        in_m = re.match(r"((?::NEW|:OLD)?\.?\w+)\s+(?:NOT\s+)?IN\s*\(([^)]+)\)", substituted, re.IGNORECASE)
        if in_m:
            val = variables.get(in_m.group(1).upper(), '').upper()
            in_vals = [v.strip().strip("'\"") for v in in_m.group(2).split(',')]
            is_not = 'NOT' in substituted.upper().split('IN')[0]
            matched = val in [v.upper() for v in in_vals]
            return (not matched if is_not else matched) if not not_flag else (matched if is_not else not matched)

        # Comparison with operators
        comp_m = re.match(r'(\S+?)\s*([=<>!]+)\s*(.*)', substituted, re.IGNORECASE)
        if comp_m:
            left_raw = comp_m.group(1).strip()
            op = comp_m.group(2).strip()
            right_str = comp_m.group(3).strip().strip("'\"").strip()

            # Look up the left side as a variable (try with and without :NEW./:OLD. prefix)
            left_up = left_raw.upper()
            left_val = (variables.get(left_up) or
                        variables.get(f':NEW.{left_up}') or
                        variables.get(f':OLD.{left_up}') or
                        left_raw)
            try:
                lv = float(left_val)
                rv = float(right_str)
                results = {'=': lv == rv, '>': lv > rv, '<': lv < rv,
                           '>=': lv >= rv, '<=': lv <= rv, '<>': lv != rv, '!=': lv != rv}
                return results.get(op, False) != not_flag
            except ValueError:
                lv_up = left_val.upper()
                rv_up = right_str.upper()
                results = {'=': lv_up == rv_up, '>': lv_up > rv_up, '<': lv_up < rv_up,
                           '>=': lv_up >= rv_up, '<=': lv_up <= rv_up, '<>': lv_up != rv_up, '!=': lv_up != rv_up}
                return results.get(op, False) != not_flag

        return True

    def _execute_plsql_body(self, body: str, param_values: Dict[str, str],
                             output_lines: List[str]) -> Optional[str]:
        """Execute a full PL/SQL body (procedure or function).
        Returns return value if any (for functions)."""
        body = body.strip()

        variables = {}
        for k, v in param_values.items():
            variables[k.upper()] = v

        # Remove variable declarations between IS/AS and BEGIN
        decl_section = ''
        exec_section = body

        # Find BEGIN in the body
        begin_idx = body.upper().find('BEGIN')
        if begin_idx >= 0:
            decl_section = body[:begin_idx].strip()
            exec_section = body[begin_idx:].strip()

        # Extract variable declarations from decl_section
        if decl_section and not decl_section.upper().startswith('DECLARE'):
            decl_section = 'DECLARE ' + decl_section
        if decl_section:
            # Parse variable declarations
            var_decl_re = re.finditer(r'(\w+)\s+(\w+(?:\([^)]*\))?)\s*(?:;|:=)', decl_section, re.IGNORECASE)
            for m in var_decl_re:
                var_name = m.group(1).upper()
                if var_name not in variables and var_name.upper() != 'END':
                    variables[var_name] = ''
            # Also capture standalone declarations
            var_decl_re2 = re.finditer(r'(\w+)\s+(\w+(?:\([^)]*\))?)\s*;', decl_section, re.IGNORECASE)
            for m in var_decl_re2:
                var_name = m.group(1).upper()
                if var_name not in variables and var_name.upper() not in ('IS', 'AS', 'BEGIN', 'END',
                    'CURSOR', 'TYPE', 'RECORD', 'TABLE', 'CONSTANT'):
                    variables[var_name] = ''

        # Execute the block
        return_val = [None]
        self._execute_plsql_block(exec_section, variables, output_lines, return_val)
        return return_val[0]

    def _fire_triggers(self, event: str, table: str, row_data: Optional[Dict[str, str]] = None,
                        timing: Optional[str] = None) -> List[str]:
        """Fire matching triggers for a DML event. Returns output lines.
        If timing is given, only fire triggers with that timing (BEFORE/AFTER)."""
        lines = []
        for tname, trig in self.triggers.items():
            if trig.table.upper() == table.upper() and event.upper() in trig.event.upper():
                if timing and trig.timing.upper() != timing.upper():
                    continue
                # Execute trigger body
                out = []
                trig_vars = {}
                if row_data:
                    for k, v in row_data.items():
                        trig_vars[f':NEW.{k.upper()}'] = v
                        trig_vars[f':OLD.{k.upper()}'] = v
                try:
                    self._execute_plsql_body(trig.body, trig_vars, out)
                except PLSQLError as e:
                    lines.append(f"  [{tname}] ORA-{abs(e.errno)}: {e.message}")
                    # Propagate to abort the DML operation
                    raise

                # Check for CHECK constraint-style triggers
                body_upper = trig.body.upper()
                if trig.timing.upper() == 'BEFORE':
                    if event.upper() == 'INSERT' and row_data:
                        # Check simple conditions like :NEW.age > 0 or :NEW.salary >= 15000
                        for key, val in row_data.items():
                            check_pat = rf":NEW\.{key}\s*([=<>!]+)\s*(\d+)"
                            cm = re.search(check_pat, body_upper, re.IGNORECASE)
                            if cm:
                                op = cm.group(1)
                                threshold = cm.group(2)
                                try:
                                    v = float(val)
                                    t = float(threshold)
                                    if op == '>' and not (v > t):
                                        lines.append(f"  Trigger {tname} fired, but condition violated")
                                    elif op == '<' and not (v < t):
                                        lines.append(f"  Trigger {tname} fired, but condition violated")
                                    elif op == '>=' and not (v >= t):
                                        lines.append(f"  Trigger {tname} fired, but condition violated")
                                    elif op == '<=' and not (v <= t):
                                        lines.append(f"  Trigger {tname} fired, but condition violated")
                                    elif op == '=' and not (v == t):
                                        lines.append(f"  Trigger {tname} fired, but condition violated")
                                except ValueError:
                                    pass
                if out:
                    for o in out:
                        lines.append(f"  [{tname}] {o}")
                    lines.append(f"  Trigger {tname} fired.")
        return lines

    def get_column_names(self, table_name: str) -> List[str]:
        table_name = table_name.upper()
        if table_name in self.tables:
            return [c.name for c in self.tables[table_name].columns]
        return []

    def get_column_types(self, table_name: str) -> Dict[str, str]:
        table_name = table_name.upper()
        if table_name in self.tables:
            return {c.name: c.dtype for c in self.tables[table_name].columns}
        return {}

    def infer_type(self, col_name: str) -> str:
        name = col_name.upper()
        if any(x in name for x in ('PRICE', 'SALARY', 'AMOUNT', 'BALANCE', 'EMI', 'BUDGET')):
            return 'NUMBER'
        if any(x in name for x in ('QTY', 'STOCK', 'COUNT', 'AGE', 'HOURS', 'RATING')):
            return 'NUMBER'
        if name in ('ID', 'SID', 'BID') or name.endswith('ID') or name.endswith('NO'):
            return 'VARCHAR2'
        if any(x in name for x in ('NAME', 'DESC', 'ADDRESS', 'COLOR', 'GENDER', 'DESIGNATION')):
            return 'VARCHAR2'
        if any(x in name for x in ('DATE', 'TIME')):
            return 'DATE'
        return 'VARCHAR2'

    def generate_dummy_value(self, col_name: str, col_type: str, row_idx: int) -> str:
        name_upper = col_name.upper()
        col_type_upper = col_type.upper()
        is_number = ('NUMBER' in col_type_upper or 'INT' in col_type_upper or
                     'FLOAT' in col_type_upper or 'DECIMAL' in col_type_upper or
                     'NUMERIC' in col_type_upper or any(x in name_upper for x in
                     ('PRICE', 'QTY', 'STOCK', 'SALARY', 'AMOUNT', 'BALANCE', 'EMI',
                      'AGE', 'COUNT', 'HOURS', 'BUDGET')))
        if name_upper == 'PRODID' or name_upper == 'PID':
            return f"P{row_idx:03d}"
        if name_upper == 'PURID':
            return f"PU{row_idx:03d}"
        if name_upper == 'SALEID' or name_upper == 'SID':
            return f"SA{row_idx:03d}"
        if name_upper == 'CUSTID' or name_upper == 'CID':
            return f"C{row_idx:02d}"
        if name_upper == 'SUPNAME':
            return random.choice(SUPPLIER_NAMES)
        if name_upper == 'CUSTNAME' or name_upper == 'CUSTOMERNAME' or name_upper == 'CNAME':
            return random.choice(CUSTOMER_NAMES)
        if name_upper == 'PRODDESC' or name_upper == 'PRODESC' or name_upper == 'PDESC' or name_upper == 'DESCRIPTION':
            return random.choice(PRODUCT_NAMES)
        if name_upper == 'PRODNAME' or name_upper == 'PNAME':
            return random.choice(PRODUCT_NAMES)
        if 'NAME' in name_upper:
            return random.choice(CUSTOMER_NAMES)
        if 'PRICE' in name_upper:
            return str(random.choice([500, 1000, 5000, 10000, 25000, 45000, 75000]))
        if 'QTY' in name_upper:
            return str(random.randint(1, 50))
        if 'STOCK' in name_upper:
            return str(random.choice([5, 10, 15, 20, 50, 100]))
        if 'SALARY' in name_upper:
            return str(random.choice([25000, 35000, 45000, 55000, 75000, 100000]))
        if 'AMOUNT' in name_upper:
            return str(random.choice([10000, 25000, 50000, 100000, 200000]))
        if 'BALANCE' in name_upper or 'BAL' in name_upper:
            return str(random.choice([5000, 10000, 25000, 50000, 100000]))
        if 'EMI' in name_upper:
            return str(random.choice([2000, 5000, 8000, 10000, 15000]))
        if 'AGE' in name_upper:
            return str(random.randint(22, 60))
        if 'HOURS' in name_upper:
            return str(random.randint(1, 40))
        if 'RATING' in name_upper:
            return random.choice(RATINGS)
        if 'GENDER' in name_upper:
            return random.choice(['M', 'F', 'Male', 'Female'])
        if 'COLOR' in name_upper:
            return random.choice(COLORS_LIST)
        if 'BTYPE' in name_upper or 'BOATTYPE' in name_upper:
            return random.choice(BOAT_TYPES)
        if 'BNAME' in name_upper or 'BOATNAME' in name_upper:
            return random.choice(BOAT_NAMES)
        if 'SHIFT' in name_upper:
            return random.choice(['FN', 'AN'])
        if 'DESIGNATION' in name_upper or 'DESIG' in name_upper:
            return random.choice(DESIGNATIONS)
        if name_upper == 'ENO' or name_upper == 'EMPNO' or name_upper == 'EID':
            return str(random.randint(100, 200))
        if name_upper == 'DEPT_NO' or name_upper == 'DEPTNO' or name_upper == 'DID':
            return f"D{random.randint(1, 5):02d}"
        if 'PHONE' in name_upper or 'PHNO' in name_upper:
            return f"98{random.randint(10000000, 99999999)}"
        if 'EMAIL' in name_upper:
            return f"user{row_idx}@example.com"
        if 'ADDRESS' in name_upper or 'ADDR' in name_upper:
            return random.choice(CITIES)
        if 'LOANID' in name_upper or 'LOAN_ID' in name_upper:
            return f"L{row_idx:03d}"
        if name_upper == 'ACCNO' or name_upper == 'ACCOUNTNO' or name_upper == 'ACC_NO':
            return f"ACC{row_idx:05d}"
        if is_number:
            return str(random.randint(1, 1000))
        if 'DATE' in col_type_upper or col_type_upper.startswith('DATE'):
            return f"{random.randint(1, 28):02d}-{random.choice(['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'])}-{random.choice(['2023','2024','2025'])}"
        return f"VAL{row_idx}"

    def process_statement(self, stmt: ParsedStatement) -> List[str]:
        output = []
        for sub in stmt.sub_statements:
            output.extend(self.process_statement(sub))
        if stmt.sub_statements:
            return output
        return getattr(self, f"_handle_{stmt.type.value.replace(' ', '_')}", self._handle_UNKNOWN)(stmt)

    def _handle_CREATE_TABLE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.table_name.upper()
        self.tables[name] = TableInfo(name=name, columns=stmt.columns)
        self.rows[name] = []
        return ["", "Table created."]

    @staticmethod
    def _strip_quotes(val: str) -> str:
        v = val.strip()
        if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
            return v[1:-1]
        return v

    def _handle_INSERT(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.insert_table.upper()
        if name not in self.tables:
            return ["", f"ERROR at line 1: ORA-00942: table or view '{name}' does not exist."]
        cols = self.get_column_names(name)

        # INSERT ... SELECT support
        if stmt.sub_statements and stmt.sub_statements[0].type == StatementType.SELECT:
            select_stmt = stmt.sub_statements[0]
            select_lines = self._handle_SELECT(select_stmt)
            # Extract rows from formatted output (skip header, sep, counts)
            parsed_select = select_stmt
            table_name = parsed_select.from_tables[0].upper() if parsed_select.from_tables else ''
            tcols, trows = self._gather_table_data(table_name) if table_name else ([], [])
            if trows:
                row_count = 0
                for row in trows:
                    ordered = list(row)
                    if stmt.insert_columns:
                        ordered = [''] * len(cols)
                        col_map = {c.upper(): i for i, c in enumerate(cols)}
                        for ic, rv in zip(stmt.insert_columns, row):
                            if ic.upper() in col_map:
                                ordered[col_map[ic.upper()]] = rv
                    # Validate FK
                    self._validate_fk(name, dict(zip([c.upper() for c in cols], ordered)))
                    before_out = self._fire_triggers('INSERT', name, dict(zip([c.upper() for c in cols], ordered)), timing='BEFORE')
                    if before_out and any('ORA-' in l for l in before_out):
                        continue
                    self._undo_log.append(('INSERT', name, len(self.rows[name]), list(ordered)))
                    self.rows[name].append(ordered)
                    row_count += 1
                return ["", f"{row_count} row(s) inserted."]

        values = [self._resolve_sequence_ref(self._strip_quotes(v)) for v in stmt.insert_values]
        if stmt.insert_columns:
            if len(stmt.insert_columns) != len(values):
                return ["", f"ERROR at line 1: ORA-00947: not enough values"]
            ordered = [''] * len(cols)
            col_map = {c.upper(): i for i, c in enumerate(cols)}
            for ic, iv in zip(stmt.insert_columns, values):
                if ic.upper() in col_map:
                    ordered[col_map[ic.upper()]] = iv
            row_data = {cols[i].upper(): ordered[i] for i in range(len(cols)) if i < len(ordered)}
        else:
            if len(values) != len(cols):
                if len(values) < len(cols):
                    return ["", f"ERROR at line 1: ORA-00947: not enough values"]
                else:
                    return ["", f"ERROR at line 1: ORA-00913: too many values"]
            ordered = values[:len(cols)]
            row_data = {cols[i].upper(): values[i] for i in range(len(cols))}

        # FK constraint validation
        fk_err = self._validate_fk(name, row_data)
        if fk_err:
            return fk_err

        # CHECK constraint validation
        check_err = self._validate_check_constraints(name, row_data, cols)
        if check_err:
            return check_err

        # Fire BEFORE INSERT triggers first — errors abort the insert
        try:
            before_out = self._fire_triggers('INSERT', name, row_data, timing='BEFORE')
            if before_out and any('ORA-' in l for l in before_out):
                return [""] + before_out
        except PLSQLError as e:
            return ["", f"  ORA-{abs(e.errno)}: {e.message}"]

        self._undo_log.append(('INSERT', name, len(self.rows[name]), list(ordered)))
        self.rows[name].append(ordered)
        self.rownum_counter += 1
        result = ["", "1 row created."]

        if before_out:
            result.extend([""] + before_out)
        # Fire AFTER INSERT triggers
        try:
            after_out = self._fire_triggers('INSERT', name, row_data, timing='AFTER')
            if after_out:
                result.extend([""] + after_out)
        except PLSQLError as e:
            result.append(f"  [{name}] ORA-{abs(e.errno)}: {e.message}")
        return result

    def _validate_fk(self, table_name: str, row_data: Dict[str, str]) -> Optional[List[str]]:
        table_def = self.tables.get(table_name)
        if not table_def:
            return None
        for col_def in table_def.columns:
            if col_def.is_foreign_key and col_def.references:
                parent_table, parent_col = col_def.references
                val = row_data.get(col_def.name.upper(), '')
                if val and val.upper() != 'NULL':
                    parent_rows = self.rows.get(parent_table, [])
                    parent_cols = self.get_column_names(parent_table)
                    pci = -1
                    for i, pc in enumerate(parent_cols):
                        if pc.upper() == parent_col.upper():
                            pci = i
                            break
                    if pci >= 0:
                        exists = any(
                            pci < len(pr) and pr[pci].strip().upper() == val.upper()
                            for pr in parent_rows
                        )
                        if not exists:
                            return ["", f"ERROR at line 1: ORA-02291: integrity constraint violated - parent key not found."]
        return None

    def _validate_check_constraints(self, table_name: str, row_data: Dict[str, str], cols: List[str]) -> Optional[List[str]]:
        table_def = self.tables.get(table_name)
        if not table_def:
            return None
        col_names_upper = [c.upper() for c in cols]
        # Column-level CHECK constraints
        for col_def in table_def.columns:
            if col_def.check_expr:
                check = col_def.check_expr.upper()
                col_idx = -1
                for i, cn in enumerate(col_names_upper):
                    if cn == col_def.name.upper():
                        col_idx = i
                        break
                if col_idx >= 0:
                    val = list(row_data.values())[col_idx] if col_idx < len(row_data) else ''
                    row_for_check = [list(row_data.values())]
                    if not self._evaluate_simple(row_for_check[0], col_names_upper, table_name, check):
                        return ["", f"ERROR at line 1: ORA-02290: check constraint violated."]
        # Table-level CHECK constraints from ALTER TABLE ADD CONSTRAINT
        for constraint_def in table_def.constraints:
            if 'CHECK' in constraint_def:
                check_match = re.search(r'CHECK\s*\((.+)\)', constraint_def, re.IGNORECASE)
                if check_match:
                    check_expr = check_match.group(1).strip()
                    row_for_check = [list(row_data.values())]
                    if not self._evaluate_simple(row_for_check[0], col_names_upper, table_name, check_expr):
                        return ["", f"ERROR at line 1: ORA-02290: check constraint violated."]
        return None

    @staticmethod
    def _strip_table_alias(col_expr: str) -> str:
        """Remove table alias prefix from column expression (e.g. 'c.Custname' -> 'CUSTNAME')."""
        s = col_expr.strip()
        if '(' in s:
            # Function call like SUM(l.Amount) -> keep as SUM(L.AMOUNT)
            return s.upper().rstrip(',')
        parts = s.split('.')
        raw = parts[-1].strip().upper().rstrip(',')
        return raw

    def _find_col_index(self, col_name: str, col_list: List[str]) -> int:
        """Find column index, trying exact match then alias-stripped match."""
        c_up = col_name.upper().strip()
        for i, tc in enumerate(col_list):
            if tc.upper().strip() == c_up:
                return i
        if '.' in c_up:
            bare = c_up.split('.')[-1]
            for i, tc in enumerate(col_list):
                if tc.upper().strip() == bare:
                    return i
        else:
            # Try matching suffix against dotted column names (e.g. 'CUSTNAME' in 'C.CUSTNAME')
            suffix = '.' + c_up
            for i, tc in enumerate(col_list):
                if tc.upper().strip().endswith(suffix):
                    return i
        return -1

    def _gather_table_data(self, table_name: str) -> Tuple[List[str], List[List[str]]]:
        """Get column names and rows for a table, generating dummy data if empty."""
        tname = table_name.upper()
        if tname in self.tables:
            cols = self.get_column_names(tname)
            rows = list(self.rows.get(tname, []))
            if not rows:
                dummy_count = random.randint(2, 4)
                for i in range(dummy_count):
                    row = [self.generate_dummy_value(c, self.get_column_types(tname).get(c, 'VARCHAR2'), i+1) for c in cols]
                    rows.append(row)
            return cols, rows
        if tname in self.views:
            view = self.views[tname]
            parsed = SQLParser.parse(view.query)
            if parsed.type == StatementType.SELECT and parsed.from_tables:
                # Complex views (JOIN, GROUP BY, aggregate, subquery) need full SELECT processing
                has_joins = len(parsed.joins) > 0 or len(parsed.from_tables) > 1
                has_agg = bool(parsed.group_by) or bool(parsed.having_clause) or \
                    any(c.upper().startswith(('COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX('))
                        for c in (parsed.select_columns or []))
                has_subq = bool(parsed.from_subqueries)
                if has_joins or has_agg or has_subq:
                    lines = self._handle_SELECT(parsed)
                    return self._parse_select_output_lines(lines)
                base_table = parsed.from_tables[0].upper()
                if base_table in self.tables:
                    base_cols = self.get_column_names(base_table)
                    base_rows = list(self.rows.get(base_table, []))
                    if parsed.select_columns and parsed.select_columns[0].upper().strip() != '*':
                        cols = [c.strip() for c in parsed.select_columns]
                    else:
                        cols = list(base_cols)
                    if parsed.select_columns and parsed.select_columns[0].upper().strip() != '*':
                        col_indices = []
                        for sc in parsed.select_columns:
                            raw = sc.strip()
                            idx = -1
                            for i, bc in enumerate(base_cols):
                                if bc.upper() == raw.upper():
                                    idx = i
                                    break
                            col_indices.append(idx)
                        rows = []
                        for row in base_rows:
                            new_row = [row[ci] if ci >= 0 and ci < len(row) else '' for ci in col_indices]
                            rows.append(new_row)
                    else:
                        rows = [list(r) for r in base_rows]
                    if parsed.where_clause and rows:
                        filtered = []
                        for row in rows:
                            if self._evaluate_simple(row, [c.upper() for c in cols], base_table, parsed.where_clause):
                                filtered.append(row)
                        rows = filtered
                    return [c.upper() for c in cols], rows
            return view.columns, [[f'VAL{j+1}' for j in range(len(view.columns))] for _ in range(2)]
        return [], []

    def _handle_SELECT(self, stmt: ParsedStatement) -> List[str]:
        lines = [""]

        # No FROM clause (DUAL or expression)
        if not stmt.from_tables:
            col_names = []
            all_data: List[List[str]] = []
            if stmt.select_columns:
                for sc in stmt.select_columns:
                    sc_up = sc.upper().strip()
                    col_names.append(sc_up)
                    if not all_data:
                        all_data.append([])

                    # Check for function calls: func_name(args) or func_name
                    func_match = re.match(r'(\w+)\s*\(([^)]*)\)', sc_up, re.IGNORECASE)
                    if func_match:
                        fname = func_match.group(1).upper()
                        fargs_str = func_match.group(2).strip()
                        fargs = [a.strip() for a in fargs_str.split(',') if a.strip()] if fargs_str else []

                        if fname in self.functions:
                            func = self.functions[fname]
                            param_values = {}
                            for i, (pname, pdirection, ptype) in enumerate(func.params):
                                if pdirection in ('IN', 'IN OUT') and i < len(fargs):
                                    param_values[pname] = fargs[i]
                                elif pdirection == 'IN':
                                    param_values[pname] = ''
                            out = []
                            ret = self._execute_plsql_body(func.body, param_values, out)
                            if ret is not None:
                                all_data[0].append(ret)
                            else:
                                all_data[0].append('(null)')
                        else:
                            # Unknown function - return dummy
                            all_data[0].append('42')
                    elif sc_up == 'SYSDATE':
                        all_data[0].append(time.strftime('%d-%b-%Y'))
                    elif sc_up == 'USER':
                        all_data[0].append('SCOTT')
                    elif sc_up == 'DUAL':
                        all_data[0].append('X')
                    else:
                        all_data[0].append(sc_up.strip("'\""))
            return self._format_select_output(col_names, all_data, lines)

        # Handle DUAL specially (single-table DUAL queries like SELECT func() FROM DUAL)
        is_dual = stmt.from_tables[0].upper() == 'DUAL' if stmt.from_tables else False
        if is_dual:
            col_names = []
            all_data: List[List[str]] = []
            if stmt.select_columns:
                for sc in stmt.select_columns:
                    sc_up = sc.upper().strip()
                    col_names.append(sc_up)
                    if not all_data:
                        all_data.append([])
                    func_match = re.match(r'(\w+)\s*\(([^)]*)\)', sc_up, re.IGNORECASE)
                    if func_match:
                        fname = func_match.group(1).upper()
                        fargs_str = func_match.group(2).strip()
                        fargs = [a.strip().strip("'\"") for a in fargs_str.split(',') if a.strip()] if fargs_str else []
                        if fname in self.functions:
                            func = self.functions[fname]
                            param_values = {}
                            for i, (pname, pdirection, ptype) in enumerate(func.params):
                                if pdirection in ('IN', 'IN OUT') and i < len(fargs):
                                    param_values[pname] = fargs[i]
                                elif pdirection == 'IN':
                                    param_values[pname] = ''
                            out = []
                            ret = self._execute_plsql_body(func.body, param_values, out)
                            if ret is not None:
                                all_data[0].append(ret)
                            else:
                                all_data[0].append('(null)')
                        else:
                            all_data[0].append('42')
                    elif sc_up == 'SYSDATE':
                        all_data[0].append(time.strftime('%d-%b-%Y'))
                    elif sc_up == 'USER':
                        all_data[0].append('SCOTT')
                    elif sc_up in self.functions:
                        # Function call without parens
                        func = self.functions[sc_up]
                        out = []
                        ret = self._execute_plsql_body(func.body, {}, out)
                        if ret is not None:
                            all_data[0].append(ret)
                        else:
                            all_data[0].append('(null)')
                    else:
                        all_data[0].append(sc_up.strip("'\""))
            return self._format_select_output(col_names, all_data, lines)

        # JOIN detection: multiple explicit tables
        is_join = len(stmt.from_tables) > 1
        # Keep table_cols in scope for GROUP BY aggregation resolution
        base_table_cols: List[str] = []

        if not is_join:
            primary_table = stmt.from_tables[0].upper()
            _source_pre_aggregated = False
            # Handle FROM subqueries (derived tables / inline views)
            if primary_table in stmt.from_subqueries:
                subq_sql = stmt.from_subqueries[primary_table]
                subq_parsed = SQLParser.parse(subq_sql)
                if subq_parsed.type != StatementType.SELECT:
                    return ["", f"ERROR at line 1: ORA-00900: invalid subquery in FROM clause."]
                subq_lines = self._handle_SELECT(subq_parsed)
                table_cols, table_rows = self._parse_select_output_lines(subq_lines)
                base_table_cols = table_cols
                if subq_parsed.group_by or subq_parsed.having_clause or \
                   any(c.upper().startswith(('COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX(')) for c in (subq_parsed.select_columns or [])):
                    _source_pre_aggregated = True

                # Determine columns to display
                if stmt.select_columns and stmt.select_columns[0].upper().strip() not in ('*', 'ALL'):
                    col_names = [self._strip_table_alias(sc) for sc in stmt.select_columns]
                else:
                    col_names = [c.upper() for c in table_cols]

                all_data = [list(r) for r in table_rows]
            elif primary_table not in self.tables and primary_table not in self.views:
                return ["", f"ERROR at line 1: ORA-00942: table or view '{primary_table}' does not exist."]
            else:
                table_cols, table_rows = self._gather_table_data(primary_table)
                base_table_cols = table_cols

                # Determine columns to display
                if stmt.select_columns and stmt.select_columns[0].upper().strip() not in ('*', 'ALL'):
                    col_names = [self._strip_table_alias(sc) for sc in stmt.select_columns]
                else:
                    col_names = [c.upper() for c in table_cols]

                all_data = [list(r) for r in table_rows]

            # Compute has_agg early for flow control
            has_agg = any(c.upper().startswith(('COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX(')) for c in col_names)

            # Don't re-apply aggregation for pre-aggregated sources (views or subqueries)
            if _source_pre_aggregated:
                has_agg = False
            elif primary_table in self.views:
                vp = SQLParser.parse(self.views[primary_table].query)
                if vp.group_by or vp.having_clause or \
                   any(c.upper().startswith(('COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX(')) for c in (vp.select_columns or [])):
                    has_agg = False

            # Apply WHERE before column resolution or aggregates
            if stmt.where_clause and not is_join and all_data:
                all_data = self._apply_where(all_data, table_cols, primary_table, stmt.where_clause)
                stmt.where_clause = ''  # Prevent double application

            # If GROUP BY or aggregate-only select, don't resolve columns yet
            if stmt.group_by:
                pass  # Keep full table data for _apply_group_by
            elif has_agg and not stmt.group_by:
                pass  # Keep full table data for aggregate block
            elif stmt.select_columns and stmt.select_columns[0].upper().strip() not in ('*', 'ALL'):
                # Resolve column order if explicit select columns (without GROUP BY)
                resolved_data = []
                for row in all_data:
                    new_row = []
                    for sc in stmt.select_columns:
                        raw = self._strip_table_alias(sc)
                        idx = -1
                        for i, tc in enumerate(table_cols):
                            if tc.upper() == raw:
                                idx = i
                                break
                        if idx >= 0 and idx < len(row):
                            new_row.append(row[idx])
                        else:
                            # Handle aggregate or expression
                            sc_up = sc.upper().strip()
                            if sc_up.startswith('COUNT('):
                                distinct_m = re.match(r'COUNT\(\s*DISTINCT\s+([\w.]+)\s*\)', sc_up, re.IGNORECASE)
                                if distinct_m:
                                    sci = self._find_col_index(distinct_m.group(1), table_cols)
                                    distinct_vals = set()
                                    for r in table_rows:
                                        if sci >= 0 and sci < len(r) and r[sci].strip() and r[sci].strip().upper() != 'NULL':
                                            distinct_vals.add(r[sci].strip().upper())
                                    new_row.append(str(len(distinct_vals)))
                                else:
                                    new_row.append(str(len(table_rows)))
                            elif sc_up.startswith('SUM('):
                                m = re.search(r'SUM\(([\w.]+)\)', sc_up)
                                if m:
                                    sci = self._find_col_index(m.group(1), table_cols)
                                    if sci >= 0:
                                        total = sum(int(r[sci]) for r in table_rows if sci < len(r) and r[sci].lstrip('-').isdigit())
                                        new_row.append(str(total))
                                    else:
                                        new_row.append('0')
                                else:
                                    new_row.append('')
                            elif sc_up.startswith('AVG(') or sc_up.startswith('MIN(') or sc_up.startswith('MAX('):
                                new_row.append(str(round(random.uniform(10, 1000), 2)))
                            else:
                                # Try arithmetic expression (e.g., Price * qty)
                                arith_val = self._evaluate_expression(sc, row, table_cols)
                                if arith_val != sc:
                                    new_row.append(arith_val)
                                else:
                                    new_row.append('')
                    resolved_data.append(new_row)
                all_data = resolved_data

            if has_agg and not stmt.group_by:
                agg_src = all_data if all_data else table_rows
                agg_cols_src = table_cols
                agg_row = []
                for c in col_names:
                    if c.upper().startswith('COUNT('):
                        distinct_m = re.match(r'COUNT\(\s*DISTINCT\s+([\w.]+)\s*\)', c, re.IGNORECASE)
                        if distinct_m:
                            ci = self._find_col_index(distinct_m.group(1), agg_cols_src)
                            distinct_vals = set()
                            for r in agg_src:
                                if ci >= 0 and ci < len(r) and r[ci].strip() and r[ci].strip().upper() != 'NULL':
                                    distinct_vals.add(r[ci].strip().upper())
                            agg_row.append(str(len(distinct_vals)))
                        else:
                            agg_row.append(str(len(agg_src)))
                    elif c.upper().startswith('SUM('):
                        m = re.search(r'SUM\(([\w.]+)\)', c, re.IGNORECASE)
                        if m:
                            ci = self._find_col_index(m.group(1), agg_cols_src)
                            total = sum(int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-').isdigit()) if ci >= 0 else 0
                            agg_row.append(str(total))
                        else:
                            agg_row.append('0')
                    elif c.upper().startswith('AVG('):
                        m = re.search(r'AVG\(([\w.]+)\)', c, re.IGNORECASE)
                        if m:
                            ci = self._find_col_index(m.group(1), agg_cols_src)
                            vals = [int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit()]
                            agg_row.append(str(round(sum(vals) / len(vals), 2)) if vals else '0')
                        else:
                            agg_row.append('0')
                    elif c.upper().startswith('MIN('):
                        m = re.search(r'MIN\(([\w.]+)\)', c, re.IGNORECASE)
                        if m:
                            ci = self._find_col_index(m.group(1), agg_cols_src)
                            vals = [int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit()]
                            agg_row.append(str(min(vals)) if vals else '0')
                        else:
                            agg_row.append('0')
                    elif c.upper().startswith('MAX('):
                        m = re.search(r'MAX\(([\w.]+)\)', c, re.IGNORECASE)
                        if m:
                            ci = self._find_col_index(m.group(1), agg_cols_src)
                            vals = [int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit()]
                            agg_row.append(str(max(vals)) if vals else '0')
                        else:
                            agg_row.append('0')
                    else:
                        arith_val = self._evaluate_expression(c, ['' for _ in agg_cols_src] if not agg_src else agg_src[0], agg_cols_src)
                        if arith_val != c:
                            agg_row.append(arith_val)
                        else:
                            agg_row.append('')
                all_data = [agg_row]
        else:
            # JOIN handling - combine data from multiple tables
            all_cols = []
            all_rows_data = []
            table_data_map = {}

            for tname in stmt.from_tables:
                t_up = tname.upper()
                if t_up not in self.tables and t_up not in self.views:
                    continue
                tcols, trows = self._gather_table_data(t_up)
                table_data_map[t_up] = (tcols, trows)
                all_cols.append((t_up, tcols))

            # Build combined column list
            if stmt.select_columns and stmt.select_columns[0].upper().strip() not in ('*', 'ALL'):
                combined_col_names = [self._strip_table_alias(sc) for sc in stmt.select_columns]
            else:
                combined_col_names = []
                for tup, tcols in all_cols:
                    combined_col_names.extend(tcols)

            # Build combined rows using stored join information
            table_list = list(table_data_map.items())
            # Use aliased column names to distinguish duplicate columns across tables
            total_col_list = []
            for tup, ccols in all_cols:
                alias = stmt.table_aliases.get(tup, tup)
                for c in ccols:
                    total_col_list.append(f'{alias}.{c}')
            if not total_col_list:
                total_col_list = [c for tup, ccols in all_cols for c in ccols]
            base_table_cols = total_col_list
            if table_list:
                if len(table_list) == 1:
                    first_tname, (first_tcols, first_trows) = table_list[0]
                    all_rows_data = [list(r) for r in first_trows]
                elif stmt.joins:
                    # Explicit JOIN syntax - chained processing for 2+ tables
                    first_tname, (first_tcols, first_trows) = table_list[0]
                    # Initialize with first table's rows and aliased column names
                    all_rows_data = [list(r) for r in first_trows]
                    first_alias = stmt.table_aliases.get(first_tname, first_tname)
                    current_cols = [f'{first_alias}.{c}' for c in first_tcols]

                    for ji, (tname, (tcols, trows)) in enumerate(table_list[1:]):
                        join_type = 'JOIN'
                        if ji < len(stmt.joins):
                            join_type = stmt.joins[ji][0]
                        is_left = 'LEFT' in join_type
                        is_right = 'RIGHT' in join_type
                        is_full = 'FULL' in join_type
                        on_condition = stmt.joins[ji][2] if ji < len(stmt.joins) else ''

                        # Build right-side aliased column names
                        right_alias = stmt.table_aliases.get(tname, tname)
                        right_cols = [f'{right_alias}.{c}' for c in tcols]
                        combined_cols = current_cols + right_cols

                        # Fallback: common column names for NATURAL JOIN (no ON clause)
                        common_cols = [c for c in first_tcols if c in tcols] if not on_condition else []

                        new_data = []
                        right_matched = set()

                        for left_row in all_rows_data:
                            matched_any = False
                            for sr_idx, sr in enumerate(trows):
                                combined_row = list(left_row) + list(sr)
                                if on_condition:
                                    if self._evaluate_condition(combined_row, combined_cols, '', on_condition):
                                        new_data.append(combined_row)
                                        matched_any = True
                                        right_matched.add(sr_idx)
                                elif common_cols:
                                    match = True
                                    for cc in common_cols:
                                        idx1 = current_cols.index(f'{first_alias}.{cc}') if f'{first_alias}.{cc}' in current_cols else -1
                                        idx2 = right_cols.index(f'{right_alias}.{cc}') if f'{right_alias}.{cc}' in right_cols else -1
                                        if idx1 >= 0 and idx2 >= 0 and idx1 < len(left_row) and idx2 < len(sr) and left_row[idx1] != sr[idx2]:
                                            match = False
                                            break
                                    if match:
                                        new_data.append(combined_row)
                                        matched_any = True
                                        right_matched.add(sr_idx)
                                else:
                                    # No ON condition and no common columns: CROSS JOIN
                                    new_data.append(combined_row)
                                    matched_any = True
                                    right_matched.add(sr_idx)

                            if not matched_any and (is_left or is_full):
                                new_data.append(list(left_row) + [''] * len(tcols))

                        # RIGHT/FULL JOIN: add unmatched right rows
                        if is_right or is_full:
                            for sr_idx, sr in enumerate(trows):
                                if sr_idx not in right_matched:
                                    new_data.append([''] * len(current_cols) + list(sr))

                        all_rows_data = new_data
                        current_cols = combined_cols
                else:
                    # Comma-join: build full cartesian product
                    all_rows_data = [[]]
                    for tname, (tcols, trows) in table_list:
                        new_data = []
                        for r in all_rows_data:
                            for sr in trows:
                                new_data.append(list(r) + list(sr))
                        all_rows_data = new_data

                # Apply WHERE before reducing to selected columns
                if stmt.where_clause:
                    all_rows_data = self._apply_where(all_rows_data, total_col_list, stmt.from_tables[0], stmt.where_clause)

                col_names = combined_col_names

                # Detect aggregate functions in select columns
                join_has_agg = any(c.upper().startswith(('COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX(')) for c in col_names)

                # If explicit select columns, filter/map the data (skip if GROUP BY or agg)
                if stmt.select_columns and stmt.select_columns[0].upper().strip() not in ('*', 'ALL') and not stmt.group_by and not join_has_agg:
                    resolved = []
                    for row in all_rows_data:
                        new_row = []
                        for sc in stmt.select_columns:
                            raw = self._strip_table_alias(sc)
                            idx = self._resolve_col(sc, total_col_list)
                            if idx >= 0 and idx < len(row):
                                new_row.append(row[idx])
                            else:
                                new_row.append('')
                        resolved.append(new_row)
                    all_rows_data = resolved
                    col_names = combined_col_names
                else:
                    col_names = combined_col_names

                all_data = all_rows_data

                # Compute aggregates for JOIN path
                if join_has_agg and not stmt.group_by:
                    agg_src = all_data
                    agg_cols_src = total_col_list
                    agg_row = []
                    for c in col_names:
                        if c.upper().startswith('COUNT('):
                            distinct_m = re.match(r'COUNT\(\s*DISTINCT\s+([\w.]+)\s*\)', c, re.IGNORECASE)
                            if distinct_m:
                                ci = self._find_col_index(distinct_m.group(1), agg_cols_src)
                                distinct_vals = set()
                                for r in agg_src:
                                    if ci >= 0 and ci < len(r) and r[ci].strip() and r[ci].strip().upper() != 'NULL':
                                        distinct_vals.add(r[ci].strip().upper())
                                agg_row.append(str(len(distinct_vals)))
                            else:
                                agg_row.append(str(len(agg_src)))
                        elif c.upper().startswith('SUM('):
                            m = re.search(r'SUM\(([\w.]+)\)', c, re.IGNORECASE)
                            if m:
                                ci = self._find_col_index(m.group(1), agg_cols_src)
                                total = sum(int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-').isdigit()) if ci >= 0 else 0
                                agg_row.append(str(total))
                            else:
                                agg_row.append('0')
                        elif c.upper().startswith('AVG('):
                            m = re.search(r'AVG\(([\w.]+)\)', c, re.IGNORECASE)
                            if m:
                                ci = self._find_col_index(m.group(1), agg_cols_src)
                                vals = [int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit()]
                                agg_row.append(str(round(sum(vals) / len(vals), 2)) if vals else '0')
                            else:
                                agg_row.append('0')
                        elif c.upper().startswith('MIN('):
                            m = re.search(r'MIN\(([\w.]+)\)', c, re.IGNORECASE)
                            if m:
                                ci = self._find_col_index(m.group(1), agg_cols_src)
                                vals = [int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit()]
                                agg_row.append(str(min(vals)) if vals else '0')
                            else:
                                agg_row.append('0')
                        elif c.upper().startswith('MAX('):
                            m = re.search(r'MAX\(([\w.]+)\)', c, re.IGNORECASE)
                            if m:
                                ci = self._find_col_index(m.group(1), agg_cols_src)
                                vals = [int(r[ci]) for r in agg_src if ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit()]
                                agg_row.append(str(max(vals)) if vals else '0')
                            else:
                                agg_row.append('0')
                        else:
                            arith_val = self._evaluate_expression(c, ['' for _ in agg_cols_src] if not agg_src else agg_src[0], agg_cols_src)
                            if arith_val != c:
                                agg_row.append(arith_val)
                            else:
                                agg_row.append('')
                    all_data = [agg_row]
            else:
                all_data = []

        # Apply WHERE for single-table queries
        if stmt.where_clause and not is_join and all_data:
            primary_table = stmt.from_tables[0].upper() if stmt.from_tables else ""
            all_data = self._apply_where(all_data, col_names, primary_table, stmt.where_clause)

        # Apply GROUP BY
        if stmt.group_by:
            # Extract aggregate functions from HAVING clause so _apply_group_by computes them
            having_agg_cols = []
            if stmt.having_clause:
                for m in re.finditer(r'(SUM|COUNT|AVG|MIN|MAX)\s*\(([^)]*)\)', stmt.having_clause, re.IGNORECASE):
                    having_agg_cols.append(m.group(0).upper().strip())
            gb_col_names = list(col_names)
            for hac in having_agg_cols:
                if hac not in gb_col_names:
                    gb_col_names.append(hac)
            all_data = self._apply_group_by(all_data, gb_col_names, stmt, base_table_cols)
            # Update col_names to match select columns if explicit
            if stmt.select_columns and stmt.select_columns[0].upper().strip() not in ('*', 'ALL'):
                col_names = [self._strip_table_alias(sc) for sc in stmt.select_columns]

        # Apply HAVING after GROUP BY
        if stmt.having_clause and all_data:
            # If HAVING uses aggregates, compute them from the grouped data
            having_agg_cols = []
            for m in re.finditer(r'(SUM|COUNT|AVG|MIN|MAX)\s*\(([^)]*)\)', stmt.having_clause, re.IGNORECASE):
                having_agg_cols.append(m.group(0).upper().strip())
            # Track which were added only for HAVING (not in original select columns)
            base_col_names = list(col_names)
            if having_agg_cols:
                for hc in having_agg_cols:
                    if hc not in col_names:
                        col_names.append(hc)
            all_data = self._apply_having(all_data, col_names, stmt)
            # Remove only HAVING-only aggregate columns (not in original select)
            extra_aggs = [c for c in having_agg_cols if c not in base_col_names]
            if extra_aggs:
                keep_indices = [i for i, c in enumerate(col_names) if c not in extra_aggs]
                col_names = [c for i, c in enumerate(col_names) if i in keep_indices]
                all_data = [[row[i] for i in keep_indices] for row in all_data]

        # Apply ORDER BY
        if stmt.order_by:
            primary_table = stmt.from_tables[0].upper() if stmt.from_tables else ""
            all_data = self._apply_order_by(all_data, col_names, stmt.order_by)

        return self._format_select_output(col_names, all_data, lines)

    def _filter_and_sort(self, data: List[List[str]], col_names: List[str],
                         table: str, stmt: ParsedStatement) -> List[List[str]]:
        result = [list(row) for row in data]
        if stmt.where_clause:
            result = self._apply_where(result, col_names, table, stmt.where_clause)
        if stmt.group_by:
            result = self._apply_group_by(result, col_names, stmt, col_names)
        if stmt.having_clause and result:
            result = self._apply_having(result, col_names, stmt)
        if stmt.order_by:
            result = self._apply_order_by(result, col_names, stmt.order_by)
        return result

    def _apply_where(self, data: List[List[str]], col_names: List[str],
                     table: str, where: str) -> List[List[str]]:
        filtered = []
        for row in data:
            if self._evaluate_condition(row, col_names, table, where):
                filtered.append(row)
        return filtered

    def _evaluate_condition(self, row: List[str], col_names: List[str],
                            table: str, condition: str) -> bool:
        cond_upper = condition.upper().strip()
        # Split on OR first (lowest precedence), then within each part split on AND
        or_parts = self._split_respecting_parens(cond_upper, 'OR')
        if len(or_parts) > 1:
            return any(self._evaluate_and_chain(row, col_names, table, p.strip()) for p in or_parts)
        return self._evaluate_and_chain(row, col_names, table, condition)

    def _evaluate_and_chain(self, row: List[str], col_names: List[str],
                            table: str, condition: str) -> bool:
        and_parts = self._split_respecting_parens(condition.upper().strip(), 'AND')
        if len(and_parts) > 1:
            return all(self._evaluate_simple(row, col_names, table, p.strip()) for p in and_parts)
        return self._evaluate_simple(row, col_names, table, condition)

    @staticmethod
    def _split_respecting_parens(text: str, keyword: str) -> List[str]:
        parts = []
        current = ""
        depth = 0
        in_string = False
        string_char = None
        keyword_upper = keyword.upper()
        i = 0
        while i < len(text):
            ch = text[i]
            if ch in ("'", '"'):
                if not in_string:
                    in_string = True
                    string_char = ch
                elif ch == string_char:
                    in_string = False
                current += ch
            elif ch == '(':
                depth += 1
                current += ch
            elif ch == ')':
                depth -= 1
                current += ch
            elif ch == ',' and depth == 0:
                current += ch
            elif depth == 0 and not in_string and text[i:i+len(keyword)].upper() == keyword_upper:
                if (i == 0 or not text[i-1].isalnum()) and (i+len(keyword) >= len(text) or not text[i+len(keyword)].isalnum()):
                    parts.append(current.strip())
                    current = ""
                    i += len(keyword) - 1
                else:
                    current += ch
            else:
                current += ch
            i += 1
        if current.strip():
            parts.append(current.strip())
        return parts

    @staticmethod
    def _resolve_col(name: str, col_names: List[str]) -> int:
        """Find column index, stripping table alias prefix if present."""
        raw = name.upper().strip()
        for i, c in enumerate(col_names):
            if c.upper().strip() == raw:
                return i
        if '.' in raw:
            raw = raw.split('.')[-1]
        stripped_raw = raw.strip()
        for i, c in enumerate(col_names):
            c_up = c.upper().strip()
            if c_up == stripped_raw:
                return i
            if '.' in c_up:
                c_part = c_up.split('.')[-1].strip()
                if c_part == stripped_raw:
                    return i
            # Handle "expr AS alias" column names
            as_idx = c_up.find(' AS ')
            if as_idx >= 0:
                alias_part = c_up[as_idx + 4:].strip()
                if alias_part == stripped_raw:
                    return i
                if '.' in alias_part:
                    alias_bare = alias_part.split('.')[-1].strip()
                    if alias_bare == stripped_raw:
                        return i
        return -1

    @staticmethod
    def _is_numeric(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    def _evaluate_simple(self, row: List[str], col_names: List[str],
                         table: str, condition: str) -> bool:
        cond = condition.strip()
        # LIKE
        like_match = re.match(r"([\w.]+)\s+LIKE\s+'([^']*)'", cond, re.IGNORECASE)
        if like_match:
            col = like_match.group(1).upper()
            pattern = like_match.group(2)
            idx = self._resolve_col(col, col_names)
            if idx >= 0 and idx < len(row):
                val = row[idx].upper()
                pat_upper = pattern.upper()
                if pat_upper.startswith('%') and pat_upper.endswith('%'):
                    return pat_upper[1:-1] in val
                elif pat_upper.startswith('%'):
                    return val.endswith(pat_upper[1:])
                elif pat_upper.endswith('%'):
                    return val.startswith(pat_upper[:-1])
                else:
                    return val == pat_upper
            return False
        # IN (including subqueries)
        in_match = re.match(r"([\w.]+)\s+(?:NOT\s+)?IN\s*\(", cond, re.IGNORECASE)
        if in_match:
            col = in_match.group(1).upper()
            start = in_match.end()
            depth = 1
            i = start
            while i < len(cond) and depth > 0:
                if cond[i] == '(':
                    depth += 1
                elif cond[i] == ')':
                    depth -= 1
                i += 1
            in_expr = cond[start:i-1].strip() if depth == 0 else cond[start:].strip()
            idx = self._resolve_col(col, col_names)
            if idx >= 0 and idx < len(row):
                val = row[idx].strip("'\"").upper()
                is_not = 'NOT' in cond.upper().split('IN')[0]
                # Detect subquery
                if 'SELECT' in in_expr.upper():
                    sub_vals = self._execute_subquery(in_expr)
                    matched = val in [v.upper() for v in sub_vals]
                else:
                    in_vals = [v.strip().strip("'\"") for v in in_expr.split(',')]
                    matched = val in [v.upper() for v in in_vals]
                return not matched if is_not else matched
            return 'NOT' not in cond.upper()
        # BETWEEN
        between_match = re.match(r"([\w.]+)\s+(?:NOT\s+)?BETWEEN\s+(.+?)\s+AND\s+(.+)", cond, re.IGNORECASE)
        if between_match:
            col = between_match.group(1).upper()
            low = between_match.group(2).strip().strip("'\"")
            high = between_match.group(3).strip().strip("'\"")
            idx = self._resolve_col(col, col_names)
            if idx >= 0 and idx < len(row):
                val = row[idx].strip("'\"")
                try:
                    v = float(val)
                    l = float(low)
                    h = float(high)
                    is_not = 'NOT' in cond.upper().split('BETWEEN')[0]
                    matched = l <= v <= h
                    return not matched if is_not else matched
                except ValueError:
                    return True
            return True
        # IS NULL / IS NOT NULL
        null_match = re.match(r"([\w.]+)\s+IS\s+(NOT\s+)?NULL", cond, re.IGNORECASE)
        if null_match:
            col = null_match.group(1).upper()
            is_not = null_match.group(2) is not None
            idx = self._resolve_col(col, col_names)
            if idx >= 0 and idx < len(row):
                val = row[idx].strip()
                is_null = val == '' or val.upper() == 'NULL'
                return not is_null if is_not else is_null
            return False
        # Simple comparison (handle both column names and function calls like SUM(qty))
        comp_match = re.match(r"([\w().*]+)\s*([=<>!]+)\s*(.+)", cond, re.IGNORECASE | re.DOTALL)
        if comp_match:
            col = comp_match.group(1).upper()
            op = comp_match.group(2).strip()
            right_side = comp_match.group(3).strip()
            # Check for scalar subquery on RHS: e.g., COL = (SELECT ...)
            if re.match(r'\(\s*SELECT\b', right_side, re.IGNORECASE):
                # Substitute correlated references with outer row values
                sub_sql = right_side
                inner_aliases = set()
                fm = re.search(r'\bFROM\s+(\w+)(?:\s+(\w+))?', sub_sql, re.IGNORECASE)
                if fm:
                    inner_aliases.add((fm.group(2) or fm.group(1)).upper())
                for jm in re.finditer(r'\bJOIN\s+(\w+)(?:\s+(\w+))?', sub_sql, re.IGNORECASE):
                    inner_aliases.add((jm.group(2) or jm.group(1)).upper())
                def sub_correlated(m):
                    alias = m.group(1).upper()
                    coln = m.group(2).upper()
                    if alias not in inner_aliases:
                        for ci, cn in enumerate(col_names):
                            cn_bare = cn.upper().strip().split('.')[-1]
                            if cn_bare == coln and ci < len(row):
                                return row[ci]
                    return m.group(0)
                sub_sql = re.sub(r'(\w+)\.(\w+)', sub_correlated, sub_sql)
                sub_val = self._execute_scalar_subquery(sub_sql)
                if sub_val is not None:
                    right_side = sub_val
                else:
                    return op == '='
            val_str = right_side.strip("'\"").strip()
            idx = self._resolve_col(col, col_names)
            if idx >= 0 and idx < len(row):
                cell_val = row[idx].strip().strip("'\"")
                # Resolve RHS - check PL/SQL variables first, then column names
                rhs_val = val_str
                rhs_is_var = False
                plsql_vars = getattr(self, '_plsql_vars', None)
                if plsql_vars and right_side.upper() in plsql_vars:
                    rhs_val = plsql_vars[right_side.upper()]
                    rhs_is_var = True
                elif plsql_vars and val_str.upper() in plsql_vars:
                    rhs_val = plsql_vars[val_str.upper()]
                    rhs_is_var = True
                if not rhs_is_var:
                    rhs_idx = self._resolve_col(right_side, col_names)
                    if rhs_idx >= 0 and rhs_idx < len(row):
                        rhs_val = row[rhs_idx].strip().strip("'\"")
                try:
                    cv = float(cell_val)
                    vv = float(rhs_val)
                    if op == '=': return cv == vv
                    elif op == '>': return cv > vv
                    elif op == '<': return cv < vv
                    elif op == '>=': return cv >= vv
                    elif op == '<=': return cv <= vv
                    elif op in ('<>', '!='): return cv != vv
                except ValueError:
                    cell_is_num = self._is_numeric(cell_val)
                    rhs_is_num = self._is_numeric(rhs_val)
                    if cell_is_num != rhs_is_num:
                        if op == '=': return False
                        elif op in ('<>', '!='): return True
                        else: return False
                    cv_up = cell_val.upper()
                    vv_up = rhs_val.upper()
                    if op == '=': return cv_up == vv_up
                    elif op in ('<>', '!='): return cv_up != vv_up
                    elif op == '>': return cv_up > vv_up
                    elif op == '<': return cv_up < vv_up
                    elif op == '>=': return cv_up >= vv_up
                    elif op == '<=': return cv_up <= vv_up
            # Left side might be a PL/SQL variable or literal
            plsql_vars = getattr(self, '_plsql_vars', None)
            if plsql_vars and col in plsql_vars:
                cell_val = plsql_vars[col]
                rhs_val = val_str
                if right_side.upper() in plsql_vars:
                    rhs_val = plsql_vars[right_side.upper()]
                elif val_str.upper() in plsql_vars:
                    rhs_val = plsql_vars[val_str.upper()]
                else:
                    rhs_idx = self._resolve_col(right_side, col_names)
                    if rhs_idx >= 0 and rhs_idx < len(row):
                        rhs_val = row[rhs_idx].strip().strip("'\"")
                try:
                    cv = float(cell_val)
                    vv = float(rhs_val)
                    if op == '=': return cv == vv
                    elif op == '>': return cv > vv
                    elif op == '<': return cv < vv
                    elif op == '>=': return cv >= vv
                    elif op == '<=': return cv <= vv
                    elif op in ('<>', '!='): return cv != vv
                except ValueError:
                    cell_is_num = self._is_numeric(cell_val)
                    rhs_is_num = self._is_numeric(rhs_val)
                    if cell_is_num != rhs_is_num:
                        if op == '=': return False
                        elif op in ('<>', '!='): return True
                        else: return False
                    cv_up = cell_val.upper()
                    vv_up = rhs_val.upper()
                    if op == '=': return cv_up == vv_up
                    elif op in ('<>', '!='): return cv_up != vv_up
                    elif op == '>': return cv_up > vv_up
                    elif op == '<': return cv_up < vv_up
                    elif op == '>=': return cv_up >= vv_up
                    elif op == '<=': return cv_up <= vv_up
            return op == '=' and val_str.upper() == 'NULL'
        # Fallback: attempt simple substring match or return False
        try:
            return cond.upper() in str(row).upper()
        except:
            return False

    def _apply_group_by(self, data: List[List[str]], col_names: List[str],
                        stmt: ParsedStatement, table_cols: Optional[List[str]] = None) -> List[List[str]]:
        if not stmt.group_by:
            return data
        search_cols = table_cols if table_cols else col_names
        gb_cols = [g.strip().upper() for g in stmt.group_by]

        # Map each select column to its index in the full data (search_cols)
        # non-aggregate columns have a direct index; aggregate columns don't
        col_to_data_idx = []
        for c in col_names:
            c_up = c.upper().strip()
            if c_up.startswith(('COUNT(', 'SUM(', 'AVG(', 'MIN(', 'MAX(')):
                col_to_data_idx.append(-1)  # aggregate column
            else:
                col_to_data_idx.append(self._find_col_index(c_up, search_cols))

        # Find group-by column indices IN search_cols (for grouping)
        gb_data_indices = []
        for gc in gb_cols:
            idx = self._find_col_index(gc, search_cols)
            if idx >= 0:
                gb_data_indices.append(idx)
            else:
                gb_data_indices.append(0)

        if not gb_data_indices:
            return data[:min(3, len(data))]

        groups: Dict[str, List[List[str]]] = {}
        for row in data:
            key = '|'.join(str(row[i]) if i < len(row) else '' for i in gb_data_indices if i < len(row))
            if key not in groups:
                groups[key] = []
            groups[key].append(row)

        result = []
        for key, rows in groups.items():
            new_row = ['' for _ in col_names]
            for i, c in enumerate(col_names):
                di = col_to_data_idx[i]
                if c.upper().startswith('COUNT('):
                    distinct_m = re.match(r'COUNT\(\s*DISTINCT\s+([\w.]+)\s*\)', c, re.IGNORECASE)
                    if distinct_m:
                        sci = self._find_col_index(distinct_m.group(1), search_cols)
                        distinct_vals = set()
                        for r in rows:
                            if sci >= 0 and sci < len(r) and r[sci].strip() and r[sci].strip().upper() != 'NULL':
                                distinct_vals.add(r[sci].strip().upper())
                        new_row[i] = str(len(distinct_vals))
                    else:
                        new_row[i] = str(len(rows))
                elif c.upper().startswith('SUM('):
                    m = re.search(r'SUM\(([\w.]+)\)', c, re.IGNORECASE)
                    if m:
                        sci = self._find_col_index(m.group(1), search_cols)
                        if sci >= 0:
                            total = sum(int(r[sci]) for r in rows if sci < len(r) and r[sci].lstrip('-').isdigit())
                            new_row[i] = str(total)
                elif c.upper().startswith('AVG('):
                    m = re.search(r'AVG\(([\w.]+)\)', c, re.IGNORECASE)
                    if m:
                        sci = self._find_col_index(m.group(1), search_cols)
                        vals = [float(r[sci]) for r in rows if sci >= 0 and sci < len(r) and r[sci].lstrip('-.').replace('.','',1).isdigit()]
                        new_row[i] = str(round(sum(vals) / len(vals), 2)) if vals else '0'
                elif c.upper().startswith('MIN('):
                    m = re.search(r'MIN\(([\w.]+)\)', c, re.IGNORECASE)
                    if m:
                        sci = self._find_col_index(m.group(1), search_cols)
                        vals = [int(r[sci]) for r in rows if sci >= 0 and sci < len(r) and r[sci].lstrip('-.').replace('.','',1).isdigit()]
                        new_row[i] = str(min(vals)) if vals else '0'
                elif c.upper().startswith('MAX('):
                    m = re.search(r'MAX\(([\w.]+)\)', c, re.IGNORECASE)
                    if m:
                        sci = self._find_col_index(m.group(1), search_cols)
                        vals = [int(r[sci]) for r in rows if sci >= 0 and sci < len(r) and r[sci].lstrip('-.').replace('.','',1).isdigit()]
                        new_row[i] = str(max(vals)) if vals else '0'
                elif di >= 0 and di < len(rows[0]):
                    # Non-aggregate column - take from first row in group
                    new_row[i] = rows[0][di]
            result.append(new_row)
        return result

    def _apply_having(self, data: List[List[str]], col_names: List[str],
                      stmt: ParsedStatement) -> List[List[str]]:
        if not stmt.having_clause or not data:
            return data
        having = stmt.having_clause
        filtered = []
        for row in data:
            row_dict = dict(zip([c.upper() for c in col_names], row))
            if self._evaluate_having(row, col_names, having):
                filtered.append(row)
        return filtered if filtered else data[:0]

    def _evaluate_having(self, row: List[str], col_names: List[str],
                         having: str) -> bool:
        return self._evaluate_condition(row, col_names, '', having)

    def _apply_order_by(self, data: List[List[str]], col_names: List[str],
                        order_by: List[str]) -> List[List[str]]:
        if not order_by or not data:
            return data
        ob_col = order_by[0].strip().upper()
        desc = 'DESC' in ob_col
        ob_clean = ob_col.replace(' ASC', '').replace(' DESC', '').strip()
        idx = -1
        for i, c in enumerate(col_names):
            if c.upper().strip() == ob_clean:
                idx = i
                break
        if idx < 0:
            return data
        try:
            return sorted(data, key=lambda r: float(r[idx]) if r[idx].lstrip('-.').replace('.','',1).isdigit() else r[idx].upper(), reverse=desc)
        except (ValueError, IndexError):
            return sorted(data, key=lambda r: str(r[idx]).upper() if idx < len(r) else '', reverse=desc)

    def _format_select_output(self, col_names: List[str], data: List[List[str]],
                              lines: List[str]) -> List[str]:
        if not col_names or not data:
            lines.append("no rows selected")
            return lines

        widths = []
        for i, c in enumerate(col_names):
            max_w = len(c)
            for row in data:
                if i < len(row):
                    max_w = max(max_w, len(str(row[i])))
            widths.append(max(max_w, len(c)) if data else max_w)

        header = ""
        for i, c in enumerate(col_names):
            header += f"{'  ' + c:>{widths[i] + 2}}"
        lines.append(header)

        sep = ""
        for w in widths:
            sep += "  " + "-" * w
        lines.append(sep)

        for row in data:
            row_str = ""
            for i, c in enumerate(col_names):
                val = str(row[i]) if i < len(row) else ""
                row_str += f"{'  ' + val:>{widths[i] + 2}}"
            lines.append(row_str)

        row_count = len(data)
        lines.append("")
        lines.append(f"{row_count} row(s) selected.")
        return lines

    def _parse_select_output_lines(self, lines: List[str]) -> Tuple[List[str], List[List[str]]]:
        """Parse formatted SELECT output back into column names and data rows."""
        data_lines = [l for l in lines if l.strip()]
        if not data_lines:
            return [], []
        if re.search(r'\d+ row\(s\) selected\.', data_lines[-1]):
            data_lines = data_lines[:-1]
        if len(data_lines) < 2:
            return [], []

        sep = data_lines[1]
        col_starts = []
        col_ends = []
        i = 0
        while i < len(sep):
            if sep[i] == '-':
                start = i
                while i < len(sep) and sep[i] == '-':
                    i += 1
                col_starts.append(start)
                col_ends.append(i)
            else:
                i += 1
        if not col_starts:
            return [], []

        col_names = []
        for s, e in zip(col_starts, col_ends):
            col_names.append(data_lines[0][s:e].strip())

        data_rows = []
        for line in data_lines[2:]:
            row = []
            for s, e in zip(col_starts, col_ends):
                val = line[s:e].strip() if e <= len(line) else ''
                row.append(val)
            data_rows.append(row)

        return col_names, data_rows

    def _execute_subquery(self, sql: str) -> List[str]:
        """Execute a subquery SELECT and return the first-column values as a flat list."""
        parsed = SQLParser.parse(sql)
        if not parsed:
            return []
        if parsed.sub_statements:
            parsed = parsed.sub_statements[0]
        if parsed.type != StatementType.SELECT or not parsed.from_tables:
            return []
        table = parsed.from_tables[0].upper()
        if table not in self.tables:
            if parsed.from_subqueries or table in self.views:
                lines = self._handle_SELECT(parsed)
                cols, rows = self._parse_select_output_lines(lines)
                if rows:
                    return [r[0] for r in rows if r]
            return []
        tcols = self.get_column_names(table)
        trows = self.rows.get(table, [])
        value_col = parsed.select_columns[0].upper().strip() if parsed.select_columns else ''
        # Handle aggregate functions in subquery
        agg_match = re.match(r'(COUNT|SUM|AVG|MIN|MAX)\((.+)\)', value_col, re.IGNORECASE)
        if agg_match:
            fname = agg_match.group(1).upper()
            inner = agg_match.group(2).strip().upper()
            if inner == '*':
                inner = ''
            ci = -1
            if inner:
                ci = self._find_col_index(inner, tcols)
            # Apply WHERE before aggregating
            rows = trows
            if parsed.where_clause:
                rows = self._apply_where(rows, tcols, table, parsed.where_clause)
            if fname == 'COUNT':
                if inner.upper().startswith('DISTINCT '):
                    distinct_col = inner.replace('DISTINCT ', '').strip()
                    distinct_ci = self._find_col_index(distinct_col, tcols)
                    distinct_vals = set()
                    for r in rows:
                        if distinct_ci >= 0 and distinct_ci < len(r) and r[distinct_ci].strip().upper() != 'NULL':
                            distinct_vals.add(r[distinct_ci].strip().upper())
                    return [str(len(distinct_vals))]
                else:
                    return [str(len(rows))]
            elif fname == 'SUM':
                total = 0
                for r in rows:
                    if ci >= 0 and ci < len(r) and r[ci].lstrip('-').isdigit():
                        total += int(r[ci])
                return [str(total)]
            elif fname == 'AVG':
                vals = []
                for r in rows:
                    if ci >= 0 and ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit():
                        vals.append(int(r[ci]))
                return [str(round(sum(vals) / len(vals), 2))] if vals else ['0']
            elif fname == 'MIN':
                vals = []
                for r in rows:
                    if ci >= 0 and ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit():
                        vals.append(int(r[ci]))
                return [str(min(vals))] if vals else ['0']
            elif fname == 'MAX':
                vals = []
                for r in rows:
                    if ci >= 0 and ci < len(r) and r[ci].lstrip('-.').replace('.','',1).isdigit():
                        vals.append(int(r[ci]))
                return [str(max(vals))] if vals else ['0']
        ci = self._find_col_index(value_col, tcols)
        if ci < 0:
            ci = 0
        rows = trows
        if parsed.where_clause:
            rows = self._apply_where(rows, tcols, table, parsed.where_clause)
        # Handle GROUP BY
        if parsed.group_by:
            gb_col_names = list(tcols)
            having_agg_cols = []
            if parsed.having_clause:
                for m in re.finditer(r'(SUM|COUNT|AVG|MIN|MAX)\s*\(([^)]*)\)', parsed.having_clause, re.IGNORECASE):
                    hac = m.group(0).upper().strip()
                    if hac not in gb_col_names:
                        gb_col_names.append(hac)
                        having_agg_cols.append(hac)
            rows = self._apply_group_by(rows, gb_col_names, parsed, tcols)
        # Handle HAVING
        if parsed.having_clause and rows:
            h_col_names = list(tcols)
            if parsed.group_by:
                for m in re.finditer(r'(SUM|COUNT|AVG|MIN|MAX)\s*\(([^)]*)\)', parsed.having_clause, re.IGNORECASE):
                    hac = m.group(0).upper().strip()
                    if hac not in h_col_names:
                        h_col_names.append(hac)
            rows = self._apply_having(rows, h_col_names, parsed)
        values = [str(r[ci]) for r in rows if ci < len(r)]
        return values

    def _execute_scalar_subquery(self, sql: str) -> Optional[str]:
        """Execute a scalar subquery (SELECT that returns one value)."""
        inner = sql.strip()
        if inner.startswith('(') and inner.endswith(')'):
            inner = inner[1:-1].strip()
        # Use full SELECT handler to support FROM subqueries, views, etc.
        parsed = SQLParser.parse(inner)
        if parsed and parsed.type == StatementType.SELECT:
            lines = self._handle_SELECT(parsed)
            cols, rows = self._parse_select_output_lines(lines)
            if rows and cols:
                return rows[0][0]
        return None

    def _evaluate_expression(self, expr: str, row: List[str], col_names: List[str]) -> str:
        """Evaluate simple arithmetic expressions like 'Stock + 10'."""
        expr = expr.strip().strip("'\"")
        # Resolve sequence references (e.g. seq.NEXTVAL)
        resolved = self._resolve_sequence_ref(expr)
        if resolved != expr:
            return resolved
        # Check for arithmetic
        try:
            # Simple: if it's a plain number, return it
            if expr.lstrip('-').isdigit():
                return expr
            # Try to evaluate column reference + number
            for op in ['+', '-', '*', '/']:
                if op in expr:
                    parts = expr.split(op)
                    if len(parts) == 2:
                        a, b = parts[0].strip(), parts[1].strip()
                        val_a = a
                        val_b = b
                        # Resolve column references
                        for ci, cn in enumerate(col_names):
                            if cn.upper() == a.upper() and ci < len(row):
                                val_a = row[ci]
                            if cn.upper() == b.upper() and ci < len(row):
                                val_b = row[ci]
                        # Try numeric evaluation
                        try:
                            na = float(val_a)
                            nb = float(val_b)
                            if op == '+':
                                return str(int(na + nb))
                            elif op == '-':
                                return str(int(na - nb))
                            elif op == '*':
                                return str(int(na * nb))
                            elif op == '/':
                                return str(round(na / nb, 2))
                        except (ValueError, ZeroDivisionError):
                            pass
            return expr
        except:
            return expr

    def _handle_UPDATE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.update_table.upper()
        if name not in self.tables:
            return ["", f"ERROR: table '{name}' does not exist."]
        cols = self.get_column_names(name)
        rows = self.rows.get(name, [])
        if not rows:
            for i in range(random.randint(2, 4)):
                row = []
                for c in cols:
                    row.append(self.generate_dummy_value(c, self.get_column_types(name).get(c, 'VARCHAR2'), i+1))
                rows.append(row)

        affected = 0
        for ri, row in enumerate(rows):
            matched = True
            if stmt.where_clause:
                matched = self._evaluate_simple(row, cols, name, stmt.where_clause)
            if matched:
                old_row = list(row)
                for set_col, set_val in stmt.set_clause:
                    for j, c in enumerate(cols):
                        if c.upper() == set_col.upper() and j < len(row):
                            row[j] = self._evaluate_expression(set_val, row, cols)
                            affected += 1
                # Validate CHECK constraints on updated row
                row_data = {cols[i].upper(): row[i] for i in range(len(cols))}
                check_err = self._validate_check_constraints(name, row_data, cols)
                if check_err:
                    # Rollback this row update
                    for i in range(len(row)):
                        row[i] = old_row[i]
                    affected = max(0, affected - len(stmt.set_clause))
                    continue
                self._undo_log.append(('UPDATE', name, ri, old_row))
        affected_rows = max(1, affected // max(len(stmt.set_clause), 1))
        result = ["", f"{affected_rows} row(s) updated."]
        # Fire triggers
        trig_out = self._fire_triggers('UPDATE', name, None)
        if trig_out:
            result.extend([""] + trig_out)
        return result

    def _handle_DELETE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.delete_table.upper()
        if name not in self.tables:
            return ["", f"ERROR: table '{name}' does not exist."]
        rows = self.rows.get(name, [])
        if not rows:
            return ["", "0 rows deleted."]
        before = len(rows)
        if stmt.where_clause:
            cols = self.get_column_names(name)
            kept = []
            for i, row in enumerate(rows):
                if not self._evaluate_simple(row, cols, name, stmt.where_clause):
                    self._undo_log.append(('DELETE', name, i, list(row)))
                    kept.append(row)
            self.rows[name] = kept
            deleted = before - len(kept)
        else:
            for i, row in enumerate(rows):
                self._undo_log.append(('DELETE', name, i, list(row)))
            self.rows[name] = []
            deleted = before
        result = ["", f"{deleted} row(s) deleted."]
        # Fire triggers
        trig_out = self._fire_triggers('DELETE', name, None)
        if trig_out:
            result.extend([""] + trig_out)
        return result

    def _handle_ALTER_TABLE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.alter_table.upper()
        if name not in self.tables:
            return ["", f"ERROR: table '{name}' does not exist."]
        table = self.tables[name]
        action = stmt.alter_action.upper()
        if action == 'ADD CONSTRAINT':
            constraint_def = stmt.alter_dtype
            table.constraints.append(constraint_def)
            return ["", "Table altered."]
        if 'ADD' in action:
            new_col = ColumnDef(name=stmt.alter_column, dtype=stmt.alter_dtype)
            table.columns.append(new_col)
            for row in self.rows.get(name, []):
                row.append('')
            return ["", "Table altered."]
        elif 'MODIFY' in action:
            for col in table.columns:
                if col.name == stmt.alter_column:
                    col.dtype = stmt.alter_dtype
                    break
            return ["", "Table altered."]
        elif 'DROP' in action:
            col_name = stmt.alter_column.upper()
            table.columns = [c for c in table.columns if c.name != col_name]
            col_idx = -1
            for i, c in enumerate(table.columns):
                if c.name == col_name:
                    col_idx = i
                    break
            if col_idx >= 0:
                for row in self.rows.get(name, []):
                    if col_idx < len(row):
                        del row[col_idx]
            return ["", "Table altered."]
        return ["", "Table altered."]

    def _handle_DROP_TABLE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.drop_name.upper()
        if name in self.tables:
            del self.tables[name]
            if name in self.rows:
                del self.rows[name]
            return ["", "Table dropped."]
        return ["", f"ERROR: table '{name}' does not exist."]

    def _handle_DROP_VIEW(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.drop_name.upper()
        if name in self.views:
            del self.views[name]
            return ["", "View dropped."]
        return ["", f"ERROR: view '{name}' does not exist."]

    def _handle_DROP_SEQUENCE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.drop_name.upper()
        if name in self.sequences:
            del self.sequences[name]
            return ["", "Sequence dropped."]
        return ["", f"ERROR: sequence '{name}' does not exist."]

    def _handle_TRUNCATE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.drop_name.upper()
        if name in self.tables:
            self.rows[name] = []
            return ["", "Table truncated."]
        return ["", f"ERROR: table '{name}' does not exist."]

    def _handle_RENAME(self, stmt: ParsedStatement) -> List[str]:
        old = stmt.drop_name.upper()
        new = stmt.sequence_name.upper()
        if old in self.tables:
            self.tables[new] = self.tables[old]
            del self.tables[old]
            if old in self.rows:
                self.rows[new] = self.rows[old]
                del self.rows[old]
            return ["", "Table renamed."]
        return ["", f"ERROR: table '{old}' does not exist."]

    def _handle_CREATE_VIEW(self, stmt: ParsedStatement) -> List[str]:
        self.views[stmt.view_name] = ViewInfo(name=stmt.view_name, query=stmt.view_query,
                                              columns=stmt.select_columns if stmt.select_columns else ['COL1'])
        return ["", "View created."]

    def _handle_CREATE_OR_REPLACE_VIEW(self, stmt: ParsedStatement) -> List[str]:
        return self._handle_CREATE_VIEW(stmt)

    def _handle_CREATE_PROCEDURE(self, stmt: ParsedStatement) -> List[str]:
        lines = stmt.dbms_output_lines[:] if stmt.dbms_output_lines else []
        self.procedures[stmt.proc_name] = ProcedureInfo(
            name=stmt.proc_name, params=stmt.proc_params,
            body=stmt.proc_body, output_lines=lines)
        return ["", "Procedure created."]

    def _handle_CREATE_FUNCTION(self, stmt: ParsedStatement) -> List[str]:
        self.functions[stmt.proc_name] = FunctionInfo(
            name=stmt.proc_name, params=stmt.proc_params,
            return_type=stmt.return_type, body=stmt.proc_body,
            output_lines=stmt.dbms_output_lines)
        return ["", "Function created."]

    def _handle_CREATE_TRIGGER(self, stmt: ParsedStatement) -> List[str]:
        self.triggers[stmt.trigger_name] = TriggerInfo(
            name=stmt.trigger_name, timing=stmt.trigger_timing,
            event=stmt.trigger_event, table=stmt.trigger_table,
            level=stmt.trigger_level, body=stmt.trigger_body)
        return ["", "Trigger created."]

    def _handle_CREATE_SEQUENCE(self, stmt: ParsedStatement) -> List[str]:
        self.sequences[stmt.sequence_name] = SequenceInfo(
            name=stmt.sequence_name, current_val=stmt.sequence_start,
            increment=stmt.sequence_increment)
        self._last_sequence_nextvals[stmt.sequence_name] = None
        return ["", "Sequence created."]

    def _resolve_sequence_ref(self, val: str) -> str:
        m = re.match(r'\A(\w+)\.(NEXTVAL|CURRVAL)\Z', val.strip(), re.IGNORECASE)
        if not m:
            return val
        seq_name = m.group(1).upper()
        op = m.group(2).upper()
        if seq_name not in self.sequences:
            raise PLSQLError(-2204, f"sequence '{seq_name}.NEXTVAL' does not exist")
        seq = self.sequences[seq_name]
        if op == 'NEXTVAL':
            new_val = str(seq.current_val)
            seq.current_val += seq.increment
            self._last_sequence_nextvals[seq_name] = new_val
            return new_val
        else:  # CURRVAL
            if self._last_sequence_nextvals.get(seq_name) is None:
                raise PLSQLError(-8002, f"{seq_name}.CURRVAL is not yet defined in this session")
            return self._last_sequence_nextvals[seq_name]

    def _handle_EXEC(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.exec_name.upper()
        exec_args = getattr(stmt, 'exec_args', [])
        lines = [""]
        if name in self.procedures:
            proc = self.procedures[name]
            param_values = {}
            for i, (pname, pdirection, ptype) in enumerate(proc.params):
                if pdirection in ('IN', 'IN OUT'):
                    if i < len(exec_args):
                        param_values[pname] = exec_args[i]
                    else:
                        param_values[pname] = ''
            output_lines = []
            self._execute_plsql_body(proc.body, param_values, output_lines)
            if output_lines:
                for ol in output_lines:
                    lines.append(ol)
            if not output_lines:
                lines.append("")
            lines.append("PL/SQL procedure successfully completed.")
        elif name in self.functions:
            func = self.functions[name]
            param_values = {}
            for i, (pname, pdirection, ptype) in enumerate(func.params):
                if pdirection in ('IN', 'IN OUT'):
                    if i < len(exec_args):
                        param_values[pname] = exec_args[i]
                    else:
                        param_values[pname] = ''
            output_lines = []
            ret = self._execute_plsql_body(func.body, param_values, output_lines)
            if output_lines:
                for ol in output_lines:
                    lines.append(ol)
            if ret is not None:
                lines.append(f"  Result: {ret}")
            lines.append("")
            lines.append("PL/SQL function successfully completed.")
        else:
            lines.append(f"ERROR: procedure/function '{name}' does not exist.")
        return lines

    def _handle_COMMIT(self, stmt: ParsedStatement) -> List[str]:
        self._undo_log.clear()
        return ["", "Commit complete."]

    def _handle_ROLLBACK(self, stmt: ParsedStatement) -> List[str]:
        # Replay undo log in reverse
        for action, tname, idx, data in reversed(self._undo_log):
            rows = self.rows.get(tname)
            if rows is None:
                continue
            if action == 'INSERT':
                # Remove the inserted row
                if idx < len(rows):
                    del rows[idx]
            elif action == 'DELETE':
                # Reinsert the deleted row at its original position
                if idx <= len(rows):
                    rows.insert(idx, data)
                else:
                    rows.append(data)
            elif action == 'UPDATE':
                # Restore old row
                if idx < len(rows):
                    rows[idx] = data
        self._undo_log.clear()
        return ["", "Rollback complete."]

    def _handle_SAVEPOINT(self, stmt: ParsedStatement) -> List[str]:
        return ["", f"Savepoint created."]

    def _handle_GRANT(self, stmt: ParsedStatement) -> List[str]:
        return ["", "Grant succeeded."]

    def _handle_REVOKE(self, stmt: ParsedStatement) -> List[str]:
        return ["", "Revoke succeeded."]

    def _handle_DESCRIBE(self, stmt: ParsedStatement) -> List[str]:
        name = stmt.describe_name.upper()
        lines = [""]
        if name in self.tables:
            table = self.tables[name]
            lines.append(f"Name:     {name}")
            lines.append(f"Columns:")
            lines.append(f"{'Name':<30} {'Type':<20} {'Null':<6} {'Key':<8}")
            lines.append("-" * 70)
            for col in table.columns:
                nullable = "Y" if not col.is_not_null else "N"
                key = ""
                if col.is_primary_key:
                    key = "PRI"
                elif col.is_foreign_key:
                    key = "FOR"
                elif col.is_unique:
                    key = "UNI"
                lines.append(f"{col.name:<30} {col.dtype:<20} {nullable:<6} {key:<8}")
            return lines
        elif name in self.views:
            view = self.views[name]
            lines.append(f"Name:     {name} (VIEW)")
            lines.append(f"Columns:")
            for c in view.columns:
                lines.append(f"  {c}")
            return lines
        return ["", f"ERROR: object '{name}' does not exist."]

    def _handle_ANONYMOUS_BLOCK(self, stmt: ParsedStatement) -> List[str]:
        lines = [""]
        body = stmt.text
        output_lines = []
        self._execute_plsql_body(body, {}, output_lines)
        if output_lines:
            for ol in output_lines:
                lines.append(ol)
        else:
            lines.append("(no output)")
        lines.append("")
        lines.append("PL/SQL procedure successfully completed.")
        return lines

    def _handle_UNKNOWN(self, stmt: ParsedStatement) -> List[str]:
        if getattr(stmt, 'is_noop', False):
            return ["", "Done."]
        upper = stmt.text.upper().strip()
        if upper in ('TABLES', 'TABLE'):
            if not self.tables:
                return ["", "No tables found."]
            lines = [f"  Tables in schema:"]
            for tname in sorted(self.tables.keys()):
                lines.append(f"  - {tname}")
            return lines
        if upper in ('VIEWS', 'VIEW'):
            if not self.views:
                return ["", "No views found."]
            lines = [f"  Views in schema:"]
            for vname in sorted(self.views.keys()):
                lines.append(f"  - {vname}")
            return lines
        if upper in ('SEQUENCES', 'SEQ'):
            if not self.sequences:
                return ["", "No sequences found."]
            lines = [f"  Sequences:"]
            for sname in sorted(self.sequences.keys()):
                seq = self.sequences[sname]
                lines.append(f"  - {sname} (current: {seq.current_val}, inc: {seq.increment})")
            return lines
        return ["", f"ORA-00900: invalid SQL statement"]


# ── Syntax Highlighter ────────────────────────────────────────────

class SQLHighlighter:
    KEYWORD_TAG = "sql_keyword"
    STRING_TAG = "sql_string"
    NUMBER_TAG = "sql_number"
    COMMENT_TAG = "sql_comment"
    BINDVAR_TAG = "sql_bindvar"

    def __init__(self, text_widget, font_bold=None, font_italic=None):
        self.text = text_widget
        self.font_bold = font_bold or FONT_BOLD
        self.font_italic = font_italic or FONT_ITALIC
        self._pending = None
        self._setup_tags()
        self._schedule_highlight()
        self.text.bind('<KeyRelease>', self._on_change)
        self.text.bind('<<Modified>>', self._on_change)

    def _setup_tags(self):
        self.text.tag_configure(self.KEYWORD_TAG, foreground=COLOR_KEYWORD, font=self.font_bold)
        self.text.tag_configure(self.STRING_TAG, foreground=COLOR_STRING)
        self.text.tag_configure(self.NUMBER_TAG, foreground=COLOR_NUMBER)
        self.text.tag_configure(self.COMMENT_TAG, foreground=COLOR_COMMENT, font=self.font_italic)
        self.text.tag_configure(self.BINDVAR_TAG, foreground=COLOR_PROMPT, font=self.font_bold)

    def _on_change(self, event=None):
        self._schedule_highlight()

    def _schedule_highlight(self):
        if self._pending is not None:
            self.text.after_cancel(self._pending)
        self._pending = self.text.after(250, self._do_highlight)

    def _do_highlight(self):
        self._pending = None
        self._highlight()

    def _highlight(self):
        for tag in (self.KEYWORD_TAG, self.STRING_TAG, self.NUMBER_TAG, self.COMMENT_TAG, self.BINDVAR_TAG):
            self.text.tag_remove(tag, "1.0", tk.END)

        content = self.text.get("1.0", tk.END)

        # Build a set of (start, end) ranges for strings and comments to skip keywords inside them
        skip_ranges = []

        # -- single-line comments
        for m in re.finditer(r'--.*?(\n|$)', content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            self.text.tag_add(self.COMMENT_TAG, start, end)
            skip_ranges.append((m.start(), m.end()))

        # /* block comments */
        for m in re.finditer(r'/\*.*?\*/', content, re.DOTALL):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            self.text.tag_add(self.COMMENT_TAG, start, end)
            skip_ranges.append((m.start(), m.end()))

        # Strings: single-quoted and double-quoted
        for m in re.finditer(r"'[^'\\]*(?:\\.[^'\\]*)*'|\"[^\"\\]*(?:\\.[^\"\\]*)*\"", content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            self.text.tag_add(self.STRING_TAG, start, end)
            skip_ranges.append((m.start(), m.end()))

        # Numbers
        for m in re.finditer(r'\b\d+(?:\.\d+)?\b', content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            self.text.tag_add(self.NUMBER_TAG, start, end)

        # Bind variables :NEW.col, :OLD.col, :var
        for m in re.finditer(r':[A-Za-z_]\w*(?:\.\w+)?', content):
            start = f"1.0+{m.start()}c"
            end = f"1.0+{m.end()}c"
            if not any(rs <= m.start() and m.end() <= re for rs, re in skip_ranges):
                self.text.tag_add(self.BINDVAR_TAG, start, end)

        # Keywords (skip those inside strings/comments)
        for m in re.finditer(r'\b[A-Za-z_]\w*\b', content):
            word = m.group()
            if word.upper() in SQL_KEYWORDS:
                if not any(rs <= m.start() and m.end() <= re for rs, re in skip_ranges):
                    start = f"1.0+{m.start()}c"
                    end = f"1.0+{m.end()}c"
                    self.text.tag_add(self.KEYWORD_TAG, start, end)


# ── Line Numbers ───────────────────────────────────────────────────

class LineNumbers(tk.Canvas):
    def __init__(self, parent, text_widget, font=None, **kwargs):
        super().__init__(parent, width=35, bg=COLOR_LINE_NUM_BG,
                         highlightthickness=0, **kwargs)
        self.text_widget = text_widget
        self.font = font or FONT
        self.text_widget.bind('<KeyRelease>', self._on_change)
        self.text_widget.bind('<MouseWheel>', self._on_change)
        self.text_widget.bind('<<Modified>>', self._on_change)
        self.text_widget.bind('<ButtonRelease-1>', self._on_change)
        self._update()

    def _on_change(self, event=None):
        if self.text_widget.edit_modified():
            self._update()
            self.text_widget.edit_modified(False)
        else:
            self._update()

    def _update(self):
        self.delete('all')
        line_count = self.text_widget.index('end-1c').split('.')[0]
        try:
            line_count = int(line_count)
        except ValueError:
            line_count = 1
        h = self.text_widget.dlineinfo('1.0')
        line_height = h[3] if h else 20
        y = 2
        for i in range(1, line_count + 1):
            self.create_text(30, y, anchor='ne', text=str(i),
                             font=self.font, fill=COLOR_LINE_NUM_FG)
            y += line_height
        self.configure(height=max(y, 20))

        x1, y1, x2, y2 = self.bbox('all') or (0, 0, 30, 20)
        if x2 > 0:
            self.configure(width=min(x2 + 6, 50))


# ── Worksheet ──────────────────────────────────────────────────────

class Worksheet:
    _next_id = 0

    def __init__(self, name: str = ""):
        Worksheet._next_id += 1
        self.id = Worksheet._next_id
        self.name = name or f"WS {self.id}"
        self.content = ""
        self.modified = False


# ── Main Application ───────────────────────────────────────────────

class OracleSQLLiteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Oracle SQL*Lite")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        self.db = MockDatabase()
        self.worksheets: List[Worksheet] = []
        self.active_worksheet: Optional[Worksheet] = None

        # Mutable font objects for GUI (size can change at runtime)
        self.font_size = FONT_SIZE
        self.font_normal = tkfont.Font(family=FONT_FAMILY, size=self.font_size)
        self.font_bold = tkfont.Font(family=FONT_FAMILY, size=self.font_size, weight="bold")
        self.font_italic = tkfont.Font(family=FONT_FAMILY, size=self.font_size, slant="italic")

        self._build_ui()
        self._create_worksheet()
        self._show_startup_banner()

    def _build_ui(self):
        self.root.configure(bg=COLOR_BG)

        # Menu Bar
        self._build_menu()

        # Toolbar
        self._build_toolbar()

        # Main PanedWindow
        self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # Left Panel - Worksheets
        self._build_left_panel()

        # Right PanedWindow (editor + console)
        self.right_pane = ttk.PanedWindow(self.main_pane, orient=tk.VERTICAL)
        self.main_pane.add(self.right_pane, weight=3)

        # Editor Area
        self._build_editor_area()

        # Output Console
        self._build_output_console()

        # Status Bar
        self._build_status_bar()

        # Keyboard shortcuts
        self.root.bind('<F5>', lambda e: self._execute_sql())
        self.root.bind('<Control-r>', lambda e: self._execute_sql())
        self.root.bind('<Control-n>', lambda e: self._create_worksheet())
        self.root.bind('<Control-w>', lambda e: self._close_worksheet())
        self.root.bind('<Control-l>', lambda e: self._clear_output())
        self.root.bind('<Control-Shift-C>', lambda e: self._clear_output())
        self.root.bind('<Control-f>', lambda e: self._toggle_search())
        self.root.bind('<Control-plus>', self._increase_font_size)
        self.root.bind('<Control-equal>', self._increase_font_size)
        self.root.bind('<Control-KP_Add>', self._increase_font_size)
        self.root.bind('<Control-minus>', self._decrease_font_size)
        self.root.bind('<Control-KP_Subtract>', self._decrease_font_size)
        self.editor_text.bind('<Control-a>', self._select_all)
        self.editor_text.bind('<Control-slash>', self._toggle_comment)
        # Tab indent / Shift-Tab dedent for selected lines
        self.editor_text.bind('<Tab>', self._indent_selection)
        self.editor_text.bind('<Shift-Tab>', self._dedent_selection)

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Worksheet", command=self._create_worksheet, accelerator="Ctrl+N")
        file_menu.add_command(label="Close Worksheet", command=self._close_worksheet, accelerator="Ctrl+W")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Worksheet menu
        ws_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Worksheet", menu=ws_menu)
        ws_menu.add_command(label="New Worksheet", command=self._create_worksheet, accelerator="Ctrl+N")
        ws_menu.add_command(label="Rename Worksheet", command=self._rename_worksheet)
        ws_menu.add_separator()
        ws_menu.add_command(label="Clear Editor", command=self._clear_editor)
        ws_menu.add_command(label="Clear All Worksheets", command=self._clear_all_sheets)

        # Query menu
        query_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Query", menu=query_menu)
        query_menu.add_command(label="Execute", command=self._execute_sql, accelerator="F5")
        query_menu.add_command(label="Clear Output", command=self._clear_output, accelerator="Ctrl+L")

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Oracle SQL*Lite", command=self._show_about)
        help_menu.add_command(label="SQL Reference", command=self._show_sql_help)

    @staticmethod
    def _make_flat_button(parent, text, command, bg='#E0E0E0', fg='black',
                          font=None, accent=False, padx=10, pady=4):
        kwargs = dict(text=text, command=command, font=font,
                      bg=bg, fg=fg, relief=tk.FLAT, bd=0,
                      padx=padx, pady=pady, cursor='hand2',
                      activebackground='#D0D0D0')
        btn = tk.Button(parent, **kwargs)
        if accent:
            btn.configure(activebackground='#B0382A')
        def _on_enter(e):
            if e.widget['bg'] != COLOR_ACCENT:
                e.widget['bg'] = '#D0D0D0'
            else:
                e.widget['bg'] = '#B0382A'
        def _on_leave(e):
            if e.widget['bg'] != '#B0382A':
                e.widget['bg'] = bg
            else:
                e.widget['bg'] = COLOR_ACCENT
        btn.bind('<Enter>', _on_enter)
        btn.bind('<Leave>', _on_leave)
        return btn

    def _build_toolbar(self):
        toolbar = tk.Frame(self.root, bg=COLOR_BG, bd=0,
                           highlightbackground=COLOR_BORDER, highlightthickness=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self._make_flat_button(toolbar, "▶ Execute", self._execute_sql,
                               bg=COLOR_ACCENT, fg='white', font=self.font_bold,
                               accent=True, padx=14, pady=4).pack(side=tk.LEFT, padx=3, pady=3)

        self._make_flat_button(toolbar, "✕ Clear Output", self._clear_output,
                               padx=10, pady=4).pack(side=tk.LEFT, padx=3, pady=3)

        self._make_flat_button(toolbar, "📄 New WS", self._create_worksheet,
                               padx=10, pady=4).pack(side=tk.LEFT, padx=3, pady=3)

        self._make_flat_button(toolbar, "🗑 Clear Editor", self._clear_editor,
                               padx=10, pady=4).pack(side=tk.LEFT, padx=3, pady=3)

        self._make_flat_button(toolbar, "❓ Help", self._show_sql_help,
                               padx=10, pady=4).pack(side=tk.RIGHT, padx=3, pady=3)

    def _build_left_panel(self):
        left_frame = tk.Frame(self.main_pane, bg=COLOR_BG, width=180)
        self.main_pane.add(left_frame, weight=0)

        tk.Label(left_frame, text="  Worksheets", font=self.font_bold,
                 bg=COLOR_BG, anchor='w').pack(fill=tk.X, padx=5, pady=(5, 2))

        list_frame = tk.Frame(left_frame, bg=COLOR_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                 bg=COLOR_BORDER, activebackground='#BBBBBB',
                                 troughcolor=COLOR_BG, bd=0, relief=tk.FLAT)
        self.ws_listbox = tk.Listbox(list_frame, font=self.font_normal,
                                     bg='white', fg='black', selectbackground='#0078D7',
                                     selectforeground='white', bd=1, relief=tk.FLAT,
                                     highlightbackground=COLOR_BORDER, highlightthickness=1,
                                     yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.ws_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ws_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.ws_listbox.bind('<<ListboxSelect>>', self._on_ws_select)
        self.ws_listbox.bind('<Double-Button-1>', lambda e: self._rename_worksheet())
        self.ws_listbox.bind('<Button-3>', self._ws_context_menu)

        btn_frame = tk.Frame(left_frame, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=5, pady=3)
        self._make_flat_button(btn_frame, "＋ New", self._create_worksheet,
                               padx=8, pady=3).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self._make_flat_button(btn_frame, "✕ Close", self._close_worksheet,
                               padx=8, pady=3).pack(side=tk.RIGHT, padx=2, fill=tk.X, expand=True)

    def _build_editor_area(self):
        editor_frame = tk.Frame(self.right_pane, bg='white')
        self.right_pane.add(editor_frame, weight=1)

        # Header bar showing active worksheet name
        header_frame = tk.Frame(editor_frame, bg=COLOR_TAB_BG, bd=0,
                                highlightbackground=COLOR_ACCENT, highlightthickness=2)
        self.editor_header = tk.Label(header_frame, text="WS 1",
                                      font=self.font_bold, bg=COLOR_TAB_ACTIVE, fg='black',
                                      anchor='w', padx=10, pady=3)
        self.editor_header.pack(fill=tk.X)
        header_frame.pack(fill=tk.X)

        # Editor panel with line numbers
        text_frame = tk.Frame(editor_frame, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.editor_text = tk.Text(text_frame, font=self.font_normal, bg=COLOR_EDITOR_BG,
                                   fg='black', insertbackground='black',
                                   wrap=tk.NONE, bd=0, padx=8, pady=5,
                                   undo=True, maxundo=100,
                                   selectbackground='#ADD6FF')
        self.editor_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.line_numbers = LineNumbers(text_frame, self.editor_text, font=self.font_normal)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbar
        v_scroll = tk.Scrollbar(self.editor_text, orient=tk.VERTICAL,
                                command=self.editor_text.yview,
                                bg=COLOR_BORDER, activebackground='#BBBBBB',
                                troughcolor=COLOR_BG, bd=0, relief=tk.FLAT)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor_text.configure(yscrollcommand=v_scroll.set)

        h_scroll = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL,
                                command=self.editor_text.xview,
                                bg=COLOR_BORDER, activebackground='#BBBBBB',
                                troughcolor=COLOR_BG, bd=0, relief=tk.FLAT)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.editor_text.configure(xscrollcommand=h_scroll.set)

        # Track modifications and cursor position
        self.editor_text.bind('<<Modified>>', self._on_editor_modified)
        self.editor_text.bind('<KeyRelease>', self._on_editor_key)
        self.editor_text.bind('<ButtonRelease-1>', self._update_cursor_pos)

        # Auto-indent on Enter
        self.editor_text.bind('<Return>', self._on_enter_indent)

        # Syntax highlighting
        self.highlighter = SQLHighlighter(self.editor_text, font_bold=self.font_bold, font_italic=self.font_italic)

        # Right-click context menu
        self.editor_text.bind('<Button-3>', self._editor_context_menu)

    def _build_output_console(self):
        console_frame = tk.Frame(self.right_pane, bg=COLOR_OUTPUT_BG)
        self.right_pane.add(console_frame, weight=1)

        # Header
        out_header_frame = tk.Frame(console_frame, bg=COLOR_TAB_BG, bd=0,
                                    highlightbackground=COLOR_BORDER, highlightthickness=1)
        tk.Label(out_header_frame, text="  Output Console", font=self.font_bold,
                 bg=COLOR_TAB_BG, fg='black', anchor='w', padx=10, pady=3
                 ).pack(fill=tk.X)
        out_header_frame.pack(fill=tk.X)

        out_frame = tk.Frame(console_frame, bg=COLOR_OUTPUT_BG)
        out_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = tk.Text(out_frame, font=self.font_normal, bg=COLOR_OUTPUT_BG,
                                   fg='black', wrap=tk.WORD, bd=0, padx=8, pady=5,
                                   state=tk.DISABLED, cursor='arrow',
                                   selectbackground='#ADD6FF')
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        out_scroll = tk.Scrollbar(self.output_text, orient=tk.VERTICAL,
                                  command=self.output_text.yview,
                                  bg=COLOR_BORDER, activebackground='#BBBBBB',
                                  troughcolor=COLOR_BG, bd=0, relief=tk.FLAT)
        out_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.configure(yscrollcommand=out_scroll.set)

        # Tags for output styling
        self.output_text.tag_configure("prompt", foreground=COLOR_PROMPT, font=self.font_bold)
        self.output_text.tag_configure("error", foreground=COLOR_ERROR, font=self.font_bold)
        self.output_text.tag_configure("success", foreground=COLOR_SUCCESS)
        self.output_text.tag_configure("header", font=self.font_bold)
        self.output_text.tag_configure("separator", foreground='#888888')
        self.output_text.tag_configure("ws_label", foreground='#555555', font=self.font_italic)

    def _build_status_bar(self):
        bar_frame = tk.Frame(self.root, bg=COLOR_STATUS_BG, bd=0,
                             highlightbackground=COLOR_BORDER, highlightthickness=1)
        bar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_bar = tk.Label(bar_frame, text="Connected to: Oracle Database 19c  |  Ready",
                                   font=self.font_normal, bg=COLOR_STATUS_BG,
                                   fg='black', anchor='w', padx=8, pady=2)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.cursor_label = tk.Label(bar_frame, text="Ln 1, Col 1",
                                     font=self.font_normal, bg=COLOR_STATUS_BG,
                                     fg='black', anchor='e', padx=8, pady=2)
        self.cursor_label.pack(side=tk.RIGHT)

    # ── Worksheet Management ───────────────────────────────────────

    def _create_worksheet(self, name: str = ""):
        ws = Worksheet(name)
        self.worksheets.append(ws)
        self.ws_listbox.insert(tk.END, ws.name)
        self._select_worksheet(ws)
        self._update_status(f"Created {ws.name}")

    def _close_worksheet(self):
        if not self.worksheets:
            return
        if self.active_worksheet:
            idx = self.worksheets.index(self.active_worksheet)
            self.worksheets.remove(self.active_worksheet)
            self.ws_listbox.delete(idx)
            if self.worksheets:
                new_idx = min(idx, len(self.worksheets) - 1)
                self._select_worksheet(self.worksheets[new_idx])
            else:
                self._create_worksheet()
            self._update_status("Worksheet closed")

    def _rename_worksheet(self):
        if not self.active_worksheet:
            return
        new_name = simpledialog.askstring("Rename Worksheet",
                                          "New name:",
                                          initialvalue=self.active_worksheet.name,
                                          parent=self.root)
        if new_name and new_name.strip():
            self.active_worksheet.name = new_name.strip()
            idx = self.worksheets.index(self.active_worksheet)
            self.ws_listbox.delete(idx)
            self.ws_listbox.insert(idx, self.active_worksheet.name)
            self.ws_listbox.selection_set(idx)
            self.editor_header.config(text=self.active_worksheet.name)
            self._update_status(f"Renamed to {self.active_worksheet.name}")

    def _select_worksheet(self, ws: Worksheet):
        self.active_worksheet = ws
        idx = self.worksheets.index(ws)
        self.ws_listbox.selection_clear(0, tk.END)
        self.ws_listbox.selection_set(idx)
        self.ws_listbox.see(idx)
        self.editor_header.config(text=ws.name)

        # Load content
        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert("1.0", ws.content)
        self.editor_text.edit_modified(False)
        self.editor_text.edit_reset()

    def _on_ws_select(self, event):
        selection = self.ws_listbox.curselection()
        if selection:
            idx = selection[0]
            if 0 <= idx < len(self.worksheets):
                self._save_active_content()
                self._select_worksheet(self.worksheets[idx])

    def _save_active_content(self):
        if self.active_worksheet:
            self.active_worksheet.content = self.editor_text.get("1.0", tk.END).rstrip('\n')
            idx = self.worksheets.index(self.active_worksheet)
            mod = self.editor_text.edit_modified()
            self.active_worksheet.modified = mod
            display = self.active_worksheet.name
            if mod:
                display += " *"
            self.ws_listbox.delete(idx)
            self.ws_listbox.insert(idx, display)
            self.ws_listbox.selection_set(idx)

    def _clear_editor(self):
        self.editor_text.delete("1.0", tk.END)
        self._update_status("Editor cleared")

    def _clear_all_sheets(self):
        for ws in self.worksheets:
            ws.content = ""
            ws.modified = False
        self._select_worksheet(self.active_worksheet or self.worksheets[0])
        self._update_status("All worksheets cleared")

    def _ws_context_menu(self, event):
        try:
            idx = self.ws_listbox.nearest(event.y)
            self.ws_listbox.selection_clear(0, tk.END)
            self.ws_listbox.selection_set(idx)
        except:
            pass
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Rename", command=self._rename_worksheet)
        menu.add_command(label="New Worksheet", command=self._create_worksheet)
        menu.add_command(label="Close", command=self._close_worksheet)
        menu.add_separator()
        menu.add_command(label="Clear Editor", command=self._clear_editor)
        menu.post(event.x_root, event.y_root)

    # ── Editor Events ──────────────────────────────────────────────

    def _on_editor_modified(self, event=None):
        if self.editor_text.edit_modified():
            self._update_ws_modified_indicator()
            self.editor_text.edit_modified(False)

    def _on_editor_key(self, event=None):
        self._update_ws_modified_indicator()
        self._update_cursor_pos()

    def _update_ws_modified_indicator(self):
        if not self.active_worksheet:
            return
        modified = self.editor_text.edit_modified() or False
        self.active_worksheet.modified = modified
        idx = self.worksheets.index(self.active_worksheet)
        display = self.active_worksheet.name
        if modified:
            display += " *"
        self.ws_listbox.delete(idx)
        self.ws_listbox.insert(idx, display)
        self.ws_listbox.selection_set(idx)

    def _update_cursor_pos(self, event=None):
        cursor = self.editor_text.index(tk.INSERT)
        if cursor:
            parts = cursor.split('.')
            line, col = parts[0], parts[1] if len(parts) > 1 else '1'
            self.cursor_label.config(text=f"Ln {line}, Col {col}")

    def _on_enter_indent(self, event=None):
        cursor = self.editor_text.index(tk.INSERT)
        line = cursor.split('.')[0]
        prev_line_text = self.editor_text.get(f"{line}.0", f"{line}.0 lineend")
        indent = ''
        for ch in prev_line_text:
            if ch in (' ', '\t'):
                indent += ch
            else:
                break
        self.editor_text.insert(tk.INSERT, '\n' + indent)
        return 'break'

    # ── Search / Replace ──────────────────────────────────────────

    def _toggle_search(self, event=None):
        if hasattr(self, 'search_frame') and self.search_frame.winfo_ismapped():
            self.search_frame.pack_forget()
            self.editor_text.focus_set()
            return
        if not hasattr(self, 'search_frame'):
            self._build_search_bar()
        self.search_frame.pack(in_=self.editor_header.master, before=self.editor_header,
                               fill=tk.X, side=tk.TOP)
        self.search_entry.focus_set()
        self.search_entry.select_range(0, tk.END)

    def _build_search_bar(self):
        sbg = '#F0F0F0'
        self.search_frame = tk.Frame(self.root, bg=sbg, bd=0,
                                     highlightbackground=COLOR_BORDER, highlightthickness=1)
        tk.Label(self.search_frame, text="Find:", bg=sbg,
                 font=self.font_normal).pack(side=tk.LEFT, padx=(8, 2))
        self.search_entry = tk.Entry(self.search_frame, width=25, font=self.font_normal,
                                     relief=tk.FLAT, bd=1, highlightthickness=0)
        self.search_entry.pack(side=tk.LEFT, padx=2, pady=4)
        self.search_entry.bind('<Return>', self._find_next)
        self.search_entry.bind('<Escape>', lambda e: self._toggle_search())

        self._make_flat_button(self.search_frame, "▼ Next", self._find_next,
                               bg=sbg, padx=6, pady=2).pack(side=tk.LEFT, padx=1)
        self._make_flat_button(self.search_frame, "▲ Prev", self._find_prev,
                               bg=sbg, padx=6, pady=2).pack(side=tk.LEFT, padx=1)

        tk.Label(self.search_frame, text="  Replace:", bg=sbg,
                 font=self.font_normal).pack(side=tk.LEFT, padx=(8, 2))
        self.replace_entry = tk.Entry(self.search_frame, width=18, font=self.font_normal,
                                      relief=tk.FLAT, bd=1, highlightthickness=0)
        self.replace_entry.pack(side=tk.LEFT, padx=2, pady=4)
        self.replace_entry.bind('<Return>', self._replace_next)

        self._make_flat_button(self.search_frame, "Replace", self._replace_next,
                               bg=sbg, padx=6, pady=2).pack(side=tk.LEFT, padx=1)
        self._make_flat_button(self.search_frame, "Replace All", self._replace_all,
                               bg=sbg, padx=6, pady=2).pack(side=tk.LEFT, padx=1)

        self.search_match_label = tk.Label(self.search_frame, text="", bg=sbg, font=self.font_normal)
        self.search_match_label.pack(side=tk.LEFT, padx=4)

        self._make_flat_button(self.search_frame, "✕", self._toggle_search,
                               bg=sbg, padx=6, pady=2).pack(side=tk.RIGHT, padx=4)

    def _find_all_matches(self):
        search_term = self.search_entry.get()
        if not search_term:
            return []
        content = self.editor_text.get("1.0", tk.END)
        matches = []
        pos = "1.0"
        while True:
            pos = self.editor_text.search(search_term, pos, tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(search_term)}c"
            matches.append((pos, end))
            pos = end
        return matches

    def _find_next(self, event=None):
        matches = self._find_all_matches()
        if not matches:
            self.search_match_label.config(text="0 matches")
            return
        cursor = self.editor_text.index(tk.INSERT)
        for pos, end in matches:
            if self.editor_text.compare(pos, '>=', cursor):
                self._highlight_match(pos, end)
                self.search_match_label.config(text=f"{matches.index((pos, end))+1} of {len(matches)}")
                return
        # wrap around
        self._highlight_match(matches[0][0], matches[0][1])
        self.search_match_label.config(text=f"1 of {len(matches)}")

    def _find_prev(self, event=None):
        matches = self._find_all_matches()
        if not matches:
            self.search_match_label.config(text="0 matches")
            return
        cursor = self.editor_text.index(tk.INSERT)
        for pos, end in reversed(matches):
            if self.editor_text.compare(pos, '<', cursor):
                self._highlight_match(pos, end)
                self.search_match_label.config(text=f"{matches.index((pos, end))+1} of {len(matches)}")
                return
        self._highlight_match(matches[-1][0], matches[-1][1])
        self.search_match_label.config(text=f"{len(matches)} of {len(matches)}")

    def _highlight_match(self, pos, end):
        self.editor_text.tag_remove(tk.SEL, "1.0", tk.END)
        self.editor_text.tag_add(tk.SEL, pos, end)
        self.editor_text.mark_set(tk.INSERT, pos)
        self.editor_text.see(pos)
        self._update_cursor_pos()

    def _replace_next(self, event=None):
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        if not search_term:
            return
        sel = self.editor_text.tag_ranges(tk.SEL)
        if sel:
            selected = self.editor_text.get(sel[0], sel[1])
            if selected.lower() == search_term.lower():
                self.editor_text.delete(sel[0], sel[1])
                self.editor_text.insert(sel[0], replace_term)
        self._find_next()

    def _replace_all(self):
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        if not search_term:
            return
        content = self.editor_text.get("1.0", tk.END)
        count = 0
        pos = "1.0"
        self.editor_text.tag_remove(tk.SEL, "1.0", tk.END)
        while True:
            pos = self.editor_text.search(search_term, pos, tk.END, nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(search_term)}c"
            self.editor_text.delete(pos, end)
            self.editor_text.insert(pos, replace_term)
            pos = f"{pos}+{len(replace_term)}c"
            count += 1
        self.search_match_label.config(text=f"Replaced {count} occurrences")

    # ── Editor Context Menu ───────────────────────────────────────

    def _editor_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        has_sel = self.editor_text.tag_ranges(tk.SEL)
        menu.add_command(label="Cut", accelerator="Ctrl+X",
                         command=lambda: self.editor_text.event_generate('<<Cut>>'),
                         state=tk.NORMAL if has_sel else tk.DISABLED)
        menu.add_command(label="Copy", accelerator="Ctrl+C",
                         command=lambda: self.editor_text.event_generate('<<Copy>>'),
                         state=tk.NORMAL if has_sel else tk.DISABLED)
        menu.add_command(label="Paste", accelerator="Ctrl+V",
                         command=lambda: self.editor_text.event_generate('<<Paste>>'))
        menu.add_command(label="Delete", accelerator="Del",
                         command=lambda: self.editor_text.event_generate('<<Clear>>'),
                         state=tk.NORMAL if has_sel else tk.DISABLED)
        menu.add_separator()
        menu.add_command(label="Select All", accelerator="Ctrl+A",
                         command=self._select_all)
        menu.add_separator()
        menu.add_command(label="Toggle Comment", accelerator="Ctrl+/",
                         command=self._toggle_comment)
        menu.add_command(label="Find / Replace", accelerator="Ctrl+F",
                         command=self._toggle_search)
        menu.post(event.x_root, event.y_root)

    def _select_all(self, event=None):
        self.editor_text.tag_add(tk.SEL, "1.0", tk.END)
        self.editor_text.mark_set(tk.INSERT, "1.0")
        self.editor_text.see(tk.INSERT)
        return 'break'

    def _toggle_comment(self, event=None):
        try:
            sel = self.editor_text.tag_ranges(tk.SEL)
            if sel:
                start_line = sel[0].string.split('.')[0]
                end_line = sel[1].string.split('.')[0]
            else:
                cursor = self.editor_text.index(tk.INSERT)
                start_line = end_line = cursor.split('.')[0]

            all_commented = True
            for line_num in range(int(start_line), int(end_line) + 1):
                line_text = self.editor_text.get(f"{line_num}.0", f"{line_num}.0 lineend")
                if not line_text.strip().startswith('--'):
                    all_commented = False
                    break

            self.editor_text.tag_remove(tk.SEL, "1.0", tk.END)
            for line_num in range(int(start_line), int(end_line) + 1):
                if all_commented:
                    line_text = self.editor_text.get(f"{line_num}.0", f"{line_num}.0 lineend")
                    stripped = line_text.lstrip()
                    if stripped.startswith('--'):
                        leading = line_text[:len(line_text) - len(stripped)]
                        rest = stripped[2:]
                        self.editor_text.delete(f"{line_num}.0", f"{line_num}.0 lineend")
                        self.editor_text.insert(f"{line_num}.0", leading + rest)
                else:
                    self.editor_text.insert(f"{line_num}.0", "--")
        except:
            pass

    def _indent_selection(self, event=None):
        sel = self.editor_text.tag_ranges(tk.SEL)
        if sel:
            start_line = sel[0].string.split('.')[0]
            end_line = sel[1].string.split('.')[0]
            self.editor_text.tag_remove(tk.SEL, "1.0", tk.END)
            for line_num in range(int(start_line), int(end_line) + 1):
                self.editor_text.insert(f"{line_num}.0", "   ")
        else:
            self.editor_text.insert(tk.INSERT, "   ")
        return 'break'

    def _dedent_selection(self, event=None):
        sel = self.editor_text.tag_ranges(tk.SEL)
        if sel:
            start_line = sel[0].string.split('.')[0]
            end_line = sel[1].string.split('.')[0]
            self.editor_text.tag_remove(tk.SEL, "1.0", tk.END)
            for line_num in range(int(start_line), int(end_line) + 1):
                line_text = self.editor_text.get(f"{line_num}.0", f"{line_num}.0 lineend")
                removed = 0
                for ch in line_text:
                    if ch == ' ':
                        removed += 1
                    elif ch == '\t':
                        removed += 1
                    else:
                        break
                if removed > 0:
                    self.editor_text.delete(f"{line_num}.0", f"{line_num}.0+{min(removed, 3)}c")
        else:
            cursor = self.editor_text.index(tk.INSERT)
            line = cursor.split('.')[0]
            col = int(cursor.split('.')[1])
            if col > 0:
                back = min(3, col)
                self.editor_text.delete(f"{line}.{col - back}", cursor)
        return 'break'

    # ── Font Size ──────────────────────────────────────────────────

    def _increase_font_size(self, event=None):
        self.font_size += 1
        self.font_normal.configure(size=self.font_size)
        self.font_bold.configure(size=self.font_size)
        self.font_italic.configure(size=self.font_size)
        self._update_status(f"Font size: {self.font_size}")

    def _decrease_font_size(self, event=None):
        if self.font_size > 6:
            self.font_size -= 1
            self.font_normal.configure(size=self.font_size)
            self.font_bold.configure(size=self.font_size)
            self.font_italic.configure(size=self.font_size)
            self._update_status(f"Font size: {self.font_size}")

    # ── Output Console ─────────────────────────────────────────────

    def _clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self._update_status("Output cleared")

    def _write_output(self, text: str, tag: str = None):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text, tag) if tag else self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def _show_startup_banner(self):
        banner = [
            "",
            "Oracle SQL*Lite - Oracle DBMS Simulator",
            "Copyright (c) 2025",
            "",
            "Connected to: Oracle Database 19c Enterprise Edition",
            "",
            "Type SQL statements in the editor above and press Execute (F5).",
            "Use the left panel to create and manage worksheets.",
            "",
            "Supported: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE,",
            "  ALTER, DROP, VIEW, PROCEDURE, FUNCTION, TRIGGER,",
            "  SEQUENCE, anonymous PL/SQL blocks, JOINs, subqueries,",
            "  aggregate functions, and more.",
            "",
        ]
        self._write_output("\n".join(banner))
        self._write_prompt()

    def _write_prompt(self):
        ws_name = self.active_worksheet.name if self.active_worksheet else "WS"
        self._write_output(f"\n[{ws_name}] SQL> ", "prompt")

    # ── SQL Execution ──────────────────────────────────────────────

    def _execute_sql(self):
        if not self.active_worksheet:
            return
        sql_text = self.editor_text.get("1.0", tk.END).strip()
        if not sql_text:
            self._write_output("\n   (empty statement)\n", "error")
            self._write_prompt()
            return

        self._save_active_content()

        # Echo the SQL to output
        ws_name = self.active_worksheet.name
        self._write_output(f"\n[{ws_name}] SQL> ", "prompt")
        sql_lines = sql_text.split('\n')
        for i, line in enumerate(sql_lines):
            if i == 0:
                self._write_output(f"{line}\n")
            else:
                self._write_output(f"   {i+1:>3}  {line}\n")

        try:
            parsed = SQLParser.parse(sql_text)
            if not parsed or (parsed.type == StatementType.UNKNOWN and not parsed.sub_statements):
                self._write_output(f"\n   ORA-00900: invalid SQL statement\n", "error")
                self._write_prompt()
                return

            output_lines = self.db.process_statement(parsed)
            if output_lines:
                for line in output_lines:
                    tag = None
                    if line.startswith("ERROR"):
                        tag = "error"
                    elif "created" in line.lower() or "altered" in line.lower() or \
                         "dropped" in line.lower() or "selected" in line.lower() or \
                         "complete" in line.lower() or "succeeded" in line.lower() or \
                         "row" in line.lower() or "truncated" in line.lower():
                        tag = "success"
                    self._write_output(f"   {line}\n", tag)
            else:
                self._write_output(f"   (no output)\n")

        except Exception as e:
            self._write_output(f"\n   Error: {str(e)}\n", "error")

        self._write_prompt()
        self._update_status("Statement executed")

    # ── Status ─────────────────────────────────────────────────────

    def _update_status(self, message: str):
        ws_name = self.active_worksheet.name if self.active_worksheet else "-"
        self.status_bar.config(text=f"Connected to: Oracle Database 19c  |  {ws_name}  |  {message}")

    # ── Dialogs ────────────────────────────────────────────────────

    def _show_about(self):
        win = tk.Toplevel(self.root)
        win.title("About Oracle SQL*Lite")
        win.geometry("380x260")
        win.resizable(False, False)
        win.configure(bg=COLOR_BG)

        accent_bar = tk.Frame(win, bg=COLOR_ACCENT, height=4)
        accent_bar.pack(fill=tk.X)

        tk.Label(win, text="Oracle SQL*Lite",
                 font=('Segoe UI', 18, 'bold'), bg=COLOR_BG, fg=COLOR_ACCENT
                 ).pack(pady=(20, 2))
        tk.Label(win, text="v1.0",
                 font=self.font_normal, bg=COLOR_BG, fg='#666666'
                 ).pack()
        tk.Label(win, text="An Oracle DBMS simulator for educational use.\n"
                           "Built with Python tkinter.\n"
                           "Supports SQL and PL/SQL syntax with realistic-looking output.",
                 font=self.font_normal, bg=COLOR_BG, fg='#333333',
                 justify=tk.CENTER).pack(pady=12)
        tk.Label(win, text="Copyright \u00A9 2025",
                 font=self.font_normal, bg=COLOR_BG, fg='#888888'
                 ).pack()

        btn_frame = tk.Frame(win, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, pady=(10, 15))
        self._make_flat_button(btn_frame, "Close", win.destroy,
                               accent=True).pack()

    def _show_sql_help(self):
        help_text = (
            "SQL*Lite Quick Reference\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "DDL:\n"
            "  CREATE TABLE table (col type, ...)\n"
            "  ALTER TABLE table ADD col type\n"
            "  ALTER TABLE table MODIFY col type\n"
            "  DROP TABLE table\n"
            "  TRUNCATE TABLE table\n\n"
            "DML:\n"
            "  INSERT INTO table VALUES (val, ...)\n"
            "  INSERT INTO table (col, ...) VALUES (val, ...)\n"
            "  UPDATE table SET col=val WHERE cond\n"
            "  DELETE FROM table WHERE cond\n\n"
            "Queries:\n"
            "  SELECT * FROM table\n"
            "  SELECT col1, col2 FROM table WHERE cond\n"
            "  SELECT func(col) FROM table GROUP BY col ORDER BY col\n"
            "  JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN\n"
            "  Subqueries, IN, BETWEEN, LIKE, IS NULL\n\n"
            "PL/SQL:\n"
            "  Anonymous: DECLARE ... BEGIN ... END;\n"
            "  CREATE PROCEDURE name (p IN type) IS ... BEGIN ... END;\n"
            "  CREATE FUNCTION name (p IN type) RETURN type IS ... BEGIN ... END;\n"
            "  CREATE TRIGGER name BEFORE/AFTER event ON table ...\n"
            "  EXEC proc_name(args)\n"
            "  DBMS_OUTPUT.PUT_LINE('text')\n\n"
            "Views & Sequences:\n"
            "  CREATE VIEW name AS SELECT ...\n"
            "  CREATE SEQUENCE name START WITH 1 INCREMENT BY 1\n\n"
            "Other:\n"
            "  DESCRIBE table  -  show table structure\n"
            "  COMMIT / ROLLBACK / SAVEPOINT\n"
            "  TABLES  -  list tables\n"
        )
        msg = tk.Toplevel(self.root)
        msg.title("SQL Reference")
        msg.geometry("620x540")
        msg.configure(bg=COLOR_BG)
        msg.minsize(400, 300)

        accent_bar = tk.Frame(msg, bg=COLOR_ACCENT, height=4)
        accent_bar.pack(fill=tk.X)

        text_frame = tk.Frame(msg, bg=COLOR_BG)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        text = tk.Text(text_frame, font=self.font_normal, wrap=tk.WORD,
                       bg='white', fg='black', bd=1, relief=tk.FLAT,
                       highlightbackground=COLOR_BORDER, highlightthickness=1,
                       padx=12, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert("1.0", help_text)
        text.config(state=tk.DISABLED)

        btn_frame = tk.Frame(msg, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        self._make_flat_button(btn_frame, "Close", msg.destroy,
                               padx=20, pady=4).pack()


# ── Entry Point ────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    app = OracleSQLLiteApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
