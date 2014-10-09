#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

from repoze.lru import lru_cache

"""Naive implementations of a spectrum (string) kernels."""


@lru_cache(500)
def k_suffix_kernel(s, t, k):
    """
    calculates k-suffix kernel of input strings s and t::

        K_{k}^{S}(s,t)=
        \begin{cases}
        1 \text{ if } s=s_{1}u, t=t_{1}u, \text{ for } u \in \Sigma^{k} & \\
        0 \textrm{ otherwise}
        \end{cases}

        (Shawe-Taylor and Cristianini 2004, p.349)

    Parameters
    ----------
    k : int
        suffix length
    s : str
        input string 1
    t : str
        input string 2

    Returns
    -------
    product : int
        returns 1, iff the strings s and t have the same suffix (of length k).
        otherwise, returns 0.
    """
    assert min(len(s), len(t)) >= k, \
        "strings must be at least as long as the given suffix length k"
    s_suffix = s[-k:] # suffix of length k
    t_suffix = t[-k:]
    return 1 if s_suffix == t_suffix else 0


def p_spectrum_kernel(s, t, p):
    """
    calculates the inner product of the p-spectra of
    the strings s and t.

    The p-spectrum of a sequence is defined as the
    histogram of frequencies of all its (contiguous)
    substrings of length p::

        \sum\limits^{|s|-p+1}_{i=1}
            \sum\limits^{|t|-p+1}_{j=1}
                K^{S}_{p}(s(i:i+p), t(j:j+p))

        (Shawe-Taylor and Cristianini 2004, p.349)

    Paramters
    ---------
    p : int
        length of contiguous substrings to be found
    s : str
        input string 1
    t : str
        input string 2

    Returns
    -------
    product : int
        returns the number of p-length contiguous substrings
        that both input strings have in common
    """
    result = 0
    for i in xrange(len(s)-p+1):
        for j in xrange(len(s)-p+1):
            result += k_suffix_kernel(s[i:i+p], t[j:j+p], p)
    return result


def bruteforce_blended_spectrum_kernel(s, t, p):
    """
    returns the number of contiguous subsequences/substrings
    between strings s and t for all substrings of length <= p.

    Note: this (bruteforce) version does not consider
    gap penalties (i.e. there's no lambda decay).

    Examples
    --------
    >>> bruteforce_blended_spectrum_kernel('a', 'a', 1)
    1
    >>> bruteforce_blended_spectrum_kernel('a', 'b', 1)
    0
    >>> bruteforce_blended_spectrum_kernel('ab', 'ab', 1)
    2
    >>> bruteforce_blended_spectrum_kernel('abccc', 'abc', 2)
    7
    """
    def delta(s, t):
        """identity function."""
        return 1 if s == t else 0

    result = 0
    for h in xrange(p):
        for i in xrange(len(s)-h):
            for j in xrange(len(t)-h):
                result += delta(s[i:i+h+1], t[j:j+h+1])
    return result


@lru_cache(500)
def p_suffix_kernel(s, t, p, lambda_weight):
    """
    evalutates the similarity of of the suffixes of the given
    input strings s and t.
    """
    if p == 0:
        return 0
    # if s and t share a suffix of length p
    if s[-p:] == t[-p:]:
        # evaluate p-suffix kernel recursively on the remaining front
        # parts of the strings (i.e. the 'head' in Prolog terminology or
        # 'car' in Lisp)
        return lambda_weight**2 * (1 + p_suffix_kernel(s[:-p], t[:-p], p-1,
                                                       lambda_weight))
    else:
        return 0


def blended_spectrum_kernel(s, t, p, lambda_weight=1):
    """
    blended version of the p-spectrum kernel,

    which considers all spectra in the range
    1 <= d <= p and weights them according to lamda_weigth^d.
    The calculation works just like the p-spectrum kernel,
    but uses the p-suffix instead of the k-suffix kernel::

        \tilde{K_{p}} =
            \sum\limits^{|s|-p+1}_{i=1}
            \sum\limits^{|t|-p+1}_{j=1}
                \tilde{K}^{S}_{p}(s(i:i+p), t(j:j+p))

        (Shawe-Taylor and Cristianini 2004, p.350f)

    Paramters
    ---------
    s : str
        input string 1
    t : str
        input string 2
    p : int
        length of contiguous substrings to be found
    lambda_weight : int
       weight common suffixes according to their length
    """
    result = 0
    for i in xrange(len(s)-p+1):
        for j in xrange(len(s)-p+1):
            result += p_suffix_kernel(s[i:i+p], t[j:j+p], p, lambda_weight)
    return result
