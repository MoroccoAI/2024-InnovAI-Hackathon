'''
Hydrus Parameter file adaptor:
    This modules changes a specific parameter of the Hydrus input file 
    and runs the model with the adapted parameter files.
    Specifically created for the 1D columns model of the project,
    but easy to adapt to other model configurations

Project: Phd Meisam Rezaei
Author: Van Hoey Stijn


TODO:
    Hydrus Routine
        -OK input: change water parameter and rerun hydrus
        -OK output: read the output file and prepare for plot, save,...
    Local sensitivity:
        -OK define parameter-adjustment step
        -OK sensitivity calculation function in for loop (all pars and all outputs)
        -OK plots in time (4 output plots, all pars in one plot)
'''

import os
import sys
import time
import datetime
import subprocess

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm

#------------------------------------------------------------------------------
# INPUT/OUTPUT ROUTINES
#------------------------------------------------------------------------------

def replaceInputWater(path_to_dir, newvalue, parname='Ks', layer=1):
    '''
    The Hydrus input file Selector.in always puts the water flow in BLOCK B
    The parameters values are given for each profile layer under the parameter
    name. As such, this definition search for the parameter and layer and 
    changes the par.
    
    Parameters
    -----------
    path_to_dir: 
        Directory with the Hydrus-input and output files in
    newvalue: 
        New parameter value to be used, %.9f value
    parname:
        The name of the parameter as is appears in the file
    layer:
        The layer where the parameter need to be changed
    '''
    try:
        os.rename(os.path.join(path_to_dir,'Selector.in'),os.path.join(path_to_dir,'Selector_old.in'))
    except:
        os.remove(os.path.join(path_to_dir,'Selector_old.in'))
        os.rename(os.path.join(path_to_dir,'Selector.in'),os.path.join(path_to_dir,'Selector_old.in'))
        
    fin = open(os.path.join(path_to_dir,'Selector_old.in'),'r')
    fout = open(os.path.join(path_to_dir,'Selector_new.in'),'wt')
    fintext = fin.readlines()
    #Get line with par headers assuming Ks is always a parameter
    #using the parameter is not possible, since eg 'n' woul give errors
    parstartline = fintext.index([x for x in fintext if 'Ks' in x][0])
    #Get index (column) of the parameter
    parcolumn = fintext[parstartline].split().index(parname)
    
    #adapting the lines after it
    adaptline = parstartline + layer
    parline = fintext[adaptline].split()
    parline[parcolumn] = '%.9f' % newvalue
    #we assume the floats are printed in eigth characters '%8s'
    parline_new = ['%18s'%i for i in parline]
    fintext[adaptline] = ''.join(parline_new)+'\n'
    fout.writelines(fintext)
    
    fin.close()
    fout.close()
    os.rename(os.path.join(path_to_dir,'Selector_new.in'),os.path.join(path_to_dir,'Selector.in'))


def runHydrus(guessed_runtime=8, path_to_dir='D:\\Python_sensitivity\\1Dmodel2',
              install_dir="C:\\Program Files (x86)\\PC-Progress\\Hydrus-1D 4.xx"):
    '''
    Run the Hydrus model from within Python
    
    Parameters
    ------------
    guessed_runtime:
        runtime of the model, in seconds (take some seconds more)
    path_to_dir:
        path to the working directory with input/output of Hydrus
    install_dir:
        path to the installation directory of the Hydrus software       
    
    '''
    oversleep = False
#    cdtorun='"C:\\Program Files\\PC-Progress\\Hydrus-1D 4.xx\\H1D_CALC.EXE"  D:\\Projecten\\2013_Meisam\\1D_model'
    cdtorun=os.path.join(install_dir,'H1D_CALC.EXE')+' '+path_to_dir
    print(cdtorun)
    proc = subprocess.Popen(cdtorun)

    time.sleep(guessed_runtime) #time nothing is happening to let model run
    proc.terminate()
    
    #WINDOWS ONLY: ADAPT FOR LINUX:
