def flatten_list( lst ):
	'''
    Flatten a list of lists, i.e., transform
        [ [ a1, ..., aN ], [ b1, ..., bN ], ... ]
    into
        [ a1, ..., aN, b1, ..., bN, ... ]
        
    :param lst: list of lists
    :return: flattened list
	'''
	return [item for sublist in lst for item in sublist]