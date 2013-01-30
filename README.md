Spam-Filter
===========

Bayesian Naive Spam Filter (Python)

Crossval.py using a cross validation technique of splitting the sample emails into random sets, selecting 1 set and then checking how well it performed at filtering spam and ham. 

builddictionary.py creates a dictionary given classified spam and ham with the probabilities of them appearing in the spam and ham emails.

spamfilter.py filters the emails given into two folders given if they were classified as spam or ham. It uses a dictionary to get the proabbility that words in an email appear in either spam or ham emails normally. 
