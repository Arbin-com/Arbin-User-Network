#coding=utf-8

from pickletools import uint8
from random import paretovariate
from re import U
import sys
from time import strftime
import clr
import datetime
import os
import matplotlib.pyplot as plt

clr.AddReference("System.Collections")
from System.Collections.Generic import List
from System import Int32
from System import UInt16

classDLL = clr.AddReference('ArbinCTI')
from ArbinCTI.Core.Control import ArbinControlLabView
from ArbinCTI.Core import *
from ArbinCTI.Core import ArbinCommandGetMetaVariablesFeed
from ArbinCTI.Core.Control import ArbinControl
from System.Collections.Generic import List
from ArbinCTI.Core import MetaVariableInfo, TE_DATA_TYPE

global Current
global Voltage
Voltage = 0
global TrueCurrent
global TestTime



class ProgramConst(object):
    __slots__ = ()      # Nikita - Change the credentials and ip addres and port as required
    USER = "admin"
    PASSWORD = "000000"  
    IP = "127.0.0.1"
    CTI_PORT = 9031


ProgramConst = ProgramConst()

g_programRunning = True
g_client = None

g_ctrl = ArbinControlLabView()
g_ctrl.Start()

#Nikita 20220922 start
def JumpChannelFeedEvent(cmd):
    print("<{} Jump Channel, result= {}>".format(cmd.socket.RemoteAddr.ToString(), JumpChannelTokenMap[cmd.Result]))

def UpLoadFeedEvent(cmd):
    print("<{} Upload File, result= {}>".format(cmd.socket.RemoteAddr.ToString(), uploadFileTokenMap[cmd.Result]))

def DownLoadFeedEvent(cmd):
    print("<{} Download File, result= {}>".format(cmd.socket.RemoteAddr.ToString(), downloadFileTokenMap[cmd.Result]))
#Nikita 20220922 end

def AssignSchFeedBackEvent(cmd):
    print("<{} Assign Channel {}, result= {}>".format(cmd.socket.RemoteAddr.ToString(), cmd.Channel + 1, assignChannelTokenMap[cmd.Result]))


def GetChannelFeedEvent(cmd):
    
    
    count = 0
    if(cmd is not None and cmd.m_Channels is not None):
        count = len(cmd.m_Channels)
    print("<{} Get Channel Data: IVCount={}>".format(cmd.socket.RemoteAddr.ToString(),count))
    for i in range(count):
        channel = cmd.m_Channels[0]
        chanIndex = channel.Channel
        chanStatus = channel.Status
        chanSchedule = channel.Schedule
        chanCANcfg = channel.CANCfg
        chanSMBcfg = channel.SMBCfg
        chanTestName = channel.Testname
        chanExitCondi = channel.ExitCondition
        chanStepnCycle = channel.StepAndCycle
        chanBarCode = channel.Barcode
        chanTestTime = channel.TestTime
        TestTime = chanTestTime
        chanStepTime = channel.StepTime
        chanVoltage = channel.Voltage
        Voltage = chanVoltage
        chanCurrent = channel.Current
        TrueCurrent = chanCurrent
        chanPower = channel.Power
        chanChargeCap = channel.ChargeCapacity
        chanDischCap = channel.DischargeCapacity
        chanIR = channel.InternalResistance
        chandvdt = channel.dvdt
        countCAN = 0
        countSMB = 0
        #x= AUX_TYPE.T
        if channel.CAN is not None:
            countCAN = len(channel.CAN)
        if channel.SMB is not None:
            countSMB = len(channel.SMB)
        countAUXType = len(channel.Auxs)
        
        
        print("<Channel {}: Status= {}, Barcode= {}, Schedule= {}, TestName= {}, ExitCond= {}, StepAndCycle= {}, TestTime= {}, StepTime= {}, Voltage= {}, Current= {}, Power= {}, ChargeCap= {}, DischargeCap= {}, IR= {}, AuxType= {}>"
        .format(chanIndex, chanStatus, chanBarCode, chanSchedule, chanTestName, chanExitCondi, chanStepnCycle, chanTestTime, chanStepTime, chanVoltage, chanCurrent, chanPower, chanChargeCap, chanDischCap, chanIR, countAUXType))

        for t in range(countAUXType - 1):
            print(f"{(channel.Auxs[t])}") 
            if channel.Auxs[t] is not None:
                count = len(channel.Auxs[t])
                print(count)
                for j in range(count):
                    print("<Channel {}:  Value= {}, dtValue= {}".format(chanIndex,  channel.Auxs[t][j].Value, channel.Auxs[t][j].dtValue))

        for t in range(countAUXType - 1):
            print(f"{(channel.Auxs[t])}") 
            if channel.Auxs[t] is not None:
                count = len(channel.Auxs[t])
                print(count)
                for j in range(count):
                    print("<Channel {}:  Value= {}, dtValue= {}".format(chanIndex,  channel.Auxs[t][j].Value, channel.Auxs[t][j].dtValue))






