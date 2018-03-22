import numpy as np 
import fitsio
import os
import datetime
import time
import sys
from array import array
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import *

##############################################################
# 20180322 #         output pol averaged data
##############################################################

if (len(sys.argv)<3):
  print 'too few inputs!'
  print 'example:'
  print 'python fitsio_combinepol.py infile outfile'
  sys.exit()
else:
  print 'input seems OK'



print 'record start time:'
starttime=datetime.datetime.now()
print starttime


infile=sys.argv[1]
outfile=sys.argv[2]


#u19700101=62135683200.0

#==============================================================
fits=fitsio.FITS(infile)

hdu0 = fits[0]
header0 = hdu0.read_header()

hdu1 = fits[1]
header1 = hdu1.read_header()

hdrver=header0['HDRVER']
date=header0['DATE']
ant_x=header0['ANT_X']
ant_y=header0['ANT_Y']
ant_z=header0['ANT_Z']
obsfreq=header0['OBSFREQ']
obsbw=header0['OBSBW']
nchan=header0['OBSNCHAN']
ra=header0['RA']
dec=header0['DEC']
bmaj=header0['BMAJ']
bmin=header0['BMIN']
date_obs=header0['DATE-OBS']
stt_imjd=header0['STT_IMJD']
stt_smjd=header0['STT_SMJD']
stt_offs=header0['STT_OFFS']
stt_lst=header0['STT_LST']
nsuboffs=header1['NSUBOFFS']
nchnoffs=header1['NCHNOFFS']
nsblk=header1['NSBLK']
npol=header1['NPOL']
tbin=header1['TBIN']
chan_bw=header1['CHAN_BW']
print 'NSBLK: ',nsblk,'sample time(s): ',tbin,'channel width(MHz): ',chan_bw

nline=header1['NAXIS2']
pol_type=header1['POL_TYPE']



rmcomm='rm -f '+outfile
os.system(rmcomm)
print rmcomm,outfile
fitsout=fitsio.FITS(outfile,'rw')

dataout = np.zeros(1,dtype=[('TSUBINT','float64'),('OFFS_SUB','float64'),('LST_SUB','float64'),('RA_SUB','float64'),('DEC_SUB','float64'),('GLON_SUB','float64'),('GLAT_SUB','float64'),('FD_ANG','float32'),('POS_ANG','float32'),('PAR_ANG','float32'),('TEL_AZ','float32'),('TEL_ZEN','float32'),('DAT_FREQ','float32',(nchan)),('DAT_WTS','float32',(nchan)),('DAT_OFFS','float32',(nchan)),('DAT_SCL','float32',(nchan)),('DATA','uint8',(nsblk,1,nchan,1))])


#=======================================================================
rowindex=0
dataout['TSUBINT'][0]=fits[1].read(rows=[rowindex], columns=['TSUBINT'])[0][0]
dataout['OFFS_SUB'][0]=fits[1].read(rows=[rowindex], columns=['OFFS_SUB'])[0][0]
dataout['LST_SUB'][0]=fits[1].read(rows=[rowindex], columns=['LST_SUB'])[0][0]
dataout['RA_SUB'][0]=fits[1].read(rows=[rowindex], columns=['RA_SUB'])[0][0]
dataout['DEC_SUB'][0]=fits[1].read(rows=[rowindex], columns=['DEC_SUB'])[0][0]
dataout['GLON_SUB'][0]=fits[1].read(rows=[rowindex], columns=['GLON_SUB'])[0][0]
dataout['GLAT_SUB'][0]=fits[1].read(rows=[rowindex], columns=['GLAT_SUB'])[0][0]
dataout['FD_ANG'][0]=fits[1].read(rows=[rowindex], columns=['FD_ANG'])[0][0]
dataout['POS_ANG'][0]=fits[1].read(rows=[rowindex], columns=['POS_ANG'])[0][0]
dataout['PAR_ANG'][0]=fits[1].read(rows=[rowindex], columns=['PAR_ANG'])[0][0]
dataout['TEL_AZ'][0]=fits[1].read(rows=[rowindex], columns=['TEL_AZ'])[0][0]
dataout['TEL_ZEN'][0]=fits[1].read(rows=[rowindex], columns=['TEL_ZEN'])[0][0]
dataout['DAT_FREQ'][0]=fits[1].read(rows=[rowindex], columns=['DAT_FREQ'])[0][0][0:nchan]
dataout['DAT_WTS'][0]=fits[1].read(rows=[rowindex], columns=['DAT_WTS'])[0][0][0:nchan]
dataout['DAT_OFFS'][0][0:nchan]=fits[1].read(rows=[rowindex], columns=['DAT_OFFS'])[0][0][0:nchan]
dataout['DAT_SCL'][0][0:nchan]=fits[1].read(rows=[rowindex], columns=['DAT_SCL'])[0][0][0:nchan]

