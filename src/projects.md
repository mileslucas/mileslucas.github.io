# Code Projects

Here are some of my notable projects organized by language. Feel free to check them out!

## Python

### [Starfish](https://github.com/iancze/Starfish)

Starfish is a tool for doing statistical inference on stellar spectra. It utilizes a Bayesian emulator along with special covariance modelling to address deficiencies in standard likelihood estimation with current synthetic spectra libraries.

### [junkin.space](https://gitlab.com/mileslucas/junkin.space/)

This was a small project for an Iowa State hackathon that ended up winning 1st place! It is a small Flask website that visualizes objects in space around Earth using [`plotly`](https://plot.ly).

### [firefly](https://github.com/mileslucas/firefly)

This will be the python alternative to [Firefly.jl](/projects.html#firefly.jl).

## Julia

### [HCIToolbox.jl](https://github.com/mileslucas/HCIToolbox.jl)

This is a project for providing common utilities for the analysis of high-contrast imaging (HCI) data. The goal is to reach good feature parity with vortex-exoplanet/VIP. 

### [Firefly.jl](https://github.com/mileslucas/Firefly.jl)

This is the focus of one of my graduate research projects, which uses a Bayesian joint linear model for characterizing high-contrast imaging (HCI) data for finding exoplanets.

### [Photometry.jl](https://github.com/juliaastro/Photometry.jl)

This is a collaborative effort to create an aperture and PSF photometry package in Julia.

### [NestedSamplers.jl](https://github.com/mileslucas/NestedSamplers.jl)

This is a version of the multi-nest algorithm interfaced with [`AbstractMCMC.jl`](https://github.com/turinglang/AbstractMCMC.jl). Eventually, this will be plugged into the [`Turing.jl`](https://github.com/turinglang/Turing.jl) for using this inference method alongside their modeling framework.

### [Spectra.jl](https://github.com/juliaastro/spectra.jl)

This is a project for creating data structures and transformations for stellar spectra. It is based largely off my work in [Starfish](/projects.html#starfish), but seeks to leverage as many advantages of Julia as possible. One of the big selling points is first-class integration with [`Unitful.jl`](https://github.com/PainterQubits/Unitful.jl).

### [SpectralLibraries.jl](https://github.com/mileslucas/SpectralLibraries.jl)

Another offshoot of my [Starfish](/projects.html#starfish) work, this is an abstraction for interfacing with grids of model atmospheres, such as PHOENIX-ACES, in Julia.

### [SpectralEmulator.jl](https://github.com/mileslucas/SpectralEmulator.jl)

Another offshoot of my [Starfish](/projects.html#starfish) work, this is a project for implementing the Bayesian Spectral Emulator from the Starfish paper, with (hopefully) advancing the optimization capabilities through automatic-differentiation.

