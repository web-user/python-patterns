from abc import ABC
from enum import Enum


class BankAccount:
    OVERDRAFT_LIMIT = -500

    def __init__(self, balance: float = 0):
        self.balance = balance

    def deposit(self, amount: float):
        self.balance += amount
        print(f'Deposited: {amount}, balance = {self.balance}')

    def withdraw(self, amount: float):
        """
        if the current balance, minus the withdrawn amount, is greater than or equal to the established limit
        Args:
            amount: the withdrawn amount
        Returns:
            Nothing.
        """
        if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            print(f'Withdrew: {amount}, balance = {self.balance}')
            return True
        return False

    def __str__(self):
        return f'Balance: {self.balance}'


class Command(ABC):

    def __init__(self):
        self.success = False

    def invoke(self):
        pass

    def undo(self):
        pass


class BankAccountCommand(Command):
    """
    Must implement command interface
    """

    class Action(Enum):
        DEPOSIT = 0
        WITHDRAW = 1

    def __init__(self, account, action, amount):
        super().__init__()
        self.account = account
        self.action = action
        self.amount = amount

    def invoke(self):
        """
        interface implementation
        Args:
            Nothing.
        Returns:
            Nothing.
        """
        if self.action == self.Action.DEPOSIT:
            self.account.deposit(self.amount)
            self.success =True
        elif self.action == self.Action.WITHDRAW:
            self.success = self.account.withdraw(self.amount)

    def undo(self):
        """
        If the last operation was successful, we can do a cancellation
        """
        if not self.success:
            return None
        # strictly speaking this is not correct
        # (you don't undo a deposit by withdrawing)
        # but it works for this demo, so...
        if self.action == self.Action.DEPOSIT:
            self.account.withdraw(self.amount)
        elif self.action == self.Action.WITHDRAW:
            self.account.deposit(self.amount)



# try using this before using MoneyTransferCommand!
class CompositeBankAccountCommand(Command, list):
    def __init__(self, items=[]):
        super().__init__()
        for i in items:
            self.append(i)

    def invoke(self):
        for x in self:
            x.invoke()

    def undo(self):
        for x in reversed(self):
            x.undo()


class MoneyTransferCommand(CompositeBankAccountCommand):
    def __init__(self, from_acct, to_acct, amount):
        super().__init__([
            BankAccountCommand(from_acct,
                               BankAccountCommand.Action.WITHDRAW,
                               amount),
            BankAccountCommand(to_acct,
                               BankAccountCommand.Action.DEPOSIT,
                               amount)])

    def invoke(self):
        ok = True
        for cmd in self:
            if ok:
                cmd.invoke()
                ok = cmd.success
            else:
                cmd.success = False
        self.success = ok


if __name__ == '__main__':
    ba = BankAccount()

    cmd = BankAccountCommand(
        ba, BankAccountCommand.Action.DEPOSIT, 1000
    )

    cmd.invoke()
    print(f'After $1000 deposit: {ba}')

    cmd.undo()
    print(f'$1000 deposit undone: {ba}')

    illegal_cmd = BankAccountCommand(ba, BankAccountCommand.Action.WITHDRAW, 700)
    illegal_cmd.invoke()
    print('After impossible withdrawal:', ba)
    illegal_cmd.undo()
    print('After undo:', ba)