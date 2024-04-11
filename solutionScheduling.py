from random import randint
import numpy as np

# Define shifts instead of courses. Each entry represents a time slot in a week.
shifts = [{'name': f'{day}{period}', 'min_nurses': 2} for day in 'MTWTFS' for period in '123']

# Add Saturday with possibly a different requirement

nurses = ['空','甲', '乙', '丙', '丁', '戊']

# Simplified: Just periods without specific rooms
#periods = [f'{day}{period}' for day in 'MTWTF' for period in '123'] + [f'S{period}' for period in '123']
periods = [
'Mon Morning','Mon Afternoon','Mon Evening',
'Tue Morning','Tue Afternoon','Tue Evening',
'Wed Morning','Wed Afternoon','Wed Evening',
'Thu Morning','Thu Afternoon','Thu Evening',
'Fri Morning','Fri Afternoon','Fri Evening',
'Sat Morning','Sat Afternoon','Sat Evening'
]

cols = 3

def randShift():
    return randint(0, len(shifts)-1)
def randPeriod():
    return randint(0, len(periods)-1)
def randNurse():
    return randint(0, len(nurses)-1)

class SolutionScheduling:
    def __init__(self, v):
        self.v = v  # v is a list representing nurse assignment to shifts

    def neighbor(self):
        fills = self.v.copy()
        choose = randint(0,1)
        if choose == 0:
            i = randPeriod()
            j = randint(0, 2)
            fills[i][j]=randNurse()
        elif choose ==1:
            i1 = randPeriod()
            i2 = randPeriod()
            j1 = randint(0, 2)
            j2 = randint(0, 2)
            t = fills[i1][j1]
            fills[i1][j1] = fills[i2][j2]
            fills[i2][j2] = t

        return SolutionScheduling(fills)

    def height(self):
        score = 0
        fills = self.v.copy()
        for i in range(len(fills)):
            if fills[i][0] == fills[i][1] or fills[i][1] == fills[i][2] or fills[i][0] == fills[i][2]:
                score -= 0.4
            else:
                score += 0.1
        for i in range(len(fills)):
            count = 0
            for j in range(len(fills[i])):
                if i < len(fills)-1 and fills[i][2] != fills[i+1][0]:
                    score += 0.1                
                if fills[i][j] =="空":
                    count +=1
            if count >=2:
                score -= 0.12             
        return score

    def str(self):
        fills = self.v
        output=[]
        for i in range(len(fills)):
            c = ''
            for j in range(len(fills[i])):
                c += nurses[fills[i][j]]
            if i % cols ==0:
                output.append("\n")
            output.append(periods[i] + ':' + c+ '  ')
        return 'height={:f} {:s}\n\n'.format(self.height(), ' '.join(output))
    
    def detail(self):
        fills = self.v
        detail = {}
        for i in range(len(fills)):
            for j in range(len(fills[i])):
                if nurses[fills[i][j]] not in detail:
                    detail[nurses[fills[i][j]]] = 1
                else:
                    detail[nurses[fills[i][j]]] += 1
        return detail

    @classmethod
    def init(cls):
        fills = [[0, 0, 0] for _ in range(len(periods))]
        for i in range(len(periods)):
            for j in range(len(fills[i])):
                fills[i][j] = randNurse()
        return SolutionScheduling(fills)
