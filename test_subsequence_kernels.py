from subsequence_kernels import (all_subsequences_kernel,
    all_noncontiguous_subsequences_kernel,
    fixed_length_subsequences_kernel_naive, fixed_length_subsequences_kernel)

def test_all_subsequences_kernel():
    assert all_subsequences_kernel('', '') == 1
    assert all_subsequences_kernel('a', '') == 1
    assert all_subsequences_kernel('', 'a') == 1
    assert all_subsequences_kernel('bar', 'bar') == 8
    assert all_subsequences_kernel('bar', 'car') == 4
    assert all_subsequences_kernel('bar', 'cat') == 2
    assert all_subsequences_kernel('gat', 'cata') == 5
    assert all_subsequences_kernel('gatt', 'cata') == 7
    assert all_subsequences_kernel('gatta', 'cata') == 14

def test_all_noncontiguous_subsequences_kernel():
    assert all_noncontiguous_subsequences_kernel('', '') == 1
    assert all_noncontiguous_subsequences_kernel('a', '') == 1
    assert all_noncontiguous_subsequences_kernel('', 'a') == 1
    assert all_noncontiguous_subsequences_kernel('bar', 'bar') == 8
    assert all_noncontiguous_subsequences_kernel('bar', 'car') == 4
    assert all_noncontiguous_subsequences_kernel('bar', 'cat') == 2
    assert all_noncontiguous_subsequences_kernel('gat', 'cata') == 5
    assert all_noncontiguous_subsequences_kernel('gatt', 'cata') == 7
    assert all_noncontiguous_subsequences_kernel('gatta', 'cata') == 14

def test_fixed_length_subsequences_kernel():
    assert fixed_length_subsequences_kernel('', '', 0) == 1
    assert fixed_length_subsequences_kernel('a', '', 0) == 1
    assert fixed_length_subsequences_kernel('', 'a', 0) == 1
    assert fixed_length_subsequences_kernel('ga', 'ca', 1) == 1
    assert fixed_length_subsequences_kernel('ga', 'cata', 1) == 2
    assert fixed_length_subsequences_kernel('gat', 'cat', 1) == 2
    assert fixed_length_subsequences_kernel('gat', 'cata', 1) == 3
    assert fixed_length_subsequences_kernel('gatt', 'cat', 1) == 3
    assert fixed_length_subsequences_kernel('gatta', 'cata', 0) == 1
    assert fixed_length_subsequences_kernel('gatta', 'cata', 1) == 6
    assert fixed_length_subsequences_kernel('gatta', 'cata', 2) == 5
    assert fixed_length_subsequences_kernel('gatta', 'cata', 3) == 2

def test_fixed_length_subsequences_kernel_naive():
    assert fixed_length_subsequences_kernel_naive('', '', 0) == 1
    assert fixed_length_subsequences_kernel_naive('a', '', 0) == 1
    assert fixed_length_subsequences_kernel_naive('', 'a', 0) == 1
    assert fixed_length_subsequences_kernel_naive('ga', 'ca', 1) == 1
    assert fixed_length_subsequences_kernel_naive('ga', 'cata', 1) == 2
    assert fixed_length_subsequences_kernel_naive('gat', 'cat', 1) == 2
    assert fixed_length_subsequences_kernel_naive('gat', 'cata', 1) == 3
    assert fixed_length_subsequences_kernel_naive('gatt', 'cat', 1) == 3
    assert fixed_length_subsequences_kernel_naive('gatta', 'cata', 0) == 1
    assert fixed_length_subsequences_kernel_naive('gatta', 'cata', 1) == 6
    assert fixed_length_subsequences_kernel_naive('gatta', 'cata', 2) == 5
    assert fixed_length_subsequences_kernel_naive('gatta', 'cata', 3) == 2

