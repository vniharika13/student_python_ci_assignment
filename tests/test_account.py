import pytest

from student_account import BankAccount


def test_deposit_increases_balance():
    account = BankAccount("Alice", 100)
    assert account.deposit(50) == 150
    assert account.balance == 150.0
    assert account.transaction_count == 1


def test_withdraw_decreases_balance_and_tracks_transaction():
    account = BankAccount("Bob", 200)
    assert account.withdraw(75) == 125
    assert account.balance == 125.0
    assert account.transaction_count == 1


def test_invalid_account_creation_values():
    with pytest.raises(ValueError, match="Owner name cannot be empty."):
        BankAccount("   ")

    with pytest.raises(ValueError, match="Opening balance cannot be negative."):
        BankAccount("Dana", -1)


def test_invalid_deposit_and_withdraw_amounts():
    account = BankAccount("Eve", 100)

    for invalid_amount in (0, -5):
        with pytest.raises(ValueError, match="Amount must be greater than zero."):
            account.deposit(invalid_amount)

    with pytest.raises(ValueError, match="Amount must be greater than zero."):
        account.withdraw(0)

    with pytest.raises(ValueError, match="Insufficient funds."):
        account.withdraw(101)


def test_transfer_between_accounts_updates_balances_and_history():
    sender = BankAccount("Alice", 200)
    receiver = BankAccount("Bob", 50)

    assert sender.transfer_to(receiver, 75) == 125
    assert sender.balance == 125.0
    assert receiver.balance == 125.0
    assert sender.transaction_count == 2
    assert receiver.transaction_count == 2

    with pytest.raises(TypeError, match="Target must be a BankAccount."):
        sender.transfer_to("Not an account", 10)


def test_monthly_interest_is_added_and_negative_rates_are_rejected():
    account = BankAccount("Frank", 1200)
    interest = account.monthly_interest(0.12)

    assert interest == 12.0
    assert account.balance == 1212.0

    with pytest.raises(ValueError, match="Annual rate cannot be negative."):
        account.monthly_interest(-0.01)


def test_statement_shows_empty_and_populated_transaction_history():
    empty_account = BankAccount("Grace", 0)
    statement = empty_account.statement()
    assert "Owner: Grace" in statement
    assert "Balance: 0.00" in statement
    assert "Transactions: 0" in statement
    assert "No transactions." in statement

    populated = BankAccount("Hank", 100)
    populated.deposit(25)
    populated.withdraw(10)
    populated_statement = populated.statement()

    assert "Owner: Hank" in populated_statement
    assert "Balance: 115.00" in populated_statement
    assert "Transactions: 2" in populated_statement
    assert "TransactionHistory:" in populated_statement
    assert "('deposit', 25)" in populated_statement
    assert "('withdraw', 10)" in populated_statement
