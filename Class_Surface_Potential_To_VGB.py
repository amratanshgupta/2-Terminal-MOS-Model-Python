import numpy as np
import matplotlib.pyplot as plt
import math as m
import random
from Mathematical_functions import diff
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())


class Surface_Potential_To_VGB():
    vt = 25.8e-3
    phi = 0.05
    ni = 1.5e10
    vt = 25.8e-3
    phi = 0.05
    delta = 0.001
    vt = 25.8e-3
    vfb = 0.0
    ni = 1.5e10
    eps = 8.854e-14 * (11.8)
    epox = 8.854e-14 * (3.9)

    def __init__(self, tox, gamma, Vgb_max, Na=1e17):
        vt = 25.8e-3
        eps = 8.854e-14 * (11.8)
        epox = 8.854e-14 * (3.9)

        self.tox = tox
        self.Cox = epox / self.tox
        self.gamma = gamma
        self.Na = Na
        self.Vgb_max = Vgb_max
        self.phi_list = []
        self.Vgb_list = []
        self.Vgb_regions = []
        self.phi_regions = []
        self.phi_vgb_map = {}
        self.count = 0
        self.phi_f = vt * m.log(self.Na / Surface_Potential_To_VGB.ni)

    def Psi_to_VGB(self):
        vt = 25.8e-3
        epox = 8.854e-14 * (3.9)
        eps = 8.854e-14 * (11.8)
        delta = 0.001
        phi = 0.05

        self.Vgb = np.array(np.linspace(0, self.Vgb_max, 500))
        self.phi_regions = [self.phi_f, 2 * self.phi_f, (2 * self.phi_f) + (5 * vt)]
        # print(self.phi_regions)
        self.count = 0
        if (phi - vt) > 0:

            for j in self.Vgb:
                if self.count == 0:
                    phi = random.uniform((Surface_Potential_To_VGB.vfb * 0.1) + 1.25, (Surface_Potential_To_VGB.vfb * 0.1) + 1.35)
                    self.count = self.count + 1
                else:
                    phi = self.phi_list[-1]

                while 1:
                    first = m.sqrt(abs((vt * m.exp(-phi / vt) + (phi - vt) + (m.exp((-2 * self.phi_f) / vt) * ((vt * m.exp(phi / vt)) - phi - vt)))))
                    # print(f'first: {first:.4f}')
                    second = m.sqrt(abs(vt * m.exp(-(phi + delta) / vt) + (phi + delta - vt) + m.exp((-2 * self.phi_f) / vt) * ((vt * m.exp((phi + delta) / vt)) - (phi + delta) - vt)))
                    # print(f'second: {second:.4f}')

                    f1 = ((self.gamma * first) + phi + (Surface_Potential_To_VGB.vfb)) - j
                    f2 = ((self.gamma * second) + (phi + delta) + (Surface_Potential_To_VGB.vfb)) - j

                    test = phi - 0.1 * (f1 / diff(f2, f1, delta))
                    # print(f"Test Value: {test}")

                    if (abs((test - phi)) / phi) < 1e-2 and abs(f1) < 1e-3:
                        # print(f" ==  break_out === {break_out}")
                        break_out = break_out + 1

                        if break_out > 2:
                            break_out = 0
                            if abs(test - self.phi_f) < 2.75e-3 or abs(test - 2 * self.phi_f) < 2.07e-3 or abs(test - ((2 * self.phi_f) + 5 * vt)) < 1.5e-3:
                                self.Vgb_regions.append(j)
                            break

                    else:
                        phi = test
                        break_out = 0
                        # print('======= phi = Test  ==========')

                self.phi_list.append(test)
                self.Vgb_list.append(j)

        else:
            phi = phi + 0.001

        self.phi_list = np.array(self.phi_list)
        self.Vgb_list = np.array(self.Vgb_list)

        for i, j in zip(self.phi_list, self.Vgb_list):
            self.phi_vgb_map[i] = j
        # print(self.phi_vgb_map)
        return (self.Vgb_regions, self.phi_vgb_map, self.phi_regions)
