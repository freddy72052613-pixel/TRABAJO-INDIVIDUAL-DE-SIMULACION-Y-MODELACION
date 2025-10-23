import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from random_generators import RandomGenerators

def plot_histogram(data, ax, bins=50, title='', xlabel='x'):
    ax.clear()
    ax.hist(data, bins=bins, density=True, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Densidad')

class DistribucionesApp:
    def __init__(self, root):
        self.root = root
        root.title('Generador de Distribuciones Aleatorias')
        root.geometry('1000x600')

        left = ttk.Frame(root)
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(root)
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        ttk.Label(left, text='Distribución:').pack(anchor='w')
        self.dist_var = tk.StringVar(value='normal')
        dists = ['uniform','exponential','erlang','gamma','normal','weibull','bernoulli','binomial','poisson']
        self.dist_combo = ttk.Combobox(left, values=dists, textvariable=self.dist_var, state='readonly')
        self.dist_combo.pack(fill='x')

        ttk.Label(left, text='Tamaño (n):').pack(anchor='w')
        self.dist_size = tk.IntVar(value=1000)
        ttk.Entry(left, textvariable=self.dist_size).pack(fill='x')

        ttk.Label(left, text='Parámetros (coma separados):').pack(anchor='w', pady=(10,0))
        self.params_entry = ttk.Entry(left)
        self.params_entry.insert(0, 'mu=0,sigma=1')
        self.params_entry.pack(fill='x')

        ttk.Button(left, text='Generar y graficar', command=self._generate_and_plot).pack(fill='x', pady=5)

        fig = Figure(figsize=(7,5))
        self.ax = fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(fig, master=right)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def _parse_params(self, text):
        d = {}
        if not text:
            return d
        parts = [p.strip() for p in text.split(',') if p.strip()]
        for p in parts:
            if '=' in p:
                k, v = p.split('=',1)
                try:
                    d[k.strip()] = float(v)
                except:
                    try:
                        d[k.strip()] = int(v)
                    except:
                        d[k.strip()] = v
        return d

    def _generate_and_plot(self):
        dist = self.dist_var.get()
        n = max(1, int(self.dist_size.get()))
        params = self._parse_params(self.params_entry.get())
        try:
            if dist == 'uniform':
                a = params.get('a', 0.0)
                b = params.get('b', 1.0)
                data = RandomGenerators.uniform(a=a,b=b,size=n)
                plot_histogram(data, self.ax, bins=50, title=f'Uniforme U({a},{b})')
            elif dist == 'exponential':
                lam = params.get('lam', params.get('lambda',1.0))
                data = RandomGenerators.exponential(lam=lam,size=n)
                plot_histogram(data, self.ax, bins=50, title=f'Exponencial (λ={lam})')
            elif dist == 'erlang':
                k = int(params.get('k',2))
                lam = params.get('lam',1.0)
                data = RandomGenerators.erlang(k=k,lam=lam,size=n)
                plot_histogram(data, self.ax, bins=50, title=f'Erlang k={k}, λ={lam}')
            elif dist == 'gamma':
                shape = params.get('shape',2.0)
                scale = params.get('scale',1.0)
                data = RandomGenerators.gamma(shape=shape, scale=scale, size=n)
                plot_histogram(data, self.ax, bins=50, title=f'Gamma(shape={shape}, scale={scale})')
            elif dist == 'normal':
                mu = params.get('mu',0.0)
                sigma = params.get('sigma',1.0)
                data = RandomGenerators.normal(mu=mu,sigma=sigma,size=n)
                plot_histogram(data, self.ax, bins=50, title=f'Normal N({mu},{sigma**2})')
            elif dist == 'weibull':
                k = params.get('k',1.5)
                lam = params.get('lam',1.0)
                data = RandomGenerators.weibull(k=k,lam=lam,size=n)
                plot_histogram(data, self.ax, bins=50, title=f'Weibull k={k}, λ={lam}')
            elif dist == 'bernoulli':
                p = params.get('p',0.5)
                data = RandomGenerators.bernoulli(p=p,size=n)
                plot_histogram(data, self.ax, bins=2, title=f'Bernoulli p={p}')
            elif dist == 'binomial':
                nn = int(params.get('n',10))
                p = params.get('p',0.5)
                data = RandomGenerators.binomial(n=nn,p=p,size=n)
                plot_histogram(data, self.ax, bins=range(0,nn+2), title=f'Binomial n={nn}, p={p}')
            elif dist == 'poisson':
                lam = params.get('lam',1.0)
                data = RandomGenerators.poisson(lam=lam,size=n)
                plot_histogram(data, self.ax, bins=range(0,int(max(data))+2), title=f'Poisson λ={lam}')
            else:
                raise ValueError('Distribución no soportada')

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror('Error', f'Error generando la distribución: {e}')

def main():
    root = tk.Tk()
    app = DistribucionesApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()