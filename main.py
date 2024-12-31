import csv
import json
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import JsonLexer
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Any


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class MeterRecord(BaseModel):
    _id: str
    meterSerial: str
    kWh: float
    amount: float
    vendor: str
    session_id: Optional[bool] = None
    error: Optional[str] = None
    errorCode: Optional[str] = None
    city: Optional[str] = None
    country_id: int
    name: Optional[str] = None
    state_id: Optional[int] = None
    street: Optional[str] = None
    timestamp: datetime
    isSynced: bool
    syncMethod: Optional[str] = None
    syncedBy: Optional[str] = None
    syncDate: Optional[datetime] = None
    session_id_0: Optional[str] = Field(default=None, alias='session_id[0]')
    session_id_1: Optional[str] = Field(default=None, alias='session_id[1]')

    class Config:
        populate_by_name = True


def load_csv(file_path):
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                # Clean empty strings to None
                cleaned_row = {k: (v if v != "" else None)
                               for k, v in row.items()}
                try:
                    validated_row = MeterRecord(**cleaned_row)
                    data.append(validated_row.model_dump())
                except Exception as e:
                    print(f"Error processing row: {cleaned_row}")
                    print(f"Error details: {e}")
                    continue
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

# Function to display the JSON content


def display_json(data):
    if not data:
        print("\nNo data available.\n")
        return
    # Use the custom encoder for datetime objects
    json_str = json.dumps(data, indent=2, cls=DateTimeEncoder)
    colorful_json = highlight(json_str, JsonLexer(), TerminalFormatter())
    print(colorful_json)


# Main function
def main():
    file_path = "data.csv"
    data = load_csv(file_path)
    display_json(data)


if __name__ == "__main__":
    main()
