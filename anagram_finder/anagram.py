"""
File: anagram.py
Name: Jane
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop


def main():
    """
    This program finds all anagrams of the input word and calculates the speed of the algorithm.
    """
    while True:
        word = input("Welcome to stanCode \"Anagram Generator\" (or -1 to quit)\nFind anagrams for: ").lower()
        if word == EXIT:
            break
        start = time.time()
        result = find_anagrams(word)
        print(f"{len(result)} anagrams: {result}")
        end = time.time()
        print('----------------------------------')
        print(f'The speed of your anagram algorithm: {end-start} seconds.')


def read_dictionary(s):
    """
    :param s: string, the word to find anagrams
    :return: list, the list of words from the dictionary
             that is in same length with s, whose letters are all contained in s, and that has all letters from s
    """
    first_filter_lst = []
    second_filter_lst = []
    # First filter
    with open(FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == len(s):
                has_ch = True
                for ch in s:
                    if ch not in line:
                        has_ch = False
                        break
                if has_ch:
                    first_filter_lst.append(line)
    # Second filter
    for ele in first_filter_lst:
        has_ch = True
        for ch in ele:
            if ch not in s:
                has_ch = False
                break
        if has_ch:
            second_filter_lst.append(ele)
    return second_filter_lst


def find_anagrams(s):
    """
    :param s: string, the word to find anagrams
    :return: list, the found anagrams
    """
    return find_anagrams_helper(s, "", s, [], read_dictionary(s), [1])


def find_anagrams_helper(s, current_s, remaining_s, result_lst, dict_lst, searching):
    """
    :param s: string, the word to find anagrams
    :param current_s: string, the letters taken from remaining_s
    :param remaining_s: string, the letters that are not yet added to current string
    :param result_lst: list, it keeps all the found anagrams
    :param dict_lst: list, the list of words from the dictionary
                     that is in same length with s, and whose letters are all contained in s
    :param searching: list, with a single element, it works as an indicator,
                      showing everytime when a base case is reached,
                      so that we can print "searching" only one time after each base case is reached
    :return: list, the found anagrams
    """
    if has_prefix(current_s, dict_lst):
        if len(current_s) == len(s):
            if current_s in dict_lst and current_s not in result_lst:
                result_lst.append(current_s)
                print(f"Found: {current_s}")
                searching[0] = 1
        else:
            if searching[0] == 1:
                print("Searching...")
                searching[0] = 0
            for i in range(len(remaining_s)):
                # Choose
                current_s += remaining_s[i]
                # Explore
                find_anagrams_helper(s, current_s, remaining_s[0:i] + remaining_s[i + 1:], result_lst,
                                     dict_lst, searching)
                # Un-choose
                current_s = current_s[:-1]
    return result_lst


def has_prefix(sub_s, lst):
    """
    :param sub_s: string, the prefix to check
    :param lst: list, words in the dictionary
    :return: boolean, if any words in the dictionary start with sub_s
    """
    for word in lst:
        if word.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
