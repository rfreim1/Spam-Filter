import os
import builddictionary
import newbuilddictionary
import spamsort
import random
import shutil
import time

#crossval(os.getcwd() + '\\spam', os.getcwd() + '\\hard_ham', 'hello.txt', 10, 'spamsorted', 'hamsorted', .9)

def crossval(spam_directory, ham_directory, dictionary_filename, kfold,
             spam_directory2, ham_directory2, spam_probability):

    if os.path.exists(os.getcwd() + '\\crossspam'):
        shutil.rmtree(os.getcwd() + '\\crossspam')
        shutil.rmtree(os.getcwd() + '\\crossham')
        shutil.rmtree(os.getcwd() + '\\testspam')
        shutil.rmtree(os.getcwd() + '\\testham')
        shutil.rmtree(os.getcwd() + '\\set')
        shutil.rmtree(os.getcwd() + '\\dictham')
        shutil.rmtree(os.getcwd() + '\\dictspam')
        shutil.rmtree(os.getcwd() + '\\test')
        
    os.makedirs(os.getcwd() + '\\crossspam')
    os.makedirs(os.getcwd() + '\\crossham')
    
    os.makedirs(os.getcwd() + '\\testspam')
    os.makedirs(os.getcwd() + '\\testham')
    
    os.makedirs(os.getcwd() + '\\set')

    os.makedirs(os.getcwd() + '\\dictham')
    os.makedirs(os.getcwd() + '\\dictspam')

    os.makedirs(os.getcwd() + '\\test')
    for i in range(kfold):
        os.makedirs(os.getcwd() + '\\set\\setspam' + str(i))
        os.makedirs(os.getcwd() + '\\set\\setham' + str(i))
  
    

    spam_listing = os.listdir(spam_directory)
    ham_listing = os.listdir(ham_directory)
    
    length_spam = len(spam_listing)
    length_ham = len(ham_listing)
    
    for s in spam_listing:
        if s[:4] == '0000':
            length_spam -= 1
            continue
        shutil.copy(spam_directory + '\\'+ s, os.getcwd() + '\\crossspam')
    for h in ham_listing:
        shutil.copy(ham_directory + '\\'+ h, os.getcwd() + '\\crossham')
    
    
    num_spam = length_spam/kfold
    num_ham = length_ham/kfold
    num = (length_spam + length_ham)/kfold
    print num

    f = open(os.getcwd() + '\\' + 'data.txt', 'w')
    
    for i in range(kfold - 1): 
        randrange = random.randrange(1, num_ham*3)
        cspam_listing = os.listdir(os.getcwd() + '\\crossspam')
        cham_listing = os.listdir(os.getcwd() + '\\crossham')
        print 'cspamlength:  ' + str(len(cspam_listing))
        print 'chamlength:  ' + str(len(cham_listing))

        if randrange >= (len(cham_listing)-(kfold-i)):
            randrange = random.randrange(0, (len(cham_listing)/(kfold-i)))
            print len(cham_listing)/(kfold-i)+1
        
        if (num-randrange) >= (len(cspam_listing)-(kfold-i-1)):
            randrange = random.randrange(1, (len(cspam_listing)/(kfold-i-1)))
            print len(cspam_listing)/(kfold-i)+1
            
        
            
        print 'randomrange: ' + str(randrange)    
        samp_s = random.sample(cspam_listing, num - randrange)
        samp_h = random.sample(cham_listing, randrange)
        print len(samp_h)

        for s in samp_s:
            shutil.move(os.getcwd() + '\\crossspam' + '\\'+ s,
                        os.getcwd() + '\\set\\setspam' + str(i))
        for h in samp_h: 
            shutil.move(os.getcwd() + '\\crossham' + '\\' + h,
                        os.getcwd() + '\\set\\setham' + str(i))

        f.write('set' + str(i) + ':   ')   
        if len(os.listdir(os.getcwd() + '\\set\\setspam' + str(i))) > 0:
            f.write(str(len(os.listdir(os.getcwd() + '\\set\\setham'
                             + str(i)))/float(
                                 len(os.listdir(os.getcwd() + '\\set\\setspam' + str(i))))) + '\n')
        else:
            f.write(str(len(os.listdir(os.getcwd() + '\\set\\setham' + str(i)))) + '\n')
    
    cspam_listing = os.listdir(os.getcwd() + '\\crossspam')
    cham_listing = os.listdir(os.getcwd() + '\\crossham')
    print 'cspamlength:  ' + str(len(cspam_listing))
    print 'chamlength:  ' + str(len(cham_listing))
    
    for s in cspam_listing:
        shutil.move(os.getcwd() + '\\crossspam' + '\\'+ s,
                    os.getcwd() + '\\set\\setspam' + str(9))
    for h in cham_listing: 
        shutil.move(os.getcwd() + '\\crossham' + '\\' + h,
                    os.getcwd() + '\\set\\setham' + str(9))
        
    f.write('set' + str(9) + ':   ')    
    if len(os.listdir(os.getcwd() + '\\set\\setspam' + str(9))) > 0:    
        f.write(str(len(os.listdir(os.getcwd() + '\\set\\setham'
                             + str(9)))/float(
                                 len(os.listdir(os.getcwd() + '\\set\\setspam' + str(9))))) + '\n')
    else:
        f.write(str(len(os.listdir(os.getcwd() + '\\set\\setham' + str(9)))) + '\n')

    for i in range(kfold):
        setspam_listing = os.listdir(os.getcwd() + '\\set\\setspam' + str(i))
        setham_listing = os.listdir(os.getcwd() + '\\set\\setham' + str(i))
        for infile in setham_listing:
            shutil.copy(os.getcwd() + '\\set\\setham'  + str(i) + '\\' + infile,
                        os.getcwd() + '\\testham')
        for infile in setspam_listing:
            shutil.copy(os.getcwd() + '\\set\\setspam'  + str(i) + '\\' + infile,
                        os.getcwd() + '\\testspam')

        for k in range(kfold):
            if k == i:
                continue
            else:
                setspam_listing = os.listdir(os.getcwd() + '\\set\\setspam' + str(k))
                setham_listing = os.listdir(os.getcwd() + '\\set\\setham' + str(k))
                for infile in setham_listing:
                    shutil.copy(os.getcwd() + '\\set\\setham'  +
                                str(k) + '\\' + infile, os.getcwd() + '\\dictham')
                for infile in setspam_listing:
                    shutil.copy(os.getcwd() + '\\set\\setspam'  +
                               str(k) + '\\' + infile, os.getcwd() + '\\dictspam')
        print 'building dict'
        print time.ctime(time.clock())
        newbuilddictionary.newbuilddictionary(os.getcwd() + '\\dictspam', os.getcwd() + '\\dictham', dictionary_filename)

        print 'dict built'
        print time.ctime(time.clock())
        f.write('Test file ' + str(i) + ': \n')
        testspam_listing = os.listdir(os.getcwd() + '\\testspam')
        testham_listing = os.listdir(os.getcwd() + '\\testham')
        for s in testspam_listing:
            shutil.copy(os.getcwd() + '\\testspam\\' + s, os.getcwd() + '\\test')
        for h in testham_listing:
            shutil.copy(os.getcwd() + '\\testham\\' + h, os.getcwd() + '\\test')

        f.write('Tested ham ' + str(i) + ': ' + str(len(testham_listing)) + '\n')
        f.write('Tested spam: ' + str(i) + ': ' + str(len(testspam_listing)) + '\n')
        print 'test folders done/starting sort'
        print time.ctime(time.clock())
            
        spamsort.spamsort(os.getcwd() + '\\test', spam_directory2,
                          ham_directory2, spam_probability, os.getcwd() + '\\' + dictionary_filename)

        print 'sort done'
        print time.ctime(time.clock())
        scorr = 0
        hcorr = 0
        sortedspam = os.listdir(os.getcwd() + '\\' + spam_directory2)
        sortedham = os.listdir(os.getcwd() + '\\' + ham_directory2)
        for infile in testspam_listing:
            for spamfile in sortedspam:
                if infile == spamfile:
                    scorr += 1

        for infile in testham_listing:
            for hamfile in sortedham:
                if infile == hamfile:
                    hcorr += 1

        print hcorr
        print scorr
        f.write('spam correct: ' + str(scorr) + '   % = ' + str(float(scorr)/len(testspam_listing)) + '\n')
        f.write('ham correct: ' + str(hcorr) + '   % = ' + str(float(hcorr)/len(testham_listing)) + '\n\n')
        
        shutil.rmtree(os.getcwd() + '\\dictham')
        shutil.rmtree(os.getcwd() + '\\dictspam')
        shutil.rmtree(os.getcwd() + '\\test')
        shutil.rmtree(os.getcwd() + '\\testspam')
        shutil.rmtree(os.getcwd() + '\\testham')

        os.makedirs(os.getcwd() + '\\testspam')
        os.makedirs(os.getcwd() + '\\testham')
        os.makedirs(os.getcwd() + '\\dictham')
        os.makedirs(os.getcwd() + '\\dictspam')

        os.makedirs(os.getcwd() + '\\test')
                
    f.close()
