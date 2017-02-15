#Global Horizontal Irradiance Data

import math

def irradiance_data(
    ref,ref_min,ref_max,temp,temp_min,temp_max,
    cm_ozone,cm_water,ka_380,ka_500,
    elevation,pressure,zenith):
    '''
    returns global horizontal irradiance (GHI)
    and direct normal irradiance (DNI) in W/m^2
    format: [GHI,DNI]
    '''
    
    SOLAR=1361 #solar constant
    
    zenith=math.radians(zenith)
    
    if(zenith<math.pi/2):
        
        #air mass
        am=1/((math.cos(zenith)+0.15*(93.885-math.degrees(zenith)))**(-1.253))
        amp=am*pressure*math.exp(-0.0001184*elevation)/101325
        
        #rayleigh scattering
        t_ra=math.exp(-0.0903*amp**0.84*(1+amp-amp**1.01))
        
        #gas transmittance
        t_ga=math.exp(-0.0127*amp**0.26)
        
        #ozone transmittance
        chi=cm_ozone*am
        t_o3=1-(0.1611*chi*(1.0+139.48*chi)**(-0.3035)-0.002715*chi/(1+0.044*chi+0.0003*chi**2))
        
        #water transmittance
        gamma=cm_water*am
        t_wv=1-(2.4959*gamma/((1+79.034*gamma)**0.6828+6.385*gamma))
        
        #aerosol transmittance
        ka=0.2758*ka_380+0.35*ka_500
        t_ae=math.exp(-ka**0.873*(1+ka-ka**0.7088)*amp**0.9108)
        
        #preliminary calcs
        cg1=0.0000509*elevation+0.868
        cg2=0.0000392*elevation+0.0387
        fh1=math.exp(-elevation/8000)
        fh2=math.exp(-elevation/1250)
        
        #linke turbidity factor
        bncl=SOLAR*t_ra*t_ae*t_o3*t_ga*t_wv
        b=0.664+0.163/fh1
        tl=1+11.1*math.log(b*SOLAR/bncl)/am
        
        #clouds
        ci_vis=(ref-ref_min)/(ref_max-ref_min)
        ci_ir=(temp-temp_min)/(temp_max-temp_min)
        ci=max(ci_vis,ci_ir)
        t_vis=math.exp(-0.1*ci_vis)
        t_ir=math.exp(-0.07*ci_ir)
        
        #ghi
        ktm=2.36*ci**5-6.2*ci**4+6.22*ci**3-2.63*ci**2-0.58*ci+1
        ghc=cg1*SOLAR*math.cos(zenith)*math.exp(-1*cg2*am*(fh1+fh2*(tl-1)))*math.exp(0.01*am**1.8)
        ghi=ktm*ghc*(0.0001*ktm*ghc+0.9)

        #dni
        dni=0.9751*SOLAR*t_ra*t_ae*t_o3*t_ga*t_wv*t_vis*t_ir
        
        return [ghi,dni]
    
    else:
        return [0,0]