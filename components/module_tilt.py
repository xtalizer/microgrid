#Tilted Angle Power Calcs

import math

def cval(day):
    days=[31,28,31,30,
          31,30,31,31,
          30,31,30,31]
    c=[0.058,0.060,0.071,0.097,
       0.121,0.134,0.136,0.122,
       0.092,0.073,0.063,0.057]
    day_count=day-21
    for p in range(0,len(days)):
        if(day_count<0 and p==0):
            return c[11]
        elif (day_count<0):
            return c[p-1]
        day_count=day_count-days[p]
    return c[11]

def irradiance_tilted(ghi,dni,albedo,tilt_mod,latitude,angledata):
    
    SOLAR=1361
    
    #convert to radians
    latitude=math.radians(latitude)
    zenith=math.radians(angledata[0])
    declination=math.radians(angledata[1])
    tilt_mod=math.radians(tilt_mod)
    hour_angle=math.radians(angledata[2])
    azimuth_solar=math.radians(angledata[3])
    day=angledata[4]
    
    #r_b calculation
    if(azimuth_solar<math.pi/2 and azimuth_solar>-math.pi/2):
        azimuth=0
    else:
        azimuth=math.pi
    cos_incidence=math.cos(zenith)*math.cos(tilt_mod)+(
        math.sin(zenith)*math.sin(tilt_mod)*math.cos(azimuth_solar-azimuth))
    r_b=cos_incidence/math.cos(zenith)
    
    #diffuse component calculation
    ir_diff=cval(day)*dni
    
    #beam component calculation
    ir_beam=ghi-ir_diff
    
    #extraterrestrial component calculation
    sunshine=math.acos(-math.tan(declination)*math.tan(latitude))
    ir_ex=(24/math.pi)*SOLAR*(1+0.033*math.cos(2*math.pi*day/365))*(
        sunshine*math.sin(latitude)*math.sin(declination)
        +math.cos(latitude)*math.cos(declination)*math.sin(sunshine))
      
    #tilted power
    aniso=ir_beam/ir_ex
    ir_tilt=((ir_beam+ir_diff*aniso)*r_b)+(
        ghi*albedo*(1-math.cos(tilt_mod))/2)+(
        ir_diff*(1-aniso)*(1+math.cos(tilt_mod))/2*(1+math.sin(tilt_mod/2)**3))
        
    return ir_tilt