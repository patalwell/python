#!/usr/bin/python
#This is a simple python calculator
import sys

print sys.argv
#from decimal import *

print "Welcome to the Console Calculator; would you like to conduct an operation? (y/n)"
response = raw_input().lower()

#while loop for our entrance into the program
while (response == "y"):
    #Ask what type of operation the user wants to perform and collect reponse: we can also user
    #answer= raw_input("What kind of operation would you like to perform? (+,-,*,/) Enter exit to exit")
    print "What kind of operation would you like to perform? (+,-,*,/) Enter exit to exit"
    answer = raw_input()

#case statements for the various user input and the operation to perform

#addition operation
    if answer == "+":
        #logic to make sure the user is inserting an integer; leveraging ValueError to act as a conditional output
        while True:
            try:
                print ("What is the first integer you'd like to add?")
                x =int(raw_input())
                #the logic you want to parse/validate, in this case we are converting to type int
            except ValueError:
                print("Sorry, You must insert a number!")
                #better try again... Return to the start of the loop
                continue
            else:
                #user input x was successfully parsed!
                #we're ready to exit the loop.
                break
        while True:
            try:
                print ("What is the second integer you'd like to add?")
                y=int(raw_input())
                #the logic you want to parse/validate, in this case we are converting to type int
            except ValueError:
                print("Sorry, You must insert a number!")
                #better try again... Return to the start of the loop
                continue
            else:
                #user input x was successfully parsed!
                #we're ready to exit the loop.
                break

        print ("{} + {} = " .format(x,y) + str (x + y))

#subtraction operation
    elif answer == "-":
        while True:
            try:
                print ("What is the first integer you'd like to subtract?")
                x =int(raw_input())
                #the logic you want to parse/validate, in this case we are converting to type int
            except ValueError:
                print("Sorry, You must insert a number!")
                #better try again... Return to the start of the loop
                continue
            else:
                #user input x was successfully parsed!
                #we're ready to exit the loop.
                break
        while True:
            try:
                print ("What is the second integer you'd like to subtract?")
                y=int(raw_input())
                #the logic you want to parse/validate, in this case we are converting to type int
            except ValueError:
                print("Sorry, You must insert a number!")
                #better try again... Return to the start of the loop
                continue
            else:
                #user input x was successfully parsed!
                #we're ready to exit the loop.
                break
        print ("{} - {} = " .format(x,y) + str (x - y))

#multiplication operation
    elif answer == "*":
        while True:
            try:
                print ("What is the first integer you'd like to multiply?")
                x =float(raw_input())
                #the logic you want to parse/validate, in this case we are converting to type int
            except ValueError:
                print("Sorry, You must insert a number!")
                #better try again... Return to the start of the loop
                continue
            else:
                #user input x was successfully parsed!
                #we're ready to exit the loop.
                break
        while True:
            try:
                print ("What is the second integer you'd like to multiply?")
                y=float(raw_input())
                #the logic you want to parse/validate, in this case we are converting to type int
            except ValueError:
                print("Sorry, You must insert a number!")
                #better try again... Return to the start of the loop
                continue
            else:
                #user input x was successfully parsed!
                #we're ready to exit the loop.
                break
        print ("{} * {} = " .format(x,y) + str (x * y))

#division operation
    elif answer == "/":
        #import demical package to deal with floats?
            while True:
                try:
                    print ("What is the first integer you'd like to divide?")
                    x =float(raw_input())
                    #the logic you want to parse/validate, in this case we are converting to type int
                except ValueError:
                    print("Sorry, You must insert a number!")
                    #better try again... Return to the start of the loop
                    continue
                else:
                    #user input x was successfully parsed!
                    #we're ready to exit the loop.
                    break
            while True:
                try:
                    print ("What is the second integer you'd like to divide?")
                    y=float(raw_input())
                    #the logic you want to parse/validate, in this case we are converting to type int
                except ValueError:
                    print("Sorry, You must insert a number!")
                    #better try again... Return to the start of the loop
                    continue
                else:
                    #user input x was successfully parsed!
                    #we're ready to exit the loop.
                    break

            print ("{} / {} = " .format(x,y) + str (x / y))

#exit command
    elif answer == "exit || Exit":
        print "See you later!"
        break
        SystemExit()

    print ("Would you like to conduct another operation? (y/n)")
    response= raw_input().lower()
print "See you later!"
SystemExit()
