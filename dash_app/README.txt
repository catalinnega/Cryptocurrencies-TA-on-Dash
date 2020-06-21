To add an indicator graph:
  - ../indicators_lib.py :  
    - update indicator list with 
      - indicator name and id 
      - indicator dash lib*, indicator settings** and indicator object***.     
        * The indicator lib is an {indicator_name}.py file in the dash_app directory.
        ** The indicator settings is imported from ../indicators/{indicator_name}/{indicator_name}_settings.py
        *** The indicator object is imported from ../indicators/{indicator_name}/{indicator_name}_obj.py
 
The lib file contains: 
    - a get_graph() method which
        - takes the following args:
            ts_ochlv - this is the array of OCHLV timestamps
            o,c,h,l,v - the OCHLV variables
            ts - the indicator timestamps
            **indicator_args - the indicator specific variables. IMPORTANT: the arguments names must be the name as the keys of the returned dict from dash_app.getters.get_vals() method!!
        - returns a plotly graph obj.
        
        
            
            
