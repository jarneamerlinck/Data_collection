#!/usr/bin/python
#-*- coding:utf-8 -*-
#vorige lijn is nodig voor ° symbool te kunnen weergeven

#Deze lijnen importeren alle nodige bibiloteken op het programma te kunnen laden
from Tkinter import Tk,Frame,StringVar,Label,Button,Entry,IntVar

import serial# nodig voor de seriele communicatie van de arduino naar de computer te kunnen lezen
import matplotlib.pyplot as plt

import numpy as np#nodig voor het uithalen van x en y waarden voor de grafiek uit de .txt bestanden
import time #nodig voor aanmaken naam bestanden en voor de delay
import pandas as pd
from openpyxl import load_workbook

#aanmaken van .txt bestanden met de geprinte namen en alle nodige namen met datums (zoals voor de titels van de grafieken)

Temperatuur =time.strftime("Temperatuur(%Y_%m_%d_%H_%M)")
Vochtigheid =time.strftime("Vochtigheid")
Licht=time.strftime("Licht(%Y_%m_%d_%H_%M)")
Zuurstof=time.strftime("Zuurstof")
DISPLAY=time.strftime("Begonnen om %H_%M")
sheet_Name=time.strftime("%Y_%m_%d_%H_%M")

Grafieken_1=time.strftime("Grafieken_T_V_%Y_%m_%d_%H_%M.png")
Grafieken_2=time.strftime("Grafieken_L_Z_%Y_%m_%d_%H_%M.png")
titel_1=time.strftime("Temperatuur(%Y_%m_%d_%H_%M)\nRelatieve vochtigheid")
titel_2=time.strftime("Licht(%Y_%m_%d_%H_%M)\nZuurstof")
info=time.strftime("%Y_%m_%d_%H_%M_Info.txt")

print(info)


file_Info=open(str(info),'w')



	
#globals
backup=0
x=0
delay=0
T=0
V=0
L=0
Z=0
a=0
looop=0
test=0
s=0

#Tk
root=Tk()
root.title('GIP6IW')
frame=Frame(root)
arduino=Frame(root)
usb=Frame(root)
infof=Frame(root)
TIme=Frame(root)
Loop=Frame(root)

Delay=StringVar()
Backup=StringVar()
X=StringVar()
INfo=StringVar()
Delay.set('2')
X.set("0 0 1")
Backup.set('1')

#column 0
t0=StringVar()
t0.set('Temperatuur')
v0=StringVar()
v0.set('Vochtigheid')
l0=StringVar()
l0.set('Licht')
z0=StringVar()
z0.set('Zuurstof')
#column 1
t2=StringVar()
v2=StringVar()
l2=StringVar()
z2=StringVar()

t2.set(T)
v2.set(V)
l2.set(L)
z2.set(Z)

labelt=Label(frame,textvariable=t0,font=("arial",40))
labelt.grid(row=0,column=0)
labelv=Label(frame,textvariable=v0,font=("arial",40))
labelv.grid(row=1,column=0)
labell=Label(frame,textvariable=l0,font=("arial",40))
labell.grid(row=2,column=0)
labelz=Label(frame,textvariable=z0,font=("arial",40))
labelz.grid(row=3,column=0)
t3=StringVar()
t3.set('°C')
v3=StringVar()
v3.set('%')
l3=StringVar()
l3.set('lux')
z3=StringVar()
z3.set('ppm')
labelt=Label(frame,textvariable=t3,font=("arial",40))
labelt.grid(row=0,column=2)
labelv=Label(frame,textvariable=v3,font=("arial",40))
labelv.grid(row=1,column=2)
labell=Label(frame,textvariable=l3,font=("arial",40))
labell.grid(row=2,column=2)
labelz=Label(frame,textvariable=z3,font=("arial",40))
labelz.grid(row=3,column=2)


def Usb():
	frame.destroy()
	arduino.destroy()
	TIme.destroy()
	infof.destroy()
	USB=StringVar()
	varU=StringVar()
	varU.set("Arduino usb location (normal /dev/ttyACM0 or /dev/ttyUSB0")
	placeU=Label(usb,textvariable=varU,font=("arial,50"))
	InputU=Entry(usb,textvariable=USB)
	InputU.grid(row=0,column=1)
	placeU.grid(row=0,column=0)
	usb.grid()


