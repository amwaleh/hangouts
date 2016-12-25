from random import shuffle
import os
from .models import Groups

def read_from_file(max_number_per_group):
    '''
    This reads from a file, should be able to pull from api
    :param max_number_per_group: max number of objects per group
    :return: a list of groups
    '''
    with open(os.path.abspath('./groups/sample.txt'), 'r') as f:
        names = f.read()
        names_list = names.replace(" ", '_').split()
    return create_groups(names_list, max_number_per_group)


def create_groups(names_list, max_number_per_group=2):
    '''
    :param names_list:  the list with names to be grouped
    :param max_number_per_group:  the max number of objects in a group
    :return: returns a new list of groups
    '''
    result = list()
    shuffle(names_list)
    if max_number_per_group > 0:
        for item in range(len(names_list)):
            start = item * max_number_per_group
            stop = (item + 1) * max_number_per_group
            result.append(names_list[start:stop])
            if stop > len(names_list)-1:
                break
        else:
            return ['list was empty ']
    print('len',len(result))
    return result

def save_groups(list_of_groups):
    '''
    :param list_of_groups: a list of the groups that have been created
    :return: last object saved in the database
    '''
    groups = Groups(groups=list_of_groups)
    groups.save()
    return groups