def GetResumeDataFeedEvent(cmd):
    count = 0
    if(cmd is not None and cmd.m_Channels is not None):
        count = len(cmd.m_Channels)
    print("<{} Get Resume Data: IVCount={}>".format(cmd.socket.RemoteAddr.ToString(),count))
    for i in range(count):
        channel = cmd.m_Channels[i]
        channelIndex = channel.Channel
        MVUD1 = channel.ResumeData.MVUD1
        MVUD2 = channel.ResumeData.MVUD2
        MVUD3 = channel.ResumeData.MVUD3
        MVUD4 = channel.ResumeData.MVUD4
        MVUD5 = channel.ResumeData.MVUD5
        MVUD6 = channel.ResumeData.MVUD6
        MVUD7 = channel.ResumeData.MVUD7
        MVUD8 = channel.ResumeData.MVUD8
        MVUD9 = channel.ResumeData.MVUD9
        MVUD10 = channel.ResumeData.MVUD10
        MVUD11 = channel.ResumeData.MVUD11
        MVUD12 = channel.ResumeData.MVUD12
        MVUD13 = channel.ResumeData.MVUD13
        MVUD14 = channel.ResumeData.MVUD14
        MVUD15 = channel.ResumeData.MVUD15
        MVUD16 = channel.ResumeData.MVUD16
        print("<Channel {}: MVUD1= {}, MVUD2= {}, MVUD3= {}, MVUD4= {}, ".format(channelIndex+1, MVUD1, MVUD2, MVUD3, MVUD4))
        print("MVUD5= {}, MVUD6= {}, MVUD7= {}, MVUD8= {}, MVUD9= {}, MVUD10= {}, ".format(MVUD5,MVUD6, MVUD7, MVUD8, MVUD9, MVUD10))
        print("MVUD11= {}, MVUD12= {}, MVUD13= {}, MVUD14= {}, MVUD15= {}, MVUD16= {}>".format(MVUD11, MVUD12, MVUD13, MVUD14, MVUD15, MVUD16))
       

       



def LogicConnectFeedEvent(cmd):
    pass


def ResumeFeedEvent(cmd):
    print("<{} Resume Channel {} result={}>".format(cmd.socket.RemoteAddr.ToString(), cmd.Channel + 1, resumeChannelTokenMap[cmd.Result]))


def StartFeedEvent(cmd):
    print("<{} Start Channel {} result={}>".format(cmd.socket.RemoteAddr.ToString(), cmd.Channel + 1, startChannelTokenMap[cmd.Result]))


def StopFeedEvent(cmd):
    print("<{} Stop Channel {} result={}>".format(cmd.socket.RemoteAddr.ToString(), cmd.Channel + 1, stopChannelTokenMap[cmd.Result]))


def LoginFeedEvent(cmd):
    print("<{} Login Result={}>".format(cmd.socket.RemoteAddr.ToString(), loginResultTokenMap[cmd.Result]))

def SetMetavariableFeedEvent(cmd):
    print("<{} Set Metavariable Channel {} result={}>".format(cmd.socket.RemoteAddr.ToString(), cmd.Channel + 1, setMetavariableTokenMap[cmd.Result]))

def GetMetaVariablesFeedEvent(cmd):
    print("<{} \n Get Metavariable Channel: {} \n MV Count={} \n Value 1 (Voltage) ={} \n Value 2(Current) ={} \n>".format(cmd.socket.RemoteAddr.ToString(), cmd.MetaVariableInfos[0].m_Channel+1, cmd.MetaVariableInfos.Count, cmd.MetaVariableInfos[0].m_Value, cmd.MetaVariableInfos[1].m_Value))

def UpdateMetaVariableAdvanceFeed(cmd):
    print("<{} Update Metavariable Channel {} result={}>".format(cmd.socket.RemoteAddr.ToString(), cmd.Channel + 1, updateMetaVariableTokenAdvanceMap[cmd.Result]))


def BrowseFeedEvent(cmd):
    DirInfolist = cmd.DirFileInfoList
    print("<{} Browse Result={}>\n".format(cmd.socket.RemoteAddr.ToString(), browseDirectoryResultMap[cmd.Result]))
    if DirInfolist is not None:
        for i in range(len(DirInfolist)):
            print("<FileType= {}, FileName= {}, Size= {}, Modified= {}".format(DirInfolist[i].Type, DirInfolist[i].DirFileName, DirInfolist[i].dwSize, DirInfolist[i].wcModified))

def UpdateMVADVEvent(cmd) :
        print("<{} Update Metavariable result={}>".format(cmd.socket.RemoteAddr.ToString(), UpdateMetavariableAdvTokenMap[cmd.Result]))

def NewOrDeleteFeedEvent(cmd):
    pass


def GetStartDataFeedEvent(cmd):
    pass


def AutomaticCalibrationFeedEvent(cmd):
    pass



