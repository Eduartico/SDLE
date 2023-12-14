def handle_join(list1, list2):
    function=lambda a, b: a.join(b)
    if list1 and list2:
        return function(list1, list2)
    elif list1 or list2:
        return list1 or list2
    else:
        return None
        
def handle_update_or_insert(key, value, merge_function, map):
    map[key] = merge_function(map[key], value) if key in map else value
    return map