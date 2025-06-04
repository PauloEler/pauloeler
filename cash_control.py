"""Simple cash control management module."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict


@dataclass
class CashControl:
    """Stores values for a daily cash report."""

    saldo_anterior: float = 0.0
    pagamentos_fornecedores: float = 0.0
    despesas_pessoais: float = 0.0
    marlene: float = 0.0
    pagamentos_diversos: float = 0.0
    vendas_dia: float = 0.0

    @property
    def saldo_atual(self) -> float:
        """Calculate the current balance."""
        return (
            self.saldo_anterior
            + self.vendas_dia
            - self.pagamentos_fornecedores
            - self.despesas_pessoais
            - self.marlene
            - self.pagamentos_diversos
        )

    def as_dict(self) -> Dict[str, Any]:
        """Return the report as a dictionary including the computed balance."""
        data = asdict(self)
        data["saldo_atual"] = self.saldo_atual
        return data

    def display(self) -> None:
        """Print a simple human readable report."""
        data = self.as_dict()
        print("Relatório de Caixa:")
        for key, value in data.items():
            print(f" - {key}: {value}")

    def to_json(self, file_path: str | Path) -> None:
        """Export the report to a JSON file."""
        path = Path(file_path)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(self.as_dict(), fh, ensure_ascii=False, indent=2)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cash control reporting")
    parser.add_argument("--json", dest="json_file", help="JSON file with input values")
    parser.add_argument("--saldo-anterior", type=float, default=0.0)
    parser.add_argument("--pagamentos-fornecedores", type=float, default=0.0)
    parser.add_argument("--despesas-pessoais", type=float, default=0.0)
    parser.add_argument("--marlene", type=float, default=0.0)
    parser.add_argument("--pagamentos-diversos", type=float, default=0.0)
    parser.add_argument("--vendas-dia", type=float, default=0.0)
    parser.add_argument("--export-json", help="Export the report to this JSON file")
    return parser.parse_args()


def _from_json(path: str | Path) -> CashControl:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return CashControl(
        saldo_anterior=data.get("saldo_anterior", 0.0),
        pagamentos_fornecedores=data.get("pagamentos_fornecedores", 0.0),
        despesas_pessoais=data.get("despesas_pessoais", 0.0),
        marlene=data.get("marlene", 0.0),
        pagamentos_diversos=data.get("pagamentos_diversos", 0.0),
        vendas_dia=data.get("vendas_dia", 0.0),
    )


def main(args: argparse.Namespace | None = None) -> None:
    if args is None:
        args = _parse_args()

    if args.json_file:
        ctrl = _from_json(args.json_file)
    else:
        ctrl = CashControl(
            saldo_anterior=args.saldo_anterior,
            pagamentos_fornecedores=args.pagamentos_fornecedores,
            despesas_pessoais=args.despesas_pessoais,
            marlene=args.marlene,
            pagamentos_diversos=args.pagamentos_diversos,
            vendas_dia=args.vendas_dia,
        )

    ctrl.display()

    if args.export_json:
        ctrl.to_json(args.export_json)


if __name__ == "__main__":
    main()
