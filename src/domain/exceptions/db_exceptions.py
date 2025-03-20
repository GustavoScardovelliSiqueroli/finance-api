class DatabaseError(Exception):
    """Base class for other database-related exceptions"""

    pass


class RecordNotFoundError(DatabaseError):
    """Raised when a record is not found in the database"""

    def __init__(self, record_name: str, record_id: str) -> None:
        self.message = f'{record_name} not found.'
        super().__init__(self.message)


class DuplicateRecordError(DatabaseError):
    """Raised when a duplicate record is found in the database"""

    def __init__(self, column: str, record: str) -> None:
        self.message = f'{column} {record} already exists.'
        super().__init__(self.message)


class DatabaseConnectionError(DatabaseError):
    """Raised when there is a database connection error"""

    def __init__(self, db_url: str) -> None:
        self.message = f'Failed to connect to database at {db_url}.'
        super().__init__(self.message)


class DataValidationError(DatabaseError):
    """Raised when data validation fails"""

    def __init__(self, errors: Exception) -> None:
        self.message = f'Data validation errors: {errors}.'
        super().__init__(self.message)


class LoginDuplicateError(DatabaseError):
    """Raised when a login is duplicated in the database"""

    def __init__(self, login: str) -> None:
        self.message = f'Login {login} already exists.'
        super().__init__(self.message)


class ForeignKeyError(DatabaseError):
    """Raised when a foreign key constraint is violated"""

    def __init__(self, table_name: str, column_name: str) -> None:
        self.message = f'Chave estrangeira {table_name}.{column_name} não encontrada.'
        super().__init__(self.message)
