import numpy as np
import matplotlib.pyplot as plt
sigma = 15
x = sigma * np.random.randint(5, size =10)
# the histogram of the data
n, bins, patches = plt.hist(x, 50, facecolor='g', alpha=0.75)
print(x)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .030, r'$\mu=100,\ \sigma=15$')
plt.text(50, .033, r'$\varphi_{\mu,\sigma^2}(x) = \frac{1}{\sigma\sqrt{2\pi}} \,e^{ -\frac{(x- \mu)^2}{2\sigma^2}} = \frac{1}{\sigma} \varphi\left(\frac{x - \mu}{\sigma}\right),\quad x\in\mathbb{R}$', fontsize=20, color='red')
plt.axis([0, 160, 0, 100])
plt.grid(True)
plt.show()
