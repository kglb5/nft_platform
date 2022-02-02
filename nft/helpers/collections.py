from collections import defaultdict


def filter_dict(dictionary_to_filter):
    return dict((k, v) for k, v in dictionary_to_filter.items() if v is not None)


def filter_list(list_to_filter):
    return list(_ for _ in list_to_filter if _ is not None)


def merge_dictionaries(dictionary_list):
    return_dict = {}
    for dictionary in dictionary_list:
        if dictionary is None:
            continue
        return_dict.update(dictionary)

    return return_dict


def sort_dict_by_values(dict):
    return sorted(dict, key=lambda k: dict[k])


def zip_lists_to_dicts(params, lists):
    num_params = len(params)
    if len(lists) != num_params:
        return None

    last_length = None
    for l in lists:
        if last_length is None:
            last_length = len(l)
        elif len(l) != last_length:
            return None

    dicts = [{} for _ in range(last_length)]
    for (i, p) in enumerate(params):
        for (j, item) in enumerate(lists[i]):
            dicts[j][p] = item
    return dicts

# This is distinct from itertools group by in that it doesn't care about contiguous objects
def group_by(object_list, key_func):
    grouped_objects = defaultdict(list)
    for object in object_list:
        key = key_func(object)
        grouped_objects[key].append(object)

    return grouped_objects
