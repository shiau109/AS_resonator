

import sys
sys.path.append(r'c:\\Users\\shiau\\AS_resonator')
print(sys.path)


import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import simulation.model as md

Qi = 1e5
Qc = 1e5
res_bare = md.Resonator()
res_bare.f_r = 6.100
res_dress_g = md.Resonator()
res_dress_g.f_r = 6.101
res_dress_g.kappa_i = res_dress_g.f_r/Qi
res_dress_g.kappa_c = res_dress_g.f_r/Qc
res_dress_g.kappa = res_dress_g.kappa_i +res_dress_g.kappa_c
iso_q = md.SQUIDTransmonModel()
iso_q.f_q = 4.0
iso_q.anharmonicity = -0.2


simQ = md.SingleReadableTransmon()
simQ.bare_cavity = res_bare
simQ.dressed_cavity_g = res_dress_g
simQ.qubit = iso_q
simQ.g = 0.04
t_point = 10000
t = np.linspace(0,10000,t_point)
scan_point = 50
chi = simQ.get_chi_eff()

f_b_eff = res_dress_g.f_r +chi
f_dr_scan = f_b_eff + np.linspace( -5*chi, 5*chi, scan_point)

signal = np.empty((scan_point, t_point))
for i, f_dr in enumerate(f_dr_scan):
    print(res_dress_g.f_r)
    sol = simQ.qubit_resonator_evo( t, res_dress_g.f_r, iso_q.f_q, 1e-4, 0 )
    signal[i] = sol.y[0]

norm_f_dr_scan = (f_dr_scan-f_b_eff)/chi
mx,my=np.meshgrid(t, norm_f_dr_scan )

plt.figure(0)
plt.pcolormesh( mx, my, abs(signal) )
plt.colorbar()    

plt.figure(1)
plt.plot(sol.t, signal[24].real, label="I")
plt.plot(sol.t, signal[24].imag, label="Q")
plt.legend()

# plt.figure(1)
# plt.plot(sol.t, sol.y[7].real)
# plt.plot(sol.t, abs(sol.y[7]))

plt.show()