import os

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
	#

memory_values(meminfo)