import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import datetime
from docx import Document
from docx.shared import Inches
from docx.shared import Pt
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re
import pyautogui
import sqlite3


li =[]

#2 - criação da janela como um top level , para que fique estatica e focada
root = Tk()
root.geometry('1006x570+0+0')
root.title('bet365')
root.resizable(False,False)
root.focus_force()
root.grab_set()


#2- criação da treeview onde terá 3 colunas , id,produtos,e stoke
frame1 = Frame(root,borderwidth=5,relief='sunken',bg='snow')
frame1.place(x=0,y=0,width=1006,height=350)
tabela = ttk.Treeview( frame1,
columns = (1,2,3,4,5,6,7,8,9,10,11,12),
height = 16,
show = 'headings')
tabela.pack( side = 'left')
tabela.heading(1, text='liga')
tabela.heading(2, text='time')
tabela.heading(3, text='tempo')
tabela.heading(4, text='placar')
tabela.heading(5, text='ataque')
tabela.heading(6, text='ataque p.')
tabela.heading(7, text='%  posse')
tabela.heading(8, text='no alvo')
tabela.heading(9, text='ao lado')
tabela.heading(10, text='escanteio')
tabela.heading(11, text='amarelo')
tabela.heading(12, text='vermelho')
tabela.column(1, width= 160)
tabela.column(2, width = 190 )
tabela.column(3, width = 65 )
tabela.column(4, width = 70 )
tabela.column(5, width = 65 )
tabela.column(6, width = 65 )
tabela.column(7, width = 70 )
tabela.column(8, width = 60 )
tabela.column(9, width = 60 )
tabela.column(10, width = 60 )
tabela.column(11, width = 55 )
tabela.column(12, width = 60 )



#2- fazendo o scrollbar da treeview
barrarolagem = ttk.Scrollbar( frame1,orient='vertical',
command=tabela.yview)
barrarolagem.pack( side = 'right', fill='y')
tabela.configure(yscrollcommand = barrarolagem.set)




#ataque
Label(root,text='ataque',font='arial 16 bold').place(x=10,y=360)
ataque_casa = Entry(root,font=('Arial',18),bd=3)
ataque_casa.place(x=10,y=395,width=95,height=30)



#ataque p.
Label(root,text='ataque p.',font='arial 16 bold').place(x=160,y=360)
ataque_p_casa = Entry(root,font=('Arial',18),bd=3)
ataque_p_casa.place(x=160,y=395,width=95,height=30)

#no alvo
Label(root,text='no alvo',font='arial 16 bold').place(x=310,y=360)
alvo_casa = Entry(root,font=('Arial',18),bd=3)
alvo_casa.place(x=310,y=395,width=95,height=30)

#lado
Label(root,text='ao lado',font='arial 16 bold').place(x=460,y=360)
lado_casa = Entry(root,font=('Arial',18),bd=3)
lado_casa.place(x=460,y=395,width=95,height=30)

#escanteio
Label(root,text='escanteio',font='arial 16 bold').place(x=605,y=360)
escanteio_casa = Entry(root,font=('Arial',18),bd=3)
escanteio_casa.place(x=610,y=395,width=95,height=30)

#amarelo
Label(root,text='amarelo',font='arial 16 bold').place(x=750,y=360)
amarelo_casa = Entry(root,font=('Arial',18),bd=3)
amarelo_casa.place(x=750,y=395,width=95,height=30)

#vermelho
Label(root,text='vermelho',font='arial 16 bold').place(x=885,y=360)
vermelho_casa = Entry(root,font=('Arial',18),bd=3)
vermelho_casa.place(x=890,y=395,width=95,height=30)





#buscar , atualizar e sair
btn_buscar= Button(root,text='buscar',bg='steelblue',font='arial 18 bold',width='6',command=lambda:pesquisa_filtro())
btn_buscar.place(x=10,y=435)
btn_buscar= Button(root,text='limpar',bg='firebrick2',font='arial 18 bold',width='6',command=lambda:limpar())
btn_buscar.place(x=130,y=435)
btn_atualizar= Button(root,text='ATUALIZAR DADOS',bg='light steel blue',font='Times 20 bold',command=lambda:atualizar_dados())
btn_atualizar.place(x=10,y=505)
btn_sair= Button(root,text='sair',bg='coral',font='Times 20 bold',command=root.destroy)
btn_sair.place(x=915,y=505)

def limpar():
    ataque_casa.delete(0,END)
    ataque_p_casa.delete(0,END)
    alvo_casa.delete(0,END)
    lado_casa.delete(0,END)
    escanteio_casa.delete(0,END)
    amarelo_casa.delete(0,END)
    vermelho_casa.delete(0,END)
    pesquisa_filtro()

