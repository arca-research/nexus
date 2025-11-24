import sqlite3
from .database_connection import Graph_Index_Connection
from contextlib import contextmanager
from pathlib import Path
from typing_extensions import override
from typing import Optional


class Sqlite_Connection(Graph_Index_Connection):
    """
    Class that represents a SQLite connection to a graph database
    """

    def __init__(self, index_path: str | Path):
        super().__init__(index_path)

    @contextmanager
    def _conn(self):
        """
        Helper to open a SQLite connection with row access by column name.
        """
        con = sqlite3.connect(self.index_path)
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA foreign_keys=ON;")
        con.execute("PRAGMA busy_timeout=5000;")
        con.row_factory = sqlite3.Row

        self.con = con
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            self.con = None
            raise
        finally:
            con.close()
            self.con = None

    @override
    def execute(self, query, params: Optional[tuple] = (), con=None):
        if con is not None:
            # If context manager override is used
            if params == ():
                return con.execute(query)
            else:
                return con.execute(query, params)
        if self.con is None:
            raise RuntimeError("execute() called outside of a _conn() context")

        if params == ():
            return self.con.execute(query)
        else:
            return self.con.execute(query, params)
