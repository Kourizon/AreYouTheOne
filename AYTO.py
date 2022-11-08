
import time
from random import random, shuffle

def create_new_contestants():
    first_names = ["Daniel","Phillip","Laura","Anne","Jeremy","Steven","Amanda","Shawn","William","Gregory","Theresa","Teresa","Howard","Alice","Russell","Michelle","Wanda","Paul","Marilyn","Bruce","Nancy","Carolyn","Donald","Tina","George","Lois","Fred","Anna","Andrea","Samuel","Joshua","Beverly","Aaron","Mildred","Kimberly","Jane","Wayne","Steve","Chris","Lillian","Frances","Douglas","Phyllis","Eugene","Nichola","Christine","Ernest","Paula","Betty","Gerald"]
    last_names = ["Jenkins","Campbell","Lopez","Johnson","Young","Alexander","Reed","Coleman","Morris","Green","Bryant","Allen","Richardson","Barnes","Rivera","Baker","Gonzales","Wilson","Hughes","Turner","Watson","James","Diaz","Peterson","Lewis","Ross","Gonzalez","King","Brooks","Moore","Garcia","Brown","Thomas","Collins","Scott","Jackson","Morgan","Davis","Stewart","Washington","Anderson","Williams","Griffin","Rodriguez","Murphy","Adams","Hill","Bell","Robinson","Gray"]
    shuffle(first_names)
    shuffle(last_names)

    first_names = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']
    last_names = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']

    contestants = []
    for i in range(16):
        contestants.append(first_names.pop() + ' ' + last_names.pop())
    shuffle(contestants)
    return contestants

def create_answers(cts):
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
    

class ideal_week():
    
    def __init__(self, contestants, Answers):
        self.all_combs = set()
        self.unused = contestants
        self.weeks = 0
        self.correctpairs = 0
        self.lastTrial = None
        self.Answers = Answers
# O(n!) very slow D:
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
        self.weeks += 1
        _tbPair = tuple(sorted((self.unused[0],self.unused[1])))
        trialmatch = None
        new_combsNC = set()
        new_combsTB = set()
        numRight = 0
        

        if self.weeks > 1:
            for c in self.all_combs:
                if len(c.intersection(self.lastTrial)) == self.correctpairs:
                    new_combsNC.add(c)
            self.all_combs = new_combsNC

            highest_val = float('inf')
            for i in range(len(self.unused)):
                for j in range(1,len(self.unused)-i):
                    occurs = 0
                    temp = tuple(sorted((self.unused[i],self.unused[i+j])))
                    for a in self.all_combs:
                        if temp in a:
                            occurs += 1
                    
                    if len(self.all_combs) - occurs > occurs:
                        occurs = len(self.all_combs) - occurs

                    if occurs < highest_val:
                        highest_val = occurs
                        _tbPair = temp

        #Gets any trial match where the truth booth pair is in the trial match
        #print(f"Week {self.weeks}:")
        #print(f"Truth Booth: {_tbPair}")
        for c in self.all_combs:
            if _tbPair in c:
                trialmatch = c
                break
        #print(f"Trying... {trialmatch}")
       
        #Checks for number of correct pairs
        for m in trialmatch: 
            if m in self.Answers:
                numRight += 1
        #print(f"There are {numRight} correct pairs in this trial")
        if numRight == 8:
            self.all_combs = set()
            self.all_combs.add(trialmatch)
            return
        self.lastTrial = trialmatch
        self.correctpairs = numRight
       
        #Gets a set of all possible combinations that have the same number of correct pairs as the tiral
        
        
        if _tbPair in self.Answers:
            self.unused.remove(_tbPair[0])
            self.unused.remove(_tbPair[1])
            for a in self.all_combs:
                if _tbPair in a:
                    new_combsTB.add(a)
        else:
            for a in self.all_combs:
                if not _tbPair in a:
                    new_combsTB.add(a)
        
        self.all_combs = new_combsTB

    def run(self):
        #print(len(self.all_combs))
        while len(self.all_combs) > 1:
            start = time.time()
            self.play_week()
            #print(f"{len(self.all_combs)} Possibilities remain")
            end = time.time()
            #print(f"Completed in {(end - start):.2f} seconds")
            #print("\n")
        print(f"Result: {self.all_combs}")
        s = set()
        s.add(self.Answers)
        print(f"Answers: {s}")
        print(f"Correct?: {self.all_combs == s}")
        
