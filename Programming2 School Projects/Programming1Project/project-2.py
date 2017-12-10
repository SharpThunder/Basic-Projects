import math

class Transaction:
    def __init__(self):
        tdict = {'Transfer': '50 TL , Recipient:Ali', 'Deposit': '200 TL'}
        self.tdict = tdict
class User(Transaction):
    def __init__(self):
        Transaction.__init__(self)
        userdict = {'manager':['manager123','admin'],'ayse':['ayse123','regular']}
        self.userdict = userdict
        print "Welcome to Banking Account Management Tool (v.1.0)", "Please log in by providing your user credentials: "
        while True:
            for i,j in userdict.items():
                self.username = str(raw_input("User Name: "))
                self.password = str(raw_input("Password: "))
                if self.username == str(i) and self.password == str(j[0]):
                    print "Welcome " + self.username + " Please choose the following options by entering the corresponding menu number."
                    break
                else:
                    print "Your user name and/or your password is not correct. Please try again!"


class Account(User):
    def __init__(self):
        User.__init__(self)
        accountsdict = {'ayse':[500,[]]} #{'user':['amount',['Transaction']]}
        self.accountsdict = accountsdict
    def depositfun(self):
        self.deposit = raw_input("Please enter the amount: ")
        if self.deposit == '*':
            #TODO: Call print main menu also get choose
            pass

        self.accountsdict[self.username][0] += int(self.deposit)
        print self.deposit + " TL has been deposited to your account. Your current balance is " + str(self.accountsdict[self.username][0]) + "TL."
        self.tdict = {}
        self.tdict['Deposit '] = self.deposit + ' TL'
        for x, y in self.tdict.items():
            b = str(x) + str(y)
            self.accountsdict[self.username][1].append(b)

        #TODO: Vıew maın menu and sıgnout
    def withdrawfun(self):
        self.withdraw = raw_input("Please enter the amount: ")
        if self.withdraw == '*':
            # TODO: Call print main menu also get choose
            pass

        self.accountsdict[self.username][0] -= int(self.withdraw)
        print self.withdraw + " TL has been deposited to your account. Your current balance is " + str(self.accountsdict[self.username][0]) + "TL."
        self.tdict = {}
        self.tdict['Withdraw '] = self.withdraw + ' TL'
        for x, y in self.tdict.items():
            b = str(x) + str(y)
            self.accountsdict[self.username][1].append(b)
        # TODO: Vıew maın menu and sıgnout
    def transferfun(self):

        self.recipient = raw_input("Please enter a recipient: ")
        if self.recipient == "*":
            pass

        self.transfer = raw_input("Please enter the amount: ")
        if self.transfer == "*":
            pass
        print self.transfer + " TL will be transferred to " + self.recipient + " today."

        self.approving = raw_input("Do you approve YES/NO? ")

        if self.approving == "*":
            pass

        if self.approving.lower() == "yes":

            self.accountsdict[self.username][0] -= int(self.transfer)
            self.accountsdict[self.recipient][0] += int(self.transfer)

            print self.transfer + " TL has been transferred to " + self.recipient + " Your current balance is", str(self.accountsdict[self.username][0]), "TL"
            self.tdict = {}
            self.tdict['Transfer '] = self.transfer + ' TL , '+'Recipient:'+self.recipient
            for x, y in self.tdict.items():
                b = str(x) + str(y)
                self.accountsdict[self.username][1].append(b)
            # TODO: Call print main menu also get choose

        elif self.approving.lower() == "no":
            print "Your transfer request has been canceled."
        else:
            print "Error"
            # TODO: Vıew maın menu and sıgnout

    def get_latestN_transactions(self):
        a= 0
        self.times = int(raw_input("Please enter a number: "))
        for x in self.accountsdict[self.username][1]:
            if a != self.times:
                a +=1
                print str(a)+'.'+ str(x)
            else:
                break
