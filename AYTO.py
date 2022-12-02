import time
import csv
import pathlib
from random import shuffle

def create_new_contestants():
    """Creates 16 contestants with random names"""
    first_names = ["Daniel","Phillip","Laura","Anne","Jeremy","Steven","Amanda","Shawn","William","Gregory","Theresa","Teresa","Howard","Alice","Russell","Michelle","Wanda","Paul","Marilyn","Bruce","Nancy","Carolyn","Donald","Tina","George","Lois","Fred","Anna","Andrea","Samuel","Joshua","Beverly","Aaron","Mildred","Kimberly","Jane","Wayne","Steve","Chris","Lillian","Frances","Douglas","Phyllis","Eugene","Nichola","Christine","Ernest","Paula","Betty","Gerald"]
    last_names = ["Jenkins","Campbell","Lopez","Johnson","Young","Alexander","Reed","Coleman","Morris","Green","Bryant","Allen","Richardson","Barnes","Rivera","Baker","Gonzales","Wilson","Hughes","Turner","Watson","James","Diaz","Peterson","Lewis","Ross","Gonzalez","King","Brooks","Moore","Garcia","Brown","Thomas","Collins","Scott","Jackson","Morgan","Davis","Stewart","Washington","Anderson","Williams","Griffin","Rodriguez","Murphy","Adams","Hill","Bell","Robinson","Gray"]
    shuffle(first_names)
    shuffle(last_names)

    #Easy to identify names for testing
    #first_names = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
    #last_names = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']

    contestants = []
    for i in range(16):
        contestants.append(first_names.pop() + ' ' + last_names.pop())
    shuffle(contestants)
    return contestants

def create_answers(cts):
    """Creates the 8 correct pairs for 16 contestants"""
    Answers = [] #THE TUPLE PAIRS MUST BE SORTED
    count = 0
    for i in range(8):
        p1 = cts[count]
        p2 = cts[count+1]
        Answers.append(tuple(sorted((p1,p2))))
        count += 2
    Answers = frozenset(Answers)
    return Answers

def test_run(_init):
    """Runs an algorithms and returns the total runtime and week count"""
    
    test_init = None
    contestants = create_new_contestants()
    Answers = create_answers(contestants)
    total_start = time.time()
    start = time.time()
    test_init = _init(contestants,Answers)
    end = time.time()
    print(f"\n[Initialized in {(end - start):.2f} seconds]")
    print("\n")

    test_init.run()
    total_end = time.time()
    print(f"Total Compile Time: {(total_end - total_start):.2f} seconds in {test_init.weeks} weeks")
    return (total_end - total_start, test_init.weeks)

def record_data(trResults, type):
    """Writes the data from a trial to the csv file, (type, weeks, time)"""
    dir_path = pathlib.Path(__file__).parent.resolve()
    dir_path = dir_path.joinpath(r"data.csv")
    with open(dir_path,'a',newline='') as f: #this automatically closes the file too :) That's cool
        writer = csv.writer(f)
        _type = type
        weeks = trResults[1]
        time = trResults[0]
        writer.writerow([_type,weeks,time])