#    subprocess.Popen("taskkill /F /T /PID %i"%proc.pid , shell=True) 
    
    #control if sleep was long enough
    #all files with the .out extension need to have 'end' in the last line
    #except of the balance, which has the runtime
    #When doing multiple runs, the calculation time of the first will be reused if this one was too short
    files_in_dir = os.listdir(path_to_dir)
    for file_in_dir in files_in_dir:
        if file_in_dir[-4:]=='.out':
            f=open(os.path.join(path_to_dir,file_in_dir))
            try:
                f.seek(-100, os.SEEK_END) #100 should be enough for the purpose here
            except:
                f.seek(0) #100 should be enough for the purpose here
                
            line = f.readlines()[-1]
            if file_in_dir ==  'Balance.out':             
                print(line)
            else:
                if line != 'end\n':
                    print(f'The sleep time was not long enough to perform the entire simulation. '
                          'The file',{file_in_dir},'has not the entire simulation period written.')
                    oversleep = True
            f.close()
    return oversleep


def filter_on_timestep(infile='Obs_Node.out',outfile='Obs_Node_filtered.out', nnodes=5):
    '''
    Reads the node file and deletes the not-measurement timesteps
    control the presence oif every timestep
    '''
    #calculate columns with data
    cols =nnodes*3+1
    conv_cnt=0
    convergence =True

    fin = open(infile) 
    fout = open(outfile, 'wt') 
    for line in fin.readlines(): 
        if not len(line.split())==cols: #copy the none-data rows
            fout.write(line) 
        elif line.split()[0] =='time': #copy the data header row
            fout.write(line)
            ftaker=True
        else:
            if ftaker==True: #Always take first line/timestep up
                fout.write(line)
                old = float(line.split()[0])
                ftaker=False
            if line.split()[0][-4:]=='0000': #only take timesteps with measurements 
                new= float(line.split()[0])
                if not abs(old-new) == 1.0:
                    print('Filtering on timestep',line.split()[0],'failed.', abs(old-new), 'hour is considered as timestep')
                if abs(old-new) == 0.0:
                    conv_cnt+=1
#                    print 'double outputs at timestep',line.split()[0]
                fout.write(line) 
                old = new
                
            if '**' in line:
                print('**..., so no convergence')
                convergence=False
            
    fin.close()
    fout.close()
    if conv_cnt >= 5:
        convergence=False
    return convergence

def readoutput_to_dataframe(filename='Obs_Node_filtered.out', startdate='3/1/2012 00:00', enddate='6/13/2012 03:00', variable='theta', nnodes=5):
    '''
    Reads data from file and puts it in a pandas dataframe to plot, handle,...
    Always considerd 5 nodes measured, hourly frequency and 12 header lines  
    
    Parameters
    -------------
    filename:
        Name of the file with the outputs of the model
    startdate: 
        Hour of the first output
    enddate:
        Hour of the last output
    variable:
        string of theta, h or flux, representing moisture, head or flux
    
    Notes
    ------
    #start-date=1march 2012, 00u
    #end-date=13jun 2012, 3u
    
    We do the date-managing with pandas here, since scikits outdated
    '''
    if nnodes==5:
        if variable == 'theta':
            cols = (2,5,8,11,14)
        elif variable == 'h':
            cols = (1,4,7,10,13)
        elif variable == 'flux':
            cols = (3,6,9,12,15)
        else:
            raise Exception('Variable must be theta, flux or h')
    elif nnodes==4:
        if variable == 'theta':
            cols = (2,5,8,11)
        elif variable == 'h':
            cols = (1,4,7,10)
        elif variable == 'flux':
            cols = (3,6,9,12)
        else:
            raise Exception('Variable must be theta, flux or h')
            
    outarray = np.loadtxt(filename, skiprows=11, usecols=cols, comments='end')
    rng = pd.date_range(start=startdate, end=enddate, freq='H')
    if nnodes==4:
        df = pd.DataFrame(outarray, index=rng, columns=['Node 10','Node 20','Node 30','Node 40'])   
    elif nnodes==5:
        df = pd.DataFrame(outarray, index=rng, columns=['Node 10','Node 20','Node 30','Node 40','Node 50'])   
    return df

