# pylint: disable=import-error

"""
Translating .asm code into object file
"""


from preprocessing import minify_text


if __name__ == '__main__':
    with (
        open('../examples/lib.inc', encoding='utf8') as file,
        open('../examples/lib.inc.min', 'w', encoding='utf8') as output
    ):
        output.write(minify_text(file.read()))