def pesquisa_filtro():
    tabela.delete(*tabela.get_children())
    atq = ataque_casa.get()
    atqp = ataque_p_casa.get()
    alvo = alvo_casa.get()
    lado = lado_casa.get()
    escanteio = escanteio_casa.get()
    amarelo = amarelo_casa.get()
    vermelho = vermelho_casa.get()
    if atq == '':
        atq = 0
    if atqp == '':
        atqp = 0
    if alvo == '':
        alvo = 0
    if lado == '':
        lado = 0
    if escanteio == '':
        escanteio = 0
    if amarelo == '':
        amarelo = 0
    if vermelho == '':
        vermelho = 0
    atq = int(atq)
    atqp = int(atqp)
    alvo = int(alvo)
    lado = int(lado)
    escanteio = int(escanteio)
    amarelo = int(amarelo)
    vermelho = int(vermelho)
    #[0]liga ,[1]time, [2]placar, [3]atq, [4]atq_fora, [5]p_atq , [6]p_atq_fora, [7]posse, [8]posse_fora, [9]no alvo, [10]no alvo_fora, [11]ao lado, [12]ao lado_fora
    for x in li:
        if x[3] >= atq or x[4] >= atq:
            if x[5] >= atqp or x[6] >=atqp:
                if x[9] >= alvo or x[10] >=alvo:
                    if x[11] >= lado or x[12] >= lado:
                        if x[13] >= escanteio or x[16] >=escanteio:
                            if x[15] >= amarelo or x[14] >=amarelo:
                                if x[17] >=vermelho or x[18] >=vermelho:
                                    tabela.insert("","end",values=(x[0], x[1], '    '+x[19], '  '+x[2], '  '+str(x[3])+' vs '+str(x[4]), '  '+str(x[5])+' vs '+str(x[6]), ''+str(x[7])+'%  vs '+str(x[8])+'%', '    '+str(x[10])+' vs '+str(x[9]), '    '+str(x[11])+' vs '+str(x[12]) , '    '+str(x[13])+' vs '+str(x[16]) , '    '+str(x[15])+' vs '+str(x[14]) , '    '+str(x[17])+' vs '+str(x[18])))
                        
                        
