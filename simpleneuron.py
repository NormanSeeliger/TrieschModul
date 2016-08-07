
""""""""""""""""""""""""""""""
" First implementation of a single neuron and basic functions"

" @author: Norman Seeliger"
" @email:  seeliger.norman@gmail.com"
" @date:   08-07-2016"

" @topic:  Module Triesch Interdisciplinary Neuroscience"
""""""""""""""""""""""""""""""
# Imports
from numpy import *
from scipy import *

class SimpleNeuron()
	"Simple neuron with basic functions"
	
	neuroncount = 0;
	
	def __init__(self,e_leak,e_e,tau_membrane,tau_e,v_reset,v_threshold):
		"Initialize neuron parameters"
		neuroncount += 1
		self.current_voltage = v_reset; # Keeping track of current voltage
		self.conductance = 0 		# Current conductance of synapse(s)
		self.voltages = [v_reset] 	# Potential trace over time
		self.e_leak = e_leak		# Reversal potential for leak
		self.e_e = e_e 				# Reversal potential for exc/inh inputs
		self.tau_membrane = tau_membrane # Membrane time constant
		self.tau_e = tau_e 			# PSP time constant
		self.v_reset = v_reset 		# Rest potential
		self.v_threshold = v_threshold # Threshold for spiking
		
		return
	
	def excite(self,inputt,weight,timestep):
		"Receive excitatory input with a given weight"
		self.conductance = exp(-1/self.tau_e)+weight# decay of conductance since last step plus newly received input
		self.current_voltage = Vm[timestep-1] + \
			(self.e_leak - self.current_voltage + \
			 self.conductance*(self.e_e-self.current_voltage)) / self.tau_membrane
		self.voltages.append(self.current_voltage)
		if self.current_voltage > self.v_threshold:
			self.current_voltage = self.v_reset
	
	def inhibit(self,inputt,weight):
		"Receive inhibitory input with a given weight"
		return
	
	def getSpikeTrain(self):
		spike_positions = numpy.zeros(len(self.voltages)
		for n in self.voltages:
			if self.voltages[n] > self.v_threshold:
				spike_positions(n) = 1
		
	
if name == "__main__" :
	SimpleNeuron(-60,0,20,3,-70,-50)