#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

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