data=fits[1].read(rows=[rowindex], columns=['DATA'])

for subindex in range(nsblk):
    dataout['DATA'][0][subindex,0,:,0]=(data[0][0][subindex,0,:,0]+data[0][0][subindex,1,:,0])/2
fitsout.write(dataout)
#=======================================================================

fitsout[0].write_key('HDRVER',hdrver,comment="")
fitsout[0].write_key('FITSTYPE','PSRFITS',comment="FITS definition ")
fitsout[0].write_key('DATE',date,comment="")
fitsout[0].write_key('OBSERVER','FAST_TEAM',comment="Observer name")
fitsout[0].write_key('PROJID','Drift',comment="Project name")
fitsout[0].write_key('TELESCOP','FAST',comment="Telescope name")
fitsout[0].write_key('ANT_X',ant_x,comment="")
fitsout[0].write_key('ANT_Y',ant_y,comment="")
fitsout[0].write_key('ANT_Z',ant_z,comment="")
fitsout[0].write_key('FRONTEND','WIDEBAND',comment="Frontend ID")
fitsout[0].write_key('NRCVR',1,comment="")
fitsout[0].write_key('FD_POLN','LIN',comment="LIN or CIRC")
fitsout[0].write_key('FD_HAND',1,comment="")
fitsout[0].write_key('FD_SANG',0.,comment="")
fitsout[0].write_key('FD_XYPH',0.,comment="")
fitsout[0].write_key('BACKEND','ROACH',comment="Backend ID")
fitsout[0].write_key('BECONFIG','N/A',comment="")
fitsout[0].write_key('BE_PHASE',1,comment="")
fitsout[0].write_key('BE_DCC',0,comment="")
fitsout[0].write_key('BE_DELAY',0.,comment="")
fitsout[0].write_key('TCYCLE',0.,comment="")
fitsout[0].write_key('OBS_MODE','SEARCH',comment="(PSR, CAL, SEARCH)")
fitsout[0].write_key('DATE-OBS',date_obs,comment="Date of observation")
fitsout[0].write_key('OBSFREQ',obsfreq,comment="[MHz] Bandfrequency")
fitsout[0].write_key('OBSBW',obsbw,comment="[MHz] Bandwidth")
fitsout[0].write_key('OBSNCHAN',nchan,comment="Number of channels")
fitsout[0].write_key('CHAN_DM',0.,comment="")
fitsout[0].write_key('SRC_NAME','Drift',comment="Source or scan ID")
fitsout[0].write_key('COORD_MD','J2000',comment="")
fitsout[0].write_key('EQUINOX',2000.,comment="")

fitsout[0].write_key('RA',ra,comment="")
fitsout[0].write_key('DEC',dec,comment="")
fitsout[0].write_key('BMAJ',bmaj,comment="[deg] Beam major axis length")
fitsout[0].write_key('BMIN',bmin,comment="[deg] Beam minor axis length")
fitsout[0].write_key('BPA',0.,comment="[deg] Beam position angle")
fitsout[0].write_key('STT_CRD1','00:00:00.00',comment="")
fitsout[0].write_key('STT_CRD2','00:00:00.00',comment="")
fitsout[0].write_key('TRK_MODE','TRACK',comment="")
fitsout[0].write_key('STP_CRD1','00:00:00.00',comment="")
fitsout[0].write_key('STP_CRD2','00:00:00.00',comment="")
fitsout[0].write_key('SCANLEN',0.,comment="")
fitsout[0].write_key('FD_MODE','FA',comment="")
fitsout[0].write_key('FA_REQ',0.,comment="")
fitsout[0].write_key('CAL_MODE','OFF',comment="")
fitsout[0].write_key('CAL_FREQ',0.,comment="")
fitsout[0].write_key('CAL_DCYC',0.,comment="")
fitsout[0].write_key('CAL_PHS',0.,comment="")
fitsout[0].write_key('STT_IMJD',stt_imjd,comment="Start MJD (UTC days) (J - long integer)")
fitsout[0].write_key('STT_SMJD',stt_smjd,comment="[s] Start time (sec past UTC 00h) (J)")
fitsout[0].write_key('STT_OFFS',stt_offs,comment="[s] Start time offset (D)")
fitsout[0].write_key('STT_LST',stt_lst,comment="[s] Start LST (D)")