g_ctrl.AssignSchFeedBackEvent += AssignSchFeedBackEvent
g_ctrl.UpLoadFeedEvent += UpLoadFeedEvent
g_ctrl.DownLoadFeedEvent += DownLoadFeedEvent
g_ctrl.BrowseFeedEvent += BrowseFeedEvent
g_ctrl.GetResumeDataFeedEvent += GetResumeDataFeedEvent
g_ctrl.GetChannelFeedEvent += GetChannelFeedEvent
g_ctrl.LoginFeedEvent += LoginFeedEvent
g_ctrl.SetMVEvent += SetMetavariableFeedEvent
g_ctrl.ResumeFeedEvent += ResumeFeedEvent
g_ctrl.StopFeedEvent += StopFeedEvent
g_ctrl.StartFeedEvent += StartFeedEvent
g_ctrl.JumpChannelFeedEvent += JumpChannelFeedEvent
g_ctrl.GetMetaVariablesFeedBackEvent += GetMetaVariablesFeedEvent
g_ctrl.UpdateMVADVEvent += UpdateMVADVEvent
#g_ctrl.ArbinCommandUpdateMetaVariableAdvancedExFeedHandlerFeedBackEvent += ArbinCommandUpdateMetaVariableAdvancedExFeedHandlerFeedBackEvent


def Client_OnConnectionChanged(socket, e):
    global g_ctrl
    if(e.Connected):
        print("<connected successfully>")
        g_ctrl.PostUserLogin( socket, ProgramConst.USER, ProgramConst.PASSWORD )
    else:
        print("<disconnect>")


def AdvanceUpdateMV():
        global g_client
        global g_ctrl
        err = 0
        myMetavariableList = List[MetaVariableInfo]()
        MV_Info = MetaVariableInfo()
        MV_Info.m_ChannelIndexInGlobal = 0
        MV_Info.m_MV_MetaCode = 52

        curr = 1
        MV_Info.m_fMV_Value = curr
        myMetavariableList.Add(MV_Info)
        g_ctrl.PostUpdateMetaVariableAdvanced(g_client, myMetavariableList, err)


       


#Nikita 20220922 start
def UploadFile():
    global g_client
    global g_ctrl

    x = datetime.datetime.now()
    curtime = x.strftime("%m%d%Y%H%M%S")

    sfilename = input("Input Filename: ").strip()
    extension = input("Input File type (.to/.sdx/.sdu/.xml): ").strip()
    dfilename = sfilename + curtime + extension

    path = input("Input File Path: ").strip()
    #file = open(path+"\\"+sfilename+extension, "rb")
    #bytesdata = file.read()
    #x = bytearray(bytesdata)     
    pkcount = 1 
    pkindex = 0 
    double = 100.2
    g_ctrl.PostUpLoadFile(g_client, dfilename, x, double, pkcount, pkindex)
    #g_ctrl.PostUpLoadFile(g_client, "NikDefault.sdu", "/Users/ArbinLab5/Desktop/RIVIAN CTI-Python/Default.sdu", False, TransferUploadThreadMethod)

def DownloadFile():
    global g_client
    global g_ctrl

    g_ctrl.PostDownLoadFile(g_client, "C:\ArbinSoftware\MITS_PRO\Work\AB_ACCC+NewBattery.sdx", 0)
#Nikita 20220922 end

result = ArbinCommandUpLoadFileFeed.CUpLoadFileResult

async def TransferUploadThreadMethod(result):
    print(result.ResultCode)
    print(result.Progressrate*100)

def Assign():
    global g_client
    global g_ctrl
    channelIndex = int(input("Input channel: ").strip())
    scheduleName = input("Input schedule name: ").strip()
    strAssign = input("AssignAll? (True or False):").strip()
    bAssignAll = True
    if strAssign == 'True':
        bAssignAll = True
    else:
        bAssignAll = False
    g_ctrl.PostAssignSchedule(g_client, scheduleName, "nikita", 0, 0, 0, 0, 0, bAssignAll, channelIndex)


def Resume():
    global g_client
    global g_ctrl
    channelIndex = input("Input channel: ").strip()
    strStop = input("Resume all? (True or False):").strip()
    bResumeAll = True
    if strStop == 'True':
        bResumeAll = True
    else:
        bResumeAll = False
    g_ctrl.PostResumeChannel(g_client, bResumeAll, channelIndex)

