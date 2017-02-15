#Solar Angle Calculations
    
import math
    
def daysinmonth(month,year):
    days=[31,28,31,30,31,30,31,31,30,31,30,31]
    daysum=0
    if(year%4==0):
        days[1]=29
    for p in range(0,month-1):
        daysum=daysum+days[p]
    return daysum

def invtan(y,x):
    theta=math.atan2(y,x)
    if(theta<0):
        theta=2*math.pi+theta
    return theta

def less90(x):
    if (x>90):
        return 0
    else:
        return x

def angle_data(date,time,utc,longitude,latitude):
    '''
    input date[mm,dd,yy] time[hh,mm], utc h in advance, longitude, latitude in degrees
    returns the solar angles as [azimuth,altitude] in degrees.
    '''
    
    #parameter calculations
    d=math.floor(365.25*date[2])+daysinmonth(date[0],date[2])+date[1]-0.5+(time[0]+time[1]/60.0-utc)/24.0
    q=(280.459+0.98564736*d)%360
    g=(357.529+0.98560028*d)%360
    lambda_s=q+1.915*math.sin(math.radians(g))+0.020*math.sin(2*math.radians(g))
    epsilon=23.429-0.00000036*d
    gmst=(18.697374558+24.06570982441908*d+0.000026*(d/36525)**2)%24
    theta_l=gmst*15+longitude
    
    #convert to radians
    theta_l=math.radians(theta_l)
    lambda_s=math.radians(lambda_s)
    epsilon=math.radians(epsilon)
    latitude=math.radians(latitude)
    
    #calculate coordinates
    y_s=-math.sin(theta_l)*math.cos(lambda_s)+math.cos(theta_l)*math.cos(epsilon)*math.sin(lambda_s)
    x_s=-math.sin(latitude)*math.cos(theta_l)*math.cos(lambda_s)-(math.sin(latitude)*math.sin(theta_l)*math.cos(epsilon)-math.cos(latitude)*math.sin(epsilon))*math.sin(lambda_s)
    z_s=math.cos(latitude)*math.cos(theta_l)*math.cos(lambda_s)+(math.cos(latitude)*math.sin(theta_l)*math.cos(epsilon)+math.sin(latitude)*math.sin(epsilon))*math.sin(lambda_s)
    
    zenith=less90(math.degrees(math.acos(z_s)))
    declination=math.degrees(math.asin(math.sin(epsilon)*math.sin(lambda_s)))
    hour_angle=15*(time[0]+time[1]/60-12)
    azimuth=math.degrees(math.atan2(y_s,x_s))
    day=d%365.25
    
    #[zenith,declination,hourangle,azimuth,day]
    return [zenith,declination,hour_angle,azimuth,day]