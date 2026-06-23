from app.repositories.accounts import InMemoryAccountRepository
from app.repositories.categories import InMemoryCategoryRepository
from app.repositories.transactions import InMemoryTransactionRepository
from app.services.accounts import AccountService
from app.services.categories import CategoryService
from app.services.transactions import TransactionService


account_repository = InMemoryAccountRepository()
category_repository = InMemoryCategoryRepository()
transaction_repository = InMemoryTransactionRepository()


def get_account_service() -> AccountService:
    return AccountService(account_repository)


def get_category_service() -> CategoryService:
    return CategoryService(category_repository)


def get_transaction_service() -> TransactionService:
    return TransactionService(
        transaction_repository,
        account_repository,
        category_repository,
    )
