#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Arne Neumann <discoursekernels.programming@arne.cl>

"""Naive implementation of a p-spectrum string kernel."""

def k_suffix_kernel(k, s, t):
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


def p_spectrum_kernel(p, s, t):
    """
    calculates the inner product of the p-spectra of
    the strings s and t.
    
    The p-spectrum of a sequence is defined as the
    histogram of frequencies of all its (contiguous)
    substrings of length p::
    
        \sum\limits^{|s|-p+1}_{i=1} \sum\limits^{|t|-p+1}_{j=1} K^{S}_{p}(s(i:i+p), t(j:j+p))
    
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
            result += k_suffix_kernel(p, s[i:i+p], t[j:j+p])
    return result
