import os
import string
import re

#builddictionary(os.getcwd() + '\\spam', os.getcwd() + '\\easy_ham', 'hello.txt')



def builddictionary(spam_directory, ham_directory, dictionary_filename):

    if os.path.exists(os.getcwd() + '\\' + dictionary_filename):
        os.remove(os.getcwd() + '\\' + dictionary_filename)     ##sees if file already exists and deletes it if so

    
    d = dict()
    listing_spam = os.listdir(spam_directory) #get directory listing from spam/ham_directory
    listing_ham = os.listdir(ham_directory)
    length_spam = len(listing_spam) #get lengths of directories
    length_ham = len(listing_ham)
    for infile in listing_spam:     #for all spam files
        if infile[:4] == '0000':        #if file starts with 0000 do not read it and remove length count
            length_spam -= 1
            continue
        else:
            d.update(readfile(infile, spam_directory, d, 'spam'))   #otherwise read the file to update the dictionary for spam emails

    for infile in listing_ham:      #for all ham files
        if infile[:4] == '0000':    #if file starts with 0000 do not read it and remove length count
            length_ham -= 1
            continue
        else:
            d.update(readfile(infile, ham_directory, d, 'ham')) #otherwise read the file to update the dictionary for ham emails

    f = open(os.getcwd() + '\\' + dictionary_filename, 'w') #open file to write in
    keys = d.keys()     #get keys of dictionary
    keys.sort()         #sort them to get in 0-9/a-z order
    for key in keys:    #then for each key write it out and then write out the probability taking in account the pseudocount
         f.write(key + ' ') 
         f.write('{:.5f}'.format(float(d[key][0]+.1)/float(length_spam + .2)) + ' ')
         f.write('{:.5f}'.format(float(d[key][1]+.1)/float(length_ham + .2)) + '\n')
         
                  


def readfile(filename, directory, d, soh):      ##reads the file
    f = open(directory+ '\\' + filename, 'r')   ##opens file
    skip = False
    usedwords = []
    for lines in f: ##for lines in file
        if lines[:5] != 'From:' and skip == False:  ##skips first few lines until "From:"
            continue
        else:
            skip = True   
##    take out all punctation including @ , . : etc
        lines = str.lower(lines)    ##makes characters lowercase
        p = re.compile(r'[\W*0-9_]')    ##compiles so to use 0-9, any whitespace, and _ as spliters for lines into words
        thisline = p.split(lines)
        
        for word in thisline:   ##for word in line
            if (word in usedwords) or (len(word) > 45) or (len(word) == 0): #if word already seen or length of 0/<45 do not count it
                continue
            else:
                usedwords.append(word)  ##otherwise add word to usedwords list
                dictstore(d, word, soh) ##and store word in dictionary
    f.close()   #close file
    return d       #return dictionary


def dictstore(d, k, soh):   ##stores word in dictionary
    if (k in d):            #if key already in dictionary
        if soh == 'spam':   ##add 1 to appropiate count(spam/ham) depending on soh
            d[k][0] += 1
        else:
            d[k][1] += 1     
    else:
        if soh == 'spam':   #if word never seen, add word as key in dictionary with count of 1
            d[k] = [1, 0]
        else:
            d[k] = [0, 1]



    
