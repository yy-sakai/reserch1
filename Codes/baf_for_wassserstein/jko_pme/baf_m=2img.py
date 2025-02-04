import numpy as np
import matplotlib.pyplot as plt

image_root = "../images/baf_tau/"

img_tau000625 = np.load(f"{image_root}tau=0.00625.npy")
# img_tau00125 = np.load(f'{image_root}tau=0.0125.npy')
img_tau0025 = np.load(f"{image_root}tau=0.025.npy")
# img_tau005 = np.load(f'{image_root}tau=0.05.npy')
img_tau01 = np.load(f"{image_root}tau=0.1.npy")
# img_tau02 = np.load(f'{image_root}tau=0.2.npy')
img_tau04 = np.load(f"{image_root}tau=0.4.npy")
img_exact = np.load(f"{image_root}exact.npy")

x = np.linspace(-0.5, 0.5, 513)
h = x[1] - x[0]
t = [0, 0.4, 0.8, 2]

plt.ylim([-0.1, 15.1])
for i in range(4):
    plt.ylim([-0.1, 15.1])
    plt.xlim([-0.23, 0.23])
    plt.plot(x, img_exact[i], "--", label=r"$exact$")
    plt.plot(x, img_tau04[i], label=r"$\tau = 0.4$")
    # plt.plot(x, img_tau02[i],label=r'$\tau = 0.2$')
    plt.plot(x, img_tau01[i], label=r"$\tau = 0.1$")
    # plt.plot(x, img_tau005[i],label=r'$\tau = 0.05$')
    plt.plot(x, img_tau0025[i], label=r"$\tau = 0.025$")
    # plt.plot(x, img_tau00125[i],label=r'$\tau = 0.0125$')
    plt.plot(x, img_tau000625[i], label=r"$\tau = 0.00625$")
    plt.legend()
    plt.savefig(f"{image_root}t={t[i]}.png")
    plt.close()

print(f"Plots saved in {image_root}")
