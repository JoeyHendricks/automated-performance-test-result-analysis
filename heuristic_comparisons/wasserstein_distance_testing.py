from scipy.stats import wasserstein_distance, ks_2samp
import pandas as pd
import numpy as np


class StatisticalDistanceTest:
    """
    This class is an algorithm that uses the kolmogorov smirnov statistics
    to define how much distance there is between a baseline and a benchmark
    test execution.

    To interpret how much distance is to much for us we use an heuristic
    to make sense of our statistics to make an best effort estimation
    if we tolerate a change or not.

    This is done by letter ranking the kolmogorov smirnov distance statistic
    from the S to F (using the Japanese ranking system), alternatively a score
    from 0 to 100 can also be used or the distance value itself can also be used
    to interpret the results and make a quick decision whether to accept
    the change or refuse it.

    Using this approach to rapidly perform an baseline versus benchmark analysis
    we can fit this method into a CI/CD pipeline to be able to do a accurate
    performance analysis in an automated fashion.

    Keep in mind that this approach leans toward being a heuristic method because
    of the unpredictable nature of performance test results it is difficult
    to create a model that will fit a very wide array of test results.

    The models used in this class can there for be consider as a general guideline
    which can be adjusted to fit your own need.
    """

    # The letter rank that interprets the wasserstein & kolmogorov smirnov distance
    LETTER_RANKS = [

        {"wasserstein_boundary": 0.030, "kolmogorov_smirnov_boundary": 0.080, "rank": "S"},
        {"wasserstein_boundary": 0.060, "kolmogorov_smirnov_boundary": 0.150, "rank": "A"},
        {"wasserstein_boundary": 0.100, "kolmogorov_smirnov_boundary": 0.170, "rank": "B"},
        {"wasserstein_boundary": 0.125, "kolmogorov_smirnov_boundary": 0.220, "rank": "C"},
        {"wasserstein_boundary": 0.150, "kolmogorov_smirnov_boundary": 0.260, "rank": "D"},
        {"wasserstein_boundary": 0.200, "kolmogorov_smirnov_boundary": 0.300, "rank": "E"},
        {"wasserstein_boundary": 0.250, "kolmogorov_smirnov_boundary": 0.340, "rank": "F"},

    ]

    def __init__(self, population_a: list, population_b: list) -> None:
        """
        Will construct the class and calculate all the required statistics.
        After all of the computation have been completed the following information can then
        be extracted from this class:

        :param population_a: An list of floats of the A population (baseline).
        :param population_b: An list of floats of the B population (benchmark).
        """
        self.sample_size = min([len(population_a), len(population_b)])
        self.sample_a = self._calculate_empirical_cumulative_distribution_function(population_a)
        self.sample_b = self._calculate_empirical_cumulative_distribution_function(population_b)
        self.wasserstein_d_value = self._calculate_wasserstein_distance_statistics()
        self.ks_d_value, self.ks_p_value = self._calculate_kolmogorov_smirnov_distance_statistics()
        self.rank = self._letter_rank_distance_statistics()

    @staticmethod
    def normalize_raw_data(raw_data: object) -> list:
        """
        Will normalize a given raw distribution to its maximum.
        :return:
        """
        return (np.array(raw_data) - np.array(raw_data).mean()) / np.array(raw_data).std()

    def _calculate_empirical_cumulative_distribution_function(self, population: list) -> object:
        """
        Will calculate the eCDF to find the empirical distribution of our population.
        It will randomly build a sample based on the smallest population size from there
        this function will then create a dataframe which will contain the measure
        and its probability.

        Further more this function also gives the option to filter out the outliers
        on the extreme ends of our new distribution.
        More info about empirical cumulative distribution functions can be found here:

        https://en.wikipedia.org/wiki/Empirical_distribution_function

        :param population: The provided measurements from one collected population.
        :return: The empirical cumulative distribution function (outliers filtered or not filtered)
        """
        raw_data = np.random.choice(population, self.sample_size)
        normalized_sample = self.normalize_raw_data(raw_data)
        sample = pd.DataFrame(
            {
                'measure': np.sort(normalized_sample),
                'probability': np.arange(len(normalized_sample)) / float(len(normalized_sample)),
            }
        )
        sample = sample[~(sample['probability'] >= 0.96)]
        return sample

    def _calculate_wasserstein_distance_statistics(self) -> float:
        """
        Computes the Wasserstein distance or Kantorovich–Rubinstein metric also known
        as the Earth mover's distance. This metric represents how much effort is needed
        to move the benchmark distribution towards the baseline.

        More information about this metric can be found here:

        https://en.wikipedia.org/wiki/Wasserstein_metric

        :return: Will return the Wasserstein metric as a float from a normalized distribution.
        """
        wasserstein = wasserstein_distance(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        return round(wasserstein, 3)

    def _calculate_kolmogorov_smirnov_distance_statistics(self) -> tuple:
        """
        Will use the kolmogorov smirnov statistical test to calculate the
        distance between two ECDF distributions. The KS test measures how
        significant the change is between the 2 largest points.

        More information about this metric can be found here:

        https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test

        :return: Gives back the KS-test D-value & the P-Value
        """
        kolmogorov_smirnov_distance, kolmogorov_smirnov_probability = ks_2samp(
            self.sample_a["measure"].values,
            self.sample_b["measure"].values
        )
        return round(kolmogorov_smirnov_distance, 3), kolmogorov_smirnov_probability

    def _letter_rank_distance_statistics(self) -> str:
        """
        An heuristic that will estimate a rank of what the amount of change is
        between our distributions. This rank is based on the Japanese letter
        ranking system the letters can be interpreted the following way:


        |  Rank |        Severity       |             Action              |
        |-------|-----------------------|---------------------------------|
        |   S   | Almost None           | Automated release to production |
        |   A   | Very low              | Automated release to production |
        |   B   | Low                   | Pending impact analysis needed  |
        |   C   | Medium                | Halt create minor defect        |
        |   D   | High                  | Halt create medium defect       |
        |   E   | Very High             | Halt create major defect        |
        |   F   | Significant change    | Halt create Priority defect     |
        |-------|-----------------------|---------------------------------|

        Depending on your situation it is fine to also automatically release
        to production when a B rank is produced as the impact is low.
        If you choose to do that I would recommend to also create a defect
        to document the automated release with an low performance risk.

        :return: The letter rank in the form as string ranging from S to F
        """
        for grade in self.LETTER_RANKS:
            ks_critical_grade = grade["kolmogorov_smirnov_boundary"]
            wasserstein_critical_grade = grade["wasserstein_boundary"]
            if self.wasserstein_d_value < wasserstein_critical_grade and self.ks_d_value < ks_critical_grade:
                return grade["rank"]
            else:
                continue
        return "F"