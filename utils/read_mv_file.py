def read_mv_file(path_name, column_to_use_as_index=0, first_data_col=0, code=None, duplicate_sample_action=None):

    mv_data = pd.read_csv(path_name, sep='\t')

    print(mv_data.head())
    data, meta_data = mv_data.copy(), None

    index_column = data.columns[column_to_use_as_index]  # Get name of column to use as index

    # make a list of (name, index) tuples; we also strip any leading or trailing spaces
    names = [(x[1].strip (), x[0]) for x in data.itertuples()]   # Sample Name, index (an integer)...strip removes any spaces

    data.head()
    # Find out if there are duplicate names...
    # make a dictionary of name:[index] and count how many stored at each key
    name_dict = defaultdict(list)
    for n in names:
        name_dict[n[0]] += [n[1]]  # {name: [row indices]}

    if duplicate_sample_action == 'Drop':

        drop_list= []   # at this point data.index is still just a number, so we make a list of them

        for k in name_dict:
            if len(name_dict[k]) > 1:
                drop_list += name_dict[k]

        if len(drop_list) > 0:
            print ("Dropping duplicate samples")
        data = data.drop(drop_list, axis='index')

    elif duplicate_sample_action == 'AddIndex':

        for k in name_dict:
            if len(name_dict[k]) > 1:
                for i, n in enumerate(name_dict[k]):     # loop the (name,index) tuples, make a new name by combining and restore
                    #desc = "{}#{}".format(data.iloc[n, column_to_use_as_index], i)
                    desc = f"{data.iloc[n, column_to_use_as_index]}#{i:02}"       #format index as a 2 character string padded with zeros
                    data.iloc[n, column_to_use_as_index] = desc

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
    