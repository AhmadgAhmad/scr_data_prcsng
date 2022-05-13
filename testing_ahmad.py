"""
The trajectory is collected with 25 Hz 
"""


from sympy import false
from Metrica_IO import *
from Metrica_EPV import *
import Metrica_Viz as mviz
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import math

DATADIR = 'C:/Users/ahmad/Documents/Graduate_study/PhD_work/First_Fall-2021/TLI/MAESTRO_group_inferring/MetrcaSport_data/sample-data-master/data'
game_id = 2


#Extracting teams and ball trajectories: 
#------------------------------------------
# Home Team: 
def ext_teams_Traj(tracking_home, tracking_away ,s_ind,e_ind, ptclr_payers_list = None, plt_inst = False,ext_home_flg = True, ext_away_flg = True):
    """
    Ruturns the trajectories of the home and away teams, respectively.
    Inputs:   
     - s_ind: index of the starting frame, 
     - e_ind: index of the ending frame, 
     - 
    """
    # Home team
    home_trajs = [None]*11
    # Away team: 
    away_trajs = [None]*11
    #The ball :
    ball_traj = []

    #++Extracting the trajectories++  
    if ptclr_payers_list is None:  
        Hp_names =list(np.linspace(1,11,11))
        Ap_names =list(np.linspace(15,25,11))
    else:
        Hp_names = [int(ptclr_payers_list[0][6:])]
        Ap_names = [int(ptclr_payers_list[0][6:]),int(ptclr_payers_list[1][6:])]
        
    # for i,p_name in enumerate(Hp_names): #todo Fix: when returning the trajs with the correct label of each player
    #     #The trajectory of each player: 
    #     try:
    #         home_trajs[i] = np.asarray([tracking_home['Home_%d_x'%p_name].iloc[s_ind:e_ind], tracking_home['Home_%d_y'%p_name].iloc[s_ind:e_ind]])  
    #     except:
    #         raise('The provided player name is not from the home team.')
    
    for i,p_name in enumerate(Ap_names): 
        try: 
            away_trajs[i] = np.asarray([tracking_away['Away_%d_x'%p_name].iloc[s_ind:e_ind], tracking_away['Away_%d_y'%p_name].iloc[s_ind:e_ind]])
        except:
            raise('The provided player name is not from the away team.')

    ball_traj = np.asarray([tracking_away['ball_x'].iloc[s_ind:e_ind], tracking_away['ball_y'].iloc[s_ind:e_ind]])   
    #++plot the ball trajectory++
    
    if plt_inst:
        fig,ax = plt.subplots(figsize=(12,8))
        ax.plot( tracking_away['ball_x'].iloc[s_ind:e_ind], tracking_away['ball_y'].iloc[s_ind:e_ind], 'b', MarkerSize=1)
        #Plot the home team trajecotries: 
        # Hp_names =list(np.linspace(1,11,11))
        # for p_name in Hp_names: 
        #     ax.plot( tracking_home['Home_%d_x'%p_name].iloc[s_ind:e_ind], tracking_home['Home_%d_y'%p_name].iloc[s_ind:e_ind], 'r', MarkerSize=1)

        #Plot the away team trajectories: 
        # Ap_names =list(np.linspace(15,25,11))
        colors = ['g','r']
        for i,p_name in enumerate(Ap_names): 
            ax.plot( tracking_away['Away_%d_x'%p_name].iloc[s_ind:e_ind], tracking_away['Away_%d_y'%p_name].iloc[s_ind:e_ind], colors[i], MarkerSize=1)

       
        ax.axis('equal')
        plt.show()
        # TODO: - Create a function to extract the relative distances instead of absolute trajectories.

    
    return tracking_home, tracking_away, home_trajs, away_trajs, ball_traj  

def saveData(dataAsList,fileName,enFlag=False):
    # Creat a Figures folder and get the directory name:
    if not os.path.exists('OutputData'):
        os.makedirs('OutputData')
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'OutputData/')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    fileFullName = results_dir + fileName
    if enFlag:
        outfile = open(fileFullName, 'wb')
        if not isinstance(dataAsList,list):
            dataAsList = [dataAsList]
        pickle.dump([dataAsList], outfile)
        outfile.close() 

def pickling_data():
    #Get the directory of the output files:
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'OutputData/')
    figresults_dir = os.path.join(script_dir, 'Figures/')

    full_fileName = results_dir + fileName
    infile = open(full_fileName, 'rb')
    OutputData = pickle.load(infile)
    costToCome_list = OutputData[0][1]
    initIter = OutputData[0][0]
    infile.close()
    if initIter is None:
        a = 1
    itersV = np.linspace(initIter, len(costToCome_list)+initIter, len(costToCome_list))
    itersV = itersV.astype(int)
    pass 

