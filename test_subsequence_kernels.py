
ASK_PARAMS = {
    ('', ''): 1,
    ('a', ''): 1,
    ('', 'a'): 1,
    ('bar', 'bar'): 8,
    ('bar', 'car'): 4,
    ('bar', 'cat'): 2,
    ('gat', 'cata'): 5,
    ('gatt', 'cata'): 7,
    ('gatta', 'cata'): 14,
}

def test_all_subsequences_kernel_recursive():
    from subsequence_kernels import all_subsequences_kernel_recursive
    for params, result in ASK_PARAMS.iteritems():
        assert all_subsequences_kernel_recursive(*params) == result

def test_all_subsequences_kernel_dp1():
    from subsequence_kernels import all_subsequences_kernel_dp1
    for params, result in ASK_PARAMS.iteritems():
        assert all_subsequences_kernel_dp1(*params) == result


FLS_KERNEL_PARAMS = {
    ('', '', 0): 1,
    ('a', '', 0): 1,
    ('', 'a', 0): 1,
    ('ga', 'ca', 1): 1,
    ('ga', 'cata', 1): 2,
    ('gat', 'cat', 1): 2,
    ('gat', 'cata', 1): 3,
    ('gatt', 'cat', 1): 3,
    ('gatta', 'cata', 0): 1,
    ('gatta', 'cata', 1): 6,
    ('gatta', 'cata', 2): 5,
    ('gatta', 'cata', 3): 2,
}


def test_fixed_length_subsequences_kernel_dp1():
    from subsequence_kernels import fixed_length_subsequences_kernel_dp1
    for params, result in FLS_KERNEL_PARAMS.iteritems():
        assert fixed_length_subsequences_kernel_dp1(*params) == result
        
        
def test_fixed_length_subsequences_kernel_recursive():
    from subsequence_kernels import fixed_length_subsequences_kernel_recursive
    for params, result in FLS_KERNEL_PARAMS.iteritems():
        assert fixed_length_subsequences_kernel_recursive(*params) == result

