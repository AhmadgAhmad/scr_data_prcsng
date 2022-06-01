**Labeled dataset of soccer events with the corresponding trajectories**


For each datapoint create a ['Label','Feature'] pairs, where
- Label = 'Team name'+'_'+'Event Type'+'_'+'event subtype if exists'
- Feature = [[(x_p1,y_p1,speed_p1,heading_p1),...,(x_p11,y_p11,speed_p11,heading_p11)],
[(x_p12,y_p12,speed_p12,heading_p12),...,(x_p22,y_p22,speed_p22,heading_p22)],[(x_ball,y_ball,theta_ball,v_ball,ball)]]: 
23 X 1 list of players and the ball trajectories and heading, where
(x,y,speed,v): n X 4 trajectory matrix. 

![alt text]([http://url/to/img.png](https://github.com/AhmadgAhmad/scr_data_prcsng/blob/master/OutputData/SoccerField.emf))
