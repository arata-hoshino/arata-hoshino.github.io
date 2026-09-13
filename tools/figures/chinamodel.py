"""
Cohort-component projection of annual births in China.

births(t) = sum_a  W(a,t) * ASFR(a) ,  sum_a ASFR(a) = TFR(t)
W(a,t) = births(t-a) * female_share(t-a) * survival

Age-specific fertility uses a skew-normal schedule calibrated so that the mean
age at childbearing matches ~29.7 (mean age at FIRST birth in China is ~29 in 2025).
The schedule is validated against the observed 2025 outturn.
"""
import numpy as np

B = {1970:27356,1971:25780,1972:25663,1973:24633,1974:22347,1975:21086,1976:18530,
1977:17860,1978:17450,1979:17268,1980:17868,1981:20782,1982:21260,1983:18996,
1984:18022,1985:21994,1986:23928,1987:25291,1988:24643,1989:24140,1990:23910,
1991:22650,1992:21250,1993:21320,1994:21100,1995:20630,1996:20670,1997:20380,
1998:19420,1999:18340,2000:17710,2001:17020,2002:16470,2003:15990,2004:15930,
2005:16170,2006:15850,2007:15940,2008:16080,2009:15910,2010:15920,2011:17970,
2012:19730,2013:17760,2014:18970,2015:16550,2016:17860,2017:17230,2018:15230,
2019:14650,2020:12020,2021:10620,2022:9560,2023:9020,2024:9540,2025:7920}
# thousands

def srb(y):
    """Sex ratio at birth (M/F). NBS/census series, linearly interpolated."""
    pts=[(1970,1.06),(1982,1.086),(1990,1.116),(2000,1.169),(2005,1.184),
         (2010,1.179),(2015,1.135),(2020,1.113),(2025,1.090),(2050,1.060)]
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return float(np.interp(y,xs,ys))

def female_share(y): return 1.0/(1.0+srb(y))
SURV = 0.985                      # female survival from birth to reproductive ages

AGES = np.arange(15,50)

def asfr_shape(mu=29.7, sigma=4.9, alpha=1.6):
    """Skew-normal fertility schedule, normalised to sum to 1."""
    from scipy.stats import skewnorm
    # convert desired mean to skewnorm loc
    d = alpha/np.sqrt(1+alpha**2)
    loc = mu - sigma*d*np.sqrt(2/np.pi)
    w = skewnorm.pdf(AGES, alpha, loc=loc, scale=sigma)
    return w/w.sum()

def women(age, year):
    by = year-age
    if by in B: b = B[by]
    else: b = PROJ.get(by)
    if b is None: return 0.0
    return b*female_share(by)*SURV

def births(year, tfr, shape):
    w = np.array([women(a,year) for a in AGES])
    return float((w*shape*tfr).sum())

PROJ = {}

def run(tfr_path, mu_path=None, sigma=4.9, alpha=1.6, end=2060):
    """tfr_path: dict year->TFR (interpolated). mu_path: dict year->mean age."""
    global PROJ
    PROJ = {}
    ys=sorted(tfr_path); tv=[tfr_path[y] for y in ys]
    out={}
    for y in range(2026,end+1):
        tfr=float(np.interp(y,ys,tv))
        mu = 29.7 if mu_path is None else float(np.interp(y,sorted(mu_path),[mu_path[k] for k in sorted(mu_path)]))
        out[y]=births(y,tfr,asfr_shape(mu,sigma,alpha))
        PROJ[y]=out[y]
    return out

def calibrate():
    """Check the schedule reproduces the observed 2025 outturn."""
    sh=asfr_shape()
    return births(2025,0.93,sh), B[2025]
