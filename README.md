# Project-PHY571
Simulation of filamentary propagation of an intense beam

The respository is divided in different parts: 
* design : use for sketch the idea and solving problem (Normally, don't need to look at this code)
* production : the core of the respository, it contains the class defined the laser, calculation, algorithm, etc
and it is divided into :
  + laser.py : class for defining laser
  + gaussian.py : class for gaussian function
  + simulation_linear : calculate and save the result of diffraction term
  + simulation_kerr : calculate and save the result of diffraction term and Kerr term
  + simulation_plasma : calculate and save the result of plasma term
  + simulation_absorption : calculate and save the result of multiphoton absorption term
  + simulation_total : calculate and save the result of all terms (Attention this code takes time)
  + simulation_pertubation : calculate and save the result of all terms with pertubation (Attention this code takes time)
  
  **The file with the name simulation can be executed independently**
  
  **The file with the name analyze can be executed if you have results from production**
  
* analysis : after having the result from the code in production, the files jupyter notebook is executed correspond to the 
files python inside production

  + analyze_diffraction correspond to simulation_linear
  + analyze_kerr correspond to simulation_kerr
  + analyze_plasma correspond to simulation_plasma
  + analyze_absorption correspond to simulation_absorption
  + analyze_total correspond to simulation_total
  + analyze_pertubation correspond to simulation_pertubation
  
 * results : files that saved from production, and used to read and analyse in analysis
 * figures : images saved from analysis
  
              
