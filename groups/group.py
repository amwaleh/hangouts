from random import shuffle
import os
def create_groups(group_number):
    result = list()
    with open(os.path.abspath('./groups/sample.txt'), 'r') as f:
        names = f.read()
        names_list = names.replace(" ", '').split()

    shuffle(names_list)
    if group_number > 0:
        for item in range(len(names_list)):
            start = item * group_number
            stop = (item + 1) * group_number
            result.append(names_list[start:stop])
            if stop > len(names_list)-1:
                break
        else:
            return ['no names were ']
    return result

if __name__ == '__main__':
    g = create_groups(4)
    for i, item in enumerate(g):
        print(i, item)