#Rayan Elsharkawi
#Mckinsey Software Engineering
#Tech Assessment - Simulating a Cashier/Discounting System
#April 25, 2018


#The two dictionaries below represent the groceries and nongroceries sold in store
groc_store = {
        "apple": 1,
        "meat": 8,
        "chicken": 5.5,
        "cheese": 3,
        "bread": 2.5,
        "oil": 2.75        
        }

nongroc_store = {
        "soap": 1.5,
        "knives": 7.00,
        "pan": 13.25,
        "towel": 4,
        "lamps": 15,
        "notebook": 2,
        }

#creating a swtich-case like system for implementing the discounts
#only for nongroceries
#employee discount
def dscnt_employee(t):
    print("30% employee discount is applied.")
    return t*0.7
#affiliate discount
def dscnt_affiliate(t):
    print("10% affiliate discount is applied.")
    return t*0.9
#2-year-customer discount
def dscnt_2yr(t):
    print("5% 2-year-customer discount is applied.")
    return t*0.95

#no discount
def nodscnt(t):
    print("**No % discount on non-groceries is applicable.")
    return t
    
OPTIONS = {
    "employee":dscnt_employee,
    "affiliate":dscnt_affiliate,
    "2-year-customer":dscnt_2yr,
    "NA": nodscnt,
#    "other":dscnt_100
}

def switchcase(customertype, tot):
    return OPTIONS[customertype](tot)

#discount on every $100 spent
#for groceries + nongroceries
def dscnt_100(t):
    count100 = t//100
    return t - (count100*5)

##Checkout class uses the shopping bag to...
# 1) separate groceries vs. nongroceries --> calculate sum of each
# 2) calculate percentage discount on nongroceries
# 3) check for final discount (on every $100 spent) and output final bill sum
    
class Checkout:
    def __init__(self, bag, customertype):
        self.__bag = bag
        self.__customertype = customertype
        self.gtot = 0
        self.ngtot = 0
        self.nngtot = 0

    def seperateBaskets(self):
        groceries = []
        nongroceries = []
        i = 0
        #iterates through the checkout bag, and segregates groceries vs. nongroceries
        while i < (len(self.__bag)):
            item = self.__bag[i]
            quantity = self.__bag[i+1]
            #groceries
            if quantity > 0:
                if item in groc_store:
                    groceries.append([item, quantity])
                    self.gtot += (groc_store[item] * quantity)       #groceries sum
                #nongroceries
                elif item in nongroc_store:
                    nongroceries.append([item, quantity])       
                    self.ngtot += (nongroc_store[item] * quantity)   #nongroceries sum
                #if item is not in either dictionary (groc or nongroc)
                else:
                    print("=>", item, "is not available in store.")
                
            #if user happens to input a quantity of 0 for an item (unlikely)
            else:
                print("=>", item, "'s quantity is 0. Not included in bill.")
            
            #increment by 2 because the bag (list) is created in a couplet structure
            #item followed by its respective quantity
            i += 2
                
        
        #printing the bill below, divided into segments to explain how the total is calculated
        print("\n--------------------------------------------------")
        print("ITEM         ($)PRICE,     QUANTITY")
        print("\nNon-groceries:")
        for sublist in nongroceries:
            item = sublist[0]
            s1 = str("%.2f" % nongroc_store[item])
            ls1 = 11 - len(item)
            s2 = str(sublist[1])     
            ls2 = 11 - len(s1)
            print("-", item, " "*(ls1)+"$"+s1, " "*(ls2)+s2)
        print("\nGroceries:")
        for sublist in groceries:
            item = sublist[0]
            s1 = str("%.2f" % groc_store[item])
            ls1 = 11 - len(item)
            s2 = str(sublist[1])     
            ls2 = 11 - len(s1)
            print("-", item, " "*(ls1)+"$"+s1, " "*(ls2)+s2)
#            print("-", item, "    $"+str(groc_store[item])+", x"+str(sublist[1]))
        print("--------------------------------------------------")
        print("Non-groceries Total (before discount):", "$"+str(self.ngtot))
        print("                      Groceries Total:", "$"+str(self.gtot))
        print("--------------------------------------------------")
        
    #calculting the % discount on nongroceries   
    def calcPrcntDscnt(self):
        self.nngtot = switchcase(self.__customertype, self.ngtot)
        if self.nngtot != self.ngtot:
            print("**After the discount, non-groceries total:", "$"+str("%.2f" % self.nngtot))
        return self.nngtot
    #calculating the final total bill
    def calc_final_total(self):
        tmp = self.nngtot + self.gtot
        #check to see if total sum > 100 --> meaning its eligible for discount
        if tmp>=100:
            print("A $5 discount is applied for every $100 spent.")
            print("*************************************************")
            return dscnt_100(tmp)
        else:
            print("**************************************************")
            return tmp
        
#this function organizes the textfile input into a shopping bag 
#also fetches the customer type --> associated with % discounts
def makeBag(inputfilename):
    with open(inputfilename,'r') as f:
        for line in f:
            w = []
            for word in line.split():
               if word.isdigit():
                   word = int(word)
               fp.append(word)
    customertype = fp.pop(0)
#    print("this is fp:", fp, customertype)
    return customertype


#running the STORE below
#constantly looping seeking user input, which acts as a customer and their checkout items
#when "done" is entered, the store closes
storeOpen = 1
print("Welcome to the Digital Store!", "\n Please proceed to checkout...")
while storeOpen:
    inputfilename = input("Enter file name (customer):")
    if inputfilename == "":
        continue
    elif inputfilename == "done":
        print("Closing the store now. Goodbye :)")
        storeOpen = 0
        break
    fp = []
    customertype = makeBag(inputfilename)
#    print("after makeBag,", fp, customertype)
    customer = Checkout(fp, customertype)
    customer.seperateBaskets()
    customer.calcPrcntDscnt()
    tobepaid = customer.calc_final_total()
    print("\nFinal Total Bill: $"+str("%.2f" % tobepaid))