class ideal_week():
    
    def __init__(self, contestants, Answers):
        """Creates an ideal_week object"""
        self.all_combs = set()
        self.unused = contestants
        self.weeks = 0
        self.correctpairs = 0
        self.lastTrial = None
        self.Answers = Answers
        #Creates all possible combinations for contestants, overridden by premadecombs
        for a in range(len(contestants)-1):
            for b in range(len(contestants)-3):
                for c in range(len(contestants)-5):
                    for d in range(len(contestants)-7):
                        for e in range(len(contestants)-9):
                            for f in range(len(contestants)-11):
                                for g in range(len(contestants)-13):
                                    for h in range(len(contestants)-15):
                                        x = self.unused.copy()
                                        p1 = tuple(sorted((x.pop(),x.pop(a))))
                                        p2 = tuple(sorted((x.pop(),x.pop(b))))
                                        p3 = tuple(sorted((x.pop(),x.pop(c))))  
                                        p4 = tuple(sorted((x.pop(),x.pop(d))))
                                        p5 = tuple(sorted((x.pop(),x.pop(e))))
                                        p6 = tuple(sorted((x.pop(),x.pop(f))))
                                        p7 = tuple(sorted((x.pop(),x.pop(g))))
                                        p8 = tuple(sorted((x.pop(),x.pop(h))))
                                        self.all_combs.add(frozenset((p1,p2,p3,p4,p5,p6,p7,p8)))

    def play_week(self):
        """Executes the ideal_week"""
        self.weeks += 1
        _tbPair = tuple(sorted((self.unused[0],self.unused[1])))
        trialmatch = None
        new_combsNC = set() #records combinations from the number of correct pairs info
        new_combsTB = set() #records combinations from the truth booth info
        numRight = 0
        

        if self.weeks > 1: #Makes more educated pairings using info from previous runs. 
            
            #Checks all remaining combinations for combinations with only the same number of intersecting pairs as
            #The previous trial
            #Example: If the last trial had 2 pairs correct, only keep combinations with 2 pairs in common with the last trial
            for c in self.all_combs:
                if len(c.intersection(self.lastTrial)) == self.correctpairs:
                    new_combsNC.add(c)
            #updates the remaining combinations to the newly shortened list
            self.all_combs = new_combsNC


            highest_val = float('inf')
            #Checks all contestant pairs that have yet to be confirmed
            for i in range(len(self.unused)):
                for j in range(1,len(self.unused)-i):
                    occurs = 0
                    temp = tuple(sorted((self.unused[i],self.unused[i+j])))

                    #find how many times that pair occurs in the remaining combinations
                    for a in self.all_combs:
                        if temp in a:
                            occurs += 1
                    
                    #sets _maxRem to the greater of either itself or all sets where the pair doesn't occur
                    #this gives you the maximum possible amount of pairs that could still remain if
                    #you sent this pair to the truth booth
                    _maxRem = occurs
                    if len(self.all_combs) - occurs > occurs:
                        _maxRem = len(self.all_combs) - occurs

                    #Record the minimun possible value for _maxRem
                    if _maxRem < highest_val:
                        highest_val = _maxRem
                        _tbPair = temp

        #picks some combination from the remaining combinations where the truth booth pair is in the trial match
        for c in self.all_combs:
            if _tbPair in c:
                trialmatch = c
                break

        #Checks for number of correct pairs
        for m in trialmatch: 
            if m in self.Answers:
                numRight += 1

        #Checks if the trial is completely correct
        if numRight == 8:
            self.all_combs = set()
            self.all_combs.add(trialmatch)
            return

        self.lastTrial = trialmatch
        self.correctpairs = numRight
        
        #Checks the truthbooth pair. Iterates through all remaining combinations and
        #only records combinations where the truth booth pair is either in or not in depending on
        #whether or not it was correct
        if _tbPair in self.Answers:
            #remove the contestants from the unused list as they shouldn't need to be checked again
            self.unused.remove(_tbPair[0])
            self.unused.remove(_tbPair[1])
            for a in self.all_combs:
                if _tbPair in a:
                    new_combsTB.add(a)
        else:
            for a in self.all_combs:
                if not _tbPair in a:
                    new_combsTB.add(a)
        
        #sets the remaining combinations to the newly reduced list
        self.all_combs = new_combsTB

    def run(self):
        """Plays out the week and print the result and run time"""
        #print(len(self.all_combs))
        while len(self.all_combs) > 1:
            start = time.time()
            self.play_week()
            end = time.time()
        print(f"Result: {self.all_combs}")
        s = set()
        s.add(self.Answers)
        print(f"Answers: {s}")
        print(f"Correct?: {self.all_combs == s}")
        
