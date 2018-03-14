#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 19:39:08 2018

@author: angelhuang
"""

import string
import sys

def load_words(list_file):
    """
    loads file into program 

    """
    
    # inFile: file
    inFile = open(list_file, 'r') #opens the file in read mode
    # wordlist: list of strings
    wordlist = [] #creates an empty list
    for line in inFile: #add every line in the file to the list
        wordlist.append(line.strip().upper()) #ensures all the words are UPPERCASE
    
    return wordlist #returns the list with all the words in the file


def possible_friends(word):
    """
    generate all possible words with a Levenshtein distance of 1 
    
    The only possible words are created by substitution, insertion, and deletion. 
    """
    alphabet = string.ascii_uppercase #generates a list of alphabet in UPPERCASE
    
    list_of_possibilities = [] #starts with an empty list 
    
    for i in range(len(word)):
        for j in alphabet:
            new_word = word[:i] + j + word[i+1:len(word)] #insertion
            new_word_2 = word[:i] + j + word[i:len(word)] #substitution
            new_word_3 = word[:i] + word[i+1:len(word)] #deletion
            list_of_possibilities.append(new_word)
            list_of_possibilities.append(new_word_2)
            list_of_possibilities.append(new_word_3)
            
    for j in alphabet:
        new_word = j + word #insert/substitute in the beggining
        new_word_2 = word[1:len(word)] #remove in the begnning
        list_of_possibilities.append(new_word)
        list_of_possibilities.append(new_word_2)

    for j in alphabet: 
        new_word = word + j #insert/substitute in the end
        new_word_2 = word[len(word)-1] #remove the last letter
        list_of_possibilities.append(new_word)
        list_of_possibilities.append(new_word_2)

            
    return set(list_of_possibilities) #returns a set of possible word 
#sets usually have a smaller runtime than lists because of hashing


def social_network(word, set_friends):
    """
    generates the number of friends/size of social network recurssively 
    
    """
    if word in set_friends: #remove the word itself from the set containing EVERYONE 
        set_friends.remove(word) #this prevents overcounting
    
    friends = set_friends.intersection(possible_friends(word)) #the friends of the word is the intersection between set_friends and generated possible friends
    
    number_of_friends = len(friends) #gives you the size of the word's network 
    
    neighbor_number = 0
    
    if number_of_friends == 0: #base case is when you don't have friend
        return 0
    else:
        for w in friends: #recurssion until base case is reached
            neighbor_number += social_network(w, set_friends)
        
    return number_of_friends + neighbor_number


def run_social_network(d, word):
    sys.setrecursionlimit(1000000) #to up the recurssion limit of the python system
    word_list = load_words(d) #load file "d" into the system
    word_set = set(word_list) #converts list of word to set to lower runtime 
    
    if word == "":
        return "word is empty"
    elif word_set == set():
        return "dictionary is empty"
    elif word not in word_set: 
        return "word not in dictionary"
    else: 
        network_size = 1 + social_network(word, word_set) #adding the 1 because the word itself is its own network 
        return network_size
    
def test_social_network_given():
    d = "very_small_test_dictionary.txt"
    word = "LISTY"
    assert run_social_network(d, word) == 5, "Failed LISTY test case"
    
    d = "dictionary he.txt"
    word = "HE"
    assert run_social_network(d, word) == 7, "Failed HE test case"
    
    print("Given Tests Passed!")

def test_social_network_custom():
    
    #TEST CASE 1: when word isn't in the dictionary
    d = "dictionary he.txt"
    word = "BOY"
    assert run_social_network(d, word) == "word not in dictionary", "Failed WORD != DICTIONARY test case"
    
    #TEST CASE 2: when word is an empty string 
    d = "dictionary he.txt"
    word = ""
    assert run_social_network(d, word) == "word is empty", "Failed EMPTY WORD test case"
    
    # TEST CASE 3: when duplicate words in dictionary
    d = "dictionary duplicate.txt"
    word = "HE"
    assert run_social_network(d, word) == 7, "Failed DUPLICATE test case"
    
    # TEST CASE 4: when dictionary is empty
    d = "empty.txt"
    word = "HE"
    assert run_social_network(d, word) == "dictionary is empty", "Failed EMPTY DICTIONARY test case"
    
    # TEST CASE 5: when cycle is present "HI -> HIS -> HI"
    d = "dictionary cycle.txt"
    word = "HE"
    assert run_social_network(d, word) == 8, "Failed cycle test case"
    
    print("Custom Tests Passed!")
    

if __name__ == "__main__":
#    test_social_network_given() #uncomment if testing the given test cases
#    test_social_network_custom() #uncomment if testing the custom test cases
    
    #comment the following 4 lines out if you want to test the test cases
    d = "dictionary.txt" 
    word = "LISTY"
    result = run_social_network(d, word)
    print(result)
