#type: ignore
import pytest
from src.services.transaction_service import TransactionService
from src.services.category_service import CategoryService
from src.infra.db.repositories.category_repository import CategoryRepository
from src.infra.db.repositories.transaction_repository import TransactionRepository
from src.domain.models.transaction import Transaction
from src.infra.db.repositories.user_repository import UserRepository
from src.domain.models.user import User
from src.domain.models.category import Category

@pytest.fixture
async def user_instance(db_session):
    user = User(login='test', password='test')
    user_rep = UserRepository(db_session)
    return await user_rep.create(user)

@pytest.fixture
def category_repository(db_session):
    return CategoryRepository(db_session)

@pytest.fixture
def category_service(category_repository):
    return CategoryService(category_repository)

@pytest.fixture
def transaction_repository(db_session):
    return TransactionRepository(db_session)

@pytest.fixture
def transaction_service(transaction_repository, category_service):
    return TransactionService(transaction_repository, category_service)

@pytest.mark.asyncio
async def test_transaction_service_full_case(transaction_service, category_service, user_instance):
    transaction = await transaction_service.create_transaction(
        Transaction(
            id=1,
            id_user=user_instance.id,
            value=1.0,
            description='test',
            type='INCOME',
        )
    )
    assert transaction

    category = await category_service.create_category(
        Category(
            id=1,
            id_user=user_instance.id,
            level=0,
            name='test',
            type='INCOME',
        )
    )
    assert category

    tr_ct = await transaction_service.add_category(
        transaction.id, category.id
    )
    assert tr_ct
    assert tr_ct.categories
    assert tr_ct.description == transaction.description

    tr_ct = await transaction_service.update_transaction(
        transaction.id, {'description': 'test2'}
    )
    assert tr_ct
    assert tr_ct.description == 'test2'

    tr_ct = await transaction_service.delete_transaction(transaction.id)
    assert tr_ct
    assert tr_ct.deleted_at

    tr_ct = await transaction_service.get_transaction_by_id(transaction.id)
    assert tr_ct
    assert tr_ct.description == 'test2'
    assert tr_ct.deleted_at