def SetMV():
    global g_client
    global g_ctrl
    import time
    Current = 0
    vlist = []
    ilist = []
    trueI = []
    Time = []
    TrueCurrent = 0
    Login()
    time.sleep(10)
    
    start_time = time.time();
    for i in range(20):
        if i<=4:
            Current = 0
        elif i <= 10:
            Current = -0.01
        else:
            Current = 0
        g_ctrl.PostSetMetaVariable(g_client, 0, 1, 52, 1, Current)
        #g_ctrl.PostUpdateMetaVariableAdvanced(g_client, 6, 1, 107, 1, CURRENT)\n",
        
        time.sleep(0.01)
        # g_ctrl.PostGetChannelsData(g_client, 1792, -1, ArbinCommandGetChannelDataFeed.GET_CHANNEL_TYPE.ALL)
        #g_ctrl.PostGetChannelsDataSimpleMode(g_client, 1024, 6, ArbinCommandGetChannelDataFeed.GET_CHANNEL_TYPE.RUNNING)    # checking different\n",
        # g_ctrl.PostGetChannelsDataSimpleMode(g_client,6,ArbinCommandGetChannelDataSimpleModeFeed.GET_CHANNEL_TYPE.ALLCHANNEL); 
        time.sleep(.98)
        
        time.sleep(0.01)
        
        #print(\"waiting\")\n",
        
        #print(\"resuming\")\n",
        #print(\"saving\")\n",
        vlist.append(Voltage)
        ilist.append(Current)
        trueI.append(TrueCurrent)
        # Time.append(TestTime)
    
    end_time =time.time();

    plt.figure()
    plt.plot(ilist, label = 'Our Current Command Sent to arbin')
    plt.plot(trueI, label = 'ARBIN CURRENT')
    plt.xlabel("Wall Clock Time [S]")
    plt.ylabel("Current [A]")
    plt.title("Arbin Lag")
    plt.legend(loc='lower left')
    #plt.axis([0,20,-0.005,0.2])\n"

    # channelIndex = input("Input channel: ").strip()
    # metaCode = input("Input Metavariable Code: ").strip()
    # metaValue = input("Input Metavariable Value: ").strip()
    # g_ctrl.PostSetMetaVariable(g_client, channelIndex, 1, metaCode, 1, metaValue)

def GetResumeData():
    global g_client
    global g_ctrl
    channelText = input("Please Input Channels:").strip()
    channels = List[UInt16]()
    for tmp in channelText.split(' '):
        channelIndex = int(tmp)
        channels.Add(UInt16(channelIndex))
    g_ctrl.PostGetResumeData(g_client, channels)

def Stop():
    global g_client
    global g_ctrl
    nChannel = (int)(input("Input channel:"))
    strStop = input("Stop all? (True or False):").strip()
    bStopAll = True
    if strStop == 'True':
        bStopAll = True
    else:
        bStopAll = False
    g_ctrl.PostStopChannel(g_client, nChannel, bStopAll)


def Login():
    global g_client
    global g_ctrl
    if(g_client is None or g_client.IsConnected()):
        g_client = ArbinClient()
        g_client.OnConnectionChanged += Client_OnConnectionChanged
        g_ctrl.ListenSocketRecv( g_client )
        result, err = g_client.ConnectAsync(ProgramConst.IP, ProgramConst.CTI_PORT, 0, Int32(0) );
        if(result != 0):
            pass
    else:
        print("Connected...")


def Shutdown():
    global g_client
    if(g_client is not None):
        g_client.ShutDown()
        g_client = None


def StartChannel():
    global g_client
    global g_ctrl
    if(g_client is None or not g_client.IsConnected()):
        print("Failed Connect Status.")
        return
    testName = input("Please Input TestName:").strip()
    channelText = input("Please Input Start Channels:").strip()
    channels = List[UInt16]()
    for tmp in channelText.split(' '):
        channelIndex = int(tmp)
        channels.Add(UInt16(channelIndex))
    if(channels.Count != 0):
        g_ctrl.PostStartChannel(g_client, testName, channels);



def GetChannel():
    global g_client
    global g_ctrl
    if(g_client is None or not g_client.IsConnected()):
        print("Failed Connect Status.")
        return
    chanIndex = int(input("Input channel index to get info from (-1 = request all channels data): ").strip())
    chanType = ArbinCommandGetChannelDataFeed.GET_CHANNEL_TYPE.ALLCHANNEL #(input("Input channel type: (ALLCHANNEL = 1, RUNNING = 2, UNSAFE = 3: ").strip())
    infoType = input("Input info type: (CAN = 0x100, SMB = 0x200, AUX = 0x400: ").strip()
    g_ctrl.PostGetChannelsData(g_client, 1792, chanIndex, chanType)

def BrowseDirectory():
    global g_client
    global g_ctrl
    
    g_ctrl.PostBrowseDirectory(g_client, 'SCHEDULE')


def ClearScreen():
    print("\033c", end="")


def Exit():
    global g_programRunning
    g_programRunning = False

def JumpChannel():
    global g_client
    global g_ctrl

    g_ctrl.PostJumpChannel(g_client, 0, 0)

