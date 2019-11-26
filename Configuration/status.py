from rw_reg_dongle import *
from time import sleep

def main():

    parseXML()
    print "Parsing complete..."

    romreg=readReg(getNode("LPGBT.RO.ROMREG"))
    if (romreg != 0xa5):
        print "Error: no communication with LPGBT. ROMREG=0x%x, EXPECT=0x%x" % (romreg, 0xa5)
        return


    print "CHIP ID:"
    print "\t0x%08x" % (readReg(getNode("LPGBT.RWF.CHIPID.CHIPID0")) << 24 | \
                        readReg(getNode("LPGBT.RWF.CHIPID.CHIPID1")) << 16 | \
                        readReg(getNode("LPGBT.RWF.CHIPID.CHIPID2")) << 8  | \
                        readReg(getNode("LPGBT.RWF.CHIPID.CHIPID3")) << 0)

    print "USER ID:"
    print "\t0x%08x" % (readReg(getNode("LPGBT.RWF.CHIPID.USERID0")) << 24 | \
                        readReg(getNode("LPGBT.RWF.CHIPID.USERID1")) << 16 | \
                        readReg(getNode("LPGBT.RWF.CHIPID.USERID2")) << 8  | \
                        readReg(getNode("LPGBT.RWF.CHIPID.USERID3")) << 0)

    print "Lock mode:"
    if (readReg(getNode("LPGBT.RO.LPGBTSETTINGS.LOCKMODE"))):
        print "\t1 = Reference-less locking. Recover frequency from the data stream."
    else:
        print "\t0 = Use external 40 MHz reference clock."

    print "LpGBT Mode:"
    mode = readReg(getNode("LPGBT.RO.LPGBTSETTINGS.LPGBTMODE"))

    if (mode==0) : print ("\t4'b0000    5 Gbps     FEC5    Off")
    if (mode==1) : print ("\t4'b0001    5 Gbps     FEC5    Simplex TX")
    if (mode==2) : print ("\t4'b0010    5 Gbps     FEC5    Simplex RX")
    if (mode==3) : print ("\t4'b0011    5 Gbps     FEC5    Transceiver")
    if (mode==4) : print ("\t4'b0100    5 Gbps     FEC12   Off")
    if (mode==5) : print ("\t4'b0101    5 Gbps     FEC12   Simplex TX")
    if (mode==6) : print ("\t4'b0110    5 Gbps     FEC12   Simplex RX")
    if (mode==7) : print ("\t4'b0111    5 Gbps     FEC12   Transceiver")
    if (mode==8) : print ("\t4'b1000    10 Gbps    FEC5    Off")
    if (mode==9) : print ("\t4'b1001    10 Gbps    FEC5    Simplex TX")
    if (mode==10): print ("\t4'b1010    10 Gbps    FEC5    Simplex RX")
    if (mode==11): print ("\t4'b1011    10 Gbps    FEC5    Transceiver")
    if (mode==12): print ("\t4'b1100    10 Gbps    FEC12   Off")
    if (mode==13): print ("\t4'b1101    10 Gbps    FEC12   Simplex TX")
    if (mode==14): print ("\t4'b1110    10 Gbps    FEC12   Simplex RX")
    if (mode==15): print ("\t4'b1111    10 Gbps    FEC12   Transceiver")

    print "State Override:"
    if (readReg(getNode("LPGBT.RO.LPGBTSETTINGS.STATEOVERRIDE"))):
        print "\t1 = Power up state machine halted."
    else:
        print "\t0 = Normal operation."

    print "VCO Bypass:"
    if (readReg(getNode("LPGBT.RO.LPGBTSETTINGS.VCOBYPASS"))):
        print "\t1 = VCO Bypass mode. System clock come from TSTCLKINP/N (5.12 GHz)."
    else:
        print "\t0 = Normal operation. System clocks comes from PLL/CDR."

    pusmstate = readReg(getNode("LPGBT.RO.PUSM.PUSMSTATE"))

    print "PUSM State:"

    if (pusmstate==0):  print "\t0  = ARESET - the FSM stays in this state when power-on-reset or an external reset (RSTB) is asserted. \n\t When external signal PORdisable is asserted, the signal generated by the internal power-on-reset is ignored. All action flags are reset in this state."
    if (pusmstate==1):  print "\t1  = RESET - synchronous reset state. In this state, the FSM produces synchronous reset signal for various circuits. \n\t All action flags are not reset in this state."
    if (pusmstate==2):  print "\t2  = WAIT_VDD_STABLE - the FSM waits for VDD to raise. It has fixed duration of 4,000 clock cycles (~100us)."
    if (pusmstate==3):  print "\t3  = WAIT_VDD_HIGHER_THAN_0V90 - the FSM monitors the VDD voltage. \n\t It waits until VDD stays above 0.9V for a period longer than 1us.\n\t This state is bypassed if PORdisable is active."
    if (pusmstate==4):  print "\t4  = FUSE_SAMPLING - initiate fuse sampling."
    if (pusmstate==5):  print "\t5  = UPDATE FROM FUSES - transfer fuse values into registers. Transfer executed only if updateEnable fuse in POWERUP2 register is blown."
    if (pusmstate==6):  print "\t6  = PAUSE_FOR_PLL_CONFIG - this state is foreseen for initial testing of the chip when optimal registers settings are not yet known and the e-fuses have not been burned. The FSM will wait in this state until pllConfigDone bit is asserted. While in this state, the user can use the I2C interface to write values to the registers. For more details about intended use please refer to Section 3.7."
    if (pusmstate==7):  print "\t7  = WAIT_POWER_GOOD - this state is foreseen to make sure that the power supply voltage is stable before proceeding with further initialization. When PGEnable bit is enabled the FSM will wait until VDD level stays above value configured by PGLevel[2:0] for longer than time configured by PGDelay[4:0]. If PGEnable is not set, one can use PGDelay[4:0] as a fixed delay. The PGLevel[2:0] and PGDelay[4:0] are interpreted according to Table 8.1 and Table 8.2."
    if (pusmstate==8):  print "\t8  = RESETOUT - in this state a reset signal is generated on the resetout pin. The reset signal is active low. The duration of the reset pulse is controlled by value of ResetOutLength[1:0] field according to Table 8.3."
    if (pusmstate==9):  print "\t9  = I2C_TRANS - this state is foreseen to execute one I2C transaction. This feature can be used to configure a laser driver chip or any other component in the system. To enable transaction, the I2CMTransEnable bit has to be programmed and master channel has to be selected by I2CMTransChannel[1:0]. Remaining configuration like I2CMTransAddressExt[2:0], I2CMTransAddress[6:0], and I2CMTransCtrl[127:0] should be configured according to the description in the I2C slaves chapter."
    if (pusmstate==10): print "\t10 = RESET_PLL - reset PLL/CDR control logic."
    if (pusmstate==11): print "\t11 = WAIT_PLL_LOCK - waits for the PLL/CDR to lock. \n\t When lpGBT is configured in simplex RX or transceiver mode the lock signal comes from frame aligner. \n\t It means that the valid lpGBT frame has to be sent in the downlink. \n\t This state can be interrupted by timeout action (see the description below)."
    if (pusmstate==12): print "\t12 = INIT_SCRAM - initializes scrambler in the uplink data path."
    if (pusmstate==13): print "\t13 = PAUSE_FOR_DLL_CONFIG - this state is foreseen for the case in which user wants to use serial interface (IC/EC) to configure the chip. The FSM will wait in this state until dllConfigDone bit is asserted. While in this state, the user can use the serial interface (IC/EC) or I2C interface to write values to the registers. For more details about intended use please refer to Section 3.7."
    if (pusmstate==14): print "\t14 = RESET_DLLS - reset DLLs in ePortRx groups and phase-shifter."
    if (pusmstate==15): print "\t15 = WAIT_DLL_LOCK - wait until all DLL report to be locked. This state can be interrupted by timeout action (see the description below)."
    if (pusmstate==16): print "\t16 = RESET_LOGIC_USING_DLL - reset a logic using DLL circuitry. In case of ePortRx groups, this signal is used to initialize automatic phase training. This state has no impact on a phase-shifter operation."
    if (pusmstate==17): print "\t17 = WAIT_CHNS_LOCKED - in this state, FSM waits until automatic phase training is finished for all enabled ePortRx groups. One should keep in mind, that data transitions have to be present on the enabled channels to acquire lock. By default this state is bypassed, it can be enabled asserting PUSMReadyWhenChnsLocked bit in POWERUP register. This state can be interrupted by timeout action (see the description below)."
    if (pusmstate==18): print "\t18 = READY - initialization is completed. Chip is operational. READY signal is asserted."


    if (readReg(getNode("LPGBT.RO.PUSM.PUSMPLLTIMEOUTACTION"))):
        print "PLL timeout:"
        print "\tPLL timeout action has been executed since the last chip reset."

    if (readReg(getNode("LPGBT.RO.PUSM.PUSMDLLTIMEOUTACTION"))):
        print "DLL timeout:"
        print "\tDLL timeout action has been executed since the last chip reset."

    if (readReg(getNode("LPGBT.RO.PUSM.PUSMCHANNELSTIMEOUTACTION"))):
        print "Channels timeout:"
        print "\tWait for channels locked timeout action has been executed since the last chip reset."

    if (readReg(getNode("LPGBT.RO.PUSM.PUSMBROWNOUTACTION"))):
        print "Brownout:"
        print "\tThe brownout action has been executed since the last chip reset."

    if (readReg(getNode("LPGBT.RO.PUSM.PUSMPLLWATCHDOGACTION"))):
        print "PLL Watchdog:"
        print "\tPLL watchdog action has been executed since the last chip reset."

    if (readReg(getNode("LPGBT.RO.PUSM.PUSMDLLWATCHDOGACTION"))):
        print "DLL Watchdog:"
        print "\tDLL watchdog action has been executed since the last chip reset."

    print "Frame Aligner State:"
    print "\t" + str(readReg(getNode("LPGBT.RO.PUSM.FASTATE")))

    print "Frame Aligner Counter:"
    print "\t%d" % readReg(getNode("LPGBT.RO.PUSM.FACOUNTER"))

    clkgfmstate = readReg(getNode("LPGBT.RO.CLKG.CLKG_SMSTATE"))
    print "LJCDR State:"

    if (clkgfmstate==0x0):  print "\t0x0 = smResetState reset state"
    if (clkgfmstate==0x1):  print "\t0x1 = smInit initialization state (1cycle)"
    if (clkgfmstate==0x2):  print "\t0x2 = smCapSearchStart start VCO calibration (jump to smPLLInit or smCDRInit when finished)"
    if (clkgfmstate==0x3):  print "\t0x3 = smCapSearchClearCounters0 VCO calibration step; clear counters"
    if (clkgfmstate==0x4):  print "\t0x4 = smCapSearchClearCounters1 VCO calibration step; clear counters"
    if (clkgfmstate==0x5):  print "\t0x5 = smCapSearchEnableCounter VCO calibration step; start counters"
    if (clkgfmstate==0x6):  print "\t0x6 = smCapSearchWaitFreqDecision; VCO calibration step; wait for race end"
    if (clkgfmstate==0x7):  print "\t0x7 = smCapSearchVCOFaster VCO calibration step; VCO is faster than refClk, increase capBank"
    if (clkgfmstate==0x8):  print "\t0x8 = smCapSearchRefClkFaster VCO calibration step; refClk is faster than VCO, decrease capBank"
    if (clkgfmstate==0x9):  print "\t0x9 = smPLLInit PLL step; closing PLL loop and waiting for lock state. \n\t Waits for lockfilter (if enabled), waits for waitPllTime (~ifenabled)"
    if (clkgfmstate==0xa):  print "\t0xa = smCDRInit CDR step; closing CDR loop and waiting for lock state"
    if (clkgfmstate==0xb):  print "\t0xb = smPLLEnd PLL step; PLL is locked"
    if (clkgfmstate==0xc):  print "\t0xc = smCDREnd CDR step; CDR is locked"

    clkglfstate = readReg(getNode("LPGBT.RO.CLKG.CLKG_LFSTATE"))
    print "LJCDR Lock Filter State:"
    if (clkglfstate==0): print "\t0 = lfUnlfLockedState low-pass lock filter is unlocked"
    if (clkglfstate==1): print "\t1 = lfConfirmLockState low-pass lock filter is confirming lock"
    if (clkglfstate==2): print "\t2 = lfLockedState low-pass lock filter is locked"
    if (clkglfstate==3): print "\t3 = lfConfirmUnlockState"


    print "Lock Filter Loss of Lock Count:"
    print "\t%d" % readReg(getNode("LPGBT.RO.CLKG.CLKG_LFLOSSOFLOCKCOUNT"))

    print "LJCDR Locked Flag:"
    print "\t%d" % readReg(getNode("LPGBT.RO.CLKG.CLKG_SMLOCKED"))

    print "Downlink FEC Errors:"
    print "\t%d" % (readReg(getNode("LPGBT.RO.FEC.DLDPFECCORRECTIONCOUNT_H")) << 8 |readReg(getNode("LPGBT.RO.FEC.DLDPFECCORRECTIONCOUNT_L")))

    print "CDR Resistor:"
    if (readReg(getNode("LPGBT.RO.CLKG.CLKG_ENABLE_CDR_R"))):
        print "\t1 = connected"
    else:
        print "\t0 = disconnected"

    print "CDR Proportional Charge Pump Current:"
    print "\t%f uA" % (5.46 * readReg(getNode("LPGBT.RO.CLKG.CLKG_CONFIG_P_CDR")))

    print "CDR Proportional Feedforward Current:"
    print "\t%f uA" % (5.46 * readReg(getNode("LPGBT.RO.CLKG.CLKG_CONFIG_P_FF_CDR")))

    print "CDR Integral Current:"
    print "\t%f uA" % (5.46 * readReg(getNode("LPGBT.RO.CLKG.CLKG_CONFIG_I_CDR")))

    print "CDR FLL Current:"
    print "\t%f uA" % (5.46 * readReg(getNode("LPGBT.RO.CLKG.CLKG_CONFIG_I_FLL")))

    print "VCO Cap Select:"
    print "\t%d" % (readReg(getNode("LPGBT.RO.CLKG.CLKG_VCOCAPSELECTH")) << 1 |readReg(getNode("LPGBT.RO.CLKG.CLKG_VCOCAPSELECTH")))

    #print ("Configuring adc...")
    #writeReg(getNode("LPGBT.RW.ADC.ADCENABLE"), 0x1)
    #writeReg(getNode("LPGBT.RW.ADC.ADCINNSELECT"), 0x15)
    #writeReg(getNode("LPGBT.RW.ADC.CONVERT"), 0x1)
    #writeReg(getNode("LPGBT.RW.ADC.GAINSELECT"), 0x1)

    init_adc()
    print "ADC Readings:"
    for i in range(16):
        name = ""
        if (i==0 ):  name="N/A";
        if (i==1 ):  name="ASENSE_2";
        if (i==2 ):  name="ASENSE_1";
        if (i==3 ):  name="ASENSE_3";
        if (i==4 ):  name="ASENSE_0";
        if (i==5 ):  name="1V2_DIV2";
        if (i==6 ):  name="2V5_DIV3";
        if (i==7 ):  name="N/A";
        if (i==8 ):  name="EOM DAC (internal signal)";
        if (i==9 ):  name="VDDIO * 0.42 (internal signal)";
        if (i==10):  name="VDDTX * 0.42 (internal signal)";
        if (i==11):  name="VDDRX * 0.42 (internal signal)";
        if (i==12):  name="VDD * 0.42 (internal signal)";
        if (i==13):  name="VDDA * 0.42 (internal signal)";
        if (i==14):  name="Temperature sensor (internal signal)";
        if (i==15):  name="VREF/2 (internal signal)";

        read = read_adc(i)
        print "\tch %X: 0x%03X = %f (%s)" % (i, read, read/1024., name)

