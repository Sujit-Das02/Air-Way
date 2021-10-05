import random,math
from collections import defaultdict,deque
from heapq import heappush,heappop

class WeightageGraph:

    def __init__(self):
        self.graph = defaultdict(list)
    def add_edge(self, src, target, flight_charge,time,seat):
        self.graph[src].append([target, flight_charge,time,seat])
    def print_graph(self):
        return self.graph

    
class AirIndia:

    def __init__(self,flights,transFlight,airports):
        self.graph=flights
        self.transGraph=transFlight
        self.vertices=airports

    def explore(self,curr,visited,store=[]):
        visited[curr]=True
        for neg in self.graph[curr]:
            if not visited[neg[0]]:
                self.explore(neg[0],visited,store)
        store.append(curr)

    def exploreTrans(self,node,visited,Airports):
        visited[node] = True
        #print("->", node, end=" ")
        Airports.append(node)
        for neg in self.transGraph[node]:
            if not visited[neg[0]]:
                self.exploreTrans(neg[0],visited,Airports)

    def CalculateCost(self,From,To,path,n,count=1,Mcost=0,Tcost=0):
        for neg in self.graph[From]:
            if neg[0]==To:
                Mcost+=neg[1]
                Tcost+=neg[2]
                if count+1==n:
                    return (Mcost,Tcost)
                else:
                    count+=1
                    return self.CalculateCost(neg[0],path[count],path,n,count,Mcost,Tcost)
    
    def isRechable(self,start,end):
        visited={}
        for node in self.vertices:
            visited[node]=False
        self.explore(start,visited)
        return visited[end]

    def checkSeat(self,From,To,path,n):
        count=1
        while From!=To and count!=n:
            for neg in self.graph[From]:
                if neg[0]==path[count]:
                    if neg[3]==0:
                        return False
                    neg[3]-=1
                    From=neg[0]
                    count+=1
                    break

        return True           
    
    def seatAvailable(self,From,To,path1,n1,path2=None,n2=None):
        status1=self.checkSeat(From,To,path1,n1)
        if path2 is None:
            return status1
        else:
            status2=self.checkSeat(To,From,path2,n2)
            return status1 and status2

    def ConnectComponent(self):
        visited={}
        for node in self.vertices:
            visited[node]=False

        stack = []
        for node in self.vertices:
            if not visited[node]:
                self.explore(node,visited,stack)

        visited = {}
        for node in self.vertices:
            visited[node] = False

        twoWay=[]
        current = stack.pop()
        self.exploreTrans(current,visited,twoWay)
        return twoWay

    def constructPath(self,start,end,prev):
        path=[]
        while start!=end:
            path.append(end)
            end=prev[end]
        path.append(end)
        path.reverse()
        
        n=0
        for node in path:
            n+=1
            print(f"> {node}",end=" ")

        return (path,len(path))
        
    def Dijkstra(self,start,indx):
        cost={}
        prev={}
        for node in self.vertices:
            cost[node]=math.inf
            prev[node]=None
        
        cost[start]=0
        heap=[]
        heappush(heap, (cost[start], start))
    
        while heap:
            Fvertex=heappop(heap)[1]
            for edge in self.graph[Fvertex]:
                if cost[edge[0]]>cost[Fvertex]+edge[indx]:
                    cost[edge[0]]=cost[Fvertex]+edge[indx]
                    prev[edge[0]]=Fvertex
                    heappush(heap,(cost[edge[0]],edge[0]))
        
        return prev

    def BFS(self,start):
        visited={}
        prev={}
        for node in self.vertices:
            visited[node]=False
            prev[node]=None

        queue=deque()
        queue.append(start)
        while queue:
            curr=queue.popleft()
            for neg in self.graph[curr]:
                if not visited[neg[0]]:
                    visited[neg[0]]=True
                    prev[neg[0]]=curr
                    queue.append(neg[0])
        
        return prev

    def takeInput(self):
        takeOn=input("\n\tTake On Airport(Select From Above List) : ").lower().strip()
        takeOff=input("\tTake Off Airport(Select From Above List) : ").lower().strip()
        return (takeOn,takeOff)

    def printData(self,flightC,Mcost,Tcost):
        print(f"\n\tFlights Change : {flightC}    Traveling Cost : ₹{Mcost}     In Flight : {Tcost} hr\n")
    
    def oneWayCal(self,takeOn,takeOff,prev):
        print("\t",end=" ")
        path,n=self.constructPath(takeOn,takeOff,prev)
        Mcost,Tcost=self.CalculateCost(path[0],path[1],path,n)
        self.printData(n-1,Mcost,Tcost)

        data=(path,n,Mcost,Tcost)
        return data

    def twoWayCal(self,takeOn,takeOff,prev1,prev2):
        print("\t",end=" ")
        path1,n1=self.constructPath(takeOn,takeOff,prev1)
        Mcost1,Tcost1=self.CalculateCost(path1[0],path1[1],path1,n1)
        path2,n2=self.constructPath(takeOff,takeOn,prev2)
        Mcost2,Tcost2=self.CalculateCost(path2[0],path2[1],path2,n2)
        opr.printData(n1+n2-2,Mcost1+Mcost2,Tcost1+Tcost2)

        data=(path1,n1,path2,n2,Mcost1,Mcost2,Tcost1,Tcost2)
        return data


