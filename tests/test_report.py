import pytest
from prettytable import PrettyTable
from janitor.module.history import History


def test_create_report():
    try:
        history = History()
        history.print_history()
        print(f"report path = {history.history_path}")
        assert True
    except Exception as ex:
        raise (ex)
        assert False