def GetMetaVariables():
    global g_client
    global g_ctrl

    # Create an instance of List<ArbinCommandGetMetaVariablesFeed.MetaVariableInfo>
    metaVariableList = List[ArbinCommandGetMetaVariablesFeed.MetaVariableInfo]()

    Chnl= [0]
    metacode = [22, 21]

    for channel in Chnl:
        for code in metacode:
            mv_info = ArbinCommandGetMetaVariablesFeed.MetaVariableInfo()
            mv_info.m_Channel = channel
            mv_info.m_MV_DataType = TE_DATA_TYPE.MP_DATA_TYPE_MetaValue
            mv_info.m_MV_MetaCode = code
            metaVariableList.Add(mv_info)

    # Define a variable to hold the error code
    error = 0

    # Call the PostGetMetaVariables function
    g_ctrl.PostGetMetaVariables(g_client, metaVariableList, error)




def UpdateMetaVariableAdvanced():
    global g_client
    global g_ctrl
    import time

    meta_variable_list = List[ArbinCommandUpdateMetaVariableAdvancedFeed]()


    mv_info = ArbinCommandUpdateMetaVariableAdvancedFeed()
    mv_info.m_ChannelIndexInGlobal = 1
    mv_info.m_MV_MetaCode = 52
    mv_info.m_fMV_Value = 0
    meta_variable_list.append(mv_info)
    
    # Simulating error output
    error = 0  # Initialize error to 0

    Login()

    start_time = time.time()

    # Simulating multiple calls to PostUpdateMetaVariableAdvanced
    for i in range(1):
        g_ctrl.PostUpdateMetaVariableAdvanced(g_client, meta_variable_list, error)
        time.sleep(1)

    end_time = time.time()


#Enumerator
def PrintCommandList():
    print("")
    print("A: Assign")
    print("B: Browse Work Directory")
    print("D: Get Resume Data")
    print("E: Exit")
    print("G: Get Channel")
    print("J: Shutdown")
    print("L: Login")
    print("M: Set MetaVariable")
    print("O: Clear Screen")
    print("R: Resume")
    print("S: Stop")
    print("X: Start Channel")
    print("U: Upload File")
    print("C: Download File")
    print("F: Jump Channel")
    print("GM: GetMetaVariables")
    print("UM: UpdateMetaVariablesAdvanced")

commandMap = {
    'A': Assign,
    'B': BrowseDirectory,
    'D': GetResumeData,
    'E': Exit,
    'G': GetChannel,
    'J': Shutdown,
    'L': Login,
    'M': SetMV,
    'O': ClearScreen,
    'R': Resume,
    'S': Stop,
    'X': StartChannel,
    'U': UploadFile,
    'C': DownloadFile,
    'F': JumpChannel,
    'GM': GetMetaVariables,
    'UM': AdvanceUpdateMV
}

channelStatusMap = {
    ArbinCommandGetChannelDataFeed.ChannelStatus.Idle : 'Idle',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Transition : 'Transition',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Charge : 'Charge',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Rest : 'Rest',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Wait : 'Wait',
    ArbinCommandGetChannelDataFeed.ChannelStatus.External_Charge : 'External Charge',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Calibration : 'Calibration',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Unsafe : 'Unsafe',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Pulse : 'Pulse',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Internal_Resistance : 'Internal Resistance',
    ArbinCommandGetChannelDataFeed.ChannelStatus.AC_Impedance : 'AC Impedance',
    ArbinCommandGetChannelDataFeed.ChannelStatus.ACI_Cell : 'ACI Cell',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Test_Settings : 'Test Settings',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Error : 'Error',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Finished : 'Finished',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Volt_Meter : 'Volt Meter',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Waiting_for_ACS : 'Waitng for ACS',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Pause : 'Pause',
    ArbinCommandGetChannelDataFeed.ChannelStatus.EMPTY : 'Empty',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Idle_from_MCU : 'Idle from MCU',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Start : 'Start',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Runing : 'Running',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Step_Transfer : 'Step Transfer',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Resume : 'Resume',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Go_Pause : 'Go Pause',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Go_Stop : 'Go Stop',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Go_Next_Step : 'Go Next Step',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Online_Update : 'Online Update',
    ArbinCommandGetChannelDataFeed.ChannelStatus.Daq_Memory_Unsafe : 'DAQ Memory Unsafe',
    ArbinCommandGetChannelDataFeed.ChannelStatus.ACR : 'ACR',
}


