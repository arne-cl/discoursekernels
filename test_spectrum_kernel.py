
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
    ('a', 'b', 1): 0,
    ('ab', 'ab', 1): 2,
    ('abccc', 'abc', 2): 7
}


def test_bruteforce_blended_spectrum_kernel():
    from spectrum_kernel import bruteforce_blended_spectrum_kernel
    for params, result in BBS_KERNEL_PARAMS.iteritems():
        assert bruteforce_blended_spectrum_kernel(*params) == result


def test_p_suffix_kernel():
    from spectrum_kernel import p_suffix_kernel
    raise NotImplementedError


def test_blended_spectrum_kernel():
    from spectrum_kernel import blended_spectrum_kernel
    raise NotImplementedError
