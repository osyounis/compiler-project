"""
Author: Younis, Omar
            
Assignment: CPSC 323 Final Project
Due Date:   12/11/2024

Purpose: This program is used to trace a programming file and checking whether
         it is accepted or reject by the language.
    
"""

from typing import Dict, List, Set, Optional

################################################################################
#                               Classes                                        #
################################################################################
class Language:
    """A class representing a language."""
    def __init__(self,
                 starting_state: str,
                 parsing_table: List[List[Optional[str]]],
                 indexes: Dict[str, int],
                 reserved: Set[str]) -> None:

        self._starting_state = starting_state       # The starting state of the language.
        self._parsing_table = parsing_table         # The language's predictive parsing table.
        self._indexes = indexes                     # The index values for the terminals
                                                    # and non-terminals in the predictive
                                                    # parsing table.
        self._reserved_words = reserved             # Hold the list of reserved words.


    def get_indexes(self) -> Dict[str, int]:
        """Returns the language's reserved words.

        Returns:
            Set[str]: A set of the reserved words.
        """
        return self._indexes


    def get_control_chars(self, non_terminal: str, terminal: str) -> Optional[str]:
        """Gets the value in the predictive parsing table when provided with a
           non-terminal and a terminal character.

        Args:
            non_terminal (str): The non-terminal character
            terminal (str): The terminal character

        Returns:
            Optional[str]: Returns the value from the predictive parsing table
            given a non-terminal and a terminal.
        """
        non_terminal_index = self._indexes[non_terminal]    # Gets the row value
                                                            # for the non-terminal.

        terminal_index = self._indexes[terminal]            # Gets the column value
                                                            #for the terminal.

        return self._parsing_table[non_terminal_index][terminal_index]


    def get_starting_state(self) -> str:
        """Gets the starting state/character of the language.

        Returns:
            str: The starting state/character of the language.
        """
        return self._starting_state



class InputStatement:
    """A class representing a statement to check whether is it accepted or
       rejected by a language."""
    def __init__(self, filename: str) -> None:
        self._accepted = None                       # The status indicating if
                                                    # the statement has been accepted
                                                    # or rejected by a language.

        with open(filename, 'r', encoding='utf-8') as f_obj:
            lines = f_obj.readlines()
        content = [line.strip().split() for line in lines]

        # Puts everything in one list
        content_list = []
        for line in content:
            for character in line:
                content_list.append(character)

        # Storing in class
        self._contents = content_list


    def set_accepted(self, flag: bool) -> None:
        """Sets the flag indicating whether the statement has been accepted or
           rejected by the language.
               
               True -> Accepted
               False -> Rejected

        Args:
            flag (bool): What bool you want to set the flag to. True is that the
            statement is accepted and false means it is rejected by the language.
        """
        self._accepted = flag


    def get_accepted(self) -> bool:
        """Returns the status of the statement indicating whether or not the
        statement has been accepted or rejected by the language tracing it.

        Returns:
            bool: Returns True if the statement is accepted by the language. 
            Returns False if the statement is rejected by the language.
        """
        return self._accepted


    def get_statement(self) -> str:
        """Gets the statement that a language is tracing.

        Returns:
            str: The statement that is being traced.
        """
        return self._contents



class Trace:
    """A class representing a Trace given a statement and a language to determine
    if the statement is accepted or rejected by the language.
    """
    def __init__(self, user_input: InputStatement, language: Language) -> None:
        self._user_input = user_input
        self._language = language
        self._trace_expression()
        self._statement_accepted_or_not()


    def _trace_expression(self) -> None:
        """Runs a trace on the statement being tested by the language to see if
        it is accepted.
        """
        # Index to track which character we are in the statement.
        i = 0
        statement = self._user_input.get_statement()
        tokens = set(self._language.get_indexes().keys())

        # Setting up our stack before we trace with a $ and the starting state of the language.
        stack = ['$', self._language.get_starting_state()]

        control_char = ''       # Holds the control character we have from our stack.
        control_val = ''        # Holds the value we get from our predictive parsing
                                # table given our control character and the
                                # character we are in our statement.

        # We loop through every character in our statement via the character index.
        while i < len(statement):
            token = statement[i]            # The character we are on from the statement.

            if token not in tokens:
                j = 0
                while j < len(token):
                    character = token[j]
                    control_char = stack.pop()      # Pop the top of our stack for our control char.

                    # If our character equals the character we popped from the stack then
                    # we have a match and can move on to the next character in the statement
                    # we are testing.
                    if character == control_char:
                        j += 1
                        continue

                    # If we don't have a match, we use our character and our control char
                    # to find out the value we get from our predictive parsing table and
                    # update our control_val variable to the answer.
                    control_val = self._language.get_control_chars(control_char, character)

                    # Now we check our control_val.
                    match control_val:

                        # If it is None, then we know this statement is rejected by our
                        # language so we can our trace and update our user statement to
                        # indicated that the provided statement was rejected.
                        case "":
                            self._user_input.set_accepted(False)
                            break

                        # If our value is "lambda" then we need to pop from our stack again
                        # and continue to check the next control value that new control
                        # character gives us when combined with the character from the
                        # statement we are on.
                        case "lambda":
                            continue

                        # If none of the above cases are met, then we take whatever the
                        # value of the control_val is and add each character from that
                        # result in reverse order to the stack.
                        case _:
                            for symbol in reversed(control_val.split()):
                                stack.append(symbol)
                i += 1
                continue
            control_char = stack.pop()      # Pop the top of our stack for our control char.

            # If our character equals the character we popped from the stack then
            # we have a match and can move on to the next character in the statement
            # we are testing.
            if token == control_char:
                i += 1
                continue

            # If we don't have a match, we use our character and our control char
            # to find out the value we get from our predictive parsing table and
            # update our control_val variable to the answer.
            control_val = self._language.get_control_chars(control_char, token)

            # Now we check our control_val.
            match control_val:

                # If it is None, then we know this statement is rejected by our
                # language so we can our trace and update our user statement to
                # indicated that the provided statement was rejected.
                case "":
                    self._user_input.set_accepted(False)
                    break

                # If our value is "lambda" then we need to pop from our stack again
                # and continue to check the next control value that new control
                # character gives us when combined with the character from the
                # statement we are on.
                case "lambda":
                    continue

                # If none of the above cases are met, then we take whatever the
                # value of the control_val is and add each character from that
                # result in reverse order to the stack.
                case _:
                    for symbol in reversed(control_val.split()):
                        stack.append(symbol)

        # Once we are out of the while loop, we check to see if the stack is empty or not. If we get
        # to this stage and the stack is empty, it means our trace was successful and the statement
        # is accepted by the language, therefore we update the user_input object's accepted flag to
        # True to show it was accepted by the language. If we get to this point and there are still
        # items in the stack, it means we needed to break out of the loop early because the trace
        # failed and the statement was rejected by the language. So we set the user_input object's
        # accepted flag to False to indicate it was rejected by the language.
        if stack.pop() == '$':
            self._user_input.set_accepted(True)
        else:
            self._user_input.set_accepted(False)


    def _statement_accepted_or_not(self) -> None:
        """Prints out the statement and whether or not it was accepted by the
        language the statement is being tested against.
        """
        if self._user_input.get_accepted() is True:
            print("Ready to compile.")
        else:
            print("ERROR: Cannot compile.")