JumpChannelTokenMap = {
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_SUCCESS : 'CTI_JUMP_SUCCESS',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_INDEX : 'CTI_JUMP_INDEX',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_ERROR : 'CTI_JUMP_ERROR',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_CHANNEL_RUNNING : 'CTI_JUMP_CHANNEL_RUNNING',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_CHANNEL_NOT_CONNECT : 'CTI_JUMP_CHANNEL_NOT_CONNECT',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_SCHEDULE_VALID : 'CTI_JUMP_SCHEDULE_VALID',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_NO_SCHEDULE_ASSIGNED : 'CTI_JUMP_NO_SCHEDULE_ASSIGNED',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_SCHEDULE_VERSION : 'CTI_JUMP_SCHEDULE_VERSION',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_POWER_PROTECTED : 'CTI_JUMP_POWER_PROTECTED',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_RESULTS_FILE_SIZE_LIMIT : 'CTI_JUMP_RESULTS_FILE_SIZE_LIMIT',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_STEP_NUMBER : 'CTI_JUMP_STEP_NUMBER',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_NO_CAN_CONFIGURATON_ASSIGNED : 'CTI_JUMP_NO_CAN_CONFIGURATON_ASSIGNED',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_AUX_CHANNEL_MAP : 'CTI_JUMP_AUX_CHANNEL_MAP',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_BUILD_AUX_COUNT : 'CTI_JUMP_BUILD_AUX_COUNT',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_POWER_CLAMP_CHECK : 'CTI_JUMP_POWER_CLAMP_CHECK',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_AI : 'CTI_JUMP_AI',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_SAFOR_GROUPCHAN : 'CTI_JUMP_SAFOR_GROUPCHAN',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_BT6000RUNNINGGROUP : 'CTI_JUMP_BT6000RUNNINGGROUP',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_CHANNEL_DOWNLOADING_SCHEDULE : 'CTI_JUMP_CHANNEL_DOWNLOADING_SCHEDULE',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_DATABASE_QUERY_TEST_NAME_ERROR :'CTI_JUMP_DATABASE_QUERY_TEST_NAME_ERROR',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_TEXTNAME_EXITS : 'CTI_JUMP_TEXTNAME_EXITS',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_GO_STEP :'CTI_JUMP_GO_STEP',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_INVALID_PARALLEL : 'CTI_JUMP_INVALID_PARALLEL',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_SAFETY : 'CTI_JUMP_SAFETY',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_SECHEDULE_NAME_DIFFERENT : 'CTI_JUMP_SECHEDULE_NAME_DIFFERENT',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_BATTERYSIMULATION_NOT_PARALLEL :'CTI_JUMP_BATTERYSIMULATION_NOT_PARALLEL',
    ArbinCommandJumpChannelFeed.JUMP_TOKEN.CTI_JUMP_CHANNEL_SUSPENT : 'CTI_JUMP_CHANNEL_SUSPENT',
}
browseDirectoryResultMap = {
    ArbinCommandBrowseDirectoryFeed.BROWSE_DIRECTORY_RESULT.CTI_BROWSE_DIRECTORY_SUCCESS : 'BROWSE_DIRECTORY_SUCCESS',
    ArbinCommandBrowseDirectoryFeed.BROWSE_DIRECTORY_RESULT.CTI_BROWSE_SCHEDULE_SUCCESS : 'BROWSE_SCHEDULE_SUCCESS',
    ArbinCommandBrowseDirectoryFeed.BROWSE_DIRECTORY_RESULT.CTI_BROWSE_DIRECTORY_FAILED : 'BROWSE_DIRECTORY_FAILED',
}

auxTypeMap = {
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.AuxV : 'AuxV',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.T : 'T',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.P : 'P',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.pH : 'pH',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.FR : 'FR',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.Conc : 'Conc',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.DI : 'DI',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.DO : 'DO',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.EC : 'EC',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.Safety : 'Safety',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.Humidity : 'Humidity',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.AO : 'AO',
    ArbinCommandGetChannelDataFeed.ChannelInfo.AUX_TYPE.MAX_NUM : 'MAX_NUM',
}

assignChannelTokenMap = {
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_SUCCESS : 'CTI_ASSIGN_SUCCESS',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_INDEX : 'CTI_ASSIGN_INDEX',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_ERROR : 'CTI_ASSIGN_ERROR',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_SCHEDULE_NAME_EMPTY_ERROR : 'CTI_ASSIGN_SCHEDULE_NAME_EMPTY_ERROR',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_SCHEDULE_NOT_FIND_ERROR : 'CTI_ASSIGN_SCHEDULE_NOT_FIND_ERROR',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_CHANNEL_RUNNING_ERROR : 'CTI_ASSIGN_CHANNEL_RUNNING_ERROR',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_CHANNEL_DOWNLOAD_ERROR : 'CTI_ASSIGN_CHANNEL_DOWNLOAD_ERROR',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_BACTH_FILE_OPENED : 'CTI_ASSIGN_BATCH_FILE_OPENED',
    #ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_SDU_CANNOT_ASSDIGN_SCHEDULE : 'CTI_ASSIGN_SDU_CANNOT_ASSIGN_SCHEDULE',
    ArbinCommandAssignScheduleFeed.ASSIGN_TOKEN.CTI_ASSIGN_SDU_SAVE_FAILED : 'CTI_ASSIGN_SDU_SAVE_FAILED',
}

