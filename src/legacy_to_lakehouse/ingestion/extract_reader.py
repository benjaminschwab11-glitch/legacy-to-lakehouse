"""Read delimited account extracts into typed rows."""

import csv
import logging
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AccountRow:
    tenant_id: str
    account_id: str
    balance: Decimal  # exact decimal, like Oracle NUMBER(p,s)


def iter_rows(path: Path) -> Iterator[AccountRow]:
    """Yield one AccountRow per line; skip rows whose balance is not a number."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        # Like a PL/SQL cursor FOR loop: one row fetched at a time, closed at the end.
        for record in reader:
            try:
                balance = Decimal(record["balance"])
            except InvalidOperation:
                logger.warning(
                    "line %d: invalid balance %r, row skipped",
                    reader.line_num,
                    record["balance"],
                )
                continue
            yield AccountRow(record["tenant_id"], record["account_id"], balance)


def count_by_tenant(rows: Iterable[AccountRow]) -> dict[str, int]:
    """Count rows per tenant, like SELECT tenant_id, COUNT(*) ... GROUP BY tenant_id."""
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.tenant_id] = counts.get(row.tenant_id, 0) + 1
    return counts
