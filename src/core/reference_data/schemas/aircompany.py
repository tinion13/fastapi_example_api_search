from pydantic import TypeAdapter

aircompanies_adapter = TypeAdapter(dict[str, str])