def read_current_value():
    '''
    instead of giving a value, just read the original value from the current selector.in
    TODO
    '''
    pass

def check_for_error(path_to_model):
    '''
    Check in model directory for error messages
    '''
    files_in_dir = os.listdir(path_to_model)
    if 'Error.msg' in files_in_dir:
        raise Exception('ATTENTION: ERROR in model run!')

def create_default_selector(path_to_model, def_values =([0.4,0.015,2.4,2.18,0.5],[0.35,0.01965,2.5, 2.271,0.5])):
    '''
    To make sure, the default parameters are always used before the 
    sensitivity indices are calculated.

    #original values - defvalues
    #   thr     ths    Alfa      n         Ks       l
    #      0     0.4   0.015     2.4       2.18     0.5 
    #      0    0.35 0.01965     2.5      2.271     0.5  
    
    TODO: adapt to make generic
    '''
    parnames=['ths','Alfa','n','Ks','l']
#    parlayer1=[0.0,0.4,0.015,2.4,2.18,0.5]
#    parlayer2=[0.0,0.35,0.01965,2.5, 2.271,0.5]
    ide=0
    for par in parnames:
        replaceInputWater(path_to_model, def_values[0][ide], parname=parnames[ide], layer=1)
        replaceInputWater(path_to_model, def_values[1][ide], parname=parnames[ide], layer=2)
        ide+=1

#------------------------------------------------------------------------------
#  LOCAL SENSITIVITY ANALYSIS
#------------------------------------------------------------------------------

def calculate_sens(path_to_model, parameter_value, perturbation_factor = 0.01, parameter_name='Ks', parameter_layer=1,
                   startdate='3/1/2011 00:00', enddate='6/13/2012 03:00', variable = 'theta', guessed_runtime=8,
                   nnodes=5, install_dir="C:\\Program Files (x86)\\PC-Progress\\Hydrus-1D 4.xx"):
    '''
    run model two (or three) times and get outputs to calculate the sensitivity indices
    one parameter changes, all the rest stays the same; all outputs are plotted
    
    make class from it to avoid the startdate/endddate arguments... TODO!
    '''
    #Make default parameter file before starting analysis
    create_default_selector(path_to_model)
    
    #run model with parameter value-> depreciated
#    replaceInputWater(path_to_model, parameter_value, parname=parameter_name, layer=parameter_layer)
#    runHydrus(guessed_runtime=guessed_runtime)  
#    filter_on_timestep(infile=os.path.join(path_to_model,'Obs_Node.out'),outfile=os.path.join(path_to_model,'Obs_Node_filtered1.out'))
#    df_par = readoutput_to_dataframe(filename=os.path.join(path_to_model,'Obs_Node_filtered1.out'), startdate=startdate, enddate=enddate, variable=variable)

    #run model with parameter value plus perturbation  
    replaceInputWater(path_to_model, parameter_value + perturbation_factor*parameter_value, parname=parameter_name, layer=parameter_layer)
    runHydrus(guessed_runtime=guessed_runtime, install_dir=install_dir)  
    filter_on_timestep(infile=os.path.join(path_to_model,'Obs_Node.out'),outfile=os.path.join(path_to_model,'Obs_Node_filtered2.out'), nnodes=nnodes)
    df_par_plus = readoutput_to_dataframe(filename=os.path.join(path_to_model,'Obs_Node_filtered2.out'), startdate=startdate, enddate=enddate, variable=variable, nnodes=nnodes)
    
    #run model with parameter value minus perturbation
    replaceInputWater(path_to_model, parameter_value - perturbation_factor*parameter_value, parname=parameter_name, layer=parameter_layer)
    runHydrus(guessed_runtime=guessed_runtime, install_dir=install_dir)  
    filter_on_timestep(infile=os.path.join(path_to_model,'Obs_Node.out'),outfile=os.path.join(path_to_model,'Obs_Node_filtered3.out'), nnodes=nnodes)
    df_par_min = readoutput_to_dataframe(filename=os.path.join(path_to_model,'Obs_Node_filtered3.out'), startdate=startdate, enddate=enddate, variable=variable, nnodes=nnodes)
    
    #calculate sensitivity for this parameter, all outputs    
    average_out = (df_par_plus+df_par_min)/2.
    #sensitivity indices:
    CAS = (df_par_plus-df_par_min)/(2.*perturbation_factor*parameter_value) #dy/dp
    CPRS = CAS*parameter_value    
    CTRS = CAS*parameter_value/average_out #or average_out  -> run less!
    
    #check for error files:
    check_for_error(path_to_model)
    return CAS, CPRS, CTRS, average_out, df_par_plus, df_par_min


