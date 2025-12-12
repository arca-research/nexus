from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3
import hashlib


def debug_only(func):
    """Marks a function as debug/internal use only"""
    func.__debug_only__ = True
    return func


class Checksums:
    def __init__(self, index_path: str | Path):
        self.index_path = Path(index_path)
        self._initialize()


    @contextmanager
    def _conn(self):
        """
        Helper to open a SQLite connection with row access by column name.
        """
        con = sqlite3.connect(self.index_path, check_same_thread=False)
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA foreign_keys=ON;")
        con.execute("PRAGMA busy_timeout=5000;")
        con.row_factory = sqlite3.Row
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()


    def _initialize(self) -> None:
        with self._conn() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS checksums (
                    checksum TEXT PRIMARY KEY,
                    inserted_at INTEGER
                );
            """)


    def compute(self, data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode("utf-8")
        return hashlib.sha256(data).hexdigest()


    def has(self, checksum: str) -> bool:
        with self._conn() as con:
            row = con.execute(
                "SELECT 1 FROM checksums WHERE checksum = ? LIMIT 1;",
                (checksum,),
            ).fetchone()
            return row is not None


    def add(self, checksum: str) -> None:
        with self._conn() as con:
            con.execute(
                """
                INSERT OR IGNORE INTO checksums (checksum, inserted_at)
                VALUES (?, strftime('%s','now'));
                """,
                (checksum,),
            )
    

    def delete(self, checksum: str) -> bool:
        with self._conn() as con:
            cur = con.execute(
                "DELETE FROM checksums WHERE checksum = ?;",
                (checksum,),
            )
            return cur.rowcount > 0


    @debug_only
    def list_all_checksums(self) -> list[str]:
        with self._conn() as con:
            rows = con.execute(
                "SELECT checksum FROM checksums ORDER BY inserted_at;"
            ).fetchall()
            return [row[0] for row in rows]
