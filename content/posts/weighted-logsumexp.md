---
title: "Developing a Single-Pass Weighted LogSumExp Function"
date: 2021-04-19T00:06:19-05:00
draft: false
---

Recently I've been thinking about the [LogSumExp](https://en.wikipedia.org/wiki/LogSumExp) trick since it is used in the [integration step of nested sampling](https://github.com/joshspeagle/dynesty/blob/9fc19cfeec17ce3d87ba16c962e6ca59cd21d548/py/dynesty/sampler.py#L431-L433). I won't go over too much of the math here, but the reason this trick exists is to greatly increase the numerical stability of the operation 

$$
\log \sum_i \exp x_i
$$

via the identity

$$
a + \log \sum_i \exp\left(x_i - a\right)
$$

## Naive implementations

In [Julia](https://julialang.org) we can implement a naive logsumexp with

```julia
logsumexp_naive(X) = log(sum(exp, X))
```

let's test the numerical accuracy against Julia's `BigFloat` for some very large numbers
```julia
using Random
rng = Random.seed!(55215)
X = 1000 .* rand(rng, 100)

logsumexp_naive(X)

# output
Inf
```
```julia
logsumexp_naive(big.(X))

# output
992.4854574035180795285906086509468594208066712019734540787001118090835360846258
```
Now let's compare that to a version using the shift, which requires 2 passes through the collection `X`, first to find the maximum and again to accumulate the sum
```julia
function logsumexp_twopass(X)
    a = maximum(X)
    return a + log(sum(x -> exp(x - a), X))
end

logsumexp_twopass(X)

# output
992.4854574035181
```

Let's use [`BenchmarkTools.jl`](https://github.com/JuliaCI/BenchmarkTools.jl) to do some timing tests

```julia
using BenchmarkTools
@btime logsumexp_naive($X)

# output
  437.848 ns (0 allocations: 0 bytes)
Inf
```
```julia
@btime logsumexp_twopass($X)

# output
  912.282 ns (0 allocations: 0 bytes)
992.4854574035181
```

we can see the extra pass over the collection almost exactly *doubles* our runtime.

## Single-pass (streaming) implementation

From ["Streaming Log-sum-exp Computation"](http://www.nowozin.net/sebastian/blog/streaming-log-sum-exp-computation.html) by [Sebastion Nowozin](http://www.nowozin.net/sebastian/), we can actually find both the `maximum` and accumulate the sum with a single pass through the collection.

```julia
function logsumexp_onepass(X)
    a = -Inf
    r = zero(eltype(X))
    for x in X
        if x ≤ a
            # standard computation
            r += exp(x - a)
        else
            # if new value is higher than current max
            r *= exp(a - x)
            r += one(x)
            a = x
        end
    end
    return a + log(r)
end
```
```julia
@btime logsumexp_onepass($X)

# output
  632.657 ns (0 allocations: 0 bytes)
992.4854574035181
```

so not *quite* as fast as the naive implementation, but still faster than the two-pass version.

## Extending to weighted sum

The [scipy implementation of logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html) allows performing an extension of the `logsumexp` algorithm with a weighted sum-

$$
\log \sum_i{ w_i \exp x_i}
$$

This is straightforward enough to implement using our single pass algorithm above

```julia
function logsumexp_onepass(X, w)
    a = -Inf
    r = zero(eltype(X))
    for (x, wi) in zip(X, w)
        if x ≤ a
            # standard computation
            r += wi * exp(x - a)
        else
            # if new value is higher than current max
            r *= exp(a - x)
            r += wi
            a = x
        end
    end
    return a + log(r)
end

# when w = 1 it should be equivalent to logsumexp
logsumexp_onepass(X, ones(length(X)))

# output
992.4854574035181
```
```julia
w = rand(rng, length(X))
```
```julia
@btime logsumexp_onepass($X, $w)

# output
  777.162 ns (0 allocations: 0 bytes)
991.6805331462472
```

## What's missing?

While the weighted `logsumexp` function above works for many different types of iterators and arrays, it doesn't support reducing over arbitrary dimensions in a multi-dimensional array-

```julia
function logsumexp_twopass(X, w; dims)
    a = maximum(X; dims=dims)
    r = sum(w .* exp.(X .- a); dims=dims)
    return a .+ log.(r)
end

logsumexp_twopass([X X], [w w]; dims=1)

# output
1×2 Matrix{Float64}:
 991.681  991.681
```

unfortunately, this method is *quite* slow
```julia
@btime logsumexp_twopass($([X X]), $([w w]); dims=1)

# output
  2.969 μs (7 allocations: 2.16 KiB)
1×2 Matrix{Float64}:
 991.681  991.681
```

This is ~3 times slower than the multi-dimensional array implementation of `logsumexp` in [`LogExpFunctions.jl`](https://github.com/juliastats/LogExpFunctions.jl), which does not support weights
```julia
using LogExpFunctions
@btime LogExpFunctions.logsumexp($([X X]); dims=1)

# output
  1.310 μs (2 allocations: 208 bytes)
1×2 Matrix{Float64}:
 992.485  992.485
```

I leave an open challenge to any readers who can get an implementation for a weighted `logsumexp` that matches the quality of the [`logsumexp` implementation in `LogExpFunctions.jl` ](https://github.com/JuliaStats/LogExpFunctions.jl/blob/master/src/logsumexp.jl).
