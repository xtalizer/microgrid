#PV Sizing

import math   
import load_profile
import irradiance
import module_tilt
import module_power
import solar_angle

def spfloor(x):
    if (math.floor(x)==0):
        return 1
    else:
        return math.floor(x)

## Date and Location ##
date=[1,1,3]
utc=math.ceil(82.95/15) #8
latitude=41.717#14.654284
longitude=82.95 #121.066269

## Meteorological Parameters ##
ref=0.24
ref_min=0.23 #albedo
ref_max=0.8
temp_amb=-10.6#24.8
temp_min=-15.1#21.9
temp_max=-5.87#28.6
cm_ozone=0.288 #0.213
cm_water=2.25 #4.25
ka_380=0.13 #0.16
ka_500=0.13 #0.16
pressure=101325

## Load Parameters ##
rel_load=[525,525,525,525,
          525,665,665,665,
          645,645,645,645,
          645,645,645,645,
          645,735,735,735,
          741,621,621,615]
kwhmo_load=150

## PV Module Parameters ##

#STC Specifications
volt_stc=68.2
amps_stc=6.39
eff_stc=0.154
pow_stc=230.5
irradiance_stc=1000.0 #watts
temp_stc=25

#Partial Derivatives
volt_change=-0.0035*volt_stc #partial derivative of voltage with temperature
amps_change=0.00056*amps_stc #partial derivative of current with temperature
pow_change=-0.0045*pow_stc

#Misc
length=1.625
width=1.019
temp_noct=48
volt_mod_mpp=31.2

#Design Constraints
tilt_mod=10
sf_mod=1
elevation=1100

## Battery Specifications ##

#Battery Specifications
volt_nom=3.8 #open circuit voltage
amphour_full=2.6 #charge

#Design Constraints
days_auto=1 #days of autonomy
sf_batt=1 #sizing factor
dod=0.8 #max discharge (temporary)
volt_bb=96 #battery bank voltage

## Calculations ##

#load Profile Calculations
kwh_load=kwhmo_load/30.0
load=load_profile.actual_load(kwhmo_load,rel_load)

#battery Calculations
kwh_bb=days_auto*kwh_load*sf_batt/dod
kwh_batt=volt_nom*amphour_full/1000
n_bat=math.ceil(kwh_bb/kwh_batt)
n_batser=volt_bb/volt_nom
n_batpar=math.ceil(n_bat/n_batser) #number of batteries

#determine power generation at each time of the day
pv=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for p in range(0,len(pv)):
    angledata=solar_angle.angle_data(date,[p,30],utc,longitude,latitude)
    if(angledata[0]<=0):
        pv[p]=0
    else:
        solardata=irradiance.irradiance_data(
            ref,ref_min,ref_max,temp_amb,temp_min,temp_max,
            cm_ozone,cm_water,ka_380,ka_500,
            elevation,pressure,angledata[0])
        print(solardata)
        ir_tilt=module_tilt.irradiance_tilted(
            solardata[0],solardata[1],ref_min,tilt_mod,latitude,angledata)
        if(ir_tilt<=0):
            pv[p]=0
        else:
            pv[p]=module_power.module_power(
                temp_stc,irradiance_stc,amps_stc,volt_stc,pow_stc,
                temp_noct,temp_amb,ir_tilt) #unit: W

#determine total power generation (Simpsons rule)
integral=0
pv.append(pv[0])
for q in range(1,(1+len(pv))//2):
    integral=integral+pv[2*q-2]+4*pv[2*q-1]+pv[2*q]
del pv[len(pv)-1] #remove added item
integral=integral*(24.0/len(pv))/3.0 #Wh/m^2

#determine number of modules used
n_mod=math.ceil((kwh_load*sf_mod*1000)/(length*width*integral))
n_modser=spfloor(volt_bb/volt_mod_mpp)
n_modpar=math.ceil(n_mod/n_modser)

#determine profiles
pv_total=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
load_total=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
batt_total=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for x1 in range(0,len(load_total)):
    load_total[x1]=load[x1]*(-1000)
for x2 in range(0,len(pv_total)):
    pv_total[x2]=pv[x2]*n_mod*length*width
for x3 in range(0,len(batt_total)):
    batt_total[x3]=-(load_total[x3]+pv_total[x3])
'''
#generate text file
writer=open('pv_data.txt','w')
writer.write('(Copy to spreadsheet)\n')
writer.write('\n')
writer.write('Load (W)\n')
for inc1 in range(0,len(load_total)):
    writer.write(str(load_total[inc1])+'\n')
writer.write('\n')
writer.write('Battery (W)\n')
for inc2 in range(0,len(batt_total)):
    writer.write(str(batt_total[inc2])+'\n')  
writer.write('\n')
writer.write('PV (W)\n')
for inc3 in range(0,len(pv_total)):
    writer.write(str(pv_total[inc3])+'\n')
'''
#output in console
print('+----------+----------+----------+----------+')
print('| {0:8} | {1:8} | {2:8} | {3:8} |'.format('Hour','Load (W)','Batt (W)','PV (W)'))
print('+----------+----------+----------+----------+')
for inc4 in range(0,24):
    print('| {0:8} | {1:8} | {2:8} | {3:8} |'.format(inc4,load_total[inc4],batt_total[inc4],pv_total[inc4]))
print('+----------+----------+----------+----------+')
print('')
print('Daily load (kWh): {0:.4f}'.format(kwh_load))
print('')
print('Number of batteries: {0:.0f}'.format(n_bat))
print('Energy from batteries (kWh): {0:.4f}'.format(kwh_bb))
print('')
print('Number of PV modules: {0:.0f}'.format(n_mod))
print('Energy from PV (kWh): {0:.4f}'.format(length*width*integral*n_mod/1000))

