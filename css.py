import os
import re

from subprocess import call


def compress_css(source, css_variables):
    """ Compress CSS content

    :param source: The source CSS string
    :param css_variables: A CSS variables object to register variable names
    :return: The compressed source
    """

    with open('tmp-in', 'w') as file:
        file.write(source)
        file.close()

    call('npx cleancss -o tmp-out tmp-in', shell=True)
    os.remove('tmp-in')

    with open('tmp-out', 'r') as file:
        contents = file.read()
        file.close()

    os.remove('tmp-out')

    def found(match):
        if match[1] not in css_variables:
            css_variables[match[1]] = '--' + css_variables['namer'].get_name()

        return match[0].replace(match[1], css_variables[match[1]])

    return re.sub(r'[{;(](--[a-zA-Z-]*)[:)]', found, contents)
