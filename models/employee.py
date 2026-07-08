from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    """Modelo de dados para representar um funcionário"""

    first_name: str
    last_name: str
    email: str
    address: str
    phone_number: str
    company_name: str
    role_in_company: str

    @classmethod
    def from_excel_row(cls, row: dict) -> "Employee":
        """
        Cria uma instância de Employee a partir de uma linha do DataFrame do Excel

        Args:
            row: Dicionário contendo os dados da linha

        Returns:
            Instância de Employee
        """
        return cls(
            first_name=row.get("First Name", ""),
            last_name=row.get("Last Name ", ""),
            email=row.get("Email", ""),
            address=row.get("Address", ""),
            phone_number=row.get("Phone Number", ""),
            company_name=row.get("Company Name", ""),
            role_in_company=row.get("Role in Company", ""),
        )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