uploadFileTokenMap = {
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_SUCCESS : 'CTI_UPLOAD_SUCCESS',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FAILED : 'CTI_UPLOAD_FAILED',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_MD5_ERROR : 'CTI_UPLOAD_MD5_ERROR',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FAILED_TEST_RUNNING : 'CTI_UPLOAD_FAILED_TEST_RUNNING',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FILE_EXIST_WITH_DIFFERENT_MD5 : 'CTI_UPLOAD_FILE_EXIST_WITH_DIFFERENT_MD5',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FILE_EXIST_WITH_SAME_MD5 : 'CTI_UPLOAD_FILE_EXIST_WITH_SAME_MD5',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FILE_EXIST_NOT_OVERRIDE : 'CTI_UPLOAD_FILE_EXIST_NOT_OVERRIDE',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FAILED_USER_CANCEL : 'CTI_UPLOAD_FAILED_USER_CANCEL',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FAILED_TIMEOUT : 'CTI_UPLOAD_FAILED_TIMEOUT',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_FAILED_CHECK_FILE_TIMEOUT : 'CTI_UPLOAD_FAILED_CHECK_FILE_TIMEOUT',
    ArbinCommandUpLoadFileFeed.UPLOAD_RESULT.CTI_UPLOAD_IN_PROGRESS : 'CTI_UPLOAD_IN_PROGRESS'
}

downloadFileTokenMap = {
    ArbinCommandDownLoadFileFeed.DOWNLOAD_RESULT.CTI_DOWNLOAD_SUCCESS : 'CTI_DOWNLOAD_SUCCESS',
    ArbinCommandDownLoadFileFeed.DOWNLOAD_RESULT.CTI_DOWNLOAD_FAILED : 'CTI_DOWNLOAD_FAILED',
    ArbinCommandDownLoadFileFeed.DOWNLOAD_RESULT.CTI_DOWNLOAD_MD5_ERR : 'DOWNLOAD_MD5_ERR',
    ArbinCommandDownLoadFileFeed.DOWNLOAD_RESULT.CTI_DOWNLOAD_MAX_LENGTH_ERR : 'CTI_DOWNLOAD_MAX_LENGTH_ERR'
}

startChannelTokenMap = {
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_SUCCESS : 'CTI_START_SUCCESS',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_INDEX :'CTI_START_INDEX',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_ERROR : 'CTI_START_ERROR',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_CHANNEL_RUNNING : 'CTI_START_CHANNEL_RUNNING',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_CHANNEL_NOT_CONNECT : 'CTI_START_CHANNEL_NOT_CONNECT',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_SCHEDULE_VALID : 'CTI_START_SCHEDULE_VALID',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_NO_SCHEDULE_ASSIGNED : 'CTI_START_NO_SCHEDULE_ASSIGNED',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_SCHEDULE_VERSION : 'CTI_START_SCHEDULE_VERSION',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_POWER_PROTECTED : 'CTI_START_POWER_PROTECTED',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_RESULTS_FILE_SIZE_LIMIT : 'CTI_START_RESULTS_FILE_SIZE_LIMIT',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_STEP_NUMBER : 'CTI_START_STEP_NUMBER',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_NO_CAN_CONFIGURATON_ASSIGNED : 'CTI_START_NO_CAN_CONFIGURATON_ASSIGNED',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_AUX_CHANNEL_MAP : 'CTI_START_AUX_CHANNEL_MAP',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_BUILD_AUX_COUNT : 'CTI_START_BUILD_AUX_COUNT',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_POWER_CLAMP_CHECK : 'CTI_START_POWER_CLAMP_CHECK',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_AI : 'CTI_START_AI',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_SAFOR_GROUPCHAN : 'CTI_START_SAFOR_GROUPCHAN',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_BT6000RUNNINGGROUP : 'CTI_START_BT6000RUNNINGGROUP',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_CHANNEL_DOWNLOADING_SCHEDULE : 'CTI_START_CHANNEL_DOWNLOADING_SCHEDULE',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_DATABASE_QUERY_TEST_NAME_ERROR : 'CTI_START_DATABASE_QUERY_TEST_NAME_ERROR',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_TEXTNAME_EXITS : 'CTI_START_TEXTNAME_EXITS',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_GO_STEP : 'CTI_START_GO_STEP',
    ArbinCommandStartChannelFeed.START_TOKEN.CTI_START_INVALID_PARALLEL : 'CTI_START_INVALID_PARALLEL',
}

