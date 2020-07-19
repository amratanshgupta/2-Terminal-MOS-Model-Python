import numpy as np
import matplotlib.pyplot as plt
import math as m


def diff(f2, f1, delta):
    try:
        x = (f2 - f1) / (delta)
        # if x < 0:
        #     print(f"Differentition NEGATIVE")
        return x
    except ZeroDivisionError as e:
        print(f"{e} : Differentition Function Failed")

#==================================================================


def newton_raphson(phi, Vgb, tox=40e-7, Na=1e17):
    """ Return Surface Potential to corresponding values of Vgb using Newton-Raphson"""

    vt = 25.8e-3
    eps = 8.854e-14 * (11.8)
    ni = 1.5e10
    q = 1.6e-19
    epox = 8.854e-14 * (3.9)
    vt = 25.8e-3
    phi_f = vt * m.log(Na / ni)
    phi = 0.05
    delta = 0.001
    Cox = epox / tox
    gamma = ((m.sqrt(2 * q * eps * Na)) / Cox)

    count = 0
    Vgb_regions = []
    phi_list = []
    dic = {}
    phi_regions_Obtain = []
    Vgb_list = []

    if (phi - vt) > 0:

        for j in Vgb:
            # print(f"Vgb = {j}")
            if count == 0:
                phi = 0.75
                count = count + 1
            else:
                phi = phi_list[-1]

            while 1:

                # print(f"Starting Surface Potential {phi}")
                first = m.sqrt((phi - vt) + (m.exp((-2 * phi_f) / vt) * ((vt * m.exp(phi / vt)) - phi - vt)))
                second = m.sqrt((phi + delta - vt) + m.exp((-2 * phi_f) / vt) * ((vt * m.exp((phi + delta) / vt)) - (phi + delta) - vt))

                f1 = j - ((gamma * first) + phi + vfb)
                f2 = j - ((gamma * second) + (phi + delta) + vfb)

                # print(f"Difference : {f1}")

                test = phi - (f1 / diff(f2, f1, delta))
                # print(f"Test Value: {test}")

                if (abs((test - phi)) / phi) < 1e-1:
                    # print(f" ==  break_out === {break_out}")
                    break_out = break_out + 1

                    if break_out > 2:   # Two consecutive same value of Phi => Only then Convergence
                        break_out = 0
                        # print('=======break==========')
                        if abs(test - phi_f) < 1.3e-3 or abs(test - 2 * phi_f) < 9e-4 or abs(test - ((2 * phi_f) + 0.6)) < 7.5e-2:
                            Vgb_regions.append(j)
                            phi_regions_Obtain.append(test)

                        break

                else:
                    phi = test
                    break_out = 0
                    # print('======= phi = Test  ==========')

            # Phi and Vgb list (corresponding values)
            phi_list.append(test)
            Vgb_list.append(j)

    else:
        phi = phi + 0.001

    phi_list = np.array(phi_list)
    # print(phi_list)
    Vgb_list = np.array(Vgb_list)
    # print(Vgb_list)
    for (i, k) in zip(phi_list, Vgb_list):
        dic[k] = i

    return (phi_list, Vgb_list, dic, phi_regions_Obtain, Vgb_regions)
    # return surface potntial corresponding to Vgb
# ==================================================
