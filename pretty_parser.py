from collections import OrderedDict


def decorateString(in_str):

        clear_str = in_str.strip(' \t\n\r')
        if clear_str.startswith("'") or clear_str.startswith('"'):
            clear_str = clear_str.replace("'","").replace('"','')
            clear_str = unicode(clear_str.decode("latin-1"))
        elif "." in clear_str:
            clear_str = float(clear_str)
        else:
            clear_str = int(clear_str)
        return clear_str


def json_decode(string):
    data = string[1: len(string)-1]
    item_type = 'dict'
    result = OrderedDict()

    if string[0] == "[":
        item_type = "array"
        result = []


    currentItem = result
    key = ""
    value = ""
    is_key = True
    nested_stack = []
    skip = False
    str_reader = False
    quote_char = None

    for i,char in enumerate(data):

        if char == "'" and str_reader is False:
            quote_char = "'"
            str_reader = True
        elif char == "'" and str_reader is True and quote_char == "'":
            str_reader = False

        elif char == '"' and str_reader is False:
            quote_char = '"'
            str_reader = True
        elif char == '"' and str_reader is True and quote_char == '"':
            str_reader = False




        if str_reader == True:
            if is_key:
                key+=char
            else:
                value+=char
        else:

            if skip and char == ",":
                skip = False
                continue

            elif char == "[":
                nested_stack.append(currentItem)
                newArr = []
                if type(currentItem) is list:
                    currentItem.append(newArr)
                else:
                    currentItem[key] = newArr
                currentItem = newArr
                is_key = True
                key = ""

            elif char == "]":
                if key.strip(' \t\n\r') != "" and  data[i-1] not in ['}', ']'] :
                    key = decorateString(key)
                    currentItem.append(key)
                skip = True
                key = ""
                is_key = True
                currentItem = nested_stack.pop()



            elif char == "{":

                nested_stack.append(currentItem)
                newDict = OrderedDict()
                if type(currentItem) is list:
                    currentItem.append(newDict)
                else:
                    currentItem[key] = newDict
                currentItem = newDict
                is_key = True
                key = ""

            elif char == "}":

                if data[i-1] != '}' and value.strip(' \t\n\r') != "":
                    value = decorateString(value)
                    currentItem[key] = value
                skip = True
                key = ""
                is_key = True
                currentItem = nested_stack.pop()




            elif char ==",":

                if str(key).strip(' \t\n\r') == "":
                    continue
                is_key = True

                if type(currentItem) is list:
                    currentItem.append(decorateString(key))
                else:
                    value = decorateString(value)
                    currentItem[key] = value
                key = ""

            elif char == ":":

                is_key = False
                value = ""
                key = decorateString(key)
                currentItem[key] = None

            else:
                if is_key:
                    key+=char
                else:
                    value+=char
    return result

