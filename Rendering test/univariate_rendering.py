import nibabel as nib
import numpy as np
import vtk
import sys

def save_Nifti_data(array,affine,filepath):
    NiftiImage = nib.Nifti1Image(array,affine)
    nib.save(NiftiImage,filepath)


def curv(path_k1,path_k2):
    #---------------------------------------------------------
    #Conculate Gauss/Mean curvature based on k1 and k2.
    #2021/07/22 by xu
    #---------------------------------------------------------
    
    imgk1 = nib.load(path_k1)
    imgk2 = nib.load(path_k2)
    arrk1 = imgk1.get_fdata()
    arrk2 = imgk2.get_fdata()

    #k1max = np.max(arrk1)
    #k1min = np.min(arrk1)
    #k2max = np.max(arrk2)
    #k2min = np.min(arrk2)
    #print(k1min)
    #print(k1max)

    arr = np.empty(arrk1.shape, dtype=np.ubyte)
    arr= arrk1*arrk2 #gauss curvature #(arrk1+arrk2) / 2.0 #mean curvature
    save_Nifti_data(arr, imgk1.affine, 'output/gauss_3_3.5.nii.gz')
    
    #img = nib.load('output/gauss_3_3.5.nii.gz')
    #img_data = img.get_fdata()
    #print(img_data.shape) #show the image data size(number of volume)



#curv('output/aoi_curv_k1_3_3.5.nii.gz','output/aoi_curv_k2_3_3.5.nii.gz')


#-------------------------------------------------------------------
#Univariate Rendering
#2021/07/29    by Xu
#
#https://stackoverflow.com/questions/66866835/vtk-interpolating
#-values-when-colouring-vtkpolydata-with-vtkimagedata
#-------------------------------------------------------------------
#Load the Nifti image data and generate the isosurface
#-------------------------------------------------------------------
namedColors = vtk.vtkNamedColors()

reader = vtk.vtkNIFTIImageReader()#load nifti image data
reader.SetFileName('input/case003_AOI.nii.gz')
reader.Update()

skin = vtk.vtkContourFilter()#maching the cube to the volume and generate the isosurface
skin.SetInputData(reader.GetOutput())
skin.ComputeNormalsOff()
skin.ComputeGradientsOn()
skin.SetValue(0,1)#setting the value about generating isosurface
skin.SetNumberOfContours(1)#setting the number about isosurface
skin.ComputeScalarsOff()
skin.Update()

smooth = vtk.vtkSmoothPolyDataFilter()#make the model's surface smooth
smooth.SetInputConnection(skin.GetOutputPort())
smooth.SetNumberOfIterations(2)
smooth.SetRelaxationFactor(0.5)
smooth.Update()
#------------------------------------------------------------------
#Load the curvature data
#------------------------------------------------------------------
curvature = vtk.vtkNIFTIImageReader()
curvature.SetFileName("output/20210624/gauss_3_3.5.nii.gz")
#curvature.SetFileName("output/20210624/mean_3_3.5.nii.gz")
#curvature.SetFileName("output/20210618/aoi_curv_k1_3_3.5.nii.gz")
#curvature.SetFileName("output/aoi_curv_k2_3_3.5.nii.gz")
curvature.Update()
#-----------------------------------------------------------------
#Change surface model's value to curvature value and generate the new model
#-----------------------------------------------------------------
probe = vtk.vtkProbeFilter()
probe.SetInputConnection(smooth.GetOutputPort())
probe.SetSourceData(curvature.GetOutput())
probe.Update()
#print(probe)

#normals = vtk.vtkPolyDataNormals()
#normals.SetInputConnection(probe.GetOutputPort())

rng = probe.GetOutput().GetScalarRange()#Get the maximum/minimum from curvature
fmin = rng[0]
fmax = rng[1]
print(fmin)
print(fmax)
#------------------------------------------------------------------
#Using curvature value to generate the color map
#------------------------------------------------------------------
#dim = np.power(2,4)#12(guass)
dim = np.power(2,12)#12(guass)
r = (fmax-fmin)/dim
table = vtk.vtkLookupTable()
table.SetTableRange(fmin*r,fmax*r)#change the table range value
table.SetNumberOfColors(dim)
#table.SetHueRange(fmin,fmax)#HSV color map
#table.SetSaturationRange(0.4,1.0)
#table.SetValueRange(1.0,1.0)
table.Build()
#------------------------------------------------------------------
#Mapping the color table and new model
#------------------------------------------------------------------
skinmapper = vtk.vtkPolyDataMapper()
skinmapper.SetColorModeToMapScalars()
skinmapper.SetLookupTable(table)
skinmapper.SetInputConnection(probe.GetOutputPort())
skinmapper.SetScalarRange(fmin*r,fmax*r) #Setting the range
skinmapper.Update()

skinProperty = vtk.vtkProperty()
#------------------------------------------------------------------
#Generate the Actor
#------------------------------------------------------------------
skinactor = vtk.vtkActor()
skinactor.SetMapper(skinmapper)

scalarBar = vtk.vtkScalarBarActor()#Set the scalar range bar
scalarBar.SetLookupTable(skinmapper.GetLookupTable())
#scalarBar.SetTitle("Indexed Curvature")
scalarBar.SetNumberOfLabels(5)
scalarBar.SetWidth(0.08)
#------------------------------------------------------------------
#Generate the renderer
#------------------------------------------------------------------
camera = vtk.vtkCamera()
ren = vtk.vtkRenderer()
ren.SetBackground([0,0,0])
ren.SetActiveCamera(camera)
ren.AddActor(skinactor)
ren.AddActor2D(scalarBar)
#------------------------------------------------------------------
#Generate the render window
#------------------------------------------------------------------
rewin = vtk.vtkRenderWindow()
rewin.SetSize(800,512)
rewin.AddRenderer(ren)
rewin.SetWindowName("Calculating  Curvature")
#------------------------------------------------------------------
#Add the actor to the render window
#------------------------------------------------------------------
iren = vtk.vtkRenderWindowInteractor()
trackball = vtk.vtkInteractorStyleTrackballCamera()
iren.SetRenderWindow(rewin)
iren.SetInteractorStyle(trackball)
#------------------------------------------------------------------
#Start to rendering and showing the window
#------------------------------------------------------------------
iren.Initialize()
ren.ResetCamera()

iren.Start()

