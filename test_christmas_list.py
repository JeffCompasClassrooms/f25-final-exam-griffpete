import os
import pytest
from pytest import fixture
from christmas_list import ChristmasList


def describe_ChristmasList():
    @fixture
    def test_list_file(tmp_path):
        list_file = tmp_path / "test_list.pkl"
        yield str(list_file)
        if os.path.exists(str(list_file)):
            os.remove(str(list_file))

    def describe_init():
        def stores_file(test_list_file):
            cl = ChristmasList(test_list_file)
            assert cl.fname == test_list_file

        def does_not_overwrite_file(test_list_file):
            cl1 = ChristmasList(test_list_file)
            cl1.saveItems([{"name": "Buzz Lightyear", "purchased": False}])
            cl2 = ChristmasList(test_list_file)
            data = cl2.loadItems()
            assert data == [{"name": "Buzz Lightyear", "purchased": False}]

        def makes_new_list(test_list_file):
            cl = ChristmasList(test_list_file)
            data = cl.loadItems()
            assert data == []
            assert isinstance(data, list)

    def describe_loadItems():
        def load_zero_items(test_list_file):
            cl = ChristmasList(test_list_file)
            result = cl.loadItems()
            assert result == []

        def loads_one_item(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.saveItems([{"name": "Mr Potato Head", "purchased": False}])
            result = cl.loadItems()
            assert result == [{"name": "Mr Potato Head", "purchased": False}]

        def loads_many_items(test_list_file):
            cl = ChristmasList(test_list_file)
            test_data = [
                {"name": "Slinky Dog", "purchased": False},
                {"name": "Etch a Sketch", "purchased": True},
                {"name": "Woody", "purchased": False}
            ]
            cl.saveItems(test_data)
            result = cl.loadItems()
            assert result == test_data

    def describe_saveItems():
        def saves_zero_items(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.saveItems([])
            result = cl.loadItems()
            assert result == []

        def saves_many_items(test_list_file):
            cl = ChristmasList(test_list_file)
            test_data = [
                {"name": "little bo peep", "purchased": False},
                {"name": "rc", "purchased": True}
            ]
            cl.saveItems(test_data)
            result = cl.loadItems()
            assert result == test_data

        def overwrites_existing_items(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.saveItems([{"name": "penguin", "purchased": False}])
            cl.saveItems([{"name": "Buzz Lightyear", "purchased": False}])
            result = cl.loadItems()
            assert result == [{"name": "Buzz Lightyear", "purchased": False}]
            assert {"name": "penguin", "purchased": False} not in result

    def describe_add():
        def adds_item_empty_list(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Mr potato head")
            result = cl.loadItems()
            assert result == [{"name": "Mr potato head", "purchased": False}]

        def adds_item_to_list(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Duke Kaboom")
            cl.add("Woody")
            result = cl.loadItems()
            assert result == [
                {"name": "Duke Kaboom", "purchased": False},
                {"name": "Woody", "purchased": False}
            ]

        def new_item_purchased_is_false(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Train Set")
            result = cl.loadItems()
            assert result[0]["purchased"] is False

    def describe_check_off():
        def marks_purchased_true(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Barrell of Monkeys")
            cl.check_off("Barrell of Monkeys")
            result = cl.loadItems()
            assert result[0]["purchased"] is True

        def marks_purchased_true_long_list(test_list_file):
            cl = ChristmasList(test_list_file)
            test_data = [
                {"name": "little bo peep", "purchased": False},
                {"name": "rc", "purchased": False},
                {"name": "woody", "purchased": False},
                {"name": "buzz lightyear", "purchased": False},
                {"name": "mr potato head", "purchased": False},
                {"name": "mrs potato head", "purchased": False}
            ]
            cl.saveItems(test_data)
            cl.check_off("rc")
            result = cl.loadItems()
            assert result[0]["purchased"] is False
            assert result[1]["purchased"] is True
            assert result[2]["purchased"] is False
            assert result[3]["purchased"] is False
            assert result[4]["purchased"] is False
            assert result[5]["purchased"] is False

        def does_nothing_null_item(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("buzz lighyear")
            cl.check_off("The Infinity Gauntlet")
            result = cl.loadItems()
            assert result[0]["purchased"] is False

        def checks_all_duplicates(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Sporky")
            cl.add("Sporky")
            cl.check_off("Sporky")
            result = cl.loadItems()
            assert result[0]["purchased"] is True
            assert result[1]["purchased"] is True

        def handles_empty_list(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.check_off("Jim Halpert")
            result = cl.loadItems()
            assert result == []

    def describe_remove():
        def removes_single_item(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Sporky")
            cl.remove("Sporky")
            result = cl.loadItems()
            assert result == []

        def removes_correct_item_long_list(test_list_file):
            cl = ChristmasList(test_list_file)
            test_data = [
                {"name": "little bo peep", "purchased": False},
                {"name": "rc", "purchased": False},
                {"name": "woody", "purchased": False},
                {"name": "buzz lightyear", "purchased": False},
                {"name": "mr potato head", "purchased": False},
                {"name": "mrs potato head", "purchased": False}
            ]
            cl.saveItems(test_data)
            cl.remove("rc")
            result = cl.loadItems()
            assert result[0]["name"] == "little bo peep"
            assert result[1]["name"] == "woody"
            assert result[2]["name"] == "buzz lightyear"
            assert result[3]["name"] == "mr potato head"
            assert result[4]["name"] == "mrs potato head"

        def removes_all_duplicate_items(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Sporky")
            cl.add("Purple Teddy Bear")
            cl.add("Sporky")
            cl.remove("Sporky")
            result = cl.loadItems()
            assert len(result) == 1
            assert result[0]["name"] == "Purple Teddy Bear"

        def does_nothing_null_item(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.add("Chicken Man")
            cl.remove("Cosmo Kramer")
            result = cl.loadItems()
            assert len(result) == 1
            assert result[0]["name"] == "Chicken Man"

        def handles_empty_list(test_list_file):
            cl = ChristmasList(test_list_file)
            cl.remove("Stanley Hudson")
            result = cl.loadItems()
            assert result == []

    def describe_print_list():
        def prints_empty_list(test_list_file, capsys):
            cl = ChristmasList(test_list_file)
            cl.print_list()
            captured = capsys.readouterr()
            assert captured.out == ""

        def prints_unpurchased_item(test_list_file, capsys):
            cl = ChristmasList(test_list_file)
            cl.add("Andy")
            cl.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[_] Andy\n"

        def prints_purchased_item(test_list_file, capsys):
            cl = ChristmasList(test_list_file)
            cl.add("Sid")
            cl.check_off("Sid")
            cl.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[x] Sid\n"

        def prints_many_items(test_list_file, capsys):
            cl = ChristmasList(test_list_file)
            cl.add("Slinky Dog")
            cl.add("Little Bo Peep")
            cl.add("Jessie")
            cl.check_off("Slinky Dog")
            cl.check_off("Jessie")
            cl.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[x] Slinky Dog\n[_] Little Bo Peep\n[x] Jessie\n"
