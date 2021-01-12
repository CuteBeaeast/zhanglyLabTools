class code_generator:
    def __init__(self, indent_level=0, indent_str='    '):
        self.__contents = []
        self.indent_level = indent_level
        self.indent_str = indent_str
        pass

    def set_indent_level(self, indent_level):
        '''
        Set the level of indentation

        Keyword Arguments:
        indent_level - The indentation level to be set

        >>> a = code_generator()
        >>> a.set_indent_level(3)
        >>> a.add_line('hello')
        >>> a.__str__()
        '            hello'
        '''
        self.indent_level = indent_level

    def add_indent_level(self):
        '''
        Increase the current indentation level by 1

        >>> a = code_generator()
        >>> a.add_indent_level()
        >>> a.add_line('hello')
        >>> a.__str__()
        '    hello'
        '''
        self.indent_level += 1

    def decrease_indent_level(self):
        '''
        Decrease the current indentation level by 1

        >>> a = code_generator()
        >>> a.add_indent_level()
        >>> a.add_line('hello')
        >>> a.__str__()
        '    hello'
        >>> a.decrease_indent_level()
        >>> a.add_line('hello')
        >>> a.__str__()
        '    hello\\nhello'
        '''
        self.indent_level -= 1

    def add_line(self, new_str):
        '''
        Add a line to the code

        Keyword Arguments:
        new_str - The new string to be appended, without indentation.

        >>> a = code_generator()
        >>> a.add_line('hello')
        >>> a.__str__()
        'hello'
        >>> a.add_indent_level()
        >>> a.add_line('hello again')
        >>> a.__str__()
        'hello\\n    hello again'
        '''
        self.__contents.append(self.indent_str * self.indent_level + new_str)
    
    def add_block(self):
        '''
        Add a code block to the code contents
        The block will be of the same indentation level.

        Return another code generator object
        >>> a = code_generator()
        >>> a.add_line('hello')
        >>> a.__str__()
        'hello'
        >>> b = a.add_block()
        >>> b.add_indent_level()
        >>> b.add_line('hello again')
        >>> a.__str__()
        'hello\\n    hello again'
        '''
        block = code_generator(indent_level=self.indent_level, 
                               indent_str = self.indent_str)
        self.__contents.append(block)

        return block

    def __str__(self):
        return '\n'.join(str(c) for c in self.__contents)

    def replace(self, place_holder, var_to_substitute):
        '''
        Replace all the place_holder in the contents with var_to_substitute
        The method behaves just like string replace method.

        Keyword Arguments:
        place_holder - the string to be replaced
        var_to_substitute - the replacement string
        '''
        new_contents = []
        for content in self.__contents:
            new_contents = content.replace(place_holder, var_to_substitute)
        
        new_generator = code_generator(self.indent_level, indent_str=self.indent_str)
        new_generator.__contents = new_contents

        return new_generator

