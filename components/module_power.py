#Efficiency

import math

def module_power(
    temp_stc,irradiance_stc,amps_stc,volt_stc,pow_stc,
    temp_noct,temp_amb,ir_tilt):
    
    #calcs
    temp_mod=(temp_noct-20)*ir_tilt/800+temp_amb
    amps_mod=(ir_tilt/irradiance_stc)*(1+1.2e-3*(temp_mod-temp_stc))*amps_stc
    volt_mod=(1+0.033*math.log(ir_tilt/irradiance_stc)
              -0.0092*(math.log(ir_tilt/irradiance_stc))**2
              -4.6e-3*(temp_mod-temp_stc))*volt_stc
    eff_mod=(amps_mod*volt_mod*irradiance_stc)/(amps_stc*volt_stc*ir_tilt)
    pow_mod=eff_mod*pow_stc*ir_tilt/irradiance_stc
    
    return pow_mod