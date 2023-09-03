from typing import List
import enum


def get_list_enum_values(cls_enum : enum.EnumMeta) -> List:
    return [item.value for item in cls_enum]

def get_list_enum(cls_enum : enum.EnumMeta) -> List:
    return [item for item in cls_enum]


class indicators(enum.Enum):
    log_return_1d = 'log return 1d'
    log_return_5d = 'log return 5d'

class prediction_models(enum.Enum):
    pass

def check_element(element : str, cls_enum : enum.EnumMeta) -> bool:
    list_enum = get_list_enum_values(cls_enum = cls_enum)
    for val in list_enum:
        if val == element:
            return True
    return False

def return_element(element : str, cls_enum : enum.EnumMeta):
    if check_element(element, cls_enum) is False: ## add error
        print('error')
    else:
        list_enum = get_list_enum(cls_enum)
        for val in list_enum:
            if val.value == element:
                return val


