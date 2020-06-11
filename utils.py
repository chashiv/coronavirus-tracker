import constants


delta_dict = {}


def get_msg_by_value(case_type, delta):
    """
    Returns the message corresponding to the altered delta
    :param case_type:
    :param delta:
    :return:
    """
    case = case_type.replace("_", ' ').title()
    if delta > 0:
        return "{case} reduced by {value}".format(case=case, value=delta)
    else:
        return "{case} increased by {value}".format(case=case, value=-delta)


def get_index_if_delta_exists(past_list, current_list, case_type):
    """
    Maintains the auxiliary data dictionary for each case type
    :param past_list:
    :param current_list:
    :param case_type:
    :return:
    """
    aux_delta_dict = {}
    for index in range(len(past_list)):
        delta = int(past_list[index]) - int(current_list[index])
        if delta:
            if index+1 in aux_delta_dict:
                aux_delta_dict[index + 1].append(get_msg_by_value(case_type, delta))
            else:
                aux_delta_dict[index + 1] = [get_msg_by_value(case_type, delta)]

    return aux_delta_dict


def get_delta_dict(past_data, current_data):
    """
    Maintains the delta dictionary of the state indices and the messages associated
    with each state
    :param past_data:
    :param current_data:
    :return:
    """
    cases_types = [
        constants.ACTIVE_CASES, constants.CURED_CASES, constants.DEATH_CASES, constants.TOTAL_CONFIRMED_CASES
    ]
    for case_type in cases_types:
        aux_delta_dict = get_index_if_delta_exists(past_data[case_type], current_data[case_type], case_type)
        for key, value in aux_delta_dict.items():
            if key in delta_dict:
                delta_dict[key] += value
            else:
                delta_dict[key] = value
    return delta_dict


def get_column_by_index(reader, index):
    """
    Returns the column value as a list from the reader based on index
    :param reader:
    :param index:
    :return:
    """
    # No of States and UTs = 36 => looping in the range (1,37)
    index_range = range(1, 39) if index == constants.TOTAL_CONFIRMED_CASES_INDEX else range(1, 37)
    return [reader[row_index][index] for row_index in index_range]


def get_data_dict(reader):
    """
    Returns the data dictionary containing list of number of cases of each type
    :param reader:
    :return:
    """
    return {
        constants.ACTIVE_CASES: get_column_by_index(reader, constants.ACTIVE_CASES_INDEX),
        constants.CURED_CASES: get_column_by_index(reader, constants.CURED_CASES_INDEX),
        constants.DEATH_CASES: get_column_by_index(reader, constants.DEATH_INDEX),
        constants.TOTAL_CONFIRMED_CASES: get_column_by_index(reader, constants.TOTAL_CONFIRMED_CASES_INDEX),
    }
