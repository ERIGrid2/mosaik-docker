import uuid


def create_unique_id( n_digits = 6 ):
    '''
    Create a unique ID.

    :param n_digits: number of digits of the returned ID (int, default: 6)

    :return: unique alphanumeric ID (string)
    '''

    return str( uuid.uuid4() ).replace( '-', '' )[:n_digits]
