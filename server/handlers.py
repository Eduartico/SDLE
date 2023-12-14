class Handlers:
    @staticmethod
    def handle_merge(list1, list2, function):
        if list1 and list2:
            return function(list1, list2)
        elif list1 or list2:
            return list1 or list2
        else:
            return None
        
    @staticmethod
    def handle_update_or_insert(key, value, merge_function, map):
        map[key] = merge_function(map[key], value) if key in map else value
        return map