def Arduino():

	global x
	global delay
	global backup
	global X
	global Delay
	global Backup

	backup=Backup.get()
	p=X.get()
	delay=Delay.get()
	p=str(p)

	delay=int(str(delay))
	backup=int(str(backup))

	P=str(p).split()
	XX=3600*int(P[0])+60*int(P[1])+int(P[2])
	x=int(XX)

	print('delay',delay)
	print('backup',backup)
	print ('p',p)
	print ('x',x)
	TIme.destroy()
	varE=StringVar()
	varE.set("Arduino is not connected or wrong USB is selected")
	ErrorA=Label(arduino,textvariable=varE,font=("arial,50"))

	button=Button(arduino,text='Next',command=serialC)
        button.config(font=("arial",25))
        button.grid(row=3,column=1)
 
	ErrorA.grid()
	arduino.grid()
	
def infoF():
	global INfo
	varI=StringVar()
	varI.set("Extra informatie")
	placeI=Label(infof,textvariable=varI)
	placeI.config(font=("arial,50"))
	InputI=Entry(infof,textvariable=INfo)
	InputI.grid(row=0,column=1)
	placeI.grid(row=0,column=0)


	button=Button(infof,text='Next',command=WriteI)
        button.config(font=("arial",25))
        button.grid(row=3,column=1)
        infof.grid()

def WriteI():
	global INfo
	write=INfo.get()
	write=str(write)
	print('Write',write)
	file_Info= open(str(info),'a') 
	file_Info.write(write)
	file_Info.close()
	Time()

def Time():

	global Delay
	global Backup
	infof.destroy()
	
	varDelay=StringVar()
	varDelay.set('Om de hoeveel seconden moeten er waardes genomen worden (min 2s) ?')
	placeDelay=Label(TIme,textvariable=varDelay,font=("arial,50"))
	InputDelay=Entry(TIme,textvariable=Delay)
	InputDelay.grid(row=0,column=1)
	placeDelay.grid(row=0,column=0)


	varB=StringVar()
	varB.set('Om de hoeveel waardes moet er een backup genomen worden ?')
	placeB=Label(TIme,textvariable=varB,font=("arial,50"))
	InputB=Entry(TIme,textvariable=Backup)
	InputB.grid(row=1,column=1)
 	placeB.grid(row=1,column=0)
	

	varX=StringVar()
	varX.set('Hoelang mag het programma draaien (h m s)')
	placeX=Label(TIme,textvariable=varX,font=("arial,50"))
	InputX=Entry(TIme,textvariable=X)
	InputX.grid(row=2,column=1)
	placeX.grid(row=2,column=0)
	
	TIme.grid()
	

	button=Button(TIme,text='Next',command=Arduino2)
	button.config(font=("arial",25))
	button.grid(row=3,column=1)
	TIme.grid()

def Arduino2():
	backup=Backup.get()
        p=X.get()
        delay=Delay.get()
        p=str(p)

        delay=int(str(delay))
        backup=int(str(backup))

        P=str(p).split()
        XX=3600*int(P[0])+60*int(P[1])+int(P[2])
        x=int(XX)
	root.after(20,loop)


class data:
	global s

	def __init__(self,place,file):
		self.place=place

		self.file=file
	def txt(self):
		open(str(self.file),'w')
	

	def write(self,value):
		self.value=value


		name= open(str(self.file),'a')
                name.write(str(s))
                name.write(',')
                name.write(str(self.value))
                name.write('\n')
                name.close()

	def screen(self):
		self.sv=StringVar()
		self.sv.set(self.value)
		self.label=Label(frame,textvariable=self.sv,font=("arial",40))
		self.label.grid(row=self.place,column=1)
		root.update()

temp=data(0,time.strftime("%Y_%m_%d_%H_%M_T.txt"))
voch=data(1,time.strftime("%Y_%m_%d_%H_%M_V.txt"))
lich=data(2,time.strftime("%Y_%m_%d_%H_%M_L.txt"))
zuur=data(3,time.strftime("%Y_%m_%d_%H_%M_Z.txt"))
temp.txt()
voch.txt()
lich.txt()
zuur.txt()











def Frameloop():

	#column 2

	labelt=Label(frame,textvariable=t2,font=("arial",40))
	labelt.grid(row=0,column=2)
	labelv=Label(frame,textvariable=v2,font=("arial",40))
	labelv.grid(row=1,column=2)
	labell=Label(frame,textvariable=l2,font=("arial",40))
	labell.grid(row=2,column=2)
	labelz=Label(frame,textvariable=z2,font=("arial",40))
	labelz.grid(row=3,column=2)
	frame.grid()
	root.update()
	return



def close(event):
	root.destroy()

