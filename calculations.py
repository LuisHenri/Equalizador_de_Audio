import numpy as np
import sympy

# GRAVE
if __name__ == "__main__":
    f_p1 = 115
    f_p2 = 600
    f_s1 = 15
    f_s2 = 700
    A_max = 2
    A_min = 10

    w_p1 = 2*np.pi*f_p1
    w_p2 = 2 * np.pi * f_p2
    w_s1 = 2 * np.pi * f_s1
    w_s2 = 2 * np.pi * f_s2

    w_0 = np.sqrt(w_p2 * w_p1)

    # PB Normalizado
    _w_p = w_p2
    _w_s = (w_s2 - w_s1) / (w_p2 - w_p1)

    _w = (pow(_w_s, 2) * pow(w_0, 2)) / ((w_p2 - w_p1) * _w_s)

    print(_w_s)
    e_ripple = np.sqrt(10**(A_max/10) - 1)
    print(e_ripple)

    A_w = 0
    n = 0
    while A_w < A_min:
        n += 1
        A_w = 10 * np.log(1 + e_ripple**2 * _w_s**(2*n))

    print(n, A_w)

    polos_reais = []
    polos_imags = []
    for i in range(n):
        k = i + 1
        p = e_ripple**(-1/n) * np.sin(((2*k - 1) * np.pi) / (2*n))
        pj = e_ripple**(-1/n) * np.cos(((2*k - 1) * np.pi) / (2*n))
        polos_reais.append(round(p, 2))
        polos_imags.append(round(pj, 2))
        print(f"Polo {i}: {p} + {pj}j")

    polos = []
    for i in range(len(polos_reais)):
        polos.append(complex(polos_reais[i], polos_imags[i]))
    print(f"Polos: {polos}")

    s1 = polos[0] + polos[1]
    s2 = polos[0] * polos[1]
    print(f"Função de atenuação normalizada A(_s) = "
          f"(s^2 - s({s1}) + {s2}")

    x, s, _s, g_0 = sympy.symbols("x s _s g_0")
    A__s = (_s - polos[0]) * (_s - polos[1])
    A__S = sympy.expand(A__s)
    print("A__s:", A__s)

    _s2 = (s**2 + w_0**2) / ((w_p2 - w_p1) * s)
    # print(_s2.subs(s, 0))

    A_s = A__s.subs(_s, _s2)
    # A_s = sympy.simplify(A_s)
    print(f"A_s: {A_s}")

    # print(A_s.subs(s, 0))

    T_s = (1 / A_s) * g_0
    print("T_s:", T_s)
    # print(T_s.subs(s, 0))

    # if n%2 == 0: #par

    result = pow(1 + e_ripple**2, -1/2)

    po = T_s - 1
    po = sympy.simplify(po)
    print(po)
    tmp = po.subs(s, 0)
    print(tmp)
    aux = sympy.solve(tmp, g_0)
    print(aux)

    # else:
    #     po = T_s - 1
    #
    #     tmp = po.subs(s, 0)
    #
    #     aux = sympy.solve(tmp, g_0)
    #     print(aux)




    # TODO:
    #  - A(_s) com sympy
    #  - A(s)
    #  - G0
