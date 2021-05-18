import pathlib
import re


def FCorrect():
    with open("test1.my_lang", "r+") as f:
        try:
            for k, i in enumerate(f):
                if ('=' in i) and not('!' in i) and not('for' in i) and not('while' in i):
                    nums = re.findall('(\d+)', i)
                    path = pathlib.Path('test1.my_lang')
                    result = i.replace(' ', '')
                    if '^' in result:
                        result = result.replace('^', '**')

                    path.write_text(path.read_text().replace(i, i[:i.index(nums[0])] + str(eval(result[2:])) + '\n'))

        except Exception as e:
            print("Exception {}".format(e))