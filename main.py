from __future__ import annotations
import concurrent.futures
import threading
from uuid import uuid4
import concurrent.futures
import math
import random, time
import numpy as np



# Thread Pool Executor (built-in python)
tp = concurrent.futures.ThreadPoolExecutor(16)

class Thread(threading.Thread):

    
    def __init__(self, target: int = 3 , self_start:bool = True, daemon: bool = True, data: list = [], basis: float = 0.75, times: int = 3) -> None:
        
        self.uuid: str = uuid4()
        self.total_tasks = 0 
        self.target = target
        self.tasks = 0
        self.data = [] if data is None or type(data) is not list else data
        self.results = []
        self.target_grouped_results = []
        self._work = False
        self.basis = basis
        self.times = times
        self.sameTarget = 0
        threading.Thread.__init__(self, name=uuid4, daemon=daemon)

        if self_start:
            self.start()

    def start(self) -> None:
        self._work = True
        return super().start()

    def setFcn(self, fcn):
        self.fcn = fcn

    
    def fcn(self, i: int, d: any) -> any: # Abstract Method
        return [d, i]

    def run_fcn(self,):
        if callable(self.fcn):
            self.threaded(self.fcn)()
            self.removeItem()

        else:
            if self.fcn is None:
                print("Function not set yet -- Thread.setFcn(fcn)")
            else:
                print("Function called for {} could not be executed: Not callable".format(str(type(self.fcn))))

    def needsOpperation(self):
        return True if len(self.data)/3 > 0 else False #

    def run(self,) -> None:
        while self._work:
            if self.needsOpperation():
                if len(self.data) >= self.target:
                    self.sameTarget += 1

                    if self.sameTarget == self.times and math.ceil(self.target * (1+self.basis)) < len(self.data):
                        self.setTarget(math.ceil(self.target * (1+self.basis))) # Increate the target if the value is greater than basis increate of the target and the target has been reached 3 times

                    self.run_fcn()
                else:
                    self.setTarget(len(self.data))
                    self.run_fcn()
            else:
                self._work = False


    def removeItem(self)-> None:

        if self.needsOpperation() and type(self.data) is list:
            for _ in range(self.target):
                if len(self.data) > 0:
                    self.data.pop(0) 
                else:
                    raise IndexError("The data list does not contain the index 0, if this error went wrong file bug report: \n\t Data::{}".format(str(self.data)))


    def setTarget(self, val: int):
        self.sameTarget = 0
        self.target = val

    def join(self) -> None:
        self._work = False

        tp.shutdown(False, cancel_futures=True) # End Worker Threads

        print("""Thread Information for Thread::{}:
            \n\tTotal Opperations Run: {}
            \n\tOpperations Running Curently: {}
            \n\tTarget Amount: {}""".format(self.uuid, self.total_tasks, self.tasks, self.target))
 
        return super().join(None) # End Runner Thread (threading library)


    def threaded(self: Thread, fcn): # Python Decorator
        def wrapper(*args, **kwargs):
            target = list(range(self.target)) 
            results = {}

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {executor.submit(fcn, i, self.data[i]): idx for idx,
                            i in enumerate(target)} 
                
                tasks = len(futures)

                self.tasks += tasks
                self.total_tasks += tasks

                for _, future in enumerate(concurrent.futures.as_completed(futures)):
                    i = futures[future] # Python Future Object
                
                    data = future.result()
                    if len(data) == 1:
                        data = data[0]
                    results[i] = data
                    self.tasks -= 1

            final = []
            for k, v in sorted(results.items()):
                final.append(v)
                self.results.append(v)
            self.target_grouped_results.append(final)
            return final
        return wrapper

# ----------------------------------------- Create Task ------------------------------------------
def value(start, stop, step):
    value = start
    while value <= stop:
        yield value
        value += step


sigmoid = lambda index, data : [data, 1/(math.exp(-data))]
tanh = lambda index, data : [data, (2*math.exp(data))-(math.exp(data))+1]
log = lambda index, data : [data, math.log10(data)]
nat_log = lambda index, data : [data, math.log(data)]
sqrt = lambda index, data : [data, math.sqrt(data)]

while True:
    try:
        print("\n\n")
        # Determine the type of process whichmath.e^-data should be run
        opperations = {
            "sigmoid": sigmoid, "tanh": tanh, "log": log, "natural log": nat_log, "square root": sqrt
        }
        # Program Loop

        opp = opperations[input("Opperation options are: {}\nWhat opperation should be used? ".format(str(opperations.keys()))).strip().lower()]
        if input("Single (y/n) ").lower().strip() == "y":
            print(opp(0, float(input("X Value: ").strip())))
            continue
        minim = float(input("Minimum Value for Range? "))
        stepim = float(input("Step Value? ")) # Because that's how code.org works
        maxim = float(input("Maximum Value for Range? ")) # Because that's how code.org works
        
        

        if maxim <= minim:
            print("Maximum must be larger than minimum!")
            continue

        t = Thread(self_start=False,  data=[x for x in value(minim, maxim, stepim)])

        t.setFcn(opp)


        print("Starting!")

        t.start()


        while t._work:
            print("Program has not finished")
            time.sleep(.25)

        print("Finished!")

        _i = input("See Results (y/n) ")
        if _i == "y" or _i == "yes":
            for x in t.target_grouped_results:
                for i in x:
                    print("({},{})".format(i[0], i[1]))
            
        # Kill Functions
        t.join()

        _i = input("Exit? (y/n) ").lower().strip()
        if _i == "y" or _i == "yes":
            exit() # End of Control Loop

    except KeyboardInterrupt:
        # Kill Functions
        t.join()

        _i = input("Exit? (y/n) ").lower().strip()

        if _i == "y" or _i == "yes":
            exit() # End of Control Loop
