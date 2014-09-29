#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

import numpy
from repoze.lru import lru_cache

"""Naive implementations of subsequence kernels"""


@lru_cache(500)
def all_subsequences_kernel(s, t):
    """
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
    """
    dp = numpy.zeros( (len(s)+1, len(t)+1) )
    for j, _tj in enumerate(t, 1):
        dp[0][j] = 1

    p = numpy.zeros(len(t)+1)
    for i, s_i in enumerate(s, 1):
        last = 0
        p[0] = 0
        for j, t_j in enumerate(t, 1):
            p[j] = p[last]
            if t_j == s_i:
                p[j] = p[last] + dp[i-1][j-1]
                last = j
            dp[i][j] = dp[i-1][j] + p[j]
    return dp[len(s)][len(t)]
