import os
import re
import math
import string
import shutil 
#spamsort(os.getcwd() + '\\' + 'test', 'spamsorted', 'hamsorted', .9, os.getcwd() + '\\' + 'hello.txt')

def spamsort(mail_directory, spam_directory, ham_directory,
             spam_probability, dictionary_filename):
    
    if not os.path.exists(spam_directory):
        os.makedirs(spam_directory)
    else:
        shutil.rmtree(spam_directory)
        os.makedirs(spam_directory)
    if not os.path.exists(ham_directory):
        os.makedirs(ham_directory)
    else:
        shutil.rmtree(ham_directory)
        os.makedirs(ham_directory)
        
    mail_listing = os.listdir(mail_directory)   #get list of files in mail direct
    count = 0
    counth = 0
    dictionary = open(dictionary_filename, 'r') #read from dictionary file
    d = dict()
    for lines in dictionary:        #create dictionary to hold info from dictionary file
        out = lines.split()
        d[out[0]] = [float(out[1]), float(out[2])]
        
    
    for mail in mail_listing:       #for files in directory
        ham = math.log(1-spam_probability)
        spam = math.log(spam_probability)
            
        usedwords = dict()    
        f = open(mail_directory + '\\' + mail) #open file
        skip = False
        for lines in f:                         ##format the words in the file/lines to read the same as in the dictionary builder
            if lines[:5] != 'From:' and skip == False:
                continue
            else:
                skip = True

            lines = str.lower(lines)
            p = re.compile(r'[\W*0-9]')
            thisline = p.split(lines)
            #print thisline
            for word in thisline:
                usedwords[word] = []

                                         #otherwise just look at next word
                
        for key in d:                ##for all the keys in the dictionary...
            if key in usedwords:
                spam += math.log(d[key][0])     ##add to value for prob of being spam
                ham += math.log(d[key][1])      ##add to value for prob of being ham                                 ##if the word was found in the file
            else: 
                spam += math.log(1 - d[key][0])     ##subtract 1 from prob of being found and then add to spam value
                ham += math.log(1 - d[key][1])      ##subtract 1 from prob then add to ham

        f.close()
        #print 'spam: ' + str(spam)
        #print 'ham: ' + str(ham)
        if spam > ham:  ##if spam value is greater than ham value label file as spam
            shutil.move(mail_directory + '\\' + mail, spam_directory)
            count +=1
            
        else:           ##otherwise label as ham
            shutil.move(mail_directory + '\\' + mail, ham_directory)
            counth +=1


    print counth   #print counts for ham files/spam files
    print count
    
    

        
        
        
            


    