def init_adc():
    mpoke (0x113, 0x04) # adc enable
    mpoke (0x112, 0x1f) # enable dividers + temp sensor
    mpoke (0x01c, 0x80) # vref enable
    sleep (0.01)

def powerdown_adc():

    mpoke (0x113, 0x00) # adc disable
    mpoke (0x01c, 0x1c) # vref disable
    mpoke (0x112,0x0) # disable dividers + temp sensor

def read_adc(channel):

    # ADCInPSelect[3:0]	|  Input
    # ------------------|----------------------------------------
    # 4'd0	        |  ADC0 (external pin)
    # 4'd1	        |  ADC1 (external pin)
    # 4'd2	        |  ADC2 (external pin)
    # 4'd3	        |  ADC3 (external pin)
    # 4'd4	        |  ADC4 (external pin)
    # 4'd5	        |  ADC5 (external pin)
    # 4'd6	        |  ADC6 (external pin)
    # 4'd7	        |  ADC7 (external pin)
    # 4'd8	        |  EOM DAC (internal signal)
    # 4'd9	        |  VDDIO * 0.42 (internal signal)
    # 4'd10	        |  VDDTX * 0.42 (internal signal)
    # 4'd11	        |  VDDRX * 0.42 (internal signal)
    # 4'd12	        |  VDD * 0.42 (internal signal)
    # 4'd13	        |  VDDA * 0.42 (internal signal)
    # 4'd14	        |  Temperature sensor (internal signal)
    # 4'd15	        |  VREF/2 (internal signal)

    # "LPGBT.RW.ADC.ADCINPSELECT"
    # "LPGBT.RW.ADC.ADCINNSELECT"
    mpoke (0x111, channel<<4 | 0xf)

    # "LPGBT.RW.ADC.ADCGAINSELECT"
    # "LPGBT.RW.ADC.ADCCONVERT"
    mpoke (0x113, 0x84)

    done = 0
    while (done==0):
        done = 0x1 & (mpeek(0x1b8) >> 6) # "LPGBT.RO.ADC.ADCDONE"

    val  = mpeek(0x1b9)               # LPGBT.RO.ADC.ADCVALUEL
    val |= (0x3 & mpeek (0x1b8)) << 8 # LPGBT.RO.ADC.ADCVALUEL

    mpoke (0x113, 0x04)

    return val

if __name__ == '__main__':
    main()


