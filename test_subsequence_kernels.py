

def test_all_subsequences_kernel_recursive():
    from subsequence_kernels import all_subsequences_kernel_recursive
    assert all_subsequences_kernel_recursive('', '') == 1
    assert all_subsequences_kernel_recursive('a', '') == 1
    assert all_subsequences_kernel_recursive('', 'a') == 1
    assert all_subsequences_kernel_recursive('bar', 'bar') == 8
    assert all_subsequences_kernel_recursive('bar', 'car') == 4
    assert all_subsequences_kernel_recursive('bar', 'cat') == 2
    assert all_subsequences_kernel_recursive('gat', 'cata') == 5
    assert all_subsequences_kernel_recursive('gatt', 'cata') == 7
    assert all_subsequences_kernel_recursive('gatta', 'cata') == 14

def test_all_subsequences_kernel_dp1():
    from subsequence_kernels import all_subsequences_kernel_dp1
    assert all_subsequences_kernel_dp1('', '') == 1
    assert all_subsequences_kernel_dp1('a', '') == 1
    assert all_subsequences_kernel_dp1('', 'a') == 1
    assert all_subsequences_kernel_dp1('bar', 'bar') == 8
    assert all_subsequences_kernel_dp1('bar', 'car') == 4
    assert all_subsequences_kernel_dp1('bar', 'cat') == 2
    assert all_subsequences_kernel_dp1('gat', 'cata') == 5
    assert all_subsequences_kernel_dp1('gatt', 'cata') == 7
    assert all_subsequences_kernel_dp1('gatta', 'cata') == 14

def test_fixed_length_subsequences_kernel_dp1():
    from subsequence_kernels import fixed_length_subsequences_kernel_dp1
    assert fixed_length_subsequences_kernel_dp1('', '', 0) == 1
    assert fixed_length_subsequences_kernel_dp1('a', '', 0) == 1
    assert fixed_length_subsequences_kernel_dp1('', 'a', 0) == 1
    assert fixed_length_subsequences_kernel_dp1('ga', 'ca', 1) == 1
    assert fixed_length_subsequences_kernel_dp1('ga', 'cata', 1) == 2
    assert fixed_length_subsequences_kernel_dp1('gat', 'cat', 1) == 2
    assert fixed_length_subsequences_kernel_dp1('gat', 'cata', 1) == 3
    assert fixed_length_subsequences_kernel_dp1('gatt', 'cat', 1) == 3
    assert fixed_length_subsequences_kernel_dp1('gatta', 'cata', 0) == 1
    assert fixed_length_subsequences_kernel_dp1('gatta', 'cata', 1) == 6
    assert fixed_length_subsequences_kernel_dp1('gatta', 'cata', 2) == 5
    assert fixed_length_subsequences_kernel_dp1('gatta', 'cata', 3) == 2

def test_fixed_length_subsequences_kernel_recursive():
    from subsequence_kernels import fixed_length_subsequences_kernel_recursive
    assert fixed_length_subsequences_kernel_recursive('', '', 0) == 1
    assert fixed_length_subsequences_kernel_recursive('a', '', 0) == 1
    assert fixed_length_subsequences_kernel_recursive('', 'a', 0) == 1
    assert fixed_length_subsequences_kernel_recursive('ga', 'ca', 1) == 1
    assert fixed_length_subsequences_kernel_recursive('ga', 'cata', 1) == 2
    assert fixed_length_subsequences_kernel_recursive('gat', 'cat', 1) == 2
    assert fixed_length_subsequences_kernel_recursive('gat', 'cata', 1) == 3
    assert fixed_length_subsequences_kernel_recursive('gatt', 'cat', 1) == 3
    assert fixed_length_subsequences_kernel_recursive('gatta', 'cata', 0) == 1
    assert fixed_length_subsequences_kernel_recursive('gatta', 'cata', 1) == 6
    assert fixed_length_subsequences_kernel_recursive('gatta', 'cata', 2) == 5
    assert fixed_length_subsequences_kernel_recursive('gatta', 'cata', 3) == 2

