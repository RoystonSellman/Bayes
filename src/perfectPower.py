# Name:        perfect powers y = x**n where y,x and n are integers and n >1
# Purpose:     Solve New Scientist Enigma 1777
#
#!/usr/bin/env python

import math

SEARCH_LIMIT = 50000

perfectPowersSet = set()

# Find the maximum power we will have to deal with
maxPower = int(math.log(SEARCH_LIMIT) / math.log(2))

for power in range(2, maxPower + 1):
    for i in range(1, SEARCH_LIMIT + 1):
        perfectPower = i**power

        if perfectPower > SEARCH_LIMIT:
            break

        perfectPowersSet.add (perfectPower)

perfectPowersList = sorted(perfectPowersSet)

#for i in range(0, len(perfectPowersList)):
#    print(i+1, perfectPowersList[i])

for i in range(2, len(perfectPowersList)):
    if (perfectPowersList[i]) /i > 100:
        print ("Rank order", i, "value :", perfectPowersList[i-1], "-->Number of tickets = ", i * 100 )
        break