root.attributes("-fullscreen",True)
root.bind("<Escape>",close)

def Return():
	return


def serialC():
	try:
		#list = serial.Serial(USB, 9600)
		#list= serial.Serial('/dev/ttyUSB0',9600)
		list.read()
	except:
		Arduino()
		serialC()

	#deze regels zijn nodig om de sensor de tijd te geven op op te starten
	list.read()
	list.read()
	list.read()

	#geeft de lijst weer => met deze data kunnen we niet werken
	list
	infoF()
print(temp.file)
def grafiek():
	#Standaard
	#Grafiek maken van de Temperatuur waarden uit een txt file
	x, y =np.loadtxt(str(temp.file), delimiter=',', unpack= True)
	fig_1 = plt.figure()
	ax1 = fig_1.add_subplot(2,1,1)
	ax1.clear()
	ax1.axes.set_ylabel('Temperatuur in  C')
	#ax1.axes.set_xlabel('Tijd in seconden')
	ax1.set_title(titel_1)
	ax1.plot(x, y, color ='tab:red')
	ax1.set_xticklabels([])

	#Grafiek maken van de Vochtigheid waarden uit een txt file
	X, Y =np.loadtxt(str(voch.file), delimiter=',', unpack= True)
	ax2 = fig_1.add_subplot(2,1,2)
	#fig.subplots_adjust(hspace =1, bottom=0.001)
	#fig.subplots_adjust(hspace =1)
	ax2.clear()
	ax2.axes.set_ylabel('Relatieve vochtigheid in %')
	#ax2.axes.set_xlabel('Tijd in seconden')
	ax2.plot(X, Y, color='tab:blue')

	#Deze lijn voegt de grafieken samen op 1 afbeelding
    
	fig_1.savefig(Grafieken_1,transparent=0, bbox_inches='tight')

	#Grafiek maken van de licht waarden uit een txt file
	X1, Y1 =np.loadtxt(str(lich.file), delimiter=',', unpack= True)
	fig_2 = plt.figure()
	ax3 = fig_2.add_subplot(2,1,1)
	ax3.clear()
	ax3.axes.set_ylabel('Licht in lux')
	ax3.axes.set_xlabel('Tijd in seconden')
	ax3.set_title(titel_2)
	ax3.plot(X1, Y1,color='tab:red')
	ax2.set_xticklabels([])

	#Grafiek maken van de zuurstof waarden uit een txt file
	X2, Y2 =np.loadtxt(str(zuur.file), delimiter=',', unpack= True)
	ax4 = fig_2.add_subplot(2,1,2)
	ax4.clear()
	ax4.axes.set_ylabel('Zuurstof in ppm')
	ax4.axes.set_xlabel('Tijd in seconden')
	ax4.plot(X2, Y2,color='tab:blue')

	#Deze lijn voegt de grafieken samen op 1 afbeelding
	fig_2.savefig(Grafieken_2,transparent=0, bbox_inches='tight')
	print("Grafiek Done")



number=0
def loop():
	global number
	global a
	global backup
	global delay
	global x
	global T
	global V
	global L
	global Z
	global looop
	global s
	print('loop start')
	list= serial.Serial('/dev/ttyUSB0',9600)
	list.readline()
	list.readline()
	list.readline()

	if (number==0):
		backup=Backup.get()
		p=X.get()
		delay=Delay.get()
		number=1
		p=str(p)

		delay=int(str(delay))
		backup=int(str(backup))
	
		P=str(p).split()
		XX=3600*int(P[0])+60*int(P[1])+int(P[2])
		x=int(XX)
		arduino.destroy()
		TIme.destroy()
		infof.destroy()
	#	Frameloop()
	while x>0 :
	        x=x-delay
		a=a+1
	        TST=list.readline()
		tst=TST.split()
        	S=delay*a
        	s=str(S)




		temp.write(tst[0])
		voch.write(tst[1])
		lich.write(tst[2])
		zuur.write(tst[3])
		temp.screen()
		voch.screen()
		lich.screen()
		zuur.screen()
		frame.grid()
				#time.sleep(delay)
        	looop=looop+1
        	if looop==backup:
        	    grafiek()
        	    looop=0
        	    print ("Grafieken gemaakt")
	if x==0 or x<0:
		grafiek()
		root.destroy()
	print('Done')



#Deze cel schrijft de ingelezen waarden in 4 .txt files


#Start programma
#List= serial.Serial('/dev/ttyUSB0',9600)
#serialC()
infoF()


   
#grafiek()
#excel()
root.mainloop()


