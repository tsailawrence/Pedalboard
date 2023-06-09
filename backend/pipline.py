
from pedalboard import Pedalboard, Chorus, Reverb, Delay, Distortion, Gain
from pedalboard.io import AudioFile

# Make a Pedalboard object, containing multiple audio plugins:


def choose_function(func_dict):
    def decorator_func(func):
        def wrapper(*args, **kwargs):
            key = args[0]  # 假設第一個參數為選擇鍵
            if key in func_dict:
                chosen_func = func_dict[key]
                if(args[1]['isOn'] == True):
                    return chosen_func(**kwargs)
            else:
                raise ValueError("Invalid input.")
        return wrapper
    return decorator_func


@choose_function({
    "Chorus": Chorus,
    "Reverb": Reverb,
    "Delay": Delay,
    "Distortion": Distortion,
    "Gain": Gain
    # 之後有新功能可以再加
})
def effect_handler(effect, isON, **kwargs):
    return True


def effect_List_handler(request_json):
    effect_params = []
    for effect_setting in request_json:
        (key, value), = effect_setting.items()
        value_effect = value_processer(value[1])
        effect_params.append(effect_handler(key, value[0], **value_effect))
    return effect_params


def value_processer(value):
    return_value = {}
    for key in value.keys():
        return_value.update({key: float(value[key])})
    return return_value


def pedalboard_handler(request_json):
    board = Pedalboard(effect_List_handler(request_json))
    return board


def effect_pipline(request_json, data_directory):

    data_directory_split = data_directory.split('.')
    output_directory = data_directory_split[0] + \
        '_output.' + data_directory_split[1]

    board = pedalboard_handler(request_json)
    # Open an audio file for reading, just like a regular file:
    with AudioFile(data_directory) as f:
        # Open an audio file to write to:
        with AudioFile(output_directory, 'w', f.samplerate, f.num_channels) as o:
            # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:
                chunk = f.read(int(f.samplerate))
                # Run the audio through our pedalboard:
                effected = board(chunk, f.samplerate, reset=False)
                # Write the output to our output file:
                o.write(effected)

    return output_directory
