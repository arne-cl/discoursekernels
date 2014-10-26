
KSUFFIX_KERNEL_PARAMS = {
    ('', '', 1): 0,
    ('', '', 2): 0,
    ('a', '', 1): 0,
    ('a', 'a', 1): 1,
    ('a', 'a', 2): 0,
    ('aa', 'ab', 1): 0,
    ('aa', 'ab', 2): 0,
    ('ab', 'ab', 1): 1,
    ('ab', 'ab', 2): 1,
}

def test_k_suffix_kernel():
    from spectrum_kernel import k_suffix_kernel
    for params, result in KSUFFIX_KERNEL_PARAMS.iteritems():
        assert k_suffix_kernel(*params) == result


PSPECTRUM_KERNEL_PARAMS = {
    ('bar', 'bar', 2): 2,
    ('bar', 'bat', 2): 1,
    ('bar', 'car', 2): 1,
    ('bar', 'cat', 2): 0,
    ('statistics', 'computation', 3): 2,
}

def test_p_spectrum_kernel():
    from spectrum_kernel import p_spectrum_kernel
    for params, result in PSPECTRUM_KERNEL_PARAMS.iteritems():
        assert p_spectrum_kernel(*params) == result


BBS_KERNEL_PARAMS = {
    ('a', 'a', 1): 1,
    # ('a','a', 2): 4, # from blended_spectrum_bf.m; doesn't work there either
    ('a', 'b', 1): 0,
    ('ab', 'ab', 1): 2,
    ('abccc', 'abc', 2): 7,
    ('abc','abccc',2): 7,
    ("b", "b", 2): 1,
    ("b", "be", 2): 1,
    ("b", "ber", 2): 1,
    ("bi", "b", 2): 1,
    ("bi", "be", 2): 1,
    ("bi", "ber", 2): 1,
    ("bie", "b", 2): 1,
    ("bie", "be", 2): 2,
    ("bie", "ber", 2): 2,
    ("bieb", "b", 2): 2,
    ("bieb", "be", 2): 3,
    ("bieb", "ber", 2): 3,
    ("biebe", "b", 2): 2,
    ("biebe", "be", 2): 5,
    ("biebe", "ber", 2): 5,
    ("bieber", "b", 2): 2,
    ("bieber", "be", 2): 5,
    ("bieber", "ber", 2): 7
}


def test_bruteforce_blended_spectrum_kernel():
    from spectrum_kernel import bruteforce_blended_spectrum_kernel
    for params, result in BBS_KERNEL_PARAMS.iteritems():
        assert bruteforce_blended_spectrum_kernel(*params) == result


PSUFFIX_KERNEL_PARAMS = {
    # result is always zero for lambda=0 or p=0
    ('', '', 0, 0): 0,
    ('', '', 0, 1): 0,
    ('hall', 'halt', 3, 1): 0,
    ('foo', 'bar', 0, 0): 0,
    ('foo', 'bar', 0, 1): 0,
    ('foo', 'foo', 1, 0): 0,
    ('foo', 'foo', 1, 1): 1,
    ('foo', 'foo', 2, 1): 2,
    ('foo', 'foo', 3, 1): 2,
    ('foo', 'foo', 4, 1): 2,
    ('foo', 'foo', 5, 1): 2,
    ('foo', 'foo', 3, 2): 20,
    ('bieber', 'fieber', 0, 0): 0,
    ('bieber', 'fieber', 0, 1): 0,
    ('bieber', 'fieber', 1, 0): 0,
    ('bieber', 'fieber', 5, 1): 5,
}


def test_p_suffix_kernel():
    from spectrum_kernel import p_suffix_kernel
    for params, result in PSUFFIX_KERNEL_PARAMS.iteritems():
        assert p_suffix_kernel(*params) == result


def test_blended_spectrum_kernel():
    from spectrum_kernel import blended_spectrum_kernel
    from test_matlab_blended_kernel import BLENDED_SPECTRUM_KERNEL_PARAMS
    for params, result in BLENDED_SPECTRUM_KERNEL_PARAMS.iteritems():
        assert blended_spectrum_kernel(*params) == result