################################################################################
#                             Main Code Loop                                   #
################################################################################
if __name__ == "__main__":
    # Indexes for the columns and rows for the terminals and non-terminals of
    # the provided language.
    symbol_indexes = {'a': 0, 'P': 0,
                       'b': 1, 'I': 1,
                       'c': 2, 'X': 2,
                       'd': 3, 'B': 3,
                       'l': 4, 'C': 4,
                       'f': 5, 'Z': 5,
                       '0': 6, 'K': 6,
                       '1': 7, 'G': 7,
                       '2': 8, 'V': 8,
                       '3': 9, 'H': 9,
                       '4': 10, 'W': 10,
                       '5': 11, 'J': 11,
                       '6': 12, 'A': 12,
                       '7': 13, 'E': 13,
                       '8': 14, 'Q': 14,
                       '9': 15, 'T': 15,
                       '+': 16, 'R': 16,
                       '-': 17, 'F': 17,
                       '*': 18, 'N': 18,
                       '/': 19, 'Y': 19,
                       ';': 20, 'S': 20,
                       ':': 21, 'D': 21,
                       '(': 22, 'L': 22,
                       ')': 23,
                       ',': 24,
                       '=': 25,
                       '"value=",': 26,
                       'print': 27,
                       'integer': 28,
                       'program': 29,
                       'begin': 30,
                       'end': 31,
                       '$': 32,
                       'var': 32}

    # The Predictive Parsing Table for the provided language.
    table = [
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'program I ; var B begin G end', '', '', '', ''],
        ['L X', 'L X', 'L X', 'L X', 'L X', 'L X', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['L X', 'L X', 'L X', 'L X', 'L X', 'L X', 'D X', 'D X', 'D X', 'D X', 'D X', 'D X', 'D X', 'D X', 'D X', 'D X', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '', 'lambda', 'lambda', 'lambda', '', '', '', '', '', '', '', ''],
        ['C : K ;', 'C : K ;', 'C : K ;', 'C : K ;', 'C : K ;', 'C : K ;', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['I Z', 'I Z', 'I Z', 'I Z', 'I Z', 'I Z', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'lambda', '', '', ', C', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'integer', '', '', '', '', ''],
        ['H V', 'H V', 'H V', 'H V', 'H V', 'H V', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'H V', '', '', '', '', '', ''],
        ['G', 'G', 'G', 'G', 'G', 'G', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'G', '', '', '', 'lambda', '', ''],
        ['A', 'A', 'A', 'A', 'A', 'A', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'W', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'print ( J I ) ;', '', '', '', '', '', ''],
        ['lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '"value=",', '', '', '', '', '', '', ''],
        ['I = E ;', 'I = E ;', 'I = E ;', 'I = E ;', 'I = E ;', 'I = E ;', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', 'T Q', '', '', '', '', 'T Q', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '+ T Q', '- T Q', '', '', 'lambda', '', '', 'lambda', '', '', '', '', '', '', '', '', '', ''],
        ['F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', 'F R', '', '', '', '', 'F R', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'lambda', 'lambda', '* F R', '/ F R', 'lambda', '', '', 'lambda', '', '', '', '', '', '', '', '', '',''],
        ['I', 'I', 'I', 'I', 'I', 'I', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', '', '', '', '', '( E )', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', 'S D Y', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', 'D Y', 'D Y', 'D Y', 'D Y', 'D Y', 'D Y', 'D Y', 'D Y', 'D Y', 'D Y', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '', '', 'lambda', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', 'lambda', '+', '-', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        ['a', 'b', 'c', 'd', 'l', 'f', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'print ( J I ) ;', '', '', '', '', '', '']
    ]

    reserved_words = {'"value=",', 'print', 'integer', 'program', 'begin', 'end', 'var'}

    # Creating the language to use for the trace
    lang = Language('P', table, symbol_indexes, reserved_words)
    file_statement = InputStatement("final24.txt")
    Trace(file_statement, lang)