class Bank(Account):
    def __init__(self):
        Account.__init__(self)

    def create_account(self):
            self.new_account_holder = raw_input("Please enter account holder name: ")
            if self.new_account_holder == "*":
                pass
                #Main Menu and choosing
            self.new_account_password = raw_input("Please create a password for account holder: ")
            if self.new_account_password == "*":
                pass
                #MAin Menu and choosing
            self.opening_balance = raw_input("Opening balance: ")
            if self.opening_balance == "*":
                pass
                # Main Menu and choosing
            if self.new_account_holder in self.accountsdict:
                print "This account holder has already exist. Please enter a new account holder name."
                Bank.create_account()

            else:

                self.userdict[self.new_account_holder] = [self.new_account_password,'regular']
                self.accountsdict[self.new_account_holder] = [self.opening_balance,[]]
                print "An account has been created for " + self.new_account_holder + " with starting balance of " + self.opening_balance + " TL."

            # Return Admin menu and signout and selection

    def close_account(self):
            self.deletedaccount = raw_input("Please enter account holder name: ")
            if self.userdict[self.username][1] == 'admin':
                if self.deletedaccount == "*":
                    pass # mainmenu
                if self.deletedaccount not in self.userdict.keys():
                    print "There is no available account for this account holder. You may try again with another name."
                    Bank.close_account()
                elif self.deletedaccount in self.userdict.keys():
                    print "The account for customer", self.deletedaccount, "will be closed."
                    self.approve = raw_input("Do you approve (yes/no?): ")
                    if self.approve == "*":
                        pass  # mainmenu
                    if self.approve.lower() == "yes":
                        del self.userdict[self.deletedaccount]
                        del self.accountsdict[self.deletedaccount]
                        print "The account for customer", self.deletedaccount, "has been closed."


                    elif self.approve.lower() == "no":
                        print "Your account closing request has been canceled."

                #admin menu signout
            elif self.userdict[self.username][1] == 'regular':
                print "====Close Your Account===="
                if self.accountsdict[self.username][0] == 0:
                    self.aproval = raw_input("Do you approve?(yes/no) ")
                    if self.aproval == "*":
                        pass
                    if self.aproval.lower() == "yes":
                        del self.userdict[self.username]
                        del self.accountsdict[self.username]
                        print "Your account has been closed now, and your session has ended.Thanks for being our customer"
                    elif self.aproval.lower == "no":
                        print "Your account closing request has been canceled."
                #Signout
                else:
                    print "Sorry, we cannot close your account at this point, as you still have some balance in your account. You should withdraw this balance before closing your account."
                #Menus

    def compute_and_print_statistics(self):

        print "===== Admin: See the Stats ====="

        print "Total number of accounts: ", len(self.userdict.keys())-1

        print "Number of accounts with non-zero balance: ", self.accountsdict.values()[0].count(0)

        self.totalbalance = 0
        for i in self.accountsdict.values()[0]:
            self.totalbalance+= int(i)
        print "Total balance: ", self.totalbalance

        print "Avarage balance: ", self.totalbalance / len(self.userdict.keys())-1

    def load_accounts_from_file(self):
        print "===== Admin: Load Customer Account Data ====="
        with open("customer_accounts.txt") as f:
            for line in f:
                print line
    def search_for_an_account(self):
        print "===== Admin: Search for an Account ====="
        self.searchedaccount = raw_input("Please enter account holder name: ")
        if self.searchedaccount == "*":
            pass
        if self.searchedaccount not in self.userdict.keys():
            print "There is no available account for this account holder. You may try again with another name. "
            Bank.search_for_an_account()
        elif self.searchedaccount in self.userdict.keys():
            print 'Account Holder: '+ self.searchedaccount
            print 'Current Balance: '+ str(self.accountsdict[self.searchedaccount][1])
class MenuEntry(Bank):
    def __init__(self):
        Bank.__init__(self)
        optionsmenu={1:'Check Balance',2:'Transfer Money',3:'Deposit',4:'Withdraw',5:'Close Account',6:'Update Password',7:'See the Latest Transactions',8:'Admin Menu',9:'Quit'}
        adminmenu={1:'Load Customer Account Data from a File',2:'Create Account',3:'Close Account',4:'Search for an account',5:'See the Stats',6:'Go to the Main Menu'}
        smallmenu = {1: 'Go to the main menu ', 2:'Quit'}
        smalladminmenu= {1: 'Go to the admin menu ', 2:'Quit'}
        self.smallmenu = smallmenu
        self.smalladminmenu= smalladminmenu
        self.optionsmenu=optionsmenu
        self.adminmenu = adminmenu
class Menu(MenuEntry):
    def __init__(self):
        MenuEntry.__init__(self)
        Menu.print_menu_and_get_user_selection(self)
        input = raw_input('Please Make Your Selection: ')
        self.input= input
        self.adminmenufun()
    def add_menu_entry(self):
        if self.userdict[self.username][1] == 'admin':
            self.newentry = raw_input('Please enter new entry: ')
            self.optionsmenu[len(self.optionsmenu.keys())+1] = self.newentry
            print 'New entry added'

    def print_menu_and_get_user_selection(self):
        for x,y in self.optionsmenu.items():
            print str(x)+'. '+ str(y)
    def adminmenufun(self):
        if self.input == 1:
            print '== == = CheckBalance == == ='
            'You have ' + self.accountsdict[self.username][0] + ' TL in your account'
        elif self.input == 2:







