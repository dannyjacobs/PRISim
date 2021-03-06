import numpy as NP
from astropy.io import fits
import healpy as HP
import glob

rootdir = '/data3/t_nithyanandan/project_HERA/'
beams_dir = 'power_patterns/Abraham/'
# simsource = 'ABRAHAM-DAVE'
# infile = 'Abraham_DeBoer_beam_A_17_197_137o5_healpix.txt'
# outfile = 'Abraham_DeBoer_beam_A_17_197_137o5_healpix.fits'

# simsource = 'ABRAHAM-DAVE-128'
# infile = 'Abraham_DeBoer_beam_195_137o5_hp_nside128full.txt'
# outfile = 'Abraham_DeBoer_beam_195_137o5_hp_nside128full.fits'

simsource = 'ABRAHAM-DAVE-128'
infile = 'XRFBg_195_137o5_hp_nside128full.txt'
outfile = 'XRFBg_195_137o5_hp_nside128full.fits'

# simsource = 'ABRAHAM-RICH'
# infile = 'Abraham_Rich_beam_1375_18H_P1_healpix.txt'
# outfile = 'Abraham_Rich_beam_1375_18H_P1_healpix.fits'

# simsource = 'ABRAHAM-RICH-128'
# infile = 'Abraham_Rich_beam_1375_18L_P1_hp_nside128.txt'
# outfile = 'Abraham_Rich_beam_1375_18L_P1_hp_nside128.fits'

# simsource = 'ABRAHAM-RICH-128'
# infile = 'Abraham_Rich_beam_1375_18H_P1_hp_nside128full.txt'
# outfile = 'Abraham_Rich_beam_1375_18H_P1_hp_nside128full.fits'

beam = NP.loadtxt(rootdir+beams_dir+infile)
nside_in = HP.get_nside(beam)
npix_in = beam.shape[0]
freq = 137.5 # in MHz
pols = ['X']
scheme = 'RING'

hdulist = []
hdulist += [fits.PrimaryHDU()]
hdulist[0].header['EXTNAME'] = 'PRIMARY'
hdulist[0].header['NPOL'] = (len(pols), 'Number of polarizations')
hdulist[0].header['SOURCE'] = (simsource, 'Source of data')
for pi,pol in enumerate(pols):
    hdu = fits.ImageHDU(beam, name='BEAM_{0}'.format(pol))
    hdu.header['PIXTYPE'] = ('HEALPIX', 'Type of pixelization')
    hdu.header['ORDERING'] = (scheme, 'Pixel ordering scheme, either RING or NESTED')
    hdu.header['NSIDE'] = (nside_in, 'NSIDE parameter of HEALPIX')
    hdu.header['NPIX'] = (npix_in, 'Number of HEALPIX pixels')
    hdu.header['FIRSTPIX'] = (0, 'First pixel # (0 based)')
    hdu.header['LASTPIX'] = (npix_in-1, 'Last pixel # (0 based)')    
    hdulist += [hdu]
    hdulist += [fits.ImageHDU(NP.asarray(freq).reshape(-1), name='FREQS_{0}'.format(pol))]
outhdu = fits.HDUList(hdulist)
outhdu.writeto(rootdir+beams_dir+outfile, clobber=True)
    
