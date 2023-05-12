import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
from c_transform import c_transform
from jacobs import push_forward1
from push_forward import lap_solve

# Wasserstein distance \int \phi d\nu + \int \phi^c d\mu
def w2(phi, psi, mu, nu):
    return np.sum(phi * nu + psi * mu)


#  every ascent step
def update_sigma(diff, H1_sq, sigma):
    if diff < 0.:
        sigma *= 0.1
    elif diff > H1_sq * sigma * upper:
        sigma *= scaleUp
    elif diff < H1_sq * sigma * lower:
        sigma *= scaleDown
    return sigma

# ascent step of J(phi) = \int phi dnu + \int phi^c dmu
# fills phi and phi_c, returns new sigma
def ascent(phi, phi_c, mu, nu, sigma):
    #phi_c[:] = phi
    phi_c, _ = c_transform(x, phi, x)                        # 1-1  phi_c, _ = c_transform(x, phi, p)

    old_J = w2(phi, phi_c, mu, nu)  

    pfwd = push_forward1(mu, phi_c, h)              # 1-2-1     pfwd : T_{\phi\#}\mu = x - (\nabla h)^{-1}(\nabla\phi^c(x)) = x - \nabla\phi^c(x)
    rho = nu - pfwd                                 # 1-2-2     rho = \nu - T_{\phi\#}\mu
    # TODO: This is by far the slowest part of the algorithm
    lp = lap_solve(rho)                             # 1-2-3     lp: \nabla_{\dot{H}^1} J(\phi_n) = (- \Delta)^{-1} * rho
    phi += sigma * lp                               # 1-2-4   phi_{n + 1/2} = phi_n + sigma * lp
#####################################################################
    #phi_c[:] = phi                                 
    phi_c, _ = c_transform(x, phi, x)                    # 2    psi_{n + 1/2} = (phi_{n + 1/2})^c
    J = w2(phi, phi_c, mu, nu)
    H1_sq = np.mean(rho * lp)                        #######       ?
    return update_sigma(J - old_J, H1_sq, sigma), J, H1_sq, phi, phi_c, pfwd   #  ?


###########################################################################################


def update(fig1, fig2, title):
    my_line.set_data(fig1, fig2, title)

scaleDown = 0.5  # \alpha_2
scaleUp   = 1 / scaleDown # \alpha_1
upper = 0.75     # \beta_2
lower = 0.25     # \beta_1

sigma = 200.
sigma1 = sigma
sigma2 = sigma
J = 0
H1_sq = 0
common_sigma = False




x = np.linspace(-1, 1, 1001)
p = x

mu = np.exp(-(x - 0.5)**2 * 100)   #e^(-(x-0.5)^2 * 100)    #True: 1. False: 0.
mu /= np.sum(mu)                   # mu = mu / np.sum(mu)
nu = np.exp(-(x + 0.2)**2 * 100) + np.exp(-(x+0.7)**2 * 100)
nu /= np.sum(nu) 

phi = np.zeros_like(x)
psi = np.zeros_like(x)  

h = x[1] - x[0]

fig, ax = plt.subplots()
artists = []


ax.set_xlim(-1,1)
ax.set_ylim(-0.0001,0.02) 

for k in range(100):
    #plt.title(r'back-and-forth update $\mu$ and $\nu$. Example 1:  Iterate ' + str(k+1))
    title = ax.text(0.5, 1.01, f"back-and-forth update $\mu$ and $\nu$. Example 2:  Iterate {str(k+1)}")
    
    sigma1, J, H1_sq, phi, psi, pfwd  = ascent(phi, psi, mu, nu, sigma1)
    print(sigma1)
    print(H1_sq)
    print(J)
    if common_sigma:
        sigma2 = sigma1
    img2, = ax.plot(x, pfwd, color='blue')
    
    
    sigma2, J, H1_sq, psi, phi, pfwd = ascent(psi, phi, nu, mu, sigma2)
    if common_sigma:
        sigma1 = sigma2
        
    img1, = ax.plot(x, pfwd, color='red')
    
    
    if k % 1 == 0:
        #plt.xlim(-1,1)
        #plt.ylim(-0.0001,0.02) 
        # plt.legend(prop={'size': 15})
        # plt.show()

        #ax.legend(prop={'size': 15})
        artists.append([img1] + [img2] + [title])
        
anim = ArtistAnimation(fig, artists, interval=100, repeat_delay=1000)
plt.show()
    
"""
for k in range(300):
    phi_c, _ = c_transform(x, phi, p)                                 #1-1
    phi += sigma * lap_solve(nu - push_forward1(mu, phi_c, h))        #1-2      phi_{n + 1/2} = phi_n + sigma * 
    psi, _ = c_transform(x, phi, p)                                   #2        psi_{n + 1/2} = (phi_{n + 1/2})^c
    
    psi_c, _ = c_transform(x, psi, p)                                 #3-1
    psi += sigma * lap_solve(mu - push_forward1(nu, psi_c, h))        #3-2
    phi, _ = c_transform(x, psi, p)                                   #4        phi_{n + 1} = (psi_{n + 1})^c
    
    title = ax.text(4.5, 1.15, 'back-and-forth update $\mu$ and $\nu$. Example 2:  Iterate {}'.format(str(k+1)))
    img1, = ax.plot(x, push_forward1(nu, psi_c, h), color='red',label=r'$T_{\phi \#} \mu$')
    img2, = ax.plot(x, push_forward1(mu, phi_c, h), color='blue', label=r'$T_{\psi \#} \nu$')
    
    if k % 1 == 0:
        ax.legend(prop={'size': 15})
        artists.append([img1, img2, title])
    
ani = animation.ArtistAnimation(fig, artists, interval=2, repeat_delay=1000)
plt.show()

"""