#sensitivity for all pars in the two layers
def local_sensitivity(path_to_model,parnames, parvalues, 
                      perturbation_factor = 0.1, nnodes=5, startdate='3/1/2011 00:00', 
                      enddate='6/13/2012 03:00',  guessed_runtime=8,
                      install_dir="C:\\Program Files (x86)\\PC-Progress\\Hydrus-1D 4.xx"):
    '''
    Fo all parameters and all layers, do sensitivity
    plot CAS and CRS for all parameters
    '''
    #thr is assumed to be zero, sp not included
    #    parnames=['ths','Alfa','n','Ks','l']
    #    parlayer1=[0.4,0.015,2.4,2.18,0.5]
    #    parlayer2=[0.35,0.01965,2.5, 2.271,0.5]
    #    parvalues=([0.4,0.015,2.4,2.18,0.5],[0.35,0.01965,2.5, 2.271,0.5])
       
    layers = len(parvalues) #length of the tuple defines the number of layers
    ide=0    
    for par in parnames: #for every parameter
        print('Running the model for sensitivity calculation of parameter ',par)
        for lay in range(layers):
            worklayer=lay+1
            print('currently changing in layer ',str(worklayer))
            
            #calcluate for first layer
            CAS, CPRS, CTRS, outputs, df_par_plus, df_par_min = calculate_sens(path_to_model, parvalues[lay][ide], parameter_name=par, 
                                                                               parameter_layer=worklayer, 
                                                                               perturbation_factor = perturbation_factor, 
                                                                               nnodes=nnodes,
                                                                               startdate=startdate, enddate=enddate,  
                                                                               guessed_runtime=guessed_runtime,
                                                                               install_dir=install_dir)                                                                                       

            #Save outputs of CPRS in files without dates
            CPRS.to_csv('CPRS_l'+str(worklayer)+'_'+par+'.txt',index=False)
            CAS.to_csv('CPRS_l'+str(worklayer)+'_'+par+'.txt',index=False)
            CTRS.to_csv('CTRS_l'+str(worklayer)+'_'+par+'.txt',index=False)
        ide+=1 

def plot_sensitivity(par='Ks', senstype="CTRS", nnodes=5):
    '''
    Plot the outputs
    '''

# read Rain data
    rain = pd.read_csv('1DModel2\\rain.csv', index_col=0, names=['rain'], parse_dates=True,
                   dayfirst=True)
    #read the CPRS outputs
    CPRS1 = pd.read_csv(senstype+'_l1_'+par+'.txt')
    CPRS1.index=rain.index
    CPRS1_rain=rain.join(CPRS1)
    CPRS2 = pd.read_csv(senstype+'_l2_'+par+'.txt')
    CPRS2.index=rain.index
    CPRS2_rain=rain.join(CPRS2)   
    
    #PLOT THE CPRS-outputs------------------------------------------
    f = plt.figure(figsize=(16, 8))
    gs = gridspec.GridSpec(3, 1,height_ratios=[1,3,3])
    