def bookingSucces(takeOn,takeOff,type,id):
    print("\t\t                 -:Booking Succesful:-              ")
    print("\t\t|-------------------------------------------------------|")
    print(f"\t\t|     Travel Mode : {type}     Ticket id : #00{id}\t|")
    print(f"\t\t|     TakeOn From : {takeOn}   TakeOff To : {takeOff}\t|")
    print("\t\t|             Wish You have a Great Journey!            |")
    print("\t\t|-------------------------------------------------------|")
        
        
if __name__ == "__main__":

    file = open("flight.txt", 'r')
    content = file.read().lower()
    flights = content.split("flights")

    # International_airports = ["Mumbai", "Kolkata", "Bangalore", "Chennai", "Hyderabad", "Lucknow", "New-Delhi",
    #                           "Ahmedabad", "Cochin", "Goa"]
    airports = []
    total_airports = 0
    for string in content.split():
        if string != "flights" and string not in airports:
            airports.append(string)
            total_airports += 1

    Graph = WeightageGraph()
    transGraph = WeightageGraph()

    for i in range(len(flights)-1):
        src, dest = flights[i].split()
        cost=(random.randrange(1000,10000)//10)*10
        time=random.randint(1,13)
        seat=1
        Graph.add_edge(src,dest,cost,time,seat)
        transGraph.add_edge(dest,src,cost,time,seat)

    edges = Graph.print_graph()
    transEdges=transGraph.print_graph()
    opr=AirIndia(edges,transEdges,airports)
    
    print("\n\t\t          =======================          ")
    print("\t\t          || Welcome To AirWay ||            ")
    print("\t\t=============================================")

    id=1
    twoWay=opr.ConnectComponent()

    while True:
        print("\n\tPlease Select Your Travelling Mode:")
        print("\t 1. One Way \t\t\t  2. Round Way\n")

        while True:
            try:
                type=int(input("\tSelect Mode(press 1 or 2) : "))
                if type==1 or type==2:
                    break
                else:
                    print("\t---Give Valid Input---")
            except:
                print("\t---Give Valid Input---")

        if type==1:
            takeOn,takeOff=opr.takeInput()
            if (takeOn not in airports) or (takeOff not in airports) or (not opr.isRechable(takeOn,takeOff)):
                print("\n\t\tSorry! out of Service.")
            else:
                print("\n\t\t\t    -:Most Optimal routes:-")
                print("\t\t\t-------------------------------\n")

                print("\t1.Minimal Travelling Cost\n")
                prev=opr.Dijkstra(takeOn,1)
                # data = (path,n,Mcost,Tcost])
                data1=opr.oneWayCal(takeOn,takeOff,prev)

                print("\t2.Minimal Travelling Time\n")
                prev=opr.Dijkstra(takeOn,2)
                data2=opr.oneWayCal(takeOn,takeOff,prev)

                print("\t3.Minimal Flight Changes\n")
                prev=opr.BFS(takeOn)   
                data3=opr.oneWayCal(takeOn,takeOff,prev)

                select=int(input("\tChose Effictive One : "))
                count=0
                found=False
                while count<3:
                    check=False
                    if select==1:
                        check=opr.seatAvailable(takeOn,takeOff,data1[0],data1[1])
                    elif select==2:
                        check=opr.seatAvailable(takeOn,takeOff,data2[0],data2[1])
                    else:
                        check=opr.seatAvailable(takeOn,takeOff,data3[0],data3[1])

                    print(f"\tSeat Available : {check}")

                    if check is True:
                        found=True
                        bookingSucces(takeOn,takeOff,"One way",id)
                        id+=1
                        break
                    else:
                        print("\n\t\t\t|--------------------------------|")
                        print("\t\t\t|  All seats are already Booked  |")
                        print("\t\t\t|--------------------------------|")
                        count+=1
                        if count<3:
                            select=int(input("\n\tChose Another One : "))
            
                if not found:
                    print("\n\t\t\t   -:All Optimal route Booking are over:-  ")
                    # print("\t\t\t------------------------------------------")
                    print("\n\t\t\t|----------------------|")
                    print("\t\t\t|   Self Finding Path  |")
                    print("\t\t\t|----------------------|")
                    old=set([*data1[0],*data2[0],*data3[0]])       
                    new=[]
                    for node in twoWay:
                        if node not in old:
                            new.append(node)
                    print(*new)
                    medium=input("\n\tChose a middle Airport(From above List) : ").lower().strip()

                    prev1=opr.BFS(takeOn)
                    prev2=opr.BFS(medium)   
                    prev3=opr.BFS(takeOff)

                    print()
                    x1=opr.oneWayCal(takeOn,medium,prev1)
                    x2=opr.oneWayCal(medium,takeOff,prev2)

                    print(f"\tSeat Available : {True}")
                    bookingSucces(takeOn,takeOff,"One Way",id)
                    id+=1
        
        if type==2:
            print("\n\t\t\t   -:Available Round Way Travelling Airports:-")
            print("\t\t\t------------------------------------------------")
            print(*twoWay)

            takeOn,takeOff=opr.takeInput()
            if (takeOn not in twoWay) or (takeOff not in twoWay):
                print("\n\t\tSorry! out of Service.")
            else:
                print("\n\t\t\t-:Most Optimal routes:-\n")

                print("\t1.Minimal Travelling Cost\n")
                prev1=opr.Dijkstra(takeOn,1)
                prev2=opr.Dijkstra(takeOff,1)
                # Data = (path1,n1,path2,n2,Mcost1,Mcost2,Tcost1,Tcost2)
                data1=opr.twoWayCal(takeOn,takeOff,prev1,prev2)
                
                print("\t2.Minimal Travelling Time\n")
                prev3=opr.Dijkstra(takeOn,2)
                prev4=opr.Dijkstra(takeOff,2)
                data2=opr.twoWayCal(takeOn,takeOff,prev3,prev4)

                print("\t3.Minimal Flight Changes\n")
                prev5=opr.BFS(takeOn)   
                prev6=opr.BFS(takeOff)
                data3=opr.twoWayCal(takeOn,takeOff,prev5,prev6)

                select=int(input("\tChose Effictive One : "))
                count=0
                found=False
                while count<3:
                    check=False
                    if select==1:
                        check=opr.seatAvailable(takeOn,takeOff,data1[0],data1[1],data1[2],data1[3])
                    elif select==2:
                        check=opr.seatAvailable(takeOn,takeOff,data2[0],data2[1],data2[2],data2[3])
                    else:
                        check=opr.seatAvailable(takeOn,takeOff,data3[0],data3[1],data3[2],data3[3])

                    print(f"\tSeat Available : {check}")

                    if check is True:
                        found=True
                        bookingSucces(takeOn,takeOff,"Round Way",id)
                        id+=1
                        break
                    else:
                        print("\n\t\t\t|--------------------------------|")
                        print("\t\t\t|  All seats are already Booked  |")
                        print("\t\t\t|--------------------------------|")
                        count+=1
                        if count<3:
                            select=int(input("\n\tChose Another One : "))
                        
                
                if not found:                    
                    print("\n\t\t\t   -:All Optimal route Booking are over:-  ")
                    # print("\t\t\t------------------------------------------")
                    print("\n\t\t\t|----------------------|")
                    print("\t\t\t|   Self Finding Path  |")
                    print("\t\t\t|----------------------|")
                    old=set([*data1[0],*data1[2],*data2[0],*data2[2],*data3[0],*data3[2]])       
                    new=[]
                    for node in twoWay:
                        if node not in old:
                            new.append(node)
                    print(*new)
                    medium=input("\n\tChose a middle Airport(From above List) : ").lower().strip()

                    prev1=opr.BFS(takeOn)
                    prev2=opr.BFS(medium)   
                    prev3=opr.BFS(takeOff)
                    print("\n\tFast :")
                    x1=opr.oneWayCal(takeOn,medium,prev1)
                    x2=opr.oneWayCal(medium,takeOff,prev2)
                    print("\tReturn :")
                    x3=opr.oneWayCal(takeOff,medium,prev3)
                    x4=opr.oneWayCal(medium,takeOn,prev2)

                    print(f"\tSeat Available : {True}")
                    bookingSucces(takeOn,takeOff,"Round Way",id)
                    id+=1

        print("\n\t\t1.Book a New Ticket\t\t\t2.Exit")
        while True:
            try:
                user=int(input("\n\tChose option : "))
                break
            except:
                print("\t\tInvalid Input.")

        if user==1:
            print("\n\t\t\t|---------------------|")
            print("\t\t\t|   -:New Ticket:-    |")
            print("\t\t\t|---------------------|")
        else:
            print("\t\t\t-:Thank You! Visit Again.:-")
            break
            