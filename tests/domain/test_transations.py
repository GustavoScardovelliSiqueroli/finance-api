import pytest

from src.domain.models.category import Category
from src.domain.models.transaction import Transaction


@pytest.mark.asyncio
async def test_realationship_transaction_category() -> None:
    test = Transaction(
        id=1,
        id_user=1,
        value=1.0,
        description='test',
        type='INCOME',
        created_at='2023-07-01 00:00:00',
        updated_at='2023-07-01 00:00:00',
        deleted_at='2023-07-01 00:00:00',
    )
    test.categories = [Category(id=1, id_user=1, name='test', type='INCOME')]
    assert test.as_dict()