#    ax1 = plt.subplot(gs[0])
#    ax2 = plt.subplot(gs[1])
#    ax3 = plt.subplot(gs[2])
    plt.subplots_adjust(hspace=0.08)
    
    ax1 = f.add_subplot(gs[0])
    ax2 = f.add_subplot(gs[1], sharex=ax1)
    ax3 = f.add_subplot(gs[2], sharex=ax1)    
    
#    rain in ax1
#  CPRS1_rain['rain'].plot(kind='bar',style='black',ax=ax1, xticks=[],yticks=[10,20,30,40])
    CPRS1_rain['rain'].plot(style='black',ax=ax1, xticks=[])#,yticks=[10,20,30,40])
    ax1.set_ylabel(r'rain (mm)')
    
    #parchange of layer 1 in ax2               
    CPRS1_rain['Node 10'].plot(ax=ax2,style='b', xticks=[])
    CPRS1_rain['Node 20'].plot(ax=ax2,style='g', xticks=[])
    CPRS1_rain['Node 30'].plot(ax=ax2,style='r', xticks=[])
    CPRS1_rain['Node 40'].plot(ax=ax2,style='y', xticks=[])
    if nnodes==5:
        CPRS1_rain['Node 50'].plot(ax=ax2,style='purple', xticks=[])
    ax2.set_ylabel(r' '+senstype+' - '+par+'$_1$')
    

    #parchange of layer 2 in ax3
    CPRS2_rain['Node 10'].plot(ax=ax3,style='b')
    CPRS2_rain['Node 20'].plot(ax=ax3,style='g')
    CPRS2_rain['Node 30'].plot(ax=ax3,style='r')
    CPRS2_rain['Node 40'].plot(ax=ax3,style='y')
    if nnodes==5:
        CPRS2_rain['Node 50'].plot(ax=ax3,style='purple')
    ax3.set_ylabel(r' '+senstype+' - '+par+'$_2$')
    

    # Shink current axis's height by 10% on the bottom
    box = ax3.get_position()
    ax3.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    
    # Put a legend below current axis
    ax3.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35),
              fancybox=False, shadow=False, ncol=5)           
              
#    ax1.xaxis.set_visible(False)
#    ax2.xaxis.set_visible(False)
    for tl in ax1.get_xticklabels():
            tl.set_visible(False)
    for tl in ax2.get_xticklabels():
            tl.set_visible(False)
    
    plt.savefig('CPRS_newversion'+par+'.pdf')

def quickplot(df,nnodes=5):
    """
    Test for docu;entation
    """
    f=plt.figure(figsize=(16,8))
    gs = gridspec.GridSpec(2, 1,height_ratios=[1,3])
    plt.subplots_adjust(hspace=0.08)
    ax1 = f.add_subplot(gs[0])
    ax2 = f.add_subplot(gs[1], sharex=ax1)
    rain.plot(ax=ax1,style='k', xticks=[])
    df['Node 10'].plot(ax=ax2,style='b')
    df['Node 20'].plot(ax=ax2,style='g')
    df['Node 30'].plot(ax=ax2,style='r')
    df['Node 40'].plot(ax=ax2,style='y')
    if nnodes==5:
        df['Node 50'].plot(ax=ax2,style='purple')
    # Shink current axis's height by 10% on the bottom
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])
    # Put a legend below current axis
    ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
              fancybox=False, shadow=False, ncol=5) 

