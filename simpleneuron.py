
""""""""""""""""""""""""""""""
" First implementation of a single neuron and basic functions"

" @author: Norman Seeliger"
" @email:  seeliger.norman@gmail.com"
" @date:   08-07-2016"

" @topic:  Module Triesch Interdisciplinary Neuroscience"
""""""""""""""""""""""""""""""
# Imports
import numpy
from scipy import *
import matplotlib.pyplot as plt
import statistics as stat
from sympy import DiracDelta

class SimpleNeuron():
    "Simple neuron with basic functions"
    
    neuroncount = 0;
    
    def __init__(self,neuronnumber,e_leak,e_e,e_i,e_k,\
                tau_membrane,tau_e,tau_i,tau_sra,\
                v_reset,v_threshold,g_sra):
        "Initialize neuron parameters"
        # SimpleNeuron(1,-60,0,-80,-70,20,3,5,100,-70,-50,0.06)
        SimpleNeuron.neuroncount += 1
        self.gsras = list()
        self.spiketrain = []
        self.neuronnumber = neuronnumber
        self.conductance_i = 0; # Current conductance of inhibitory synapse(s) 
        self.conductance = 0;   # Current conductance of excitatory synapse(s)
        self.conductance_sra = 0; # spike rate adaptation conductance
        self.g_sra = g_sra;        # increase in sra conductance per step
        self.tau_sra = tau_sra   # time constant for sra 
        self.e_k = e_k
        self.current_voltage = e_leak; # Keeping track of current voltage
        self.voltages = [e_leak]   # Potential trace over time
        self.e_leak = e_leak        # Reversal potential for leak
        self.e_e = e_e          # Reversal potential for exc inputs
        self.e_i = e_i          # Reversel potential fpr inh inputs
        self.tau_membrane = tau_membrane # Membrane time constant
        self.tau_e = tau_e      # PSP time constant
        self.tau_i = tau_i      # ISP time constant
        self.v_reset = v_reset      # Rest potential
        self.v_threshold = v_threshold  # Threshold for spiking        
        return
    
    def excite(self,weight):
        "Receive excitatory input with a given weight"
        self.conductance = self.conductance - self.conductance/self.tau_e + weight   
    
    def inhibit(self,weight):
        "Receive inhibitory input with a given weight"
        self.conductance_i = self.conductance_i - self.conductance_i/self.tau_i + weight
    
    def updateVoltage(self):
        "Update membrane voltage after received exc and inh input"
        self.current_voltage = self.voltages[-1] + \
            (self.e_leak - self.voltages[-1] + \
             self.conductance     *(self.e_e-self.voltages[-1]) + \
             self.conductance_i   *(self.e_i-self.voltages[-1])+ \
             self.conductance_sra *(self.e_k-self.voltages[-1])) / self.tau_membrane
        self.voltages.append(self.current_voltage)
        if self.current_voltage > self.v_threshold:
            self.spiketrain.append(1)
            self.current_voltage = self.v_reset
            self.voltages.append(self.current_voltage)
        else:
            self.spiketrain.append(0)
        self.adaptToSpikeRate()
        
    def adaptToSpikeRate(self):
        "Spike-rate adaptation calculation"
        if self.spiketrain[-1] == 1:
            self.conductance_sra = self.conductance_sra - self.conductance_sra/self.tau_sra + \
                                   self.g_sra
        else :
            self.conductance_sra = self.conductance_sra - self.conductance_sra/self.tau_sra
        self.gsras.append(self.conductance_sra)
            
            
#        spike_train = self.getSpikeTrain();
#        current_time = len(self.voltages) - len(spike_train) 
#            # every spike has 2 entries of the potential and the rest
#        sum_dirac = 0;
#        for moment in spike_train :
#            sum_dirac += DiracDelta(current_time - moment) 
#        self.conductance_sra = self.conductance_sra - self.conductance_sra/self.tau_sra + \
#                               self.g_sra*sum_dirac
    
    def getSRA(self):
        "Returns SRA values of neuron"
        return self.gsras
    
    def getSpikeTrain(self):
        "Get positions of spikes in time trace"
        spike_positions = list()
        for pos,n in enumerate(self.voltages):
            if n == self.v_reset:
                # exact reset value is definitely 1 step after a spike
                spike_positions.append(pos)
        return spike_positions
        
    def getISI(self):
        "Return inter-spike intervals of the voltage train"
        before = 0; ISI = 0; ISIs = list()
        for pos,n in enumerate(self.voltages):
            if n == self.v_reset: # reset after a spike
                ISI = pos - before;
                ISIs.append(ISI);
                before = pos;                
        return ISIs
                
    def getVoltageTrain(self):
        "Result voltages"
        return self.voltages
        
    def whoAreYou(self):
        "Returns the consecutive number of the neuron"
        return self.neuronnumber
        
class SimpleNetwork() :
    "Network of SimpleNeurons"
    
    def __init__(self,size) :
        "Create Network with fixed size"
        self.matrix = [numpy.random.randint(0,2,5),numpy.random.randint(0,2,5),\
                        numpy.random.randint(0,2,5),numpy.random.randint(0,2,5),numpy.random.randint(0,2,5)]       
        
Neuron1 = SimpleNeuron(1,-60,0,-80,-70,20,3,5,10,-70,-50,0.06)

# paramters
Hz = 20;
duration = 10;
rangee = 1000 * duration;
weights = 2.0;

exc_activity_vector = [weights]*Hz*duration + [0]*(1000-Hz)*duration;
numpy.random.shuffle(exc_activity_vector)

inh_activity_vector = [weights]*Hz*duration + [0]*(1000-Hz)*duration;
numpy.random.shuffle(inh_activity_vector)
for step in range(0,rangee,1):
    Neuron1.excite(exc_activity_vector[step])
    #Neuron1.inhibit(inh_activity_vector[step])
    Neuron1.updateVoltage()

# plotting        
#plt.plot(Neuron1.getVoltageTrain())
#plt.xlabel('Time [ms]')
#plt.ylabel('Voltage [mV]')
#plt.axis([0,10000,-75,-45])

plt.figure(2)
#SRAS = Neuron1.getSRA()
#plt.plot(SRAS)
#plt.xlabel('Simualtion time [ms]')
#plt.ylabel('SRA conducatance [a.u.]')

ISIs = Neuron1.getISI()
plt.hist(ISIs)
print(stat.stdev(ISIs)/stat.mean(ISIs)) # sample or population deviation
plt.xlabel('ISI [ms]')
plt.ylabel('Amount [#]')