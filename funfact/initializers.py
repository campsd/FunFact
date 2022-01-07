#!/usr/bin/env python
# -*- coding: utf-8 -*-
from funfact import active_backend as ab
from funfact.util.iterable import as_tuple


class Zeros:
    '''Initializes all elements to 0.

    Args:
        dtype (None): Numerical type of elements.
    '''
    def __init__(self, dtype=None):
        self.dtype = dtype or ab.float32

    def __call__(self, shape):
        return ab.zeros(shape, self.dtype)


class Ones:
    '''Initializes all elements to 1.

    Args:
        dtype: Numerical type of elements.
    '''
    def __init__(self, dtype=None):
        self.dtype = dtype or ab.float32

    def __call__(self, shape):
        return ab.ones(shape, self.dtype)


class Normal:
    '''Initializes elements using i.i.d. normal distributions.

    Args:
        std: Standard deviation of the distribution.
        truncation:

            - If `True`, clamp values at twice the standard deviation.
            - If `False`, no truncation happens.
            - If number, clamp values at the specified multiple of standard
            deviation

        dtype: numerical type of elements.
    '''
    def __init__(self, std=0.01, truncation=False, dtype=None):
        self.std = std
        self.dtype = dtype or ab.float32
        if truncation is True:
            self.truncation = 2.0 * std
        elif truncation is False:
            self.truncation = 0
        else:
            self.truncation = float(truncation) * std

    def __call__(self, shape):
        n = ab.normal(0.0, self.std, as_tuple(shape), dtype=self.dtype)
        if self.truncation:
            n = ab.maximum(-self.truncation, ab.minimum(self.truncation, n))
        return n


class Uniform:
    '''Initializes elements using the uniform distributions.

    Args:
        scale: Upper bound of the distribution. Lower bound is always 0.
        dtype: numerical type of elements.
    '''
    def __init__(self, scale=0.01, dtype=None):
        self.scale = scale
        self.dtype = dtype or ab.float32

    def __call__(self, shape):
        return self.scale * ab.uniform(
            0, self.scale, as_tuple(shape), dtype=self.dtype
        )


class VarianceScaling:
    '''Initializes with adaptive scale according to the shape.

    Args:
        scale: Scaling factor (positive float).
        distribution: 'truncated' or 'normal' or 'uniform'.

            - If `'normal'`, draw from a zero-mean normal distribution with
            standard deviation `sqrt(scale / n)`, where `n` is the
            dimensionality of `axis`.

            - If `'truncated'`, the absolute values of the samples are
            truncated below 2 standard deviations before truncation.

            - If `'uniform'`, samples are drawn from:
                - a uniform interval, if `dtype` is real
                - a uniform disk, if `dtype` is complex with a mean of zero
                and a standard deviation of `scale`.

        axis: dimension of the given shape.
        dtype: numerical type of elements.
    '''
    def __init__(
        self, scale=0.01, distribution='normal', axis=0, dtype=None
    ):
        self.scale = scale
        self.axis = axis
        self.dtype = dtype or ab.float32
        if distribution == 'normal':
            self.distribution = Normal(
                1.0, truncation=False, dtype=dtype
            )
        elif distribution == 'truncated':
            self.distribution = Normal(
                1.0, truncation=2, dtype=dtype
            )
        elif distribution == 'uniform':
            self.distribution = Uniform(
                1.0, dtype=dtype
            )
        else:
            raise ValueError(f'Invalid distribution: {distribution}.')

    def __call__(self, shape):
        shape = as_tuple(shape)
        std = (self.scale / shape[self.axis])**0.5
        return std * self.distribution(shape)


def stack(initializer, append: bool = True):
    '''Stacks initializers for the purpose of vectorization.

    Args:
        append (bool):
            If True, the last index of shape is considered the vectorizing
            index. If False, the first index of shape tuple is considered
            the vectorizing index.
    '''
    def wrapper(shape):
        nvec = shape[-1] if append else shape[0]
        shape = shape[:-1] if append else shape[1:]
        axis = -1 if append else 0
        return ab.stack([initializer(shape) for i in range(nvec)], axis)
    return wrapper
