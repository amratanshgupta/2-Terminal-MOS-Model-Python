import numpy as np
import matplotlib.pyplot as plt
import math as m
import random
from Mathematical_functions import diff
from Class_Surface_Potential_To_VGB import Surface_Potential_To_VGB
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())


class Total_charge_VGB(Surface_Potential_To_VGB):
    """Returns Inversion charge, Depletion Charge, Total Charge in 2-Terminal MOS"""
    vt = 25.8e-3
    q = 1.6e-19
    eps = 8.854e-14 * (11.8)
    epox = 8.854e-14 * (3.9)
    ni = 1.5e10
    # Cox = epox / tox

    def __init__(self, tox, gamma, Vgb_max, Na=1e17):
        vt = 25.8e-3
        q = 1.6e-19
        eps = 8.854e-14 * (11.8)
        epox = 8.854e-14 * (3.9)
        Surface_Potential_To_VGB.__init__(self, tox, gamma, Vgb_max, Na=1e17)
        self.phi_f = vt * m.log(self.Na / Surface_Potential_To_VGB.ni)
        self.Na = Na
        self.Qtotal = []
        self.Qinv = []
        self.Qdep = []
        self.VGB_QTotal = {}
        self.VGB_Qdep = {}
        self.VGB_Qinv = {}
        self.VGB_Qinv_list = []

        self.Surface_Potential, self.phi_vgb_map, self.phi_regions = Surface_Potential_To_VGB.Psi_to_VGB(self)
        # print(self.phi_vgb_map)

    def Total_Charge(self):
        self.Qtotal = []
        vt = 25.8e-3
        q = 1.6e-19
        eps = 8.854e-14 * (11.8)
        epox = 8.854e-14 * (3.9)
        for k in self.phi_vgb_map.keys():
            first = m.sqrt(abs((vt * m.exp(-k / vt)) + (k - vt) + (m.exp((-2 * self.phi_f) / vt) * ((vt * m.exp(k / vt)) - k - vt))))
            if k >= 0:
                Q_total = -1 * first * (m.sqrt(2 * q * eps * self.Na))
                self.Qtotal.append(Q_total)
                mapped_VGB = self.phi_vgb_map[k]
                self.VGB_QTotal[mapped_VGB] = Q_total
                # self.VGB_QTotal[self.phi_vgb_map[k]] = Q_total

            elif k < 0:
                Q_total = first * (m.sqrt(2 * q * eps * self.Na))
                self.Qtotal.append(Q_total)
                mapped_VGB = self.phi_vgb_map[k]
                self.VGB_QTotal[mapped_VGB] = Q_total

        return(self.VGB_QTotal, self.Qtotal)

    def Qdepletion(self):
        self.Qdep = []
        vt = 25.8e-3
        q = 1.6e-19
        eps = 8.854e-14 * (11.8)
        epox = 8.854e-14 * (3.9)
        for k in self.phi_vgb_map.keys():
            first = m.sqrt(abs((vt * m.exp(-k / vt)) + (k - vt)))
            if k >= 0:
                Q_depletion = -1 * first * (m.sqrt(2 * q * eps * self.Na))
                self.Qdep.append(Q_depletion)
                mapped_VGB = self.phi_vgb_map[k]
                self.VGB_Qdep[mapped_VGB] = Q_depletion

            elif k < 0:
                Q_depletion = first * (m.sqrt(2 * q * eps * self.Na))
                self.Qdep.append(Q_depletion)
                mapped_VGB = self.phi_vgb_map[k]
                self.VGB_Qdep[mapped_VGB] = Q_depletion
        # print(f'Qdep {len(self.Qdep)}', f'{len(self.Surface_Potential_Qdep.keys())}')
        return(self.VGB_Qdep, self.Qdep)

    def Qinversion(self):
        self.Qinv = []
        vt = 25.8e-3
        q = 1.6e-19
        eps = 8.854e-14 * (11.8)
        epox = 8.854e-14 * (3.9)
        # for k in self.phi_vgb_map.keys():
        #     vt = 25.8e-3
        #     first = abs(m.sqrt(abs(((m.exp((-2 * self.phi_f) / vt) * ((vt * m.exp(k / vt)) - k - vt)) - vt))) - m.sqrt(abs(k - vt)))
        #     Q_inv = -1 * first * (m.sqrt(2 * q * eps * Na))
        #     self.Qinv.append(Q_inv)
        #     self.Surface_Potential_Qinv[k] = Q_inv

        # for i, j in zip(self.Surface_Potential_Qinv.keys(), self.Qinv):
        #     print(i, j, end='\n')
        # return(self.Surface_Potential_Qdep, self.Qinv)
        (Qdep_dic, Qdep_list) = Total_charge_VGB.Qdepletion(self)
        (Qtotal_dic, Qtotal_list) = Total_charge_VGB.Total_Charge(self)

        for (i, j) in zip(Qtotal_list, Qdep_list):
            k = (i * 1e7) - (j * 1e7)
            Q_inver = k * 1e-7
            self.Qinv.append(Q_inver)

        for var in Qdep_dic.keys():
            self.VGB_Qinv_list.append(var)

        # print(f'Qinv: {len(self.Qinv)}', f'{len(self.Surface_Potential_Qinv_list)}')
        return(self.VGB_Qinv_list, self.Qinv)

    def Plot_Q_vs_VGB(self):
        # Total_charge_VGB_Surface_Potential.Qdepletion(self)
        # Total_charge_VGB_Surface_Potential.Qinversion(self)

        plt.plot(self.VGB_Qinv_list, self.Qinv, 'r')
        plt.plot(self.VGB_Qdep.keys(), self.Qdep, 'g')
        plt.plot(self.VGB_QTotal.keys(), self.Qtotal, 'b', linestyle=':')
        plt.title(r'Total Semiconductor Charge($Q_{SC}$) vs  Gate-Body bias for 2-Terminal MOS')
        plt.ylabel(r'$Q_{Total}$ (C)')
        plt.xlabel(r'$V_{GB}$ (V)')
        plt.legend([r'$Q_{inv}$', r'$Q_{dep}$', r'$Q_{sc}$'])
        plt.ticklabel_format(style='sci', axis='y', scilimits=(1, 4))

        plt.axvline(x=0, ymin=0.0, ymax=1.0, color='k')
        plt.axhline(y=0, xmin=0.0, xmax=1.0, color='k')
        plt.show()


if __name__ == "__main__":
    Na = 1e17
    q = 1.6e-19
    tox = 40e-7
    eps = 8.854e-14 * (11.8)
    epox = 8.854e-14 * (3.9)
    Cox = epox / tox
    Vgb_max = 5.5
    gamma = ((m.sqrt(2 * q * eps * Na)) / Cox)

    x = Total_charge_VGB(tox, gamma, Vgb_max, Na)
    y = x.Total_Charge()
    z = x.Qinversion()
    v = x.Qdepletion()

    b = x.Plot_Q_vs_VGB()