fitsout[1].write_key('INT_TYPE','TIME',comment="Time axis (TIME, BINPHSPERI, BINLNGASC, etc)")
fitsout[1].write_key('INT_UNIT','SEC',comment="Unit of time axis (SEC, PHS (0-1),DEG)")
fitsout[1].write_key('SCALE','FluxDen',comment="")
fitsout[1].write_key('NPOL',1,comment="Nr of polarisations")
fitsout[1].write_key('POL_TYPE','AABB',comment="Polarisation identifier")
fitsout[1].write_key('TBIN',tbin,comment="[s] Time per bin or sample")
fitsout[1].write_key('NBIN',1,comment="")
fitsout[1].write_key('NBIN_PRD',0,comment="Nr of bins/pulse period (for gated data)")
fitsout[1].write_key('PHS_OFFS',0.0,comment="Phase offset of bin 0 for gated data")
fitsout[1].write_key('NBITS',8,comment="Nr of bits/datum ")
fitsout[1].write_key('NSUBOFFS',nsuboffs,comment="Subint offset ")
fitsout[1].write_key('NCHNOFFS',nchnoffs,comment="Channel/sub-band offset for split files")
fitsout[1].write_key('NCHAN',nchan,comment="Number of channels")
fitsout[1].write_key('CHAN_BW',chan_bw,comment="[MHz] Channel/sub-band width")
fitsout[1].write_key('NSBLK',nsblk,comment="Samples/row ")
fitsout[1].write_key('EXTNAME','SUBINT  ',comment="name of this binary table extension")
fitsout[1].write_key('EXTVER',1,comment="")


'''
for rowindex in range(1,nline):
    dataout['TSUBINT'][0]=fits[1].read(rows=[rowindex], columns=['TSUBINT'])[0][0]
    dataout['OFFS_SUB'][0]=fits[1].read(rows=[rowindex], columns=['OFFS_SUB'])[0][0]
    dataout['LST_SUB'][0]=fits[1].read(rows=[rowindex], columns=['LST_SUB'])[0][0]
    dataout['RA_SUB'][0]=fits[1].read(rows=[rowindex], columns=['RA_SUB'])[0][0]
    dataout['DEC_SUB'][0]=fits[1].read(rows=[rowindex], columns=['DEC_SUB'])[0][0]
    dataout['GLON_SUB'][0]=fits[1].read(rows=[rowindex], columns=['GLON_SUB'])[0][0]
    dataout['GLAT_SUB'][0]=fits[1].read(rows=[rowindex], columns=['GLAT_SUB'])[0][0]
    dataout['FD_ANG'][0]=fits[1].read(rows=[rowindex], columns=['FD_ANG'])[0][0]
    dataout['POS_ANG'][0]=fits[1].read(rows=[rowindex], columns=['POS_ANG'])[0][0]
    dataout['PAR_ANG'][0]=fits[1].read(rows=[rowindex], columns=['PAR_ANG'])[0][0]
    dataout['TEL_AZ'][0]=fits[1].read(rows=[rowindex], columns=['TEL_AZ'])[0][0]
    dataout['TEL_ZEN'][0]=fits[1].read(rows=[rowindex], columns=['TEL_ZEN'])[0][0]
    dataout['DAT_FREQ'][0]=fits[1].read(rows=[rowindex], columns=['DAT_FREQ'])[0][0][0:nchan]
    dataout['DAT_WTS'][0]=fits[1].read(rows=[rowindex], columns=['DAT_WTS'])[0][0][0:nchan]
    dataout['DAT_OFFS'][0][0:nchan]=fits[1].read(rows=[rowindex], columns=['DAT_OFFS'])[0][0][0:nchan]
    dataout['DAT_SCL'][0][0:nchan]=fits[1].read(rows=[rowindex], columns=['DAT_SCL'])[0][0][0:nchan]

    data=fits[1].read(rows=[rowindex], columns=['DATA'])
    for subindex in range(nsblk):
        dataout['DATA'][0][subindex,0,:,0]=(data[0][0][subindex,0,:,0]+data[0][0][subindex,1,:,0])/2
        #dataout['DATA'][0][subindex,0,:,0]=(fits[1].read(rows=[index], columns=['DATA'])[0][0][subindex,0,:,0]/2+fits[1].read(rows=[rowindex], columns=['DATA'])[0][0][subindex,0,:,0]/2)
    fitsout[-1].append(dataout)
'''


#fitsout.write(dataout)


#==============================================================


fitsout.close()
print '--------------------------------------------'
print '             Finished!                      '


endtime=datetime.datetime.now()
print 'START:',starttime
print 'END:',endtime
duration=endtime-starttime
print 'DURATION:',duration.seconds,' sec'
