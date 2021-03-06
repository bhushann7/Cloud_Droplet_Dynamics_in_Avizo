 #This is a script developed to produce CLoudDropletVisualization for a given timestep range in Avizo
 #To run this script,copy the main code and paste in the Python console in Avizo and run
 #Output will be saved in the output directory specified in the Snapshot module

#------------------------------------ Main Script begins ---------------------------------------------

import os
import math
#-----------------------------------------------------------------------------

## Variables ##

# index to start reading files
start = 0
# number of files
nfiles = 35
# calculate index to stop reading files
stop = start + nfiles

## set pathways ##
eulrdir = "/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Eulerian/eul_data_for_avizo/Eul_100_TO_3500"
lagrdir = "/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Lagrangian/csv_data1/csv_100_TO_3500"

## get lists of files ##
eulrfiles = sorted([f for f in os.listdir(eulrdir) if f.endswith('.nc')])
lagrfiles = sorted([f for f in os.listdir(lagrdir) if f.endswith('.csv')])

#Index for reference of current timestep
i=100


#-------------------------------------------------------------------------------
#Load files in loop
for n in range(start, stop):

    #Convert refernece integer i to string
    istring=str(i)

    eulrfile = eulrfiles[n]
    lagrfile = lagrfiles[n]

    eulrfilepath = os.path.join(eulrdir, eulrfile)
    lagrfilepath = os.path.join(lagrdir, lagrfile)

    #----------------------------------------------------------------------------------------------
    ## Eulerian ##

    #Load Eulerian file
    hx_project.load(eulrfilepath)

    #Volume Rendering for Eulerian file
    Eul_volrenset=hx_project.create('HxVolumeRenderingSettings')
    Eul_volrenset.ports.data.connect(hx_project.get(eulrfile))
    Eul_volrenset.fire()

    Eul_volren=hx_project.create('HxVolumeRender2')
    Eul_volren.ports.volumeRenderingSettings.connect(hx_project.get('Volume Rendering Settings'))
    Eul_volren.fire()

    #Changing required propeties of Eulerian file
    port_rbox=Eul_volren.ports.colormapLookup
    port_rbox.selected=0
    Eul_volren.fire()

    port_slider=Eul_volren.ports.alphaScale
    port_slider.value=0.25
    Eul_volren.fire()

    #------------------------------------------------------------------------------------------------
   
    #Colormap for Eulerian file
    cmap1=hx_project.create('HxDisplayColormap')
    cmap1.ports.data.connect(hx_project.get('Volume Rendering'))
    text_cmap1=cmap1.ports.position
    text_cmap1.texts[0].value=150
    cmap1.fire()

    #-------------------------------------------------------------------------------------------------

    #Changing Camera Position
    hx_viewer_manager.viewers[0].camera.position=(-191.335205078125,-294.9089453125,-550.6705322265625)
    hx_viewer_manager.viewers[0].camera.view_direction = (0.4161407947540283,0.5126282572746277,0.75102519988901367)

    #-------------------------------------------------------------------------------------------------

    #Lagrangian
    #Load Lagrangian file
    hx_project.load(lagrfilepath)

    #Create Cluster from Spreadsheet
    Lag_pcv=hx_project.create('HxSpreadSheetToCluster')
    Lag_pcv.ports.data.connect(hx_project.get(lagrfile))
    Lag_pcv.fire()


    port_menu=Lag_pcv.ports.coordinates
    port_menu.menus[0].selected=1
    port_menu.menus[1].selected=2
    port_menu.menus[2].selected=3

    Lag_pcv.fire()

    Lag_pcv.ports.action.was_hit=True
    Lag_pcv.fire()

    #Create PointCloud View of Lanrangian  file
    Lag_pointCloud=hx_project.create('HxClusterView')
    Lag_pointCloud.ports.data.connect(hx_project.get('step'+str(istring).zfill(6)+'.Cloud'))
    Lag_pointCloud.fire()

    #Change properties of PointCloud View
    color_menu=Lag_pointCloud.ports.color
    color_menu.menus[0].selected=2

    #--------------------------------------------------------------------------------------------
     #Load Colormap from library  suitable for Lagrangian file
    hx_project.load('/home/HPCS/bipink/Avizo_test/0.5m/New_Data/physics2.icol.am') #Custom Colormap loaded
    Lag_pointCloud.ports.colormap.connect(hx_project.get('physics2.icol.am'))
    Lag_pointCloud.fire()

    #Connecting loaded colormap to current colormap of Lagrangian file
    cmap2=hx_project.create('HxDisplayColormap')
    cmap2.ports.data.connect(hx_project.get('Point Cloud View'))



    #---------------------------------------------------------------------------------------
    
    #CSV data min max range
    import pandas as pd

    df=pd.read_csv(lagrfilepath)

    vmin=df['r'].min()
    vmax=df['r'].max()
    
    #Assigning extracted min-max values to colormap
    Lag_pointCloud.ports.colormap.range=(vmin,vmax)

     #--------------------------------------------------------------------------------------------

    #Changing the display shape of Lagrangian data
    Lag_pointCloud.ports.options.toggles[0] = HxPortToggleList.Toggle(label="spheres", checked=HxPortToggleList.Toggle.CHECKED)
    Lag_pointCloud.ports.options.toggles[0] = HxPortToggleList.Toggle(label="spheres", checked=HxPortToggleList.Toggle.UNCHECKED)

    #Changing colormap position
    text_cmap2=cmap2.ports.position
    text_cmap2.texts[0].value=1000
    cmap2.fire()

    
   
    #------------------------------------------------------------------------------------------
    #Saving the image using Snapshot module
    snapshot =hx_project.create('HxSnapshotModule')
    snapshot.ports.input.connect(hx_project.get('Point Cloud View'))
    port_savdes=snapshot.ports.snapPath
    port_savdes.filenames ='/home/HPCS/bipink/Avizo_test/0.5m/New_Data/Outputs/0.5_avizo_outputs_0_4k/img_'+istring+'.png'
    snapshot.fire()

    snapshot.ports.action.was_hit=True
    snapshot.fire()

    #-------------------------------------------------------------------------------------------
    #Deleting python objects created and clearing the Project view
    del port_savdes
    del snapshot
    del port_menu
    del color_menu
    del Lag_pcv
    del Lag_pointCloud
    del port_slider
    del port_rbox
    del Eul_volren
    del Eul_volrenset
    del text_cmap2
    del cmap2
    del text_cmap1
    del cmap1
    #Removing everything from the Project view
    hx_project.remove_all()

    #Incrementing refrence pointer for loading next file
    i=i+100

    #End of loop --------------------------------------------------------------------------------