class educated_week():
    def __init__(self,contestants,Answers):
        self.confirmed = set()
        self.weeks = 0
        self.unused = contestants
        self.Answers = Answers
        self.confirmedWrong = set()
        self.history = dict()
        self.bestpast = None
    
    def playweek(self):
        self.weeks += 1
        trialmatch = []
        _tbPair = tuple()
        invalid = True
        while invalid:
            for i in self.confirmed:
                trialmatch.append(i)
            #print(f"confirmed: {self.confirmed}")
            #print(f"trialmatch1: {trialmatch}")
            bp_part = []
            if self.bestpast != None:
                shuffle(self.bestpast[0])
                for i in range(self.bestpast[1]):
                    bp_part.append(self.bestpast[0][i])
            temp = self.unused.copy()
           
            #print(f"self.unused: {self.unused}")
            _finbpP = []
            
            _listofconfirmed = list()
            for i in self.confirmed:
                _listofconfirmed.append(i[0])
                _listofconfirmed.append(i[1])
            for k in bp_part:    
                if k[0] not in _listofconfirmed and k[1] not in _listofconfirmed:
                    _finbpP.append(k)
            #print(f"bp: {bp_part}       finbp: {_finbpP}")
            bp_part = _finbpP
            for i in _finbpP:
                temp.remove(i[0])
                temp.remove(i[1])
                trialmatch.append(i)
            #print(f"trialmatch2: {trialmatch}")
            shuffle(temp)
            #print(f"temp: {temp}")
            for i in range(0,len(temp)-1,2):
                trialmatch.append(tuple(sorted((temp[i],temp[i+1]))))
            #print(f"Week{self.weeks}: {trialmatch}")
            
            invalid = False
            _tbPair = trialmatch[7]
            for a in self.confirmedWrong:
                if a in trialmatch:
                    invalid = True
                    trialmatch = []
                    #print("REDO REDO  REDO  REDO")
        
        #Checking for correct pairs
        trialmatch = frozenset(trialmatch)
        numRight = 0
        for m in trialmatch: 
            if m in self.Answers:
                numRight += 1
        #print(f"numRight: {numRight}")
        if _tbPair in self.Answers:
            self.confirmed.add(_tbPair)
            self.unused.remove(_tbPair[0])
            self.unused.remove(_tbPair[1])
            #print("right!")
        else:
            self.confirmedWrong.add(_tbPair)
            #print("wrong!")
        self.history[trialmatch] = numRight
        if self.bestpast == None or self.bestpast[1] < numRight:
            self.bestpast = (list(trialmatch),numRight)
        
        
    def run(self):
        while len(self.confirmed) != 8:
            self.playweek()
        print(f"Result: {self.confirmed}")
        print(f"Answers: {self.Answers}")
        print(f"Correct?: {self.confirmed == self.Answers}")
    

class random_week():
    def __init__(self,contestants,Answers):
        self.confirmed = set()
        self.weeks = 0
        self.contestants = contestants
        self.Answers = Answers
    def playweek(self):
        self.weeks += 1
        #print(self.weeks)
        while True:
            shuffle(self.contestants)
            _tbPair = tuple(sorted((self.contestants[0],self.contestants[1])))
            if _tbPair not in self.confirmed:
                break
        if _tbPair in self.Answers:
            self.confirmed.add(_tbPair)
            self.contestants.remove(_tbPair[0])
            self.contestants.remove(_tbPair[1])
        
    def run(self):
        while len(self.confirmed) != 8:
            self.playweek()
        print(f"Result: {self.confirmed}")
        print(f"Answers: {self.Answers}")
        print(f"Correct?: {self.confirmed == self.Answers}")
    




if __name__ == "__main__":
    # ideal_week , random_week , educated_week

    test_run(random_week)
    
    test_run(educated_week)

    test_run(ideal_week)




