#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

from collections import defaultdict
import numpy
from repoze.lru import lru_cache

"""Naive implementations of subsequence kernels"""


@lru_cache(500)
def all_subsequences_kernel(s, t):
    """
    counts the number of contiguous and non-contiguous subsequences
    that the input strings have in common (incl. the empty string).

    Shawe-Taylor and Cristianini (2004, p. 353f)
    """
    # if s or t are empty strings
    if not s or not t:
        return 1  # each string contains the empty string by definition
    else:
        s_head, s_tail = s[:-1], s[-1]
        result = 0
        for k, _ti in enumerate(t):
            if t[k] == s_tail:
                result += all_subsequences_kernel(s_head, t[:k])
    return all_subsequences_kernel(s_head, t) + result


def all_noncontiguous_subsequences_kernel(s, t):
    """
    counts the number of non-contiguous subsequences
    that the input strings have in common. instead of recursion,
    this implementation uses a dynamic programming matrix
    for all values that can be reused.

    Shawe-Taylor and Cristianini (2004, p. 356)

    TODO: convert to zero-based numbering
    """
    dp = numpy.zeros( (len(s)+1, len(t)+1) )
    for j, _tj in enumerate(t, 1):  # TODO: get rid of loop
        dp[0][j] = 1

    pre = numpy.zeros(len(t)+1)
    for i, s_i in enumerate(s, 1):
        last = 0
        pre[0] = 0
        for j, t_j in enumerate(t, 1):
            pre[j] = pre[last]
            if t_j == s_i:
                pre[j] = pre[last] + dp[i-1][j-1]
                last = j
            dp[i][j] = dp[i-1][j] + pre[j]
    return dp[len(s)][len(t)]


@lru_cache(500)
def fixed_length_subsequences_kernel_naive(s, t, p):
    """
    Shawe-Taylor and Cristianini (2004, p. 358)
    """
    if p == 0:
        return 1
    elif not s or not t:
        if p > 0:
            return 0
    else:
        s_head, s_tail = s[:-1], s[-1]
        result = 0
        for j, t_j in enumerate(t):
            if t_j == s_tail:
                result += fixed_length_subsequences_kernel_naive(s_head, t[:j], p-1)
        return fixed_length_subsequences_kernel_naive(s_head, t, p) + result


def fixed_length_subsequences_kernel(s, t, p, debug=False):
    """
    Shawe-Taylor and Cristianini (2004, p. 359)

    TODO: convert to zero-based numbering
    """
    dp = numpy.ones( (len(s)+1, len(t)+1) )
    pre = numpy.zeros(len(t)+1)

    for l in xrange(1, p+1):
        dp_recursive = dp
        for j, _tj in enumerate(t, 1):  # TODO: get rid of loop
            dp[0][j] = 1
        for i, s_i in enumerate(s[:len(s)-p+l], 1):
            last = 0
            pre[0] = 0
            for j, t_j in enumerate(t, 1):
                pre[j] = pre[last]
                if t_j == s_i:
                    pre[j] = pre[last] + dp_recursive[i-1][j-1]
                dp[i][j] = dp[i-1][j] + pre[j]
    if debug:
        return dp[len(s)][len(t)], dp
    return dp[len(s)][len(t)]


def gap_weighted_subsequences_kernel_recursive(s, t, p, lambda_weight):
    """
    Shawe-Taylor and Cristianini (2004, p. 364f).

    TODO: fix recursion for p
    TODO: add tests
    """
    delta = lambda x, y: 1 if x == y else 0  # identity function
    head = lambda x: x[:-1]
    tail = lambda x: x[-1] if x else ''  # last char or '' if empty

    s_head, s_tail = head(s), tail(s)
    t_head, t_tail = head(t), tail(t)
    if p == 1:
        return delta(s_tail, t_tail) * (lambda_weight ** 2)

    result = 0

    if s_tail == t_tail:
        for i, s_i in enumerate(s, 1):
            for j, t_j in enumerate(t, 1):
                rec = gap_weighted_subsequences_kernel_recursive(s[:i], t[:j], p-1, lambda_weight)
                result += (lambda_weight ** (2 + len(s) - i + len(t) - j)) * rec
    return result


def gap_weighted_subsequences_kernel(s, t, p, lambda_weight):
    """
    Shawe-Taylor and Cristianini (2004, p. 369).

    TODO: add tests
    """
    dps = numpy.zeros( (len(s)+1, len(t)+1) )
    for i, s_i in enumerate(s, 1):
        for j, t_j in enumerate(t, 1):
            if s_i == t_j:
                dps[i][j] = lambda_weight ** 2

    dp = numpy.zeros( (len(s)+1, len(t)+1) )
    kern = defaultdict(int)
    for l in xrange(2, p+1):
        kern[l] = 0
        for i, s_i in enumerate(s, 1):
            for j, t_j in enumerate(t, 1):
                dp[i][j] = dps[i][j] + lambda_weight * dp[i-1][j] \
                            + lambda_weight * dp[i, j-1] \
                            - lambda_weight**2 *  dp[i-1][j-1]
                if s_i == t_j:
                    dps[i][j] = lambda_weight**2 * dp[i-1][j-1]
                    kern[l] += dps[i][j]
    return kern[p]