#------------------------------------------------------------------------------
#  PARAMETER RESPONSE SURFACE
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Custom definition for contourplot---------------------------------------------
def Contour_ofspace(axs, Z, xmin, xmax, ymin, ymax, NumberLines=6, 
                addinline = False, colormapt=False, interpol = 'bilinear',
                *args, **kwargs):
    '''
    Contourplot made easier and nicer
    (Taken from pySTAN Package, Van Hoey Stijn)
    
    Parameters
    ------------
    axs: axes.AxesSubplot object
        an subplot instance where the graph will be located,
        this supports the use of different subplots 
    Z: narray 2D
        array to translate in controu lines
    xmin: float
        minimal x value
    xmax: float
        maximal x value
    ymin: float
        minimal y value
    ymax: float
        miaximal y value
    Numberlines: int
        number of levels t plot the contout lines
    addinline: bool
        if True, the labels of the lines are added
    colormapt: bool
        if True a colormap is added
    *args, **kwargs: arg
        passed to the plt.contour function 

    Returns
    --------
    axs instance
    
    Examples
    ----------
    >>> fig = plt.figure()
    >>> axs = fig.add_subplot(111)
    >>> Z=np.random.random((10,10))
    >>> xmin,xmax,ymin,ymax = 0.0,1.0,0.,1.
    >>> ContourPlot(axs,Z,xmin,xmax,ymin,ymax,NumberLines=3,
                addinline = True, colormapt=True, colors='k', linestyle = ':')

    '''
    #calculates step to use for number of elements
    delta1 =(float(xmax)-float(xmin))/float((Z.shape[1]-1))
    delta2 =(float(ymax)-float(ymin))/float((Z.shape[0]-1))
    #make grid
    x = np.arange(xmin, xmax+1e-10, delta1)
    y = np.arange(ymin, ymax+1e-10, delta2)
    X, Y = np.meshgrid(x, y)

##    #handmatig de levels ingeven, waar je lijn wil hebben...
##    levels = np.arange(-1.2, 1.6, 0.2)
##    CS = plt.contour(Z, levels,origin='lower',linewidths=2,
#                       extent=(-3,3,-2,2)) 
        #enkel werkzaam als X,Y niet opgegeven in contour

    CS = axs.contour(X, Y, Z, NumberLines, *args,
                     **kwargs) #, origin='lower', colors='k'
    
    if addinline == True:
        axs.clabel(CS, fontsize=9, inline=1)

    #always plotting colormap, but adapting alpha 
    #makes sure that the boundaries are correct
    if colormapt == True:
        alphat = 0.85
    else:
        alphat = 0.0
        
    #colormap for image
    im = axs.imshow(Z, interpolation=interpol, origin='lower', 
                    cmap=cm.gray, extent=(xmin, xmax, ymin, ymax), 
                    alpha=alphat)
    
    axs.set_aspect('auto')                    
    if colormapt==True:
        plt.colorbar(im, orientation='horizontal', shrink=0.8)

    return axs
# end custom definition for contourplot----------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------    
#definition for reading measurements-------------------------------------------
def read_meas(filename='vocht_metingen.csv', start='5/14/2011 08:00', 
              end='9/2/2011 11:00', nnodes=5):
    '''
    READ MEASUREMENTS and crop the timeserie from given start-end dates
    '''  
    meas = pd.read_csv(filename, index_col=0, header=0, parse_dates=True, dayfirst=True)
    if nnodes==5:
        meas.columns=['Node 10','Node 20','Node 30','Node 40','Node 50']
    elif nnodes==4:
        meas.columns=['Node 10','Node 20','Node 30','Node 40']
    else:
        raise Exception('Only valid for 4 or 5 nodes')
        
    subrng = pd.date_range(start='5/14/2011 08:00', end='9/2/2011 11:00', freq='H')
    meas_calib =  meas.reindex(index=subrng)/100.
    
    return meas_calib
# end definition for reading measurements--------------------------------------
#------------------------------------------------------------------------------    

