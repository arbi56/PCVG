#extract_features.py
from .get_stats import get_stats
import pandas as pd

def extract_features(data_df, get_stats=True):
 
    """ Extracts the features froa a pandas DataFrame where the column names encode the features.
        The column names are
        replaced with F0, F1, F2... which also become the index for the feature DataFrame returned.
        Optionally extracts some statistics for the features

        Parameters:

            data_df - the DataFrame to use

        The column names are strings encoding the feature information.

        Returns:

            data_df - the original datafrane with the columns renames as F0, F1, F2...
            features_df - a DataFrame containing the features; each column represents a field of the feature

        For MarkerView, the column name is a string made up of fields separated by underscores and have the following meaning:

            Field 0 = m/z
            Fiels 1 = retention time in minutes

            if the field contains 'x' the rest of the string encodes an experiment number

            if the field contains parentheses, they enclose a MarkerView assigned 'group', either (Monoisotopic) or (Isotope);
            we remove the parentheses and store the first 4 characters

    """

    # We parse the column names and store each one as a dictionary of dictionaries.
    # The outer key is the new feature name (F0, F1...) and the inner keys are the fields of the features.
    # This is converted to a Pandas DataFrame and transposed to get the features in rows

    features = {}   # master dictionary
    new_names = []

    for i, c in enumerate(data_df.columns):

        feature_index = f'F{i}'

        this_feature = {}      #local dictionary for this feature
        parts = c.split('_')   #split the inedx of the item

        this_feature['mz'] = float(parts[0])
        this_feature['rt'] = float(parts[1])

        # loop the remaining parts looking for recognized fields
        for p in parts[2:]:
            if "(" in p:
                this_feature['iso'] = p.strip("()")[:4]
            elif p[1] == 'x':
                this_feature['expt'] = int(p[1:])   # store the chars following the 'x' as an integer

        # store the local feature in the master dictionary with the new feature name as the key...
        features[feature_index] = this_feature

        #...and save the name so we can change the columnn names
        new_names.append(feature_index)

    feature_df = pd.DataFrame(features).transpose()

    # Make sure the experiment number is a n integer
    if 'expt' in feature_df.columns:
        feature_df.expt = feature_df.expt.astype(int)

    feature_df = feature_df.fillna('n/a');
    
    data_df.columns = new_names

    if get_stats:
        feature_df = get_stats(feature_df, data_df)

    return data_df, feature_df
    
