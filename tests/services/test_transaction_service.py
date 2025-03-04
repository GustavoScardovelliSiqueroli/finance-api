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
from src.services.split_service import SplitService
from src.infra.db.repositories.split_repositoy import SplitRepository

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
def split_repository(db_session):
    return SplitRepository(db_session)

@pytest.fixture
def split_service():
    return SplitService(split_repository)

@pytest.fixture
def transaction_service(transaction_repository, category_service, split_service):
    return TransactionService(transaction_repository, category_service, split_service=split_service)


async def test_create_transaction(transaction_service, user_instance):
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

@pytest.mark.asyncio
async def test_create_category(category_service, user_instance):
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

@pytest.mark.asyncio
async def test_add_category(transaction_service, category_service, user_instance):
    transaction = await transaction_service.create_transaction(
        Transaction(
            id=1,
            id_user=user_instance.id,
            value=1.0,
            description='test',
            type='INCOME',
        )
    )
    category = await category_service.create_category(
        Category(
            id=1,
            id_user=user_instance.id,
            level=0,
            name='test',
            type='INCOME',
        )
    )
    tr_ct = await transaction_service.add_category(transaction.id, category.id)
    assert tr_ct
    assert tr_ct.categories
    assert tr_ct.categories[0].id == category.id

@pytest.mark.asyncio
async def test_update_transaction(transaction_service, user_instance):
    transaction = await transaction_service.create_transaction(
        Transaction(
            id=1,
            id_user=user_instance.id,
            value=1.0,
            description='test',
            type='INCOME',
        )
    )
    tr_ct = await transaction_service.update_transaction(transaction.id, {'description': 'test2'})
    assert tr_ct
    assert tr_ct.description == 'test2'

@pytest.mark.asyncio
async def test_get_transaction_by_id(transaction_service, user_instance):
    transaction = await transaction_service.create_transaction(
        Transaction(
            id=1,
            id_user=user_instance.id,
            value=1.0,
            description='test',
            type='INCOME',
        )
    )
    tr_ct = await transaction_service.get_transaction_by_id(transaction.id)
    assert tr_ct
    assert tr_ct.description == 'test'

@pytest.mark.asyncio
async def test_delete_transaction(transaction_service, user_instance):
    transaction = await transaction_service.create_transaction(
        Transaction(
            id=1,
            id_user=user_instance.id,
            value=1.0,
            description='test',
            type='INCOME',
        )
    )
    tr_ct = await transaction_service.delete_transaction(transaction.id)
    assert tr_ct
    assert tr_ct.deleted_at