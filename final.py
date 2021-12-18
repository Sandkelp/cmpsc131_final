fread = open("Booklist.txt", "r")  # opens the book
startNumber = 0  # initilizes how many books they started with
currentNumber = 0  # initilizes how many books the library currently has
restrict = False  # sets the default option of being restricted as false
booklist = []  # initializes the booklist array

# the function below reads each line and adds the data into the array
s = fread.readline()
while s != "":
    s = s.rstrip("\n")
    a = s.split("#")
    s = fread.readline()
    if a[2] == "TRUE":
        restrict = True

    startNumber = a[1] #how many copies there are
    
    daysBorrowedFor = 0 #this is the counter for how many dayst the book was borrowed


    
    booklist.append([a[0], int(startNumber), int(startNumber), restrict, daysBorrowedFor])
    # the array looks like ["book name", start_number_of_books, current_number_of_books, restricted_or_not]

fread.close()

# function that reads the library logs
readLibLogs = open("LibraryLog.txt", "r")

borrowArray = []

names = []


for trans in readLibLogs:
    goodVal = trans.rstrip("\n")
    goodVal = trans.split("#")

    # #    ____
    # #   |  _ \
    # #   | |_) |  ___   _ __  _ __  ___ __      __
    # #   |  _ <  / _ \ | '__|| '__|/ _ \\ \ /\ / /
    # #   | |_) || (_) || |   | |  | (_) |\ V  V /
    # #   |____/  \___/ |_|   |_|   \___/  \_/\_/
    # #
    # #
    if goodVal[0] == 'B':
        # see if the person exists already, if not then make a new person array
        k = 0
        personExists = False
        indexOfName = -1
        while k < len(names) and personExists != True:
            if names[k][0] == str(goodVal[2]):
                personExists = True  # if found it sets the condition to true
                indexOfName = k
            k += 1

        # looks for the book in booklist
        indexOfBook = -1
        w = 0
        while w < len(booklist) and indexOfBook == -1:
            if booklist[w][0] == goodVal[3]:
                indexOfBook = w
            w += 1

        dayBorrow = goodVal[1]
        # if the person has already borrowed a book then it adds that they have borrowed one more book
        if personExists:
            names[indexOfName][1] += 1
            names[indexOfName][3].append([goodVal[3], int(dayBorrow), int(goodVal[4])])  # adds the book onto the list of books checked out

        # if they have not borrowed a book yet then it adds them to the name array
        else:
            names.append([goodVal[2], 1, 0, [[goodVal[3], int(dayBorrow), int(goodVal[4])]]])

        booklist[indexOfBook][2] -= 1  #updates booklist to show that a book has been checked out

        #names array [name, numofbooksOut, $fines, [[nameofBook, dayBorrowed, dayssupposed to be borrowed for], [same format as other one]] ]

        
        #names[indexOfName][4]
    #    _____        _
    #   |  __ \      | |
    #   | |__) | ___ | |_  _   _  _ __  _ __
    #   |  _  / / _ \| __|| | | || '__|| '_ \
    #   | | \ \|  __/| |_ | |_| || |   | | | |
    #   |_|  \_\\___| \__| \__,_||_|   |_| |_|
    #
    #
    elif goodVal[0] == 'R':

        # find the book in book list and add it back
        indexOfBook = -1
        w = 0
        while w < len(booklist) and indexOfBook == -1:
            if booklist[w][0] == goodVal[3]:
                indexOfBook = w
            w += 1
        booklist[indexOfBook][2] += 1 #adds book back to the library

        # gets the person
        indexOfName = -1
        k = 0
        while k < len(names):
            if names[k][0] == str(goodVal[2]):
                indexOfName = k
            k += 1

        # get index of book checked out in names array
        booksCheckedOutByPerson = names[indexOfName][3]
        g = 0
        indexOfBookBorrowed = -1
        while g < len(booksCheckedOutByPerson) and indexOfBookBorrowed == -1:
            if goodVal[3] == booksCheckedOutByPerson[g][0]:
                indexOfBookBorrowed = g
            g += 1


        #sees what day they checked it out

        #caclulate the fine

        if booklist[indexOfBook][3]:  # if its restricted it gets a 7 day borrow
            borrowmax = 7
        else:
            borrowmax = 28  # else its just the regular

        dayreturned = int(goodVal[1]) + 1# gets the day returned

        dayborrowed = int(names[indexOfName][3][indexOfBookBorrowed][1]) # gets the day borrowed

        totaldays = dayreturned - dayborrowed

        numberofdaysleft = int(borrowmax) - int(totaldays)

        fines = 0
        if numberofdaysleft < 0:
            fineddays = numberofdaysleft * -1
            if borrowmax == 7:
                fines = fineddays * 5
            else:
                fines = fineddays * 1

        names[indexOfName][2] += fines
        
        #adding the borrowed days to the array

        booklist[indexOfBook][4] += totaldays #adds the number of days borrowed to the counter.



        #add the fine to the person




    # else if add book
    # A#11#Introduction to programming
    #                 _      _     ____                 _
    #       /\       | |    | |   |  _ \               | |
    #      /  \    __| |  __| |   | |_) |  ___    ___  | | __
    #     / /\ \  / _` | / _` |   |  _ <  / _ \  / _ \ | |/ /
    #    / ____ \| (_| || (_| |   | |_) || (_) || (_) ||   <
    #   /_/    \_\\__,_| \__,_|   |____/  \___/  \___/ |_|\_\
    #
    #

    elif goodVal[0] == 'A':
        #find in booklist
        bookExists = False
        w = 0
        while w < len(booklist):
            if booklist[w][0] == goodVal[2].strip('\n'):
                bookExists = True
            w += 1
        # if found then add it up

        if bookExists:
            booklist[w - 1][2] += 1  # adds it to number of books available
            booklist[w - 1][1] += 1  # adds it to number of books that can max be taken out, or the starter amount

        # if not then add the book
        else:
            booklist.append([goodVal[2].strip('\n'), 1, 1, False, 0])
    #    _____                  ______  _
    #   |  __ \                |  ____|(_)
    #   | |__) |__ _  _   _    | |__    _  _ __    ___
    #   |  ___// _` || | | |   |  __|  | || '_ \  / _ \
    #   | |   | (_| || |_| |   | |     | || | | ||  __/
    #   |_|    \__,_| \__, |   |_|     |_||_| |_| \___|
    #                  __/ |
    #                 |___/
    elif goodVal[0] == 'P':
        #find name
        indexOfName = -1
        k = 0
        while k < len(names):
            if names[k][0] == str(goodVal[2]):
                indexOfName = k
            k += 1
        #subtract fine paid
        names[indexOfName][2] -= int(goodVal[3])
