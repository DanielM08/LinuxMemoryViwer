import os
import subprocess
import pandas as pd


meminfo = dict((i.split()[0].rstrip(':'),int(i.split()[1])) for i in open('/proc/meminfo').readlines())

def memory_values(meminfo):
	mem_kb = meminfo['MemTotal'] 
	mem_free_kb = meminfo['MemFree']
	mem_cached = meminfo['Cached']
	mem_swap_cached = meminfo['SwapCached']
	mem_total_swap = meminfo['SwapTotal']
	mem_swap_free = meminfo['SwapFree']

	print("\n")
	print("Total Memory: " + str(mem_kb) + "\n")
	print("Free Memory: " + str(mem_free_kb) + "\n")
	print("Cached: " + str(mem_cached) + "\n")
	print("SwapCached: " + str(mem_swap_cached) + "\n")
	print("Total Swap: " + str(mem_total_swap) + "\n")
	print("Free Swap: " + str(mem_swap_free) + "\n")

memory_values(meminfo)


pageFaults = subprocess.check_output('ps h -e -o pid,min_flt,maj_flt', shell = True)

#print(pageFaults)

def page_faults(pageFaults):
	#Byte to String
	#pagesF = "".join(map(chr, pageFaults))
	pagesF = pageFaults.split('\n')

	pid = []
        min_flt = []
        maj_flt = []
	for i in range(0, len(pagesF)):
	    lstAux1 = pagesF[i].split(' ')
            lstAux1 = [item for item in lstAux1 if item != '']
            if(lstAux1):
                pid.append(lstAux1[0])
                min_flt.append(lstAux1[1])
                maj_flt.append(lstAux1[2])
        proc_flt = pd.DataFrame().from_dict({'pid':pid,
            'min_flt':min_flt, 'maj_flt':maj_flt})
        print(proc_flt)

page_faults(pageFaults)