def ext_event_frams_players( events = None, team = None,evt_type = None, evt_sbtyp =  None, rdm_2nd_plr_flg = True):
    """
    Given an event, it extracts the event start and end frames, and the names of the player/plyres who are involved in the event  
    Inputs: 
     - team: 'Home', 'Away'
     - evt_typ: 'PASS', 'BALL LOST', 'RECOVERY', 'CHALLENGE', 'BALL OUT', 'SHOT'
     - evt_sbtyp: INTERCEPTION, HEAD-INTERCEPTION, AERIAL-LOST, AERIAL-WON, HEAD, CROSS, HEAD-ON-TARGET-GOAL 
     - rdm_2nd_plr_flg: Flag to randomize assigning the 2nd player of the event, if such event is for a singular player
    Outputs: 
     - evt_strt_end_frms: 
     - from_to_players:
     - player:
     - evt_time: 
    """
    if team is None: 
        raise('No team name is provided')
    if evt_type is None: 
        raise('No event name is provided')
    if events is None: 
        raise('Event data is not provided')

    #Extracting the team events and the events based on the type: 
    team_evts_data = events[events['Team']==team]
    team_evts = team_evts_data[team_evts_data.Type == evt_type]
    if evt_sbtyp is not None: 
        team_evts = team_evts[team_evts_data.Subtype == evt_sbtyp] 
    # Extract the start and end frames of the events and the players who are involved: 
    team_s_frames = team_evts['Start Frame'].array        # Home team starting frames for losing the ball
    team_e_frames = team_evts['End Frame'].array          # Home team ending frames for recovering the ball
    team_frames = [team_s_frames,team_e_frames] # Start and end frames 
    evt_strt_end_frms = np.asarray(team_frames).T 
    
    team_from_player = team_evts['From'].array            #The players of the event. 
    team_to_player = team_evts['To'].array              #The players of the event.
    team_From_To_players = [team_from_player,team_to_player]
    #Todo extract the number of the players directly: 

    
    # todo
    if rdm_2nd_plr_flg: 
        pass

    from_to_players = np.asarray(team_From_To_players).T 

    return evt_strt_end_frms, team_From_To_players
    


#Extract the tracking data and plot the specified time window: 
# tracking_home, tracking_away, home_trajs, away_trajs  = ext_teams_Traj(s_ind = 10,e_ind = 2000,plt_inst=True)

# Extract interseptions data traces: 
# Each team will have 2 types of interseption, (i) Recovery interspetion (ii) Losing the ball interseption
# -----------------------------------------------
#Extracting the trajectories from the game file: 
# Home team
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_home = mio.to_metric_coordinates(tracking_home)
# Away team: 
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')
tracking_away = mio.to_metric_coordinates(tracking_away)

    

events = mio.read_event_data(DATADIR,game_id)
events = mio.to_metric_coordinates(events)
home_lost_inter_frames, home_From_To_players  = \
    ext_event_frams_players( events = events, team = 'Home',evt_type = 'BALL LOST', evt_sbtyp =  'INTERCEPTION')
home_lost_from_player = home_From_To_players[0]

away_rec_inter_frames, away_rec_From_To_players  = \
    ext_event_frams_players( events = events, team = 'Away',evt_type = 'RECOVERY', evt_sbtyp =  'INTERCEPTION')
away_rec_from_player = away_rec_From_To_players[0]

away_pass_inter_frames, away_pass_From_To_players  = \
    ext_event_frams_players( events = events, team = 'Away',evt_type = 'PASS')
away_pass_from_player = away_rec_From_To_players[0]

#-------------------------------------------------------------------------------------





# +++ Configuration of the interseption event: 
# ~ The 1st config of the event is: HOME_LOST w/ AWAY_REC
# ~ The 2nd config of the event is: AWAY_LOST w/ HOME_REC
# The event must be fed in this order: a team loses the ball where the other team recover it right away. 
#  If this order is reversed (recovering then losign the ball) will take the end of the previous 
# interseption with the begining of the current interseption (2 separate interseption instances mixed together).

#1st configuration: 
Fst_confg_players = np.asarray([home_lost_from_player,away_rec_from_player]).T
pass_confg_players = np.asarray([away_pass_From_To_players[0],away_pass_From_To_players[1]]).T

