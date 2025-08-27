import time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from transactions_demo.models import BankAccount

def transfer_money(from_account_id, to_account_id, amount):
    """
    Simulates transfering money, demonstrating a race condition and how to fix it with transactions and locking.
    """

    # The Fix: Wrap the entire logic in the atomic block
    with transaction.atomic():
        from_account = BankAccount.objects.select_for_update().get(id = from_account_id)
        to_account = BankAccount.objects.select_for_update().get(id = to_account_id)
        print(f"Transferring ${amount} from {from_account.name} to {to_account.name}")
        print(f"Initial balances: {from_account.name}=${from_account.balance}, {to_account.name}=${to_account.balance}")

        if from_account.balance >= amount:
            # similate a delay between reading and writing
            # giving the second process a change to run
            time.sleep(1)
            from_account.balance -= amount
            to_account.balance += amount

            from_account.save()
            to_account.save()
            print("Transfer Successfull")
        else:
            print("Transfer failed: Insufficent Funds.")
        print(f"Final Balance: {from_account.name}=${from_account.balance}, {to_account.name}=${to_account.balance}")

class Command(BaseCommand):
    help = 'Simulate a bank transfer race condition'
    def handle(self, *args, **options):
        # Setup initial state
        checking, _ = BankAccount.objects.get_or_create(name="Checking", defaults={'balance': Decimal('1000.00')})
        savings, _ = BankAccount.objects.get_or_create(name="Savings", defaults={'balance': Decimal('5000.00')})
        checking.balance = Decimal('1000.00')
        savings.balance = Decimal('5000.00')
        checking.save()
        savings.save()

        print("--- Running two transfers concurrently ---")
        print("This will simulate a race condition if not handled correctly.")
        print("To run this test, open two separate terminal windows.")
        print("In each terminal, run the command: python manage.py run_transfer")
        print("Press Enter in both terminals at roughly the same time.")
        input("Press Enter to start...")

        # The actual transfer logic is called here
        transfer_money(checking.id, savings.id, Decimal('800.00'))
