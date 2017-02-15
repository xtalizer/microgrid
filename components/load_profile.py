#Load Profile Generator

def actual_load(kWhmo_load,rel_load):
    '''
    input actual montly load and relative load profile[0-23h]
    returns actual load profile proportional to relative load profile
    '''
    
    rel_load.append(rel_load[0]) #integrate from 0 to 23 then back to 0
    
    #Simpson's Rule
    integral=0
    for p in range(1,(1+len(rel_load))//2):
        integral=integral+rel_load[2*p-2]+4*rel_load[2*p-1]+rel_load[2*p]
    del rel_load[len(rel_load)-1] #remove added item
    integral=integral*(24.0/len(rel_load))/3.0
    
    #Scale up the relative load
    scale=kWhmo_load/(30.0*integral)
    for q in range (0,len(rel_load)):
        rel_load[q]=scale*rel_load[q]
    
    return rel_load