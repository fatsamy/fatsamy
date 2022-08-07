from datetime import date
from matplotlib import pyplot as plt

#print(plt.style.available) #die vorhanden Style anzeigen lassen.
#plt.style.use('ggplot') #Auswahl vom Style

today = str(date.today())

def single_plot(x_label = str, 
                x_list = list, 
                y_label = str,
                y_list = list,
                title_= str):

    plt.plot(x_list, y_list, color='#adad3b', linewidth=3, label='graph')


    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title_)

    plt.legend() # nicht vergessen! sonst werden die Linien nicht beschriftet

    plt.grid(True)


    plt.savefig(f'Charts/{today}_{title_}.png')

    plt.show()


def max_plot(x_label = str, 
                x_list = list, 
                y_label = str,
                y_list = list,
                label = str):

    plt.plot(x_list, y_list, linewidth=3, label=label)


    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title('all Workouts')

    plt.legend() # nicht vergessen! sonst werden die Linien nicht beschriftet

    plt.grid(True)


