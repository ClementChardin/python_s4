import os.path as osp
import json
import numpy as np
import subprocess
from pylab import *
import itertools

DIR_NAME = osp.dirname(osp.abspath(__file__))
class PhC(object):
    def __init__(self,
                 lambda_x=0.830,
                 lambda_y=0.830,
                 angle_phi=0,
                 angle_theta=0,
                 s_polarization=1,
                 p_polarization=.0,
                 holeradius=0.293,
                 thickness_start=.2,
                 thickness_stop=.2,
                 n_thickness=1,
                 epsilon=1.99**2,
                 norders=20,
                 lambda_start=.9,
                 lambda_stop=1.2,
                 n_lambdas=300):
        n_thickness_minus_1 = max(1, n_thickness - 1)
        thickness_range = max(thickness_stop-thickness_start, 1e-10)

        self.lambda_start = lambda_start
        self.lambda_stop = lambda_stop
        self.n_lambdas = n_lambdas

        self.params = dict(lambda_x=lambda_x,
                           lambda_y=lambda_y,
                           angle_phi=angle_phi,
                           angle_theta=angle_theta,
                           s_polarization=s_polarization,
                           p_polarization=p_polarization,
                           holeradius=holeradius,
                           thickness_start=thickness_start,
                           thickness_stop=thickness_stop,
                           thickness_step=(thickness_range)/n_thickness_minus_1,
                           epsilon=epsilon,
                           norders=norders,
                           lambda_start = lambda_start,
                           lambda_stop = lambda_stop)
        
    def calculate_with_sampler(self):
        """dumps the json first"""
        self.calculate()
 #       results = []
            #print "calculating lambda=" + str(lambda_um)
        with open(osp.join(DIR_NAME, "params.json"),"w") as f:
            json.dump(self.params, f)           
        process = subprocess.Popen([osp.join(DIR_NAME, "S4.exe"), osp.join(DIR_NAME, "sampler.lua")], shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode:
            raise ValueError("S4 didn't return code 0")
        self.results = np.loadtxt(osp.join(DIR_NAME, "tempfile.txt"))
   #     if len(self.dat.shape) == 1:
  #          results.append(self.dat[1:])
 #       else:
#            results.append(self.dat)
#        self.results = results
        return np.array(self.results)

    def calculate(self):
        """dumps the json first"""
        results = []
        for lambda_um in np.linspace(self.lambda_start, self.lambda_stop, self.n_lambdas):
#            print "calculating lambda=" + str(lambda_um)
            self.params["lambda_um"] = lambda_um
            with open(osp.join(DIR_NAME, "params.json"),"w") as f:
                json.dump(self.params, f)
        
            process = subprocess.Popen([osp.join(DIR_NAME, "S4.exe"), osp.join(DIR_NAME, "PhC.lua")], shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode:
                raise ValueError("S4 didn't return code 0")
            dat = np.loadtxt(osp.join(DIR_NAME, "tempfile.txt"))
            if len(dat.shape) == 1:
                results.append(dat[1:])
            else:
                results.append(dat[:,1])
            self.results = results
        return results

def plot_different_angles_phi(angle_start, angle_stop, angle_step):
    i = 0
    o = PhC()
    x = np.linspace(o.lambda_start, o.lambda_stop, o.n_lambdas)
    N_angles = (angle_stop - angle_start) / angle_step

    color_cycle = itertools.cycle(plt.cm.spectral(np.linspace(0,1,N_angles)))
 #   for i in range(10):
#        plot(x,scipy.special.jv(i,x),color=color_cycle.next())
    
    for angle in range(angle_start, angle_stop + angle_step, angle_step):
        o.params["angle_phi"] = angle
        print(o.params["angle_phi"])
        res = o.calculate()
        y = np.array([res[k][0] for k in range(0,len(res))])
        plot(x, y + i,color=color_cycle.next(), label = "angle = " + str(angle))
        plot(x, [i]*len(x), ':k')
        i = i+1
    plot(x, [i]*len(x), ':k')
    legend()


def plot_different_angles_phi_sampler(angle_start, angle_stop, angle_step):
    i = 0
    o = PhC()
    
    for angle in range(angle_start, angle_stop + angle_step, angle_step):
        o.params["angle_phi"] = angle
        print(o.params["angle_phi"])
        res = o.calculate_with_sampler()
        y = 1-res[:,1]#[res[k][0] for k in range(0,len(res))]
        x = res[:,0]
        plot(x, y + i, label = "angle = " + str(angle))
#        plot([i]*len(x), ':k')
        i = i+1
#    plot([i]*len(x), ':k')
    legend()


