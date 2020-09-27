from collections import defaultdict
import pandas as pd

def read_mv_file(path_name, column_to_use_as_index=0, first_data_col=0, code=None, duplicate_sample_action=None):
    """Loads a MarkerView file that was exported with the Table export plug-in (this correctly handes data from multiple experiments)
        
        The table has columns for:
            Sample_Name
            Sample_ID - a combination of the original file and sample name and the peaks file
            MV_Group - the sample group assigned in MarkerView...sometimes refered to as 'Sample Type'
            Data - each column represents a feature and the header encodes the feature values
                    e.g 100.9308_17.84_x1 indicates m/a = 100.9308, RT = 17.84 min, in experiment 1 (the parameters for this experiment are not avilable)
                The header may also include isotopic information determined by MarkerView during the peak finding
                    e.g. 112.0515_1.04_x1_(Monoisotopic) or 113.0539_1.04_x1_(Isotope) - these are the only values available
        
        Parameters:
        
                path_name: path to the file in the format of the local OS)
                column_to_use_as_index: the index number of the column that will be the index of the data DataFrame...for MV this is column 0, the Sample_Name
                first_data_col: the index of the first column containing data; this and subsequent columns are extracted as the data DataFrame and teh others as metaData
                code: a code can be appended to the data; this is necessary when data sets are merged
                duplicate_sample_action: data sets can contain damples with the same nmae, for example QCs that are injected multiple times without changing the name.
                    This can confuse merging and plotting so can be deat with. Oprtions are "AddIndex" (add an index number corresponding to sample position to each name)
                    or "Drop" (remove all duplicate samples)
                    
        Output:
            data: a Pandas Dataframe containing only the data columns and values; index is the sample name
            meta_data: a Pandas DataFrame containg the meta data (input columns before the first data column)
            sample_groups: a dictionary with key=Sample_Group and value = a list of Sample_names in the group
    """

    mv_data = pd.read_csv(path_name, sep='\t')

    data, meta_data = mv_data.copy(), None

    index_column = data.columns[column_to_use_as_index]  # Get name of column to use as index

    # Find out if there are duplicate names...
    # make a dictionary of name:[index] and count how many stored at each key; we also strip any leading or trailing spaces
    
    names = [(x[1].strip (), x[0]) for x in data.itertuples()]   # Sample Name, index (an integer)...strip removes any spaces

    name_dict = defaultdict(list)
    
    for n in names:
        name_dict[n[0]] += [n[1]]  # {name: [row indices]}

    if duplicate_sample_action == 'Drop':

        drop_list= []   # at this point data.index is still just a number, so we make a list of them

        for k in name_dict:
            if len(name_dict[k]) > 1:
                drop_list += name_dict[k]

        if drop_list:
            print ("Dropping duplicate samples")
            data = data.drop(drop_list, axis='index')
            # since we removed some samples, we check for empty columns, since 0 is False
            #data.any() will be True for any columns that have at least one non-zero entry
            data = data.loc[:, data.any()] 

    elif duplicate_sample_action == 'AddIndex':

        for k in name_dict:
            
            if len(name_dict[k]) > 1:
                
                for i, n in enumerate(name_dict[k]):     # loop the (name,index) tuples, make a new name by combining and restore
                    
                    data.iloc[n, column_to_use_as_index] = f"{data.iloc[n, column_to_use_as_index]}#{i:02}"       #format as name + index number as a 2 character string padded with zeros                
    
    #make the name column the DataFrame index
    data.set_index(index_column, inplace=True)

    # If first_data_col is True (i.e. > 0) split the frame in two pieces..the index of each will be the same
    if first_data_col:
        meta_data = data.iloc[:, :first_data_col-1]
        data = data.iloc[:, first_data_col:]

    #if there's a code append it to all feature names
    if code:
        data.columns = ["{}_{}".format(s, code) for s in data.columns]  # append a code to the column names
        
    # Make a dictionary {group name: [samples names]}
    sample_groups = meta_data.groupby('MV_Group').apply(lambda x: x.index.tolist())

    return data, meta_data, sample_groups
