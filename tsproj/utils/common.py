"""used to manage the common util functions for the proejct
"""


def request_to_dict(input_request):
    """
    used to convert querydict request data into pure dict object data
    """
    temp_dict = {}
    for key in input_request:
        temp_dict[key] = input_request[key]
    return temp_dict