resumeChannelTokenMap = {
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_SUCCESS : 'RESUME_SUCCESS',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_INDEX : 'RESUME_INDEX',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_ERROR : 'RESUME_ERROR',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_CHANNEL_RUNNING : 'RESUME_CHANNEL_RUNNING',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_CHANNEL_NOT_CONNECT : 'RESUME_CHANNEL_NOT_CONNECT',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_SCHEDULE_VALID : 'RESUME_SCHEDULE_VALID',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_NO_SCHEDULE_ASSIGNED : 'RESUME_NO_SCHEDULE_ASSIGNED',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_SCHEDULE_VERSION : 'RESUME_SCHEDULE_VERSION',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_POWER_PROTECTED : 'RESUME_POWER_PROTECTED',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_RESULTS_FILE_SIZE_LIMIT : 'RESUME_RESULTS_FILE_SIZE_LIMIT',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_STEP_NUMBER :'RESUME_STEP_NUMBER',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_NO_CAN_CONFIGURATON_ASSIGNED : 'RESUME_NO_CAN_CONFIGURATION_ASSIGNED',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_AUX_CHANNEL_MAP : 'RESUME_AUX_CHANNEL_MAP',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_BUILD_AUX_COUNT : 'RESUME_BUILD_AUX_COUNT',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_POWER_CLAMP_CHECK : 'RESUME_POWER_CLAMP_CHECK',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_AI : 'RESUME_AI',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_SAFOR_GROUPCHAN : 'RESUME_SAFOR_GROUPCHAN',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_BT6000RUNNINGGROUP : 'RESUME_BT6000RUNNINGGROUP',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_CHANNEL_DOWNLOADING_SCHEDULE : 'RESUME_CHANNEL_DOWNLOADING_SCHEDULE',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_DATABASE_QUERY_TEST_NAME_ERROR : 'RESUME_DATABASE_QUERY_TEST_NAME_ERROR',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_NO_TEST_NAME : 'RESUME_NO_TEST_NAME',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_LOAD_RESUME : 'RESUME_LOAD_RESUME',
    ArbinCommandResumChanneleFeed.RESUME_TOKEN.RESUME_MAX_MULTIPLE_RESULT : 'RESUME_MAX_MULTIPLE_RESULT',
}

setMetavariableTokenMap = {
    ArbinCommandSetMetaVariableFeed.SET_MV_RESULT.CTI_SET_MV_SUCCESS : 'CTI_SET_MV_SUCCESS',
    ArbinCommandSetMetaVariableFeed.SET_MV_RESULT.CTI_SET_MV_FAILED : 'CTI_SET_MV_FAILED',
    ArbinCommandSetMetaVariableFeed.SET_MV_RESULT.CTI_SET_MV_METACODE_NOTEXIST : 'CTI_SET_MV_METACODE_NOTEXIST',
    ArbinCommandSetMetaVariableFeed.SET_MV_RESULT.CTI_SET_MV_CHANNEL_NOT_STARTED : 'CTI_SET_MV_CHANNEL_NOT_STARTED',
}

getMetaVariableTokenMap = {
    ArbinCommandGetMetaVariablesFeed.GET_MV_RESULT.CTI_GET_MV_SUCCESS : 'CTI_GET_MV_SUCCESS',
    ArbinCommandGetMetaVariablesFeed.GET_MV_RESULT.CTI_GET_MV_ERROR : 'CTI_GET_MV_ERROR',
}

updateMetaVariableTokenAdvanceMap = {
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_SUCCESS : 'CTI_SET_MV_SUCCESS',
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_FAILED : 'CTI_SET_MV_FAILED',
}

stopChannelTokenMap = {
    ArbinCommandStopChannelFeed.STOP_TOKEN.SUCCESS : 'SUCCESS',
    ArbinCommandStopChannelFeed.STOP_TOKEN.STOP_INDEX : 'STOP_INDEX',
    ArbinCommandStopChannelFeed.STOP_TOKEN.STOP_ERROR : 'STOP_ERROR',
    ArbinCommandStopChannelFeed.STOP_TOKEN.STOP_NOT_RUNNING: 'STOP_NOT_RUNNING',
    ArbinCommandStopChannelFeed.STOP_TOKEN.STOP_CHANNEL_NOT_CONNECT : 'STOP_CHANNEL_NOT_CONNECT'
}

loginResultTokenMap = {
    ArbinCommandLoginFeed.LOGIN_RESULT.CTI_LOGIN_SUCCESS : 'CTI_LOGIN_SUCCESS',
    ArbinCommandLoginFeed.LOGIN_RESULT.CTI_LOGIN_FAILED : 'CTI_LOGIN_FAILED',
    ArbinCommandLoginFeed.LOGIN_RESULT.CTI_LOGIN_BEFORE_SUCCESS : 'CTI_LOGIN_BEFORE_SUCCESS',
}

UpdateMetavariableAdvTokenMap = {
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_SUCCESS : 'CTI_SET_MV_SUCCESS',
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_FAILED : 'CTI_SET_MV_FAILED',
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_METACODE_NOTEXIST : 'CTI_SET_MV_METACODE_NOTEXIST',
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_CHANNEL_NOT_STARTED : 'CTI_SET_MV_CHANNEL_NOT_STARTED',
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_METACODE_NOTEXIST_Pro7 : 'CTI_SET_MV_METACODE_NOTEXIST_Pro7',
    ArbinCommandUpdateMetaVariableAdvancedFeed.SET_MV_RESULT.CTI_SET_MV_METACODE_UPDATE_TOO_FREQUENTLY_200MS : 'CTI_SET_MV_METACODE_UPDATE_TOO_FREQUENTLY_200MS'
}

while(g_programRunning):
    PrintCommandList()
    line = input("\nPlease Input Command:\n").strip().upper()
    if(line == ''):
        continue
    commandMap.get(line, lambda: print("Please enter the correct command\n"))()