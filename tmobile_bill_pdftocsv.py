import pdfplumber
import re
import sys
from typing import Tuple, Dict, List
from decimal import Decimal
from collections import defaultdict
import csv
from io import StringIO

def extract_phone_bill_from_pdf(pdf_file: str) -> Tuple[Decimal, Dict[str, Decimal], str]:
    """
    Extract phone bill data from a PDF file.

    Args:
        pdf_file (str): Path to the PDF file

    Returns:
        Tuple[Decimal, Dict[str, Decimal], str]: (account_total, line_wise_extras, bill_period)
    """
    # Compile regex pattern once
    bill_period_pattern = re.compile(r"\b[A-Za-z]{3} \d{1,2} - [A-Za-z]{3} \d{1,2}\b")

    account_total = Decimal('0')
    bill_period = ""
    line_wise_extras = defaultdict(Decimal)

    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = pdf.pages[1].extract_text()

            if not text:
                return account_total, dict(line_wise_extras), bill_period

            lines = [line for line in map(str.strip, text.split("\n")) if line]

            for line in lines:
                if line.startswith("Charged") and not bill_period:
                    if match := bill_period_pattern.search(line):
                        bill_period = match.group(0)
                        if account_total != 0:
                            break

                elif line.startswith("Account") and not account_total:
                    if parts := line.split(maxsplit=2):
                        try:
                            account_total = Decimal(parts[1].strip().replace("$", ""))
                            if bill_period:
                                break
                        except (IndexError, ValueError):
                            continue

                elif line.startswith("("):
                    key = line[:14]
                    try:
                        value = Decimal(line.rpartition("-")[-1].split(maxsplit=1)[0].strip().replace("$", ""))
                        line_wise_extras[key] = value
                    except (ValueError, IndexError):
                        continue

    except Exception as e:
        print(f"Error processing PDF {pdf_file}: {e}", file=sys.stderr)
        return account_total, dict(line_wise_extras), bill_period

    return account_total, dict(line_wise_extras), bill_period

def generate_csv(files: List[str]) -> str:
    """
    Generate CSV content from multiple PDF files.

    Args:
        files (List[str]): List of PDF file paths

    Returns:
        str: CSV formatted string
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Line", "Bill Period", "Base charge", "Extra charges (Equipment, Services etc)", "Bill Amount"])

    for pdf_file in files:
        account_total, line_wise_extras, bill_period = extract_phone_bill_from_pdf(pdf_file)

        if line_wise_extras:
            base_cost_per_line = account_total / len(line_wise_extras)
            for line, extra in line_wise_extras.items():
                total = extra + base_cost_per_line
                writer.writerow([line, bill_period, f"${base_cost_per_line:.2f}", f"${extra:.2f}", f"${total:.2f}"])

    return output.getvalue()

def main():
    if len(sys.argv) < 2:
        print("Please provide at least one PDF file.", file=sys.stderr)
        sys.exit(1)

    csv_content = generate_csv(sys.argv[1:])
    print(csv_content)

if __name__ == "__main__":
    main()
