#

_BASE = 26
_A_OFFSET = 65
_Z_OFFSET = 90

def _toCharacter(num):
    if num > _BASE - 1:
        raise ValueError('`num` must be less 26.')
    if num < 0:
        raise ValueError('`num` must be greater than or equal to 0.')
    return chr(num + _A_OFFSET)

def indexToColumn(index):
    """
    Given a 0-based index, returns the upper case column letter sequence. E.g.:
        * Given 0 returns 'A'
        * Given 4 returns 'E'
        * Given 25 returns 'Z'
        * Given 27 returns 'AB'
    @param index The column index.
    @return string The column letter sequence.
    """
    if index < 0:
        raise ValueError('`index` must be a number greater than or equal to 0')
    ratio = int(index) / _BASE
    chars = [_toCharacter(int(index) % _BASE)]
    while ratio > 0:
        chars.append(_toCharacter(int(ratio - 1) % _BASE))
        ratio = int(ratio - 1) / _BASE
    return ''.join(reversed(chars))

def _toNumber(col):
    val = ord(col)
    if val < _A_OFFSET or val > _Z_OFFSET:
        raise ValueError('`col` must be a capital letter between A and Z')
    return val - _A_OFFSET 

def columnToIndex(column):
    """
    Given a column (e.g. 'A', 'F', 'AC', etc.) returns the 0-based index. E.g.:
        * Given 'A' retuns 0
        * Given 'E' returns 4
        * Given 'Z' returns 25
        * Given 'AB' returns 27
    @param string The column letter sequence.
    @return string the column index.
>>> col1 = 26
>>> col2 = 26 * col1 + 26
>>> col3 = 26 * col2 + 26
>>> col4 = 26 * col3 + 26

    """
    

def test(index):
    print('%s: %s' % (index, indexToColumn(index)))

if __name__ == "__main__":
    test(0)
    test(26)
    test(26 + 26)
    test(78)
    test(702)
    test(4351)
    test(18278)
    test(475254)
    test(12356630)
