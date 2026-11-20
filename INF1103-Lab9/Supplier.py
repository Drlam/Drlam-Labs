class Supplier:
    def __init__(self, supplier_id: int, name: str, contact_email: str) -> None:
        self.__supplier_id: int = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    # Getter methods
    def get_supplier_id(self) -> int:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    # Display supplier information
    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.__supplier_id}, Name: {self.__name}, "
            f"Contact Email: {self.__contact_email}"
        )