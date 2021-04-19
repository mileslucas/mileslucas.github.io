# Projects

I am a fairly active open-source developer on [GitHub](https://github.com/mileslucas). Most of my projects are related to astronomy in some way and I typically code in [Julia](https://julialang.org) and [Python](https://www.python.org). Below are some projects I feel like highlighting.

## JuliaHCI <a href="https://github.com/JuliaHCI"><i class="fab fa-github"></i></a>

JuliaHCI is a group of Julia packages for high-contrast imaging (HCI). [`ADI.jl`](https://github.com/juliahci/ADI.jl) was inspired by the [vortex imaging pipeline (`VIP`)](https://github.com/vortex-exoplanet/vip) and contains algorithms and metrics used for removing speckles in angular differential imaging (ADI). [`Firefly.jl`](https://github.com/juliahci/Firefly.jl) is still experimental, but will contain statistical models for exoplanets for use with `ADI.jl`

## JuliaAstro <a href="https://juliaastro.github.io"><i class="fas fa-home"></i></a> <a href="https://github.com/JuliaAstro"><i class="fab fa-github"></i></a>

I'm particularly active around JuliaAstro; some notable packages I've worked on or written are

### Photometry.jl <a href="https://github.com/juliaastro/Photometry.jl"><i class="fab fa-github"></i></a>

The main feature of this package is allocation-free aperture photometry. The performance compared to `photutils` is a couple orders of magnitude faster using the unique array represantation of the apertures.

### Transits.jl <a href="https://github.com/juliaastro/Transits.jl"><i class="fab fa-github"></i></a>

`Transits.jl` provides fast and accurate analytical limb-darkened light curves, using the formalism from [Agol et al. 2020](https://ui.adsabs.harvard.edu/abs/2020AJ....159..123A/abstract). The goal of this package is to provide the orbits, light curves, and distributions to fit transiting light-curves with packages like [`Optim.jl`](https://github.com/julianlsolvers/Optim.jl) and [`Turing.jl`](https://github.com/turinglang/Turing.jl). Long-term I have visions for separating out the orbit code into its own package, adding more limb-darkening models, adding some radial-velocity specific distributions and code into its own package, and adding Gaussian process covariance modeling.

### PSFModels.jl <a href="https://github.com/juliaastro/PSFModels.jl"><i class="fab fa-github"></i></a>

`PSFModels.jl` uses a similar design idea as the apertures `Photometry.jl` to provide fast, allocation-free PSF models such as Gaussians and Airy disks. Evaluating a Gaussian PSF is 4 orders of magnitude faster than AstroPy's 2D Gaussian model, which makes fitting PSF models effortless with [`Optim.jl`](https://github.com/julianlsolvers/Optim.jl).

### CCDReduction.jl <a href="https://github.com/juliaastro/CCDReduction.jl"><i class="fab fa-github"></i></a>

`CCDReduction.jl` was developed as part of Google Summer of Code (GSoC) 2020. I helped mentor an undergraduate student in developing this package, which provides convenient utilities and functions for reducing CCD data and was inspired by `ccdproc`.

## NestedSamplers.jl <a href="https://github.com/turinglang/NestedSamplers.jl"><i class="fab fa-github"></i></a>

`NestedSamplers.jl` provides implementations of static nested sampling algorithms. Similar to `dynesty`, it breaks up the nested sampling algorithm into three distinct pieces which work together to perform Bayesian inference. It supports single and multi-ellipsoidal bounding spaces as well as a variety of methods for proposing new points. `NestedSamplers.jl` implements the [`AbstractMCMC.jl`](https://github.com/turinglang/AbstractMCMC.jl) interface, which greatly increases the flexibility and standardizes sampling with `NestedSamplers.jl`.