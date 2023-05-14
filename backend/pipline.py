
from pedalboard import Pedalboard, Chorus, Reverb
from pedalboard.io import AudioFile

# Make a Pedalboard object, containing multiple audio plugins:


def choose_function(func_dict):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            key = args[0]  # 假設第一個參數為選擇鍵
            if key in func_dict:
                chosen_func = func_dict[key]
                return chosen_func(*args[1:], **kwargs)
            else:
                raise ValueError("Invalid input.")
        return wrapper
    return decorator_func


@choose_function({
    "Chorus": Chorus,
    "Reverb": Reverb
    # 之後有新功能可以再加
})
def effect_handler(effect, input):
    return True


def effect_List_handler(request_json):
    effect_params = []
    for effect_setting in request_json:
        effect_params.append(effect_handler(effect_setting))
    return effect_params


request_json = {}
board = Pedalboard(effect_List_handler(request_json))
