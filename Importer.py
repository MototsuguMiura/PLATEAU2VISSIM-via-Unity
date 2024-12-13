import os
import win32com.client as com
import math
import ctypes

##### user input #####
lat = 34.4041666666667
lon = 132.48125
######################

def openVissim():
    ## Connecting the COM Server => Open a new Vissim Window:
    Vissim = com.gencache.EnsureDispatch("Vissim.Vissim.24") #
    return Vissim

if not('Vissim' in locals()):
    Vissim = openVissim()
    Vissim.LoadNet(r'D:\Plateau\2024\Unity\Hiroshima\Vissim\Hiroshima.inpx')

## Stop Vissim GUI
ctypes.windll.user32.MessageBoxW(0, "スクリプトの完了まで画面描写を中止します。インポート完了まで暫くお待ちください", "Progress info", 0)
Vissim.SuspendUpdateGUI()

## Get refference point for coordinate conversion
CORRECTION_FACTOR = 1.001120232
SPHERE_RADIUS = 6378137

RefMapX = Vissim.Net.NetPara.AttValue('RefPointMapX')
RefMapY = Vissim.Net.NetPara.AttValue('RefPointMapY')
RefNetX = Vissim.Net.NetPara.AttValue('RefPointNetX')
RefNetY = Vissim.Net.NetPara.AttValue('RefPointNetY')

LatMapY = (2 * math.atan(math.exp(RefMapY * CORRECTION_FACTOR / SPHERE_RADIUS )) - math.pi /2) / (math.pi/180)
LocalScale = 1 / math.cos(LatMapY * math.pi/180)

## Convert WGS84 to Vissim coordinate
def Convert_WGS2Vissim(latitude, longitude):
    MerX = math.pi/180 * SPHERE_RADIUS * longitude / CORRECTION_FACTOR
    NetX = (MerX - RefMapX)/LocalScale + RefNetX

    MerY = SPHERE_RADIUS / CORRECTION_FACTOR * math.log(math.tan((math.pi/180 * latitude + math.pi/2)/2))
    NetY = (MerY - RefMapY)/LocalScale + RefNetY
    return NetX, NetY

## Convert Vissim Coordinate to WGS84
def Convert_Vissim2WGS(NetX, NetY):
    MerX = (NetX - RefNetX) * LocalScale + RefMapX
    longitude = CORRECTION_FACTOR * MerX / (math.pi/180 * SPHERE_RADIUS)

    MerY = (NetY - RefNetY) * LocalScale + RefMapY
    latitude = (2 * math.atan(math.exp(MerY * CORRECTION_FACTOR / SPHERE_RADIUS) ) - math.pi/2 ) / (math.pi/180)
    return latitude, longitude

## Get network coordinates where the 3D models should be located
net_coord = Convert_WGS2Vissim(lat, lon)

## Import OBJ files
read_files = os.listdir('./')
for file in read_files:
    base, ext = os.path.splitext(file)
    if ext == '.obj':
        Vissim.Net.Static3DModels.AddStatic3DModel(0, file, f'POINT({net_coord[0]} {net_coord[1]} 0)')

## Resume Vissim GUI
Vissim.ResumeUpdateGUI()
ctypes.windll.user32.MessageBoxW(0, "インポートが完了しました", "Progress info", 0)