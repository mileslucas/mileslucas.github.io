---
title: "Regex for Astronomical Angles"
date: 2021-04-22T00:00:50-05:00
tags: [julia, astro, angles, strings]
draft: false
---

Today I dug a little deeper than I expected into some regex parsing for the [AstroAngles.jl](https://github.com/juliaastro/AstroAngles.jl) package. I wanted to detail the way I approached the problem and the solution I landed on (in hopes that someone will come along and tell me how much better it could have been).

## Sexagisimal and Angles

In astronomy,  we represent the coordinates of things on the sky [using angles](https://en.wikipedia.org/wiki/Celestial_coordinate_system). This is convenient because we can essentially look at the sky as a big sphere with us at the middle and form a [coordinate system](https://en.wikipedia.org/wiki/ECEF#In_astronomy) similar to our latitude and longitude system. You might say, well what happens as the Earth moves, as the other planets move, as stars and galaxies move, etc.? Which is a great point- in astronomy there's an extreme range of magnitudes of distances we study, so while one coordinate system works well for [describing stars in our galaxy](https://en.wikipedia.org/wiki/ECEF#In_astronomy), another one might work better for [describing where Mars is](https://en.wikipedia.org/wiki/Ecliptic_coordinate_system). Nonetheless, the point is all these coordinate systems share something: representing coordinates with angles.

Historically, the angles of choice for the [most widely used coordinate system](https://en.wikipedia.org/wiki/International_Celestial_Reference_System) are [hour angles](https://en.wikipedia.org/wiki/Hour_angle) and degrees, typically displayed in [sexagesimal](https://en.wikipedia.org/wiki/Sexagesimal). For example, the angle 1.024° would be broken down into

> 1 degree, 1 arcminute, and 26.4 arcseconds

which is notated frequently like
> "1:1:26.4"

You can see this kind of notation everywhere, like [Simbad](http://simbad.u-strasbg.fr/simbad/sim-basic?Ident=m41&submit=SIMBAD+search)

> ICRS coord. (ep=J2000) :	06 46 01.0 -20 45 24 (Optical)

or [ExoFOP](https://exofop.ipac.caltech.edu/tess/target.php?id=171089242),

> 19:54:38.65 41:08:16.59

and is used for [target lists when observing](https://www2.keck.hawaii.edu/observing/starlist.html).

As the size and scale of astronomy have increased, being able to automate calculations with these coordinates has become more important. One of the natural steps of doing calculations with the coordinates is translating them from the various string sexagesimal formats to a numerical format in our programming language of choice.

## AstroAngles.jl

One of the first Julia packages I contributed to was [SkyCoords.jl](https://github.com/JuliaAstro/SkyCoords.jl/commit/8e3d6794430d05a1a7ae68f01f8143736df74bc4) since I was trying to use it for some homework problem. Since then, one of the things that I really felt was lacking in terms of the [package's usability](https://github.com/JuliaAstro/SkyCoords.jl/issues/30#issuecomment-734994080) was going to and from the string representations I was using and the radians used by SkyCoords.jl.

A brief slack discussion on the `#astronomy` channel raised the desire for a lightweight package for converting, representing, and parsing sexagesimal angles. Thus, [AstroAngles.jl was born](https://github.com/JuliaAstro/AstroAngles.jl/commit/e221d9b81fc3ceac07f5bfbc0f84bddd4d7167d0).

## Regex 😅

Now for the not so glamorous part: how the hell do we support this

> 19:54:38.65 41:08:16.59

just as easily as

> 1°2′3″ N 19h54′36.65″E

and possibly any combination in-between?

**with [regex](https://en.wikipedia.org/wiki/Regular_expression)**

Now, anybody who has had to learn regex for a programming class knows the usual dread-

<img alt="regex meme" src="/images/pam_regex.jpg" width=400>

(A tool I frequently use to brush up and reference is [RegExr](https://regexr.com))

Before we dig into the technicalities of the [PCRE regex syntax](https://www.debuggex.com/cheatsheet/regex/pcre), let's get an idea of the pseudo-regex we need for parsing our angles.

### Degrees

For degrees, we can have something that roughly looks like
```
"[+-]xx[:d° ]xx[:m'′ ]xx.x[s\"″ ][NS]"
```
where the brackets (`[]`) mean it could be any of the things. So we could have a leading "+" or "-", we could have simple ":" delimiters, spaces, unicode symbols; we could have a cardinal direction "N" or "S", too. These options translate pretty straightforward into regex (here using Julia's PCRE-compliant regex)

```julia
julia> template = r"[+-]xx[:d°\s]xx[:m'′\s]xx.x[s\"″\s][NS]";

julia> occursin(template, "41:08:16.59")
false
```

this doesn't quite work how we want, yet. Mostly because we want to parse numbers, not literal `"xx"` and `"xx.x"`. A convient thing we can do is write a template for a generic decimal number and reuse it.

```julia
# use raw string to avoid escaping '\' backslashes
num = raw"\d+\.?\d*"
# use Regex to allow string interpolation
template = Regex("[+-]$num[:d°\\s]$num[:m'′\\s]$num[s\"″\\s][NS]")
```
```julia
julia> occursin(template, "41:08:16.59")
false
```

okay, what's wrong? Well, let's try another string and see if that provides a hint:

```julia
julia> occursin(template, "+41:08:16.59 N")
true
```

The problem with our regex is that it is too restrictive: for example, the leading "+" or "-" should be optional, but right now it is required to match! We can fix that by appending `"?"` to the groups we want to appear 0 or 1 times.

```julia
julia> template = Regex("[+-]?$num[:d°\\s]?$num[:m'′\\s]?$num[s\"″\\s]?[NS]?");

julia> occursin(template, "41:08:16.59")
true
```

Yay, it works! Unforunately, we can't actually use this for parsing data- merely for string matching. To parse values, we need to use regex capture groups, which use parantheses (`()`)

```julia
julia> template = Regex("([+-]?$num)[:d°\\s]?($num)[:m'′\\s]?($num)[s\"″\\s]?[NS]?");

julia> m = match(template, "-41:08:16.59")
RegexMatch("-41:08:16.59", 1="-41", 2="08", 3="16.59")
```

you can see how I've grouped our string into three values, degrees, arcminutes, and arcseconds. This can now be parse using Julia's build in string parsing

```julia
julia> deg = parse(Float64, m.captures[1]);

julia> min = parse(Float64, m.captures[2]);

julia> sec = parse(Float64, m.captures[3]);

julia> (deg, min, sec)
(-41.0, 8.0, 16.59)
```

This was essentially the state of string-parsing in the `v0.1` release of AstroAngles.jl, with of course regex matching hour-angle formats and additional utilities for converting between tuples like the `(deg, min, sec)` above and decimal radians, degrees, or hour angles.

## Feature parity with astropy

Following up to a [feature request](https://github.com/JuliaAstro/AstroAngles.jl/issues/2#issue-863407759), which I had initially not wanted to entertain, I realized [astropy](https://docs.astropy.org/en/stable/coordinates/angles.html#examples) supported a few more delimiters and parsing options than AstroAngles.jl did. In order to match the feature coverage, I began figuring out how to implement the cardinal directions ("N", "S", "E", "W") and having the minute and second fields be optional (e.g. "12.034d").

### Cardinal directions

To support the cardinal directions, I needed to add an optional capture group, combining two syntaxes used before - `( )?`

```julia
template = Regex("([+-]?$num)[:d°\\s]?($num)[:m'′\\s]?($num)[s\"″\\s]?(N|S)?")
```

there's a slight difference in how to represent *or* in capture groups (`()`) than letter groups (`[]`). In capture groups `(N|S)?` means "literal 'N' *or* literal 'S' either 0 or 1 times". We can see how this affects our capture groups

```julia
julia> match(template, "41:08:16.59")
RegexMatch("41:08:16.59", 1="41", 2="08", 3="16.59", 4=nothing)

julia> match(template, "+41:08:16.59S")
RegexMatch("+41:08:16.59S", 1="+41", 2="08", 3="16.59", 4="S")
```

for our parsing code, all we have to do is check if the direction is "S" and flip the sign on the degrees output (see the AstroAngles.jl source for the parsing implementation details).

### Partial input

Finally, how can we optionally support the minutes and seconds fields? If we just make them optional with `?`, we'll just have to change the parsing code downstream to check for `nothing`

```julia
julia> template = Regex("([+-]?$num)[:d°\\s]?($num)?[:m'′\\s]?($num)?[s\"″\\s]?(N|S)?");

julia> match(template, "10.203d")
RegexMatch("10.203d", 1="10.203", 2=nothing, 3=nothing, 4=nothing)

julia> match(template, "10:45 S")
RegexMatch("10:45 S", 1="10", 2="45", 3=nothing, 4="S")

julia> match(template, "-0::45")
RegexMatch("-0::45", 1="-0", 2=nothing, 3="45", 4=nothing)
```

## Wrapping up

The above regex is essentially what I've landed on for the [implementation in AstroAngles.jl](https://github.com/JuliaAstro/AstroAngles.jl/blob/506fa5ddc9b510bf157d2479687850e9aac44610/src/parsing.jl#L2-L12). If you are an expert on parsing and have advice for the implementation, please open a GitHub issue! I feel pretty good about the current diversity of input formats: if you have a format that is used in astronomy that can't be parsed by AstroAngles.jl, open a GitHub issue! If you find the library useful give it a star. I hope you learned a little about regex, sky coordinates, or angles.