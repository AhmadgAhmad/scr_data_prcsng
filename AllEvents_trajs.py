"""
@ Ahmad Ahmad

This script search for all possible events in the events dataset, 
and extract the corresponding trajectory for each event from the trajectory dataset.


For each datapoint create a ['Label','Feature'] pairs, where
- Label = 'Team name'+'_'+'Event Type'+'_'+'event subtype if exists'
- Event_plyrs = [plyr 1, plyr 2 (if exist)]
- Feature = [[(x_p1,y_p1,speed_p1,heading_p1),...,(x_p11,y_p11,speed_p11,heading_p11)],
[(x_p12,y_p12,speed_p12,heading_p12),...,(x_p22,y_p22,speed_p22,heading_p22)],[(x_ball,y_ball,theta_ball,v_ball,ball)]]: 
23 X 1 list of players and the ball trajectories and heading, where
(x,y,speed,v): n X 4 trajectory matrix. 



"""

from cmath import nan
from sympy import false
from Metrica_IO import *
from Metrica_EPV import *
import Metrica_Viz as mviz
import Metrica_Velocities as mvel
import matplotlib.pyplot as plt
from extr_evts_trajs import *
import numpy as np
import pickle
import os
import math
import json


def main():
    # Extract the names of all possible events: 
    # set up initial path to data
    script_dir = os.path.dirname(__file__)
    DATADIR = os.path.join(script_dir, 'Eevnts_Trajs_data/')
    # DATADIR = 'C:/Users/ahmad/Documents/Graduate_study/PhD_work/First_Fall-2021/TLI/MAESTRO_group_inferring/MetrcaSport_data/sample-data-master/data'
    game_id = 2 # let's look at sample match 2

    # read in the event data
    #---------------------------------------------------------------------------------------------------------------------------
    events = mio.read_event_data(DATADIR,game_id)
    print( events['Type'].value_counts())           # count the number of each event type in the data
    events = mio.to_metric_coordinates(events)      # transform the coordinates to meters such that the center of the filed is the (0,0) position
    
    tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
    tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

    # Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
    tracking_home = mio.to_metric_coordinates(tracking_home)
    tracking_away = mio.to_metric_coordinates(tracking_away)
    # reverse direction of play in the second half so that home team is always attacking from right->left
    tracking_home,tracking_away,events = mio.to_single_playing_direction(tracking_home,tracking_away,events)
    
    # Calculate player velocities and headings 
    tracking_home = mvel.calc_player_velocities_heading(tracking_home,smoothing=True)
    tracking_away = mvel.calc_player_velocities_heading(tracking_away,smoothing=True)

    # Calculate player x-velocity and y-velocity and use each one in the image channel [to mitigate the discontinuity of mapping the angle to the line]. 



    #------------------------------------------------------------------------------------------------------------------------

    
    # For each event, find the initial and final time frames of the event: 
    # Search for (event, subevent) pairs:
    Team = events['Team']
    Type = events['Type']
    Subtype = events['Subtype']
    SFrame = events['Start Frame']
    EFrame = events['End Frame']
    Plyr1 = events['From']
    Plyr2 = events['To']
    dataset_game1  = []
    for (ev_team,ev_type,ev_subtype,ev_sframe,ev_eframe,plyr1,plyr2) in zip(Team,Type,Subtype,SFrame,EFrame,Plyr1,Plyr2): 
        ev_plyrs = [None,None]
        # Event Label: 
        if type(ev_subtype) != 'str': 
            ev_label =  ev_team+'_'+ev_type
        else:
            ev_label =  ev_team+'_'+ev_type+'_'+ev_subtype
        # Event Players: 
        if type(plyr1) is str: 
            ev_plyrs[0] = int(plyr1[6:])
        if type(plyr2) is str: 
            ev_plyrs[1] = int(plyr2[6:])        
        #Event feature: 
         # Home team
        home_trajs = [None]*11
        # Away team: 
        away_trajs = [None]*11
        #The ball :
        ball_traj = []

        #++Extracting the trajectories++  
        
        Hp_names =list(np.linspace(1,11,11))
        Ap_names =list(np.linspace(15,25,11))    
        for i,p_name in enumerate(Hp_names): #todo Fix: when returning the trajs with the correct label of each player
            #The trajectory of each player: 
            try:
                # home_trajs[i] = np.asarray([tracking_home['Home_%d_x'%p_name].iloc[ev_sframe:ev_eframe], tracking_home['Home_%d_y'%p_name].iloc[ev_sframe:ev_eframe],\
                # tracking_home['Home_%d_speed'%p_name].iloc[ev_sframe:ev_eframe], tracking_home['Home_%d_heading'%p_name].iloc[ev_sframe:ev_eframe]]).T
                home_trajs[i] = np.asarray([tracking_home['Home_%d_x'%p_name].iloc[ev_sframe:ev_eframe], tracking_home['Home_%d_y'%p_name].iloc[ev_sframe:ev_eframe],\
                tracking_home['Home_%d_vx'%p_name].iloc[ev_sframe:ev_eframe], tracking_home['Home_%d_vy'%p_name].iloc[ev_sframe:ev_eframe]]).T

            except:
                raise('The provided player name is not from the home team.')
        
        for i,p_name in enumerate(Ap_names): 
            try: 
                # away_trajs[i] = np.asarray([tracking_away['Away_%d_x'%p_name].iloc[ev_sframe:ev_eframe], tracking_away['Away_%d_y'%p_name].iloc[ev_sframe:ev_eframe],\
                # tracking_away['Away_%d_speed'%p_name].iloc[ev_sframe:ev_eframe], tracking_away['Away_%d_heading'%p_name].iloc[ev_sframe:ev_eframe]]).T
                away_trajs[i] = np.asarray([tracking_away['Away_%d_x'%p_name].iloc[ev_sframe:ev_eframe], tracking_away['Away_%d_y'%p_name].iloc[ev_sframe:ev_eframe],\
                tracking_away['Away_%d_vx'%p_name].iloc[ev_sframe:ev_eframe], tracking_away['Away_%d_vy'%p_name].iloc[ev_sframe:ev_eframe]]).T
            except:
                raise('The provided player name is not from the away team.')

        # ball_traj = np.asarray([tracking_away['ball_x'].iloc[ev_sframe:ev_eframe], tracking_away['ball_y'].iloc[ev_sframe:ev_eframe]\
        #     ,tracking_away['ball_speed'].iloc[ev_sframe:ev_eframe], tracking_away['ball_heading'].iloc[ev_sframe:ev_eframe]]).T
        ball_traj = np.asarray([tracking_away['ball_x'].iloc[ev_sframe:ev_eframe], tracking_away['ball_y'].iloc[ev_sframe:ev_eframe]\
            ,tracking_away['ball_vx'].iloc[ev_sframe:ev_eframe], tracking_away['ball_vy'].iloc[ev_sframe:ev_eframe]]).T 
            
        feature = [home_trajs,away_trajs,ball_traj]
        #Data point: 
        data_point = {'Label':ev_label, 'Event_plyrs':ev_plyrs,'Feature':feature}
        dataset_game1.append(data_point) 

    saveData(dataAsList = dataset_game1,fileName ='dataset_game2_wps' ,enFlag=True)
    a = 1





    # For each event frames, extract the feature of each player, i.e. (x,y,theta,v,team_name): n X 5. 


    #Create the datapoints ['label', 'feature']: 
   






if __name__ == '__main__':
    # a = json.open('dataset_game1.json')
    main()
