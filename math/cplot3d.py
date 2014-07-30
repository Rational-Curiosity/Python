def cplot3d(expr, xlim = [-1, 1], ylim = [-1, 1], points = 50, style = "real-imag"):
    # Adaptado de http://ask.sagemath.org/question/9843/3d-complex-function-plot/
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    import matplotlib.pyplot as plt
    from numpy import arange, array, meshgrid, abs, size, absolute, angle
    from sympy import Symbol, lambdify

    if hasattr(expr, 'atoms'):
        var = list(expr.atoms(Symbol))[0]
        Fz=lambdify(var, expr, 'numpy')
    else:
        Fz=expr

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = arange(xlim[0], xlim[1], (xlim[1]-xlim[0])/(points-1))
    Y = arange(ylim[0], ylim[1], (ylim[1]-ylim[0])/(points-1))
    X, Y = meshgrid(X, Y)
    R=Fz(X + 1j*Y)
    if style == "abs-angle":
        Z = absolute(R)
        T = angle(R)
        N = (T - T.min())/(T.max() - T.min())  # normalize 0..1
        zlabel = "abs(f(z))"
        keyhue = "arg(f(z))"
    elif style == "real-angle":
        Z = R.real
        T = angle(R)
        N = (T - T.min())/(T.max() - T.min())  # normalize 0..1
        zlabel = "Re(f(z))"
        keyhue = "arg(f(z))"
    elif style == "angle-real":
        Z = angle(R)
        T = R.real
        N = (T - T.min())/(T.max() - T.min())  # normalize 0..1
        zlabel = "arg(f(z))"
        keyhue = "Re(f(z))"
    elif style == "real-imag":
        Z = R.real
        T = R.imag
        N = (T - T.min())/(T.max() - T.min()) #abs(T/T.max())  # normalize 0..1
        zlabel = "Re(f(z))"
        keyhue = "Im(f(z))"
    plt.title(' $\mathrm{f(z)}$')
    ax.set_xlabel(' $\mathrm{Re(z)}$')
    ax.set_ylabel(' $\mathrm{Im(z)}$')
    ax.set_zlabel(' $\mathrm{'+zlabel+'}$')
    surf = ax.plot_surface(
        X, Y, Z, rstride=1, cstride=1,
        facecolors=cm.jet(N),
        linewidth=0, antialiased=True, shade=False)
    # Colorbar see http://stackoverflow.com/a/6601210
    m = cm.ScalarMappable(cmap=cm.jet, norm=surf.norm)
    m.set_array(T)
    p=plt.colorbar(m)
    p.set_label(' $\mathrm{'+keyhue+'}$')

    #fig.set_size_inches(14,7) #http://stackoverflow.com/questions/332289/how-do-you-change-the-size-of-figures-drawn-with-matplotlib
    #plt.show() # if you run it as a python script

