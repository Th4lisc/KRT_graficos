import pandas as pd
#from tkinter import *
from tkinter import Tk, Tcl, filedialog, ttk, PhotoImage, Label, Button, StringVar
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

arquivo = None
def abrir():
    global arquivo
    arquivo = filedialog.askopenfilename(filetypes=(('Text files','*.txt'),),
                                         title = 'Escolha o arquivo')
    if arquivo != None:
        arquivonome = Label(janela1, text = arquivo,
                        font = '3ds 10',
                        fg = 'white', bg = 'black')
        botao1 = Button(janela1, text = 'Ok', command = paginaMenuGrafico)
        arquivonome.grid(row =3, column =1)
        botao1.grid(row =4, column =1, pady =15)

def paginaArquivo():
    global janela1
    janela1 = Tk()
    janela1.title('Defina o arquivo')
    janela1.iconbitmap('KRT-icon.ico')
    janela1.geometry('505x290+430+150')
    janela1.minsize(505,290)
    janela1.maxsize(505,290)
    janela1['bg'] = 'black'

    img = PhotoImage(file = 'KRTresize.png', width = 87, height = 90)
    icon = Label(janela1, image = img, borderwidth = 0)

    title = Label(janela1, text = 'Kamikaze Racing Team',
                  font = '3ds 20',
                  fg = '#FFD700', bg = 'black')
    
    texto = Label(janela1, text = 'Selecione o arquivo:',
                  font = '3ds 16',
                  fg = 'white', bg = 'black')

    botao = Button(janela1, text = 'Procurar arquivo', command = abrir)

    icon.grid(row =0, column =0, pady =(20,50))
    title.grid(row =0, column =1)
    texto.grid(row =2, column =0, padx =(10,0))
    botao.grid(row =2, column =1)

    janela1.mainloop()
    
def paginaMenuGrafico():
    janela1.destroy()
    janela = Tk()
    janela.title('KRT gráficos')
    janela.iconbitmap('KRT-icon.ico')
    janela.geometry('700x350+430+150')
    janela.minsize(700,350)
    janela.maxsize(700,350)
    janela['bg'] = 'black'
    
    global brakechoose
    brakechoose = StringVar()

    img = PhotoImage(file = 'KRTresize.png', width = 87, height = 90)
    icon = Label(janela, image = img, borderwidth = 0)

    title = Label(janela, text = 'Kamikaze Racing Team',
              font = '3ds 20',
              fg = '#FFD700', bg = 'black')

    subtitle = Label(janela, text = 'Dados Arduino',
                 font = '3ds 16',
                 fg = 'white', bg = 'black')

    linha1 = Label(janela, text = 'Gráfico temperatura do disco: ',
              font = '3ds 14',
              fg = 'white', bg = 'black')

    combo = ttk.Combobox(janela, text = 'Selecione lado', width = 15, textvariable = brakechoose)
    combo['values'] = ('Lado Esquerdo','Lado Direito')
    combo.set('Escolha um lado')


    btn = Button(janela, text = 'Mostrar gráfico', command = graficoFreio)

    linha2 = Label(janela, text = 'Gráfico acelerômetro: ',
              font = '3ds 14',
              fg = 'white', bg = 'black')


    btn1 = Button(janela, text = 'Mostrar gráfico', command = graficoAcelerometro)

    btn2 = Button(janela, text = 'Voltar', command = lambda:[janela.destroy(), paginaArquivo()])

    icon.grid(row =0, column =0, rowspan =2, pady =(20,50))
    title.grid(row =0, column =1)
    subtitle.grid(row =1, column =1)
    linha1.grid(row =4, column =0, pady =(10,0))
    combo.grid(row =4, column =1)
    btn.grid(row =4, column =2)
    linha2.grid(row =5, column =0, pady =(15,0))
    btn1.grid(row =5, column =2)
    btn2.grid(row =6, column =2, pady =40, sticky ='e')

    janela.mainloop()

def graficoFreio():
    with open(arquivo,'r') as arquivodf:
        df = pd.read_table(arquivodf, sep= '   ', engine = 'python' )
        df = pd.DataFrame(df)
        df.columns = ['tempo','Sensor1','s1','°C','Sensor2','s2','°C']
        df.drops('Sensor1','°C','Sensor2')

    if (brakechoose.get() == 'Lado Direito'):
        source = ColumnDataSource(data=dict(df))
        
        p = figure(width=1350, title='Temperatura Lado Direito', x_range=df['tempo'].drop_duplicates())
        p.xaxis.axis_label = 'Tempo(hr:min;sec)'
        p.yaxis.axis_label = 'Variação Temperatura'
        p.xaxis.major_label_orientation = 240
        
        p.line(x='tempo', y='s1', source=source, legend_label='Dianteiro', color='#FFD700')
        p.line(x='tempo', y='s2', source=source, legend_label='Traseiro', color='black')

        show(p)
    
        arquivodf.close()

    else:
        source = ColumnDataSource(data=dict(df))
        
        p = figure(width=1350, title='Temperatura Lado Esquerdo', x_range=df['tempo'].drop_duplicates())
        p.xaxis.axis_label = 'Tempo(hr:min;sec)'
        p.yaxis.axis_label = 'Variação Temperatura'
        p.xaxis.major_label_orientation = 240
        
        p.line(x='tempo', y='s1', source=source, legend_label='Dianteiro', color='#FFD700')
        p.line(x='tempo', y='s2', source=source, legend_label='Traseiro', color='black')

        show(p)
    
        arquivodf.close()
        
    
def graficoAcelerometro():
    with open(arquivo,'r') as arquivodf:
        df = pd.read_table(arquivodf, sep= '   ', engine = 'python' )
        df = pd.DataFrame(df)
        df.columns = ['tempo','AcX','ax','AcY','ay','AcZ','az','GyX','gx','GyY','gy','GyZ','gz','Temp','temp']
        df.drop(columns=['AcX','AcY','AcZ','GyX','GyY','GyZ','Temp'])

        source = ColumnDataSource(data=dict(df))
        
        p = figure(width=1350, title='Acelerômetro', x_range=df['tempo'].drop_duplicates())
        p.xaxis.axis_label = 'Tempo(hr:min;sec)'
        p.yaxis.axis_label = 'Variação Aceleração'
        p.xaxis.major_label_orientation = 240
        
        p.line(x='tempo', y='temp', source=source, legend_label='Temp. sensor', color='#FF6347')
        p.line(x='tempo', y='ax', source=source, legend_label='Lateral', color='#FFD700')
        p.line(x='tempo', y='ay', source=source, legend_label='Frontal', color='black')

        show(p)

        arquivodf.close()

paginaArquivo()