def atualizar_dados():
    li.clear()
    pesquisa_filtro()
    url_base = 'https://www.bet365.com/#/IP/B1'
    navegador = webdriver.Chrome()
    navegador.get('{}'.format(url_base))
    sleep(3)
    navegador.find_element_by_xpath('/html/body/div[4]/div/div[1]').click()
    sleep(4)
    content = navegador.page_source
    site = BeautifulSoup(content,'html.parser')
    homes = site.findAll('div', attrs={'class': 'ovm-Competition ovm-Competition-open'})

    valor_da_liga = 1
    for home in homes:
        valor_da_liga += 1
        liga = home.find('div',attrs={'class': 'ovm-CompetitionHeader_NameText'})
        esoccer = liga.text[0]+liga.text[1]+liga.text[2]
        
        def pesquisa():
            
                contents = navegador.page_source
                sites = BeautifulSoup(contents,'html.parser')
                try:
                    horario = sites.find('span', attrs={'class': 'ml1-SoccerClock_Clock'})
                    horario = horario.text
                    
                except:
                    horario = 'NONE'
                
                jogo = sites.find('div',attrs={'class': 'lv-LiveTabView lv-LiveTabView_HasScoreboard'})        
                placar_casa = jogo.findAll('span',attrs={'class': 'lsb-ScoreBasedScoreboard_TeamScore'})
                placar =' vs '.join([placar.text for placar in placar_casa])
                os2times = jogo.findAll('div',attrs={'class': 'lsb-ScoreBasedScoreboard_TeamName'})
                time =' vs '.join([time.text for time in os2times]) 
                dados = jogo.findAll('div',attrs={'class':'ml-WheelChart'})
                dados2 = jogo.findAll('div',attrs={'class':'ml1-StatsLower_MiniBarWrapper'})
                valor_teste=0
                for dado2 in dados2:
                    valor_teste+=1
                    if valor_teste == 1:
                        alvo_casa = dado2.find('b',attrs={'class': 'ml-ProgressBar_MiniBarValue ml-ProgressBar_MiniBarValue-2'})
                        alvo_fora = dado2.find('b',attrs={'class': 'ml-ProgressBar_MiniBarValue ml-ProgressBar_MiniBarValue-1'})     
                    if valor_teste == 2:
                        lado_casa = dado2.find('b',attrs={'class': 'ml-ProgressBar_MiniBarValue ml-ProgressBar_MiniBarValue-1'})
                        lado_fora = dado2.find('b',attrs={'class': 'ml-ProgressBar_MiniBarValue ml-ProgressBar_MiniBarValue-2'})
                valor_teste=0  
                certo = 0     
                for dado in dados:
                    valor_teste+=1
                    if valor_teste == 1:
                        ataque_casa = dado.find('div',attrs={'class': 'ml-WheelChart_Team1Text'})
                        ataque_fora = dado.find('div',attrs={'class': 'ml-WheelChart_Team2Text'})
                    if valor_teste == 2:
                        ataque_p_casa = dado.find('div',attrs={'class': 'ml-WheelChart_Team1Text'})
                        ataque_p_fora = dado.find('div',attrs={'class': 'ml-WheelChart_Team2Text'})
                    if valor_teste == 3:    
                        posse_casa = dado.find('div',attrs={'class': 'ml-WheelChart_Team1Text'})
                        posse_fora = dado.find('div',attrs={'class': 'ml-WheelChart_Team2Text'})
                          
                        
                            
                valor_teste=0 
                painel = sites.find('div',attrs={'class': 'ml1-StatsLower'})
                cartoes = painel.findAll('div',attrs={'class': 'ml1-StatsColumn_MiniValue'}) 
                for cartao in cartoes:
                    valor_teste+=1
                    if valor_teste == 1:
                        c_amarelo_casa = int(cartao.text)
                    if valor_teste == 2:
                        c_vermelho_casa = int(cartao.text)
                    if valor_teste == 3:
                        escanteio_casa = int(cartao.text)
                        
                    if valor_teste == 4:
                        c_amarelo_fora = int(cartao.text)             
                    if valor_teste == 5:
                        c_vermelho_fora = int(cartao.text)
                    if valor_teste == 6:
                        escanteio_fora = int(cartao.text)
                
                
                timer = time
                ataque_casa = int(ataque_casa.text)
                ataque_fora = int(ataque_fora.text)
                ataque_p_casa = int(ataque_p_casa.text)
                ataque_p_fora = int(ataque_p_fora.text)
                
                try:
                    posse_casa = int(posse_casa.text)
                    posse_fora = int(posse_fora.text)
                except:
                    posse_casa = 0
                    posse_fora = 0
                
                alvo_casa = int(alvo_casa.text)
                alvo_fora = int(alvo_fora.text)
                lado_casa = int(lado_casa.text)
                lado_fora = int(lado_fora.text)
                
                
                li.append([liga.text,timer, placar,ataque_casa ,ataque_fora,ataque_p_casa ,ataque_p_fora,posse_casa ,posse_fora ,alvo_casa,alvo_fora ,lado_casa ,lado_fora, escanteio_casa, escanteio_fora, c_amarelo_casa, c_amarelo_fora, c_vermelho_casa, c_vermelho_fora, horario ])
                
                
                
                
            
            #fim da função..............................................................
        
        if esoccer != 'E-s':
            valor_do_time = 1
            #print('\n\n\n',liga.text)
            tm = home.findAll('div', attrs={'class':'ovm-FixtureDetailsTwoWay_TeamsWrapper'})    
            
                                            
            for tmm in tm:
                
                valor_do_time+=1
                #print('',tmm.text)
                try:    
                    navegador.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[{}]/div[2]/div[{}]/div[2]/div/div'.format(valor_da_liga,valor_do_time)).click()
                    sleep(1)
                    pesquisa()
                except:
                    pass
                                            
                
    navegador.close()
    #[0]liga ,[1]time, [2]placar, [3]atq, [4]atq_fora, [5]p_atq , [6]p_atq_fora, [7]posse, [8]posse_fora, [9]no alvo, [10]no alvo_fora, [11]ao lado, [12]ao lado_fora, [13]escanteio, [14]escanteio_fora, [15]amarelo, [16]amarelo_fora, [17]vermelho, [18]vermelho_fora
    for x in li:
        tabela.insert("","end",values=(x[0], x[1], '    '+x[19],'   '+x[2], '  '+str(x[3])+' vs '+str(x[4]), '  '+str(x[5])+' vs '+str(x[6]), ''+str(x[7])+'%  vs '+str(x[8])+'%', '    '+str(x[10])+' vs '+str(x[9]), '    '+str(x[11])+' vs '+str(x[12]) , '    '+str(x[13])+' vs '+str(x[16]) , '    '+str(x[15])+' vs '+str(x[14]) , '    '+str(x[17])+' vs '+str(x[18])))
    #tabela.insert("","end",values=())
root.mainloop()