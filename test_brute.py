import pytest
from brute import Brute

def describe_brute_once():
    def describe_with_good_pass():
        def returns_true_for_char():
            brute = Brute("a")
            assert brute.bruteOnce("a") is True

        def returns_true_string():
            brute = Brute("password123")
            assert brute.bruteOnce("password123") is True

        def returns_true_uppercase():
            brute = Brute("ABCDEF")
            assert brute.bruteOnce("ABCDEF") is True

        def returns_true_lowercase():
            brute = Brute("abcdef")
            assert brute.bruteOnce("abcdef") is True

        def returns_true_digits():
            brute = Brute("12345678")
            assert brute.bruteOnce("12345678") is True

    def describe_with_bad_pass():
        def returns_false():
            brute = Brute("password")
            assert brute.bruteOnce("wrong") is False

        def returns_false_not_upper():
            brute = Brute("Password")
            assert brute.bruteOnce("password") is False

    def describe_edge_cases():
        def handles_empty_pass_true():
            brute = Brute("")
            assert brute.bruteOnce("") is True

        def returns_empty_pass_false():
            brute = Brute("")
            assert brute.bruteOnce("a") is False

        def handles_weird_pass():
            brute = Brute("a!b@c#")
            assert brute.bruteOnce("a!b@c#") is True


def describe_brute_many():
    def describe_success():
        def returns_true_first_try(mocker):
            brute = Brute("password")
            mocker.patch.object(brute, 'randomGuess', return_value='password')
            result = brute.bruteMany(limit=10)
            assert result >= 0
            assert isinstance(result, float)

        def returns_true_second_try(mocker):
            brute = Brute("abc")
            mocker.patch.object(brute, 'randomGuess', side_effect=['wrong', 'abc'])
            result = brute.bruteMany(limit=10)
            assert result >= 0
            assert isinstance(result, float)

        def returns_true_last_try(mocker):
            brute = Brute("abc")
            wrong_guesses = ['wrong'] * 9
            mocker.patch.object(brute, 'randomGuess', side_effect=wrong_guesses + ['abc'])
            result = brute.bruteMany(limit=10)
            assert result >= 0
            assert isinstance(result, float)

    def describe_failure():
        def returns_neg_one_bad_guess(mocker):
            brute = Brute("password")
            mocker.patch.object(brute, 'randomGuess', return_value='wrong')
            result = brute.bruteMany(limit=5)
            assert result == -1

        def returns_neg_one_reached_limit(mocker):
            brute = Brute("password")
            mocker.patch.object(brute, 'randomGuess', return_value='password')
            result = brute.bruteMany(limit=0)
            assert result == -1
