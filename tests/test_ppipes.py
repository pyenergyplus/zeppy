"""py.test for ppipes.py"""

from zeppy import ppipes
import pytest

@pytest.mark.parametrize('seconds, expected', [
    (1, 1),
    ])
def test_waitsome(seconds, expected):
    """py.test for waitsome"""
    result = ppipes.waitsome(seconds)
    assert result == expected
        
@pytest.mark.parametrize('args_list, expected', [
    ([(1, ), (2, ), (3, )], [{'args':(1, )}, {'args':(2, )}, {'args':(3, )}]),
    ([(1, 2, ), (2, 2, ), (3, 2, )], [{'args':(1, 2)}, {'args':(2, 2)}, {'args':(3, 2)}]),
    ([1, 2, 3], [{'args':(1, )}, {'args':(2, )}, {'args':(3, )}]),
])
def test_arglist_helper(args_list, expected):
    """py.test for arglist_helper"""
    result = ppipes.arglist_helper(args_list)
    assert result == expected