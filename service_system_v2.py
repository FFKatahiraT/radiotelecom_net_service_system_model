import random
import numpy as np
import matplotlib.pyplot as plt

def poisson():
	time_sequence=[]
	for i in range(N):
		time_sequence.append([np.random.exponential(scale=1/lmb, size=None), np.random.randint(l_min,l_max)])
	return time_sequence

def service_system(time_sequence, N_0):
	q=0	#quantity of packages in the storage
	time=0
	mu_list=[]
	packages_rejected=0
	gamma=[]
	time_package_in=[]
	time_package_out=[]
	time_total=0
	i=0
	while i<len(time_sequence)-1 or q>0:
		while i<(len(time_sequence)-1):
			if time>=time_sequence[i][0]:	#add a package to the storage
				time-=time_sequence[i][0]
				time_package_in.append(time_total)	#list of package processing time	
				i+=1
				q+=1
			else:
				break
		if q>0 and q<=N_0:
			mu=C/time_sequence[i][1]
			time+=1/mu	#service time
			time_total+=time	#list of package processing time
			time_package_out.append(time_total)	#list of package processing time	
			rho=lmb/mu 	#calc rho for this package
			if N_0>=N**2:
				P_b=0
			else:
				P_b = P_n_calc(N_0-1, rho)
			gamma.append(lmb*(1-P_b))
			q-=1
			mu_list.append(mu)
		elif q>N_0:
			packages_rejected+=1	#If storage overfilled a package will be rejected
			q-=1
		elif q==0:
			time=time_sequence[i][0]	#downtime
		else:
			print('Something went wrong')
		
		time_of_processing=timeofprocessing(time_package_in, time_package_out)	#calculating package delay time in service system
		T_av = calc_average_value(time_of_processing)
		gamma_av = calc_average_value(gamma)	#Calculating average gamma
		mu_av = calc_average_value(mu_list)
	return mu_av, gamma_av, T_av, packages_rejected

def MM1N0():
	global N_0
	N_0=N//2
	time_sequence=poisson()
	return service_system(time_sequence, N_0)

def MM1infty():
	global N_0
	N_0=N**2
	time_sequence=poisson()
	return service_system(time_sequence, N_0)
	
def plot_scatter(x, y, xlabel, ylabel, title):
	plt.grid()
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.scatter(x, y)
	plt.tight_layout()
	plt.savefig(title+'.eps')
	plt.show()

def plot_perfomance(SS_type):
	plt.grid()
	plt.xlabel(r'Channel utilization rate $\rho$')
	plt.ylabel(r'Specific SS perfomance $\frac{\gamma}{\mu}$')
	plt.title('SS perfomance on rho '+SS_type)
	theor_perfomance=[]
	if SS_type=='MM1N0':
		for i in range(len(rho_list)):
			theor_perfomance.append(rho_list[i]*((1-rho_list[i]**N_0))/(1-rho_list[i]**(N_0+1)))
	elif SS_type=='MM1infty':
		for i in range(len(rho_list)):
			theor_perfomance.append(rho_list[i])
	plt.scatter(rho_list, gammadermu, label='Experiment')
	plt.scatter(rho_list, theor_perfomance, label='Theory')
	plt.legend(loc='best')
	plt.tight_layout()
	plt.savefig('SS perfomance on rho'+SS_type+'.eps')
	plt.show()

def plot_delay(SS_type):
	plt.grid()
	plt.xlabel(r'Channel utilization rate $\rho$')
	plt.ylabel(r'Specific average delay time $T_{av} \mu$')
	plt.title('Delay time on rho '+SS_type)
	theor_delay=[]
	for i in range(len(rho_list)):
		theor_delay.append(1/(1-rho_list[i]))
	plt.scatter(rho_list, muxT_av, label='Experiment')
	plt.scatter(rho_list, theor_delay, label='Theory')
	plt.legend(loc='best')
	plt.tight_layout()
	plt.savefig('Delay time on rho'+SS_type+'.eps')
	plt.show()

def timeofprocessing(time_in, time_out):
	time_of_processing=[]
	for i in range(len(time_out)):
		time_of_processing.append(time_out[i]-time_in[i])
	return time_of_processing

def arrange(y):
	arranged_y=[]
	while True:
		arranged_y.append(max(y))
		del(y[y.index(max(y))])
		if len(y) == 0:
			break
	return arranged_y

def W_calc(T_package_processing):
	W=[]	#Package wait time in storage
	for i in range(len(T_package_processing)):
		W.append(T_package_processing[i]-1/mu)
	return W

def tau_calc(time_package_out):
	tau=[]
	for i in range(1, len(time_package_out)):
		tau.append(time_package_out[i]-time_package_out[i-1])
	return tau

def P_n_calc(q, rho):
	if rho==1.0:
		rho=1-10**-6
	try:
		P_n=(1-rho)/(1-rho**(N_0+1))*rho**(q+1)	#q+1=n (packages in service system)
	except:
		P_n=(1-rho)*rho**(q+1)	#q+1=n (packages in service system)
	return P_n

def calc_average_value(value_list):
	if len(value_list)<=0:
		return 0
	av_value=0	
	for i in range(len(value_list)):
		av_value+=value_list[i]
	av_value/=len(value_list)
	return av_value

def main(SS_type):
	global lmb, rho_list, muxT_av, gammadermu
	gamma_lmb, T_lmb, lmb_list, mu_list = [], [], [], []
	rho_list, muxT_av, gammadermu = [], [], []
	lmb=0
	for i in range(1000):
		lmb+=10
		if SS_type=='MM1N0':
			mu_av, gamma_av, T_av, packages_rejected= MM1N0()	#Calc MM1N0 SS
		elif SS_type=='MM1infty':
			mu_av, gamma_av, T_av, packages_rejected= MM1infty()	#Calc MM1infty SS
		gamma_lmb.append(gamma_av)
		mu_list.append(mu_av)
		lmb_list.append(lmb)
		T_lmb.append(T_av) 
		print(i,'steps calculated')
		# print('T_av='+str(round(T_av,2)), 'gamma_av='+str(round(gamma_av, 2)))
		print('packages_rejected: ', packages_rejected, 'lambda: ', lmb)

	for i in range(len(lmb_list)):
		rho_list.append(lmb_list[i]/mu_list[i])
		muxT_av.append(mu_list[i]*T_lmb[i])
		gammadermu.append(gamma_lmb[i]/mu_list[i])
	# plotter(lmb_list, T_lmb, r'Package speed $\lambda$', r'Average package delay time $T_{av}$', 'Average delay time')
	# plotter(lmb_list, gamma_lmb, r'Package speed $\lambda$', r'Average SS perfomance $\gamma$', 'SS perfomance gamma(lmb)')
	plot_delay(SS_type)
	plot_perfomance(SS_type)


#############DATA INIT#############
N=10**2
l_min=1
l_max=10
C=2*10**6/N	#throughput
tau_0=1
###################################
main('MM1N0')
main('MM1infty')