readLibLogs.close()

#     ____                     _    _
#    / __ \                   | |  (_)
#   | |  | | _   _   ___  ___ | |_  _   ___   _ __   ___
#   | |  | || | | | / _ \/ __|| __|| | / _ \ | '_ \ / __|
#   | |__| || |_| ||  __/\__ \| |_ | || (_) || | | |\__ \
#    \___\_\ \__,_| \___||___/ \__||_| \___/ |_| |_||___/
#
#

print("option 1: can a student borrow a book")
print("option 2: what are the most popular books in the library, how many days were they borrowed")
option= int(input("Please enter an option: "))
#can a student borrow a book
if option==1:
    nameOfStudent = input("please give a name: ")
    indexOfName = -1
    k = 0
    while k < len(names):
        if names[k][0] == str(goodVal[2]):
            indexOfName = k
        k += 1
    if names[indexOfName][1] >= 3 or names[indexOfName][2] > 0:
        print("no, the student cannot borrow a book")
    else:
        print("yes the student can borrow a book")

# what is the most popular book
elif option==2:
   borrowedDays = [0 for x in booklist]
   i = 0
   currentBook = 0
   while i < len(names):
       for j in range(len(names[i][3])):
           for k in range(len(booklist)):
               if names[i][3][j][0] == booklist[k][0]:
                   currentBook = k
           borrowedDays[currentBook] += names[i][3][j][2]
       i += 1

   i = 0
   popularity = []
   while i < len(borrowedDays):
       popularity.append('The popularity of ' + booklist[i][0] + ': Borrowed for ' + str(borrowedDays[i]) + ' Days')
       i += 1

   i = 0
   n = len(borrowedDays)
   for i in range(n - 1):
       for j in range(0, n - i - 1):
           if borrowedDays[j] < borrowedDays[j + 1]:
               popularity[j], popularity[j + 1] = popularity[j + 1], popularity[j]
               borrowedDays[j], borrowedDays[j + 1] = borrowedDays[j + 1], borrowedDays[j]

   i = 0
   while i < len(borrowedDays):
       print(popularity[i])
       i += 1

# what books have the highest borrow ratio


# make a sorted list of sorted borrow ratios, high first



#who has fines at the end of the day

elif option == 3:

    for name in names: #gets each name array in the main names array

        if name[2] > 0: #checks to see if the person has fines

            print(name[0] + "has $" + str(name[2]) + " in fines.") #if they have a fine it prints their name along with their fine.

