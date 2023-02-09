from datetime import date
import json
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from collections import Counter


categories = ["dm", "dr", "lm", "lr", "sm", "sr", "bib", "sol", "hind", "melo", "rec"]
dates = []
total = []
dm = []
dr = []
lm = []
lr = []
sm = []
sr = []
bib = []
sol = []
hind = []
melo = []
rec = []

def refresh_data():
    uso = json.load(open("usage.json"))
    dates.clear()
    total.clear()
    for j in categories:
        eval(j).clear()
    for i in uso:
        dates.append(i)
        counter = Counter()
        counter.update(uso[i])
        for j in categories:
            if j not in counter:
                eval(j).append(0)
            else:
                eval(j).append(counter[j])
    for i, j, k, l, m, n, o, p, q, r, s in zip(dm, dr, lm, lr, sm, sr, bib, sol, hind, melo, rec):
        total.append(i + j + k + l + m + n + o + p + q + r + s)

    cat_sum = [sum(dm), sum(dr), sum(lm), sum(lr), sum(sm), sum(sr), sum(bib), sum(sol), sum(hind), sum(melo), sum(rec)]
    return cat_sum

def new_json_data(entry):
    with open("usage.json", "r") as file:
        data = json.load(file)
        if list(data.keys())[-1] == date.today().strftime("%d/%m/%y"):
            data[date.today().strftime("%d/%m/%y")].append(entry)
        else:
            data[date.today().strftime("%d/%m/%y")] = [entry]
    with open("usage.json", "w") as file:
        json.dump(data, file, separators=(",", ":"), indent = 3)


def plot_total_data(dict): # El json de uso del bot
    x_ind = np.arange(len(dates))
    plt.plot(dates, total, label = "Totales")
    plt.title("Uso diario de Astorito") #Titulo
    plt.grid(ls = "--")
    plt.xticks(ticks=x_ind,
               labels=dates)  # cambia los labels de x para que no sean los numeros que cree para mover las barras
    plt.locator_params(axis="x", tight=True, nbins=12)  # Solo va a mostrar nbins ticks en el eje X
    plt.gcf().autofmt_xdate()  # Inclina las fechas
    #plt.show()
    plt.savefig("grafico_uso0.png")
    plt.close()

def plot_detail_data(dict): # El json de uso del bot
    x_ind = np.arange(len(dates[-7:]))
    width = 0.07
    plt.bar(x_ind + width/2, dm[-7:], width = width, label = "Dict. Mel")
    plt.bar(x_ind - width/2, dr[-7:], width = width, label = "Dict. Rit")
    plt.bar(x_ind + 1.5*width, lm[-7:], width = width, label = "Lect. Mel.")
    plt.bar(x_ind - 1.5*width, lr[-7:], width = width, label = "Lect. Rit")
    plt.bar(x_ind + 2.5*width, sm[-7:], width = width, label = "Sec. Mel.")
    plt.bar(x_ind - 2.5*width, sr[-7:], width = width, label = "Sec. Rit")
    plt.bar(x_ind + 3.5 * width, bib[-7:], width=width, label="Biblio")
    plt.bar(x_ind - 3.5 * width, sol[-7:], width=width, label="Solfeo")
    plt.bar(x_ind + 4.5 * width, hind[-7:], width=width, label="Hindemith")
    plt.bar(x_ind - 4.5 * width, melo[-7:], width=width, label="Melo Cast.")
    plt.bar(x_ind - 5.5 * width, rec[-7:], width=width, label="Recon")

    plt.title("Detalle últimos 7 dias") #Titulo
    plt.legend()  #Muestra las referencias de "label"
    plt.xticks(ticks=x_ind, labels=dates[-7:]) # cambia los labels de x para que no sean los numeros que cree para mover las barras
    plt.grid(ls = "--")
    plt.locator_params(axis = "x",tight = True, nbins = 12) # Solo va a mostrar nbins ticks en el eje X
    #plt.show()
    plt.gcf().autofmt_xdate() # Inclina las fechas
    plt.savefig("grafico_uso1.png")
    plt.close()

def plot_pie_data(dict): # El json de uso del bot
    cat = ["D.Melo", "D.Rit", "Lec.Melo", "Lec.Rit", "Sec.Melo", "Sec.Rit", "Bilbio.",
                  "Solfeo", "Hindemith", "M.Castillo", "Reconoc"]
    plt.bar(cat, refresh_data())
    plt.title("Uso total por categoria") #Titulo
    plt.grid(ls = ":")
    plt.gcf().autofmt_xdate()  # Inclina las fechas
    #plt.show()
    plt.savefig("grafico_uso2.png")
    plt.close()