class educated_week():
    def __init__(self,contestants,Answers):
        """creates an educated_week object"""
        self.confirmed = set()
        self.weeks = 0
        self.unused = contestants
        self.Answers = Answers
        self.confirmedWrong = set()
        self.history = dict()
        self.bestpast = None #is a tuple of the best past trial, and the number of correct pairs in that trial
    
    def playweek(self):
        """Executes the educated week"""
        self.weeks += 1
        trialmatch = []
        _tbPair = tuple()
        invalid = True
        
        while invalid:
            #Adds all confirmed pairs to the beginning of trialmatch
            for i in self.confirmed:
                trialmatch.append(i)

            bp_part = []
            #If there are previous runs, add pairs from the best past run, based on the amount correct in that trial
            if self.bestpast != None:
                shuffle(self.bestpast[0])
                for i in range(self.bestpast[1]):
                    bp_part.append(self.bestpast[0][i])
            temp = self.unused.copy()
           
            _finbpP = []
            
            # Removes any duplicate pairs from confirmed and the educated pairs added previously
            _listofconfirmed = list()
            for i in self.confirmed:
                _listofconfirmed.append(i[0])
                _listofconfirmed.append(i[1])
            # Removes pairs that are confirmed from bp_part
            for k in bp_part:    
                if k[0] not in _listofconfirmed and k[1] not in _listofconfirmed:
                    _finbpP.append(k)

            # Puts those pairs into trialmatch and removes the contestants from the pool of unused contestants
            bp_part = _finbpP
            for i in _finbpP:
                temp.remove(i[0])
                temp.remove(i[1])
                trialmatch.append(i)

            # Randomly pairs and adds unused contestants to finish the 8 pairs
            shuffle(temp)
            for i in range(0,len(temp)-1,2):
                trialmatch.append(tuple(sorted((temp[i],temp[i+1]))))

            # Assumes that the trial is valid
            invalid = False
            _tbPair = trialmatch[7]
            # if any pairs in the trialmatch have been previously confirmed to be wrong, restart by setting invalid to True
            for a in self.confirmedWrong:
                if a in trialmatch:
                    invalid = True
                    trialmatch = []
        
        #Checking for correct pairs
        trialmatch = frozenset(trialmatch)
        numRight = 0
        for m in trialmatch: 
            if m in self.Answers:
                numRight += 1
       
        #Checks if the truth booth pair was correct, records result
        if _tbPair in self.Answers:
            self.confirmed.add(_tbPair)
            self.unused.remove(_tbPair[0])
            self.unused.remove(_tbPair[1])
        else:
            self.confirmedWrong.add(_tbPair)

        #Adds the trial to the history and checks if it is the best run yet
        self.history[trialmatch] = numRight
        if self.bestpast == None or self.bestpast[1] < numRight:
            self.bestpast = (list(trialmatch),numRight)
        
        
    def run(self):
        """Plays out the week and print the result and run time"""
        while len(self.confirmed) != 8:
            self.playweek()
        print(f"Result: {self.confirmed}")
        print(f"Answers: {self.Answers}")
        print(f"Correct?: {self.confirmed == self.Answers}")
    
class random_week():
    def __init__(self,contestants,Answers):
        """Creates a random_week object"""
        self.confirmed = set()
        self.weeks = 0
        self.contestants = contestants
        self.Answers = Answers
    def playweek(self):
        """Executes the random week"""
        self.weeks += 1
        #Picks a random truth booth pair that hasn't been used before
        while True:
            shuffle(self.contestants)
            _tbPair = tuple(sorted((self.contestants[0],self.contestants[1])))
            if _tbPair not in self.confirmed:
                break
        #Checks if the truth booth pair is in the answers, if so, record it
        if _tbPair in self.Answers:
            self.confirmed.add(_tbPair)
            self.contestants.remove(_tbPair[0])
            self.contestants.remove(_tbPair[1])
        
    def run(self):
        """Plays out the week and print the result and run time"""
        while len(self.confirmed) != 8:
            self.playweek()
        print(f"Result: {self.confirmed}")
        print(f"Answers: {self.Answers}")
        print(f"Correct?: {self.confirmed == self.Answers}")
    

if __name__ == "__main__":
    # ideal_week , random_week , educated_week
    
    #Simulates mulitple runs and records data
    for i in range(100):
        record_data(test_run(random_week),'ideal')
    

    