#=====================================================================

    def Plot_Psi_Vs_VGB(self):
        vt = 25.8e-3

        plt.plot(self.Vgb_list, self.phi_list)
        plt.title('Surface Potential  vs  Gate-Body Voltage for 2-Terminal MOS')

        #######  Lines and Labels ######
        ##  X & Y Axis ###
        plt.axhline(y=0, xmin=0.0, xmax=1.0, color='k')
        plt.axvline(x=0, ymin=0.0, ymax=1.0, color='k')
        ##### Axes Scale Limits ##
        plt.ylim(0,)
        # plt.xlim(0,)
        #####

        plt.annotate("Depletion", xy=((self.Vgb_regions[0] - 0.5, (self.phi_f - 0.25))))
        plt.annotate("Weak\nInversion", xy=((self.Vgb_regions[1] - 0.65, (self.phi_f + 0.025))))
        plt.annotate("Moderate\nInversion", xy=((self.Vgb_regions[2] - 0.65, (2 * self.phi_f + 0.01))))
        plt.annotate("Strong\nInversion", xy=((self.Vgb_regions[2] + 0.76, (2 * self.phi_f + 0.135))))

        plt.axhline(y=(2 * self.phi_f) + (5 * vt), color='g', linestyle='--')
        plt.axhline(y=2 * self.phi_f, color='g', linestyle='--')
        plt.axhline(y=self.phi_f, color='g', linestyle='--')

        plt.axvline(x=self.Vgb_regions[0], color='#968F8F', linestyle='--')
        plt.axvline(x=self.Vgb_regions[1], color='#968F8F', linestyle='--')
        plt.axvline(x=self.Vgb_regions[2], color='#968F8F', linestyle='--')

        # print(u"$V_{L0}$", end=' ')
        # print("= {}".format(self.Vgb_regions[0]))

        # print(r"$V_{M0}$", end=' ')
        # print("= {}".format(self.Vgb_regions[1]))

        # print(r"$V_{H0}$", end=' ')
        # print(" = {}".format(self.Vgb_regions[2]))

        plt.xlabel(r'$V_{GB}$ (V)')
        plt.ylabel('Surface Potential (V)')
        # plt.text(Vgb_regions[2] - vfb, phi_f + 0.1, r'$V_{FB}$ = - 1.0 V')

        plt.text(self.Vgb_regions[0] - Surface_Potential_To_VGB.vfb, 0.1, r'$V_{L0}$ =' + '{:.3f} V'.format(self.Vgb_regions[0]))
        plt.text(self.Vgb_regions[1] - Surface_Potential_To_VGB.vfb, 0.1, r'$V_{M0}$ =' + '{:.3f} V'.format(self.Vgb_regions[1]))
        plt.text(self.Vgb_regions[2] - Surface_Potential_To_VGB.vfb, 0.1, r'$V_{H0}$ =' + '{:.3f} V'.format(self.Vgb_regions[2]))

        plt.text(0, self.phi_f + 0.01, r'$\phi_{F}$ =' + '{:.3f} V'.format(self.phi_f))
        plt.text(0, (2 * self.phi_f) + 0.01, r'$2 \phi_{F}$ =' + '{:.3f} V'.format(2 * self.phi_f))
        plt.text(0, (2 * self.phi_f + 5 * vt) + 0.01, r'$2 \phi_{F} + 5V_t$ =' + '{:.3f} V'.format(2 * self.phi_f + 5 * vt))
        plt.text(self.Vgb_max - 1, self.phi_f + 0.01, r'$V_{FB}$ =' + '{:.2f} V'.format(Surface_Potential_To_VGB.vfb))
        # plt.legend()
        plt.show()
        return None
        # print('-' * 10 + "END" + '-' * 10)


if __name__ == "__main__":
    tox = 40e-7
    Na = 1e17
    q = 1.6e-19
    eps = 8.854e-14 * (11.8)
    epox = 8.854e-14 * (3.9)
    Cox = epox / tox
    Vgb_max = 7
    gamma = ((m.sqrt(2 * q * eps * Na)) / Cox)

    x = Surface_Potential_To_VGB(tox, gamma, Vgb_max, Na)
    a, b, c = x.Psi_to_VGB()
    # print(c)

    y = x.Plot_Psi_Vs_VGB()
