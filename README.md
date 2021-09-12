<!-- LOGO -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/images/banner.jpg?raw=true"/>
</p>

<!-- INTRO -->
## In a nutshell what is this project is all about?

Continuous performance testing is nothing new, but one of the biggest pitfalls of a reliable automated performance test 
is the manual analysis of its results. This manual intervention slows down the pace required to keep up with our ever 
more demanding online world. 

By verifying automatically if there's a significant change in behavior and producing a metric to represent the change 
between your baseline and benchmark we can speed up our testing effort, reduce our time to market and liberate a 
performance engineer to focus on more pressing matters.

This project hopes to bring a helping hand to performance engineers around the globe by providing them with a 
solution that can be embedded in their testing process to reliably perform complicated 
comparison analysis in an automated fashion. 

## Start using the raw format of your performance test results

The calculations behind this project rely heavily on having every single measurement from your performance 
test available. This is commonly known as [raw data](https://en.wikipedia.org/wiki/Raw_data). 

> It could be that you are unfamiliar with this term within the performance testing context and its philosophy within our industry. 
> I would recommend you to read through some of my mentor [Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) excellent Linkedin 
> [articles](https://www.linkedin.com/pulse/performance-testing-act-like-detective-use-raw-data-stijn-schepers/) that cover this topic in great detail.

Why this raw format of your test results is so powerful can be best seen in the graph animation below. 

<!-- Raw Data Vs Averages animation -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/averages-vs-raw-data.gif?raw=true"/>
</p>

The first view that is shown in the animation is the average response time over a time axis. 
In this view, we can see that the response time patterns of the system are relatively stable, 
but once the overlay switches to the raw data scatter plot (Keep in mind that both views are the same test.).
We can see a completely different picture of a system that is not quite as stable as the average 
line graph would have us believe. 

As can be seen in this example is that the aggregation of data hides the actual performance of 
our system under test and gives us a false understanding of whatever is going on.
Because this project is based on this raw data philosophy from [Stijn Schepers](https://www.linkedin.com/in/stijnschepers/) we base our automated analysis, 
not on a single metric like the average or the median, but we look into discovering change throughout the 
entire raw data set, ***that is why using raw data is a prerequisite for being able to use this comparison algorithm 
without it, it makes less sense to use this solution.***.

## How do the calculations used in this algorithm work?

The main goal behind this project is to form a single metric that we can use to interpret the amount of regression 
between our baseline and benchmark with a [heuristic model](https://en.wikipedia.org/wiki/Heuristic) in which we can define what we consider to be too much.

To produce a concise metric we start with generating a [probability distribution](https://en.wikipedia.org/wiki/Probability_distribution) for our baseline and benchmark 
raw test results using [percentiles](https://en.wikipedia.org/wiki/Percentile) ranging from 0 to 95 as a graph 
this distribution will look like this as an exponential curve: 

<!-- ECDF Curve -->
<p align="center">
  <img src="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/blob/master/media/gif/wasserstein_and_kolmogorov_smirnov_simulation.gif?raw=true"/>
</p>

___
<!-- FOOTER -->
<p align="center">
    <a href="https://github.com/JoeyHendricks/automated-performance-test-result-analysis/issues">- Report Bug or Request Feature</a> -
    <a href="https://events.tricentis.com/pac/home">Made for the Performance Advisory Council </a> -
    <a href="https://www.linkedin.com/in/joey-hendricks/">Follow me on Linkedin </a> -
</p>

