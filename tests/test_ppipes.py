"""py.test for ppipes.py"""

from zeppy import ppipes
import pytest


@pytest.mark.parametrize(
    "strlength, expected",
    [
        (3, 3),  # strlength, expected
    ],
)
def test_randstr(strlength, expected):
    """py.test for randstr"""
    result = ppipes.randstr(
        strlength,
    )
    assert len(result) == expected
    result2 = ppipes.randstr(strlength)
    assert result2 != result


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (0.1, 0.1),
    ],
)
def test_waitsome(seconds, expected):
    """py.test for waitsome"""
    result = ppipes.waitsome(seconds)
    assert result == expected


# @pytest.mark.parametrize('args_list, expected', [
#     ([(1, ), (2, ), (3, )], [{'args':(1, )}, {'args':(2, )}, {'args':(3, )}]),
#     ([(1, 2, ), (2, 2, ), (3, 2, )], [{'args':(1, 2)}, {'args':(2, 2)}, {'args':(3, 2)}]),
#     ([1, 2, 3], [{'args':(1, )}, {'args':(2, )}, {'args':(3, )}]),
# ])
# def test_arglist_helper(args_list, expected):
#     """py.test for arglist_helper"""
#     result = ppipes.arglist_helper(args_list)
#     assert result == expected


@pytest.mark.parametrize(
    "args_kwargs, expected",
    [
        (
            [{"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}}],
            [{"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}}],
        ),  # args_kwargs, expected
        (
            [
                {
                    "args": (1, 2, 3),
                    "kwargs": {"a": 1, "b": 1},
                },
                {
                    "args": (1,),
                    "kwargs": {
                        "a": 1,
                    },
                },
            ],
            [
                {"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}},
                {
                    "args": (1,),
                    "kwargs": {
                        "a": 1,
                    },
                },
            ],
        ),  # args_kwargs, expected
        (
            [
                {
                    "args": (1, 2, 3),
                    "kwargs": {"a": 1, "b": 1},
                },
                11,
            ],
            [
                {"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}},
                {"args": (11,), "kwargs": {}},
            ],
        ),  # args_kwargs, expected
        (
            [
                {
                    "args": (1, 2, 3),
                    "kwargs": {"a": 1, "b": 1},
                },
                11,
                12,
            ],
            [
                {"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}},
                {"args": (11,), "kwargs": {}},
                {"args": (12,), "kwargs": {}},
            ],
        ),  # args_kwargs, expected
    ],
)
def test_args_kwargs_helper(args_kwargs, expected):
    """py.test for args_kwargs_helper"""
    result = ppipes.args_kwargs_helper(args_kwargs)
    print(result)
    print(expected)
    assert result == expected


@pytest.mark.parametrize(
    "args_kwargs, expected",
    [
        (
            {"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}},
            {"args": (1, 2, 3), "kwargs": {"a": 1, "b": 1}},
        ),  # args_kwargs, expected
        (
            (
                1,
                2,
                3,
            ),
            {"args": (1, 2, 3), "kwargs": {}},
        ),  # args_kwargs, expected
        (11, {"args": (11,), "kwargs": {}}),  # args_kwargs, expected
        (11, {"args": (11,), "kwargs": {}}),  # args_kwargs, expected
        ([], {"args": [], "kwargs": {}}),  # args_kwargs, expected
    ],
)
def test_clean_args_kwargs(args_kwargs, expected):
    """py.test for clean_args_kwargs"""
    result = ppipes.clean_args_kwargs(args_kwargs)
    print(result)
    print(expected)
    assert result == expected