#------------------------------------------------------------------------------    
#definition for response surface-----------------------------------------------
def par_response_surface(path_to_model, x1min, x1max, x2min,  x2max, parname1,
                         parname2, meas, par1_layer = 1, par2_layer = 1,
                         ndx=100, ndy=100, 
                         startdate='5/14/2011 8:00', 
                         enddate='9/2/2011 11:00',
                         meas_start = '5/14/2011 08:00', 
                         meas_end = '9/2/2011 11:00', plotnlines= 4,
                         saveit=False, interpol = 'bilinear',
                         install_dir="C:\\Program Files (x86)\\PC-Progress\\Hydrus-1D 4.xx"):
    """
    """

    x = np.linspace(x1min,x1max,ndx)
    y = np.linspace(x2min, x2max,ndy) 
    print(x,y)
    X,Y = np.meshgrid(x, y)
    
    parspace=np.zeros((x.size,y.size))
    create_default_selector(path_to_model, def_values =([0.4,0.015,2.4,2.18,0.5],[0.35,0.01965,2.5, 2.271,0.5]))
    for i in range(x.size):
        x1=x[i]
        for j in range(y.size):
            x2=y[j]
            replaceInputWater(path_to_model, x1, parname=parname1, layer=par1_layer)
            replaceInputWater(path_to_model, x2, parname=parname2, layer=par2_layer)
            
            oversleep = runHydrus(guessed_runtime=5, path_to_dir= path_to_model, install_dir=install_dir)
            converge = filter_on_timestep(infile=os.path.join(path_to_model,'Obs_Node.out'),outfile=os.path.join(path_to_model,'Obs_Node_filtered.out'))
            if converge == True and oversleep == False:
                df = readoutput_to_dataframe(filename=os.path.join(path_to_model,'Obs_Node_filtered.out'), startdate=startdate, enddate=enddate, variable='theta')
                subrng = pd.date_range(start=meas_start, end=meas_end, freq='H')
                df_calib =  df.reindex(index=subrng)
                SSE=((meas-df_calib)**2).sum().sum()
                print(SSE)
            else:
                SSE = 1e8
            parspace[i,j]=SSE
    
    if saveit==True:
        np.savetxt('parspace_'+parname1+'_'+parname2+'_'+ str(datetime.date.today())+'.txt', parspace)    
    #parspace = np.loadtxt('parspace_Ks_ths_100el.txt')

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    Z=parspace.copy()
    xmin,xmax,ymin,ymax = x1min, x1max, x2min, x2max
    Contour_ofspace(ax1,Z,xmin,xmax,ymin,ymax,NumberLines=plotnlines, interpol =interpol,
                    addinline = True, colormapt=True, colors='k', linestyle = ':')
    return parspace, ax1
#end definition for response surface-------------------------------------------
#------------------------------------------------------------------------------    

#------------------------------------------------------------------------------ 
#definition to load previous result--------------------------------------------
def load_parspace(parspacefile, x1min, x1max, x2min, x2max, plotnlines= 7, 
                  interpol = 'bilinear'):
    """
    load a previous file
    """
    parspace = np.loadtxt(parspacefile)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    Z=parspace.copy()
    xmin,xmax,ymin,ymax = x1min, x1max, x2min, x2max
    Contour_ofspace(ax1,Z,xmin,xmax,ymin,ymax,NumberLines=plotnlines, interpol = interpol,
                    addinline = True, colormapt=True, colors='k', linestyle = ':')
    return ax1
# end definition to load previous result---------------------------------------
#------------------------------------------------------------------------------  

#------------------------------------------------------------------------------ 
#definition to plot previous result--------------------------------------------
def plot_parspace(parspace, x1min, x1max, x2min, x2max, plotnlines= 7, 
                  interpol = 'bilinear'):
    """
    load a previous file
    """
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    Z=parspace
    xmin,xmax,ymin,ymax = x1min, x1max, x2min, x2max
    Contour_ofspace(ax1,Z,xmin,xmax,ymin,ymax,NumberLines=plotnlines, interpol = interpol,
                    addinline = True, colormapt=True, colors='k', linestyle = ':')
    return ax1
# end definition to plot previous result---------------------------------------
#------------------------------------------------------------------------------ 




       
        
        
        
        
        
        
        
        
        
        
        
        
    

