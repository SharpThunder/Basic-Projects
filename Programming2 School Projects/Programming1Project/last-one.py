current_balance = 100
reduction = 0
addition = 0
withdrawn = 0
new_balance = 0



print "Welcome to Banking Account Management Tool (v.1.0)", "Please log in by providing your user credentials: "
import math

lst1 = ["1.Check Balance"+"\n"+"2.Transfer Money"+"\n"+"3.Deposit"+ "\n"+"4.Withdraw"+"\n"+"5.Close Account"+"\n"+"6.Update Password"+"\n"+"7.See the Latest Transactions"+"\n"+"8.Admin Menu"+"\n"+"9. Quit"]

lst2 = ["1.Load Customer Account Data from a File"+ "\n"+ "2.Create Account"+"\n"+ "3.Close Account"+"\n"+"4.Search for an account"+"\n"+"5.See the Stats"+"\n"+"6.Go to the Main Menu"+"\n"]


def check_user_input():
    account_info = dict()

    account_info["username"] = "ayse"
    account_info["password"] = "ayse12345"
    account_info["balance"] = current_balance

    account_info["admin"] = "admin"
    account_info["admin password"] = "admin123"
    account_info["recipient"] = " "
    lst_name=["ayse"]


    vals = account_info.values()
    while True:
        username = raw_input("User Name: ")
        password = raw_input("Password: ")
        if username in vals and password in vals:
            print "Welcome ayse! Please choose the following options by entering the corresponding menu number."
        else:
            print "Your user name and/or your password is not correct. Please try again!"
            return check_user_input()
        break

    def ask_user():
        while True:
            x = raw_input("What do you want to do next?, 1. Go to the main menu , 2. Quit:  ")
            if x== "*":
                print show_the_menu(lst1)
                print ask_to_choose()

            if x == "1":

                show_the_menu(lst1)

                ask_to_choose()

            else:

               exit(0)

    def show_the_menu(lst1):
        for i in lst1:
            print i



    def ask_to_choose():
        global current_balance
        global reduction
        global addition
        global withdrawn
        answer = raw_input("Please Make Your Selection: ")
        if answer == "1":
            print "=====Check Balance====="
            print "You have", current_balance , "Tl in your account"

            print ask_user()
            print ask_to_choose()


        elif answer == "2":
            print "=====Transfer Money====="

            recipient = raw_input("Please enter a recipient: ")
            if recipient == "*":
                print show_the_menu(lst1)
                print ask_to_choose()
            transfer = raw_input("Please enter the amount: ")
            if  transfer == "*":
                print show_the_menu(lst1)
                print ask_to_choose()




            print transfer, "TL will be transferred to", recipient, "today."
            approving = raw_input("Do you approve YES/NO? ")

            if approving == "*":
                print show_the_menu(lst1)
                print ask_to_choose()

            if approving == "yes" or "YES":
                current_balance = int(current_balance) - int(transfer)
                print transfer, "TL has been transferred to", recipient, "Your current balance is", str(current_balance), "TL"
                reduction = int(reduction) + int(transfer)
                account_info["recipient"] = recipient

            elif approving == "no" or "NO":
                print "Your transfer request has been canceled."


            print ask_user()
            print ask_to_choose()

        elif answer == "3":
            print "===== Deposit Money====="
            deposite = raw_input("Please enter the amount: ")
            if deposite== "*":
                print show_the_menu(lst1)
                print ask_to_choose()

            current_balance= int(current_balance) + int(deposite)

            addition = int(addition) + int(deposite)



            print deposite, "TL has been deposited to your account. Your current balance is", str(current_balance), "TL."

            print ask_user()
            print ask_to_choose()

        elif answer == "4":
            print "===== Witdraw Money ====="
            withdrawn_money = raw_input("Please enter the amount: ")
            if withdrawn_money == "*":
                print show_the_menu(lst1)
                print ask_to_choose()
            current_balance = int(current_balance) - int(withdrawn_money)

            withdrawn = int(withdrawn) + int(withdrawn_money)

            print withdrawn_money, "TL has been withdrawn from your account. Your current balance is", str(current_balance), "TL."

            print ask_user()
            print ask_to_choose()

        elif answer == "5":
            print "====Close Your Account===="
            if current_balance == 0:
                print "===== Close Your Account ====="
                aproval = raw_input("Do you approve?(yes/no) ")
                if aproval == "*":
                    print show_the_menu(lst1)
                    print ask_to_choose()
                if aproval == "yes" or "Yes":
                    print "Your account has been closed now, and your session has ended.Thanks for being our customer"
                elif aproval == "no" or "No":
                    print "Your account closing request has been canceled."
            else:
                print "Sorry, we cannot close your account at this point, as you still have some balance in your account. You should withdraw this balance before closing your account."

                print ask_user()
                print ask_to_choose()

        elif answer == "6":
            print "==== Update Password ===="
            def change_password():
                password = raw_input("Please enter your current password: ")
                if password == "*":
                    print show_the_menu(lst1)
                    print ask_to_choose()
                new_password = raw_input("Please enter your new password: ")
                if new_password == "*":
                    print show_the_menu(lst1)
                    print ask_to_choose()
                repeat_new_password = raw_input("Please re-enter your new password: ")
                if repeat_new_password == "*":
                    print show_the_menu(lst1)
                    print ask_to_choose()
                if password not in vals:
                    print "Sorry your current password is uncorrect, please try again. "
                    return change_password()
                elif new_password != repeat_new_password:
                    print "Sorry, your new password entries do not match! Please try again!"
                    return change_password()
                elif password in vals and new_password == repeat_new_password:
                    print "Your password has been succesfully updated."
                    account_info["password"] = new_password
                    print ask_user()
            change_password()



        elif answer == "7":
            print "====See the Latest Transactions===="
            print "Here, you may view your latest transactions starting from the most recent one."
            seeing = raw_input("Please enter how many transactions you want to see:")
            if seeing == "*":
                print show_the_menu(lst1)
                print ask_to_choose()
            if seeing == "1":
                print "1.deposit:", addition, "TL", ",", "balance:", current_balance

            elif seeing == "2":
                print "1.deposit:", addition, "TL", ",", "balance:", current_balance
                print "2.withdraw:", withdrawn, ",", "balance:", current_balance

            elif seeing == "3":

                print "1.deposit:", addition, "TL", ",", "balance:", current_balance
                print "2.withdraw:", withdrawn, ",", "balance:", current_balance
                print "3.transfer:", reduction, "TL", ",", "recipient:", account_info["recipient"], ",", "balance", current_balance

            else:
                print "not defined."

            return ask_user()



        elif answer == "8":

            def turn_admin_menu():
                while True:
                    aproval = raw_input("What do you want to do next?, 1. Go to the main menu , 2. Quit:  ")
                    if aproval == "*":
                        print show_the_menu(lst1)
                        print ask_to_choose()
                    if aproval == "1":
                        show_the_menu(lst2)
                        admin_selection()

                    elif aproval == "2":
                        exit(0)

                    else:
                        print "Your entery is not a valid choice. Please try again."
                        print turn_admin_menu()

            print "===== Admin Operations ====="

            def admin_identity():
                global new_balance
                print "Please provide admin credentials: "
                admin_user_name = raw_input("User name: ")
                if admin_user_name == "*":
                    print show_the_menu(lst1)
                    print ask_to_choose()

                admin_password = raw_input("Password: ")
                if admin_password == "*":
                    print show_the_menu(lst1)
                    print ask_to_choose()
                if admin_user_name != account_info["admin"] or admin_password != account_info["admin password"]:
                    print "Your user name or password is wrong, please try again. "
                    return admin_identity()
                elif admin_user_name == account_info["admin"] and admin_password == account_info["admin password"]:

                    def admin_menu(lst2):
                        for i in lst2:
                            print i

                    admin_menu(lst2)

            admin_identity()

            def admin_selection():
                global new_balance
                admin_choice = raw_input("Welcome! Please choose one of the following options by entering the corresponding menu number: ")
                if admin_choice== "*":
                       print show_the_menu(lst1)
                       print ask_to_choose()


                elif admin_choice == "1":
                    print "===== Admin: Load Customer Account Data ====="
                    with open("customer_accounts.txt") as f:
                        for line in f:
                          print line


                    r=turn_admin_menu()


                elif admin_choice == "2":
                    print "===== Admin: Create Account ====="

                    def new_account():
                        global new_balance
                        new_account_holder = raw_input("Please enter account holder name: ")
                        if new_account_holder == "*":
                            print show_the_menu(lst1)
                            print ask_to_choose()
                        new_account_password = raw_input("Please create a password for account holder: ")
                        if new_account_password== "*":
                            print show_the_menu(lst1)
                            print ask_to_choose()
                        opening_balance = raw_input("Opening balance: ")
                        if opening_balance== "*":
                            print show_the_menu(lst1)
                            print ask_to_choose()
                        if new_account_holder in vals:
                            print "This account holder has already exist. Please enter a new account holder name."
                            return new_account()

                        else:
                            print "An account has been created for", new_account_holder, "with starting balance of", opening_balance, "TL."
                            account_info["account holder"] = new_account_holder
                            account_info["account holder password"] = new_account_password
                            account_info["account holder balance"] = opening_balance
                            new_balance = int(new_balance) + int(opening_balance)
                            lst_name.append(new_account_holder)


                            print turn_admin_menu()

                    new_account()

                elif admin_choice == "3":
                    print "===== Admin: Close Account ====="

                    def close_account():
                        account_holder = raw_input("Please enter account holder name: ")
                        if account_holder== "*":
                            print show_the_menu(lst1)
                            print ask_to_choose()
                        if account_holder not in lst_name:
                            print "There is no available account for this account holder. You may try again with another name."
                            return close_account()
                        elif account_holder in lst_name:
                            print "The account for customer", account_holder, "will be closed."
                            approve = raw_input("Do you approve (yes/no?): ")
                            if approve == "*":
                                print show_the_menu(lst1)
                                print ask_to_choose()
                            if approve == "yes":
                                if account_holder in lst_name:
                                    lst_name.remove(account_holder)



                                    print "The account for customer", account_holder, "has been closed."


                            elif approve == "no":
                                print "Your account closing request has been canceled."

                        print turn_admin_menu()

                    close_account()

                elif admin_choice == "4":
                    print "===== Admin: Search for an Account ====="

                    def search_account():
                        global new_balance
                        global current_balance
                        account_holder = raw_input("Please enter account holder name: ")
                        if account_holder == "*":
                            print show_the_menu(lst1)
                            print ask_to_choose()
                        if account_holder not in lst_name:
                            print "There is no available account for this account holder. You may try again with another name. "
                            return search_account()
                        elif account_holder in lst_name:
                              if account_holder == lst_name[0]:
                                   print account_holder
                                   print str(current_balance)
                              else:
                                  print account_holder
                                  print str(new_balance)

                        print turn_admin_menu()

                    search_account()

                elif admin_choice == "5":
                    print "===== Admin: See the Stats ====="

                    print "Total number of accounts: " , len(lst_name)

                    print "Number of accounts with non-zero balance: " , [current_balance, new_balance].count(0)

                    print "Total balance: ", (int(new_balance)+int(current_balance))

                    print "Avarage balance: " , (int(new_balance)+int(current_balance)) / len(lst_name)


                elif admin_choice == "6":
                    show_the_menu(lst1)
                    ask_to_choose()


            admin_selection()

        elif answer == "9":
               exit(0)

        else:
            print answer,"is not a valid entry. Please choose from the above menu "

            return ask_to_choose()













    show_the_menu(lst1)
    ask_to_choose()

check_user_input()