#2nd configuration :
# Snd_confg_players = np.asarray([away_lost_from_player,home_rec_from_player]).T





# Extract the players and the ball trajectories of the corresponding event:   
home_inter_trajs = []
#TODO Create a structures of the trajectories: 
# Accumulate the trajectories 
data_pass = []
for i,k in enumerate(away_pass_inter_frames):#enumerate(away_lost_inter_frames):
    print(i)
    print(k)
    # from_player = Fst_confg_players[0][i]
    # to_player = Fst_confg_players[1][i]
    ip1 = np.random.randint(100)
    ip2 = np.random.randint(100)
    from_player = pass_confg_players[i][0]
    to_player = pass_confg_players[ip2][1]

    #Extracting the event trajectories for player-to-player-ball trajectories: 
    plt_inst = True
    # if i== 10: 
    #     plt_inst = True
    # else: 
    #     plt_inst = False
    tracking_home, tracking_away, home_trajs, away_trajs, ball_traj  = ext_teams_Traj(tracking_home = tracking_home , tracking_away = tracking_away,s_ind = k[0],e_ind = k[1],plt_inst=plt_inst,ptclr_payers_list=[from_player,to_player])
    # tracking_home, tracking_away, home_trajs, away_trajs, ball_traj  = ext_teams_Traj(s_ind = k[0],e_ind = k[1],plt_inst=plt_inst)
    
    # Pickling the trajectories to be used in the inference: 
    player1_traj = away_trajs[0].T
    player2_traj = away_trajs[1].T
    ball1_traj = ball_traj.T
    data_inst = [player1_traj,player2_traj,ball1_traj]
    data_pass.append(data_inst)
    # Timing the signals (data is captured in 25Hz)
    T_len = len(ball1_traj)
    time_vector = np.linspace(0,0.04*T_len,T_len)
    
    if i == 6:
        #Trajectories in the x direction: 
        p1p2_Xtraj = abs(player1_traj[:,0]-player2_traj[:,0])  
        fig,ax = plt.subplots(figsize=(12,8))
        # ax.plot(time_vector ,p1p2_Xtraj , 'b', MarkerSize=1)
        # plt.xlabel(r'time [s]', fontsize=16)
        # plt.ylabel(r"$x$", fontsize=16)

        p1b_Xtraj = abs(player1_traj[:,0]-ball1_traj[:,0])  
        # fig,ax = plt.subplots(figsize=(12,8))
        ax.plot(time_vector ,p1b_Xtraj , 'b', MarkerSize=1)
        ax.plot(time_vector ,p1p2_Xtraj , 'b', MarkerSize=1)
        plt.xlabel(r'time [s]', fontsize=16)
        plt.ylabel(r"$x$", fontsize=16)

        p2b_Xtraj = abs(player2_traj[:,0]-ball1_traj[:,0])  
        fig,ax = plt.subplots(figsize=(12,8))
        ax.plot(time_vector ,p2b_Xtraj , 'b', MarkerSize=1)
        plt.xlabel(r'time [s]', fontsize=16)
        plt.ylabel(r"$x$", fontsize=16)

        #Trajectories in the y direction: 
        p1p2_Ytraj = abs(player1_traj[:,1]-player2_traj[:,1])
        fig,ax = plt.subplots(figsize=(12,8))
        ax.plot(time_vector ,p1p2_Ytraj , 'b', MarkerSize=1)
        plt.xlabel(r'time [s]', fontsize=16)
        plt.ylabel(r"$y$", fontsize=16)

        p1b_Ytraj = abs(player1_traj[:,1]-ball1_traj[:,1])  
        fig,ax = plt.subplots(figsize=(12,8))
        ax.plot(time_vector ,p1b_Ytraj , 'b', MarkerSize=1)
        plt.xlabel(r'time [s]', fontsize=16)
        plt.ylabel(r"$y$", fontsize=16)

        p2b_Ytraj = abs(player2_traj[:,1]-ball1_traj[:,1])  
        fig,ax = plt.subplots(figsize=(12,8))
        ax.plot(time_vector ,p2b_Ytraj , 'b', MarkerSize=1)
        plt.xlabel(r'time [s]', fontsize=16)
        plt.ylabel(r"$y$", fontsize=16)

    
    a = 1 
# saveData(dataAsList = data_pass,fileName ='Game2_AwayTeam_NegEx' ,enFlag=True)
a = 1 




# Extracting +ve and -ve examples: 
#-------------------------------------------
# Loosing the ball (home team): 

#Recovering the ball (home team):
