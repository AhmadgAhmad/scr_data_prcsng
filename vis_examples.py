from sympy import false
from Metrica_IO import *
from Metrica_EPV import *
import Metrica_Viz as mviz
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import math
from scipy.io import savemat

def extr_data(fileName):
    # Get the directory of the output files:
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'OutputData/')
    full_fileName = results_dir + fileName
    infile = open(full_fileName, 'rb')
    OutputData = pickle.load(infile)
    dataset = OutputData
    infile.close()

    return  dataset

#extract the datapoints: 
AwayTeam_passes_N = extr_data('Game2_AwayTeam_NegEx')
AwayTeam_passes_N_dic = {'data':AwayTeam_passes_N}
AwayTeam_passes_P= extr_data('Game2_AwayTeam_passes')
AwayTeam_passes_P_dic = {'data':AwayTeam_passes_P}
#Save to matlab
savemat('Game_p.mat',AwayTeam_passes_P_dic)
savemat('Game_n.mat',AwayTeam_passes_N_dic)
##
fig,ax_xp1p2 = plt.subplots(figsize=(12,8))
plt.xlabel(r'time [s]', fontsize=16)
plt.ylabel(r"$x$", fontsize=16)
fig,ax_xp1b = plt.subplots(figsize=(12,8))
plt.xlabel(r'time [s]', fontsize=16)
plt.ylabel(r"$x$", fontsize=16)
fig,ax_xp2b = plt.subplots(figsize=(12,8))
plt.xlabel(r'time [s]', fontsize=16)
plt.ylabel(r"$x$", fontsize=16)

fig,ax_yp1p2 = plt.subplots(figsize=(12,8))
plt.xlabel(r'time [s]', fontsize=16)
plt.ylabel(r"$y$", fontsize=16)
fig,ax_yp1b = plt.subplots(figsize=(12,8))
plt.xlabel(r'time [s]', fontsize=16)
plt.ylabel(r"$y$", fontsize=16)
fig,ax_yp2b = plt.subplots(figsize=(12,8))
plt.xlabel(r'time [s]', fontsize=16)
plt.ylabel(r"$y$", fontsize=16)

for i in range(len(AwayTeam_passes_N[0])):
    #Plot the positive examples: 
    # #------------------------
    player1_traj = AwayTeam_passes_P[0][i][0]
    player2_traj = AwayTeam_passes_P[0][i][1]
    ball1_traj = AwayTeam_passes_P[0][i][2]



    T_len = len(ball1_traj)
    time_vector = np.linspace(0,0.04*T_len,T_len)
    p1p2_Xtraj = abs(player1_traj[:,0]-player2_traj[:,0])  
    ax_xp1p2.plot(time_vector ,p1p2_Xtraj , 'g', MarkerSize=1)

    p1b_Xtraj = abs(player1_traj[:,0]-ball1_traj[:,0])  
    ax_xp1b.plot(time_vector ,p1b_Xtraj , 'g', MarkerSize=1)

    p2b_Xtraj = abs(player2_traj[:,0]-ball1_traj[:,0])  
    ax_xp2b.plot(time_vector ,p2b_Xtraj , 'g', MarkerSize=1)
    #Trajectories in the y direction: 
    p1p2_Ytraj = abs(player1_traj[:,1]-player2_traj[:,1])
    ax_yp1p2.plot(time_vector ,p1p2_Ytraj , 'g', MarkerSize=1)
    
    p1b_Ytraj = abs(player1_traj[:,1]-ball1_traj[:,1])  
    ax_yp1b.plot(time_vector ,p1b_Ytraj , 'g', MarkerSize=1)
    
    p2b_Ytraj = abs(player2_traj[:,1]-ball1_traj[:,1])  
    ax_yp2b.plot(time_vector ,p2b_Ytraj , 'g', MarkerSize=1)

    player1_trajN = AwayTeam_passes_N[0][i][0]
    player2_trajN = AwayTeam_passes_N[0][i][1]
    ball1_trajN = AwayTeam_passes_N[0][i][2]



    T_len = len(ball1_trajN)
    time_vector = np.linspace(0,0.04*T_len,T_len)
    p1p2_XtrajN = abs(player1_trajN[:,0]-player2_trajN[:,0])  
    ax_xp1p2.plot(time_vector ,p1p2_XtrajN , 'r', MarkerSize=1)

    p1b_XtrajN = abs(player1_trajN[:,0]-ball1_trajN[:,0])  
    ax_xp1b.plot(time_vector ,p1b_XtrajN , 'r', MarkerSize=1)

    p2b_XtrajN = abs(player2_trajN[:,0]-ball1_trajN[:,0])  
    ax_xp2b.plot(time_vector ,p2b_XtrajN , 'r', MarkerSize=1)
    #Trajectories in the y direction: 
    p1p2_YtrajN = abs(player1_trajN[:,1]-player2_trajN[:,1])
    ax_yp1p2.plot(time_vector ,p1p2_YtrajN , 'r', MarkerSize=1)
    
    p1b_YtrajN = abs(player1_trajN[:,1]-ball1_trajN[:,1])  
    ax_yp1b.plot(time_vector ,p1b_YtrajN , 'r', MarkerSize=1)
    
    p2b_YtrajN = abs(player2_trajN[:,1]-ball1_trajN[:,1])  
    ax_yp2b.plot(time_vector ,p2b_YtrajN , 'r', MarkerSize=1)


    
    a  = 1
a = 1
    #Plot the negative examoles: 
    # -------------------------  



 