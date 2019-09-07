import csv
import argparse
import math
import itertools
import random

class User(object):
    firstName = ''
    lastName = ''
    email = ''
    failure = ''
    def __init__(self, firstName, lastName, email, failure, delivered, reported):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.failure = failure
        self.delivered = delivered
        self.reported = reported

def main():
    # In memory objects to use
    users = []
    disqualified = []
    entries = []

    # Include arguments for the csvs to use    
    parser = argparse.ArgumentParser(description = 'Random name picker!')
    parser.add_argument('--phishing', help = 'File name of phishing report.')
    parser.add_argument('--m1', help = 'File name for month 1 of quarter.')
    parser.add_argument('--m2', help = 'File name for month 2')
    parser.add_argument('--m3', help = 'File name for month 3')
    args = parser.parse_args()
    
    # Get all the users as a list
    with open(args.phishing, newline='') as csvfile:
        # This is opening the phishing report - email, first name, last name, and number of failures
        header = True
        report = csv.reader(csvfile, delimiter=',')
        for row in report:
            if header:    #skip first line
                header = False
                continue
            users.append(User(row[2], row[3], row[0], row[18], row[17], row[25]))

    for user in users:
        # Add disqualified users to the disqualified list
        if user.failure != '0':
            disqualified.append(user.email)
    
        # Calculate reported emails, and insert them into the entries list
        reportedEmailPercentage = (int(user.reported) / int(user.delivered)) * 10
        if user.email not in disqualified:
            for _ in itertools.repeat(None, math.ceil(reportedEmailPercentage)):
                entries.append(user.email) 

    # Disqualification list. Whomp whomp.
    print('The following users have been disqualified:\n' + '\n'.join(disqualified))
    
    # Check security awareness reports
    quarter = [args.m1, args.m2, args.m3]
    for months in quarter:
        with open(months, newline='') as csvfile:
            # This is the first month of the quarter's review. 
            header = True
            report = csv.reader(csvfile, delimiter=',')
            for row in report:
                enrolledMonth = row[11][:2]
                completedMonth = row[13][:2]
                if header:    #skip first line
                    header = False
                    continue
                # Check if disqualified
                if row[0] not in disqualified:
                # check month enrolled equal to month completed
                    if enrolledMonth == completedMonth:
                        entries.append(row[0])
    
    # Shuffle the list
    random.shuffle(entries)
    # Pick random number
    something = len(entries)
    print('----------------')
    print('Number of entries: ' + str(something) + '\n')

    # Use random number to access an email from the list
    winnerIndex = random.randint(0,something)
    # Print out the winner
    print("This quarter's winner is:  " + entries[winnerIndex])

if __name__ == '__main__':
    main()

