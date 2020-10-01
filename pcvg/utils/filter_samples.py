#filter_samples.py

from .get_stats import get_stats

def filter_samples(data_df, feature_df, samples_to_keep, extract_stats=True):
    """
        Genarates new data and feature DataFrames containg only the listed samples and their features.
        If desired, recalculates the feature statistics

        Parameters:

            data_df: data DataFrame
            feature_df: feature DataFrame
            samples_to_keep: list of sample names that we want to retain
            extract_stats: true if we want to add statistics to the feature DataFrame

        Returns new data and feature DataFrames or the originals if an empty sample list was provided
    """

    # check that the list exist....if there isn't one we have nothing to do
    if not samples_to_keep or len(samples_to_keep) == 0:
        print("Empty list of samples to keep")
        return data_df, feature_df

    # get a copy o the dataframe conating the samples we want
    data_to_use = data_df.loc[samples_to_keep, :].copy()

    # remove any features that are now empty (i.e. were only samples that were dropped)...
    data_to_use = data_to_use.loc[:, data_to_use.any()]

    #...and the corresponding features
    features_to_use = feature_df.loc[data_to_use.columns, :]

    # extract column-wise statistics, i.e. across all samples
    if extract_stats:
        features_to_use = get_stats(features_to_use, data_to_use)

    return data_to_use, features_to_use