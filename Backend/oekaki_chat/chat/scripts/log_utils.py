
def print_info(py_name, *messages):
    print('[Info][{}.py]'.format(py_name), *messages)


def print_info_x(py_name, locals_dict, *targets):
    # locals_dict = locals().items()
    val_dict = {}
    for (symbol, value) in locals_dict:
        for target in targets:
            if id(value) == id(target):
                val_dict[symbol] = target
    print('[Info][{}.py]'.format(py_name), val_dict)
