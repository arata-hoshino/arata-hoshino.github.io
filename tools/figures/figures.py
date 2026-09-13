"""
figures.py -- every figure in the book, in book order.

Run:  python3 run_china.py && python3 figures.py
Needs ET Book (ETBembo) in ~/.fonts.  `npm pack typeface-et-book` and copy
package/et-book/source/4-ttf/*.ttf there.

House style lives in bookstyle.py; the geometric chart primitives (Voronoi
treemap, sunburst, circle packing, chord ribbons, weighted KDE ridgeline,
unit charts) live in charts.py and are implemented from scratch so that every
drawing step is auditable.

Data files in this folder:
  data_worldbank_fertility_latest.csv  217 countries, TFR / CBR / population / births, 2024
  data_tfr_panel.csv                   217 countries x 1960-2024 total fertility rate
  data_pop_panel.csv                   217 countries x 1960-2024 population
  china_proj.json                      output of run_china.py
All three World Bank files were taken from the Open Data API, not from any
secondary compilation.
"""
import csv, json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from bookstyle import setup, save, INK, MID, LIGHT, FAINT
import charts
import chinamodel as cm

P = json.load(open('china_proj.json'))
A = {int(k): v for k, v in P['A'].items()}
Bs = {int(k): v for k, v in P['B'].items()}
B = cm.B

GREYS = ['#1a1a1a', '#3d3d3d', '#606060', '#858585', '#a8a8a8', '#c8c8c8', '#e4e4e4']


def blank(figsize):
    """A figure with no axes furniture at all, for the geometric charts."""
    fig, ax = setup(figsize)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_visible(False)
    ax.set_aspect('equal')
    return fig, ax


def panels(figsize, n=2, wr=None):
    """A row of n axes sharing the house style."""
    setup((1, 1)); plt.close()
    fig, axes = plt.subplots(1, n, figsize=figsize,
                            gridspec_kw={'width_ratios': wr or [1] * n})
    for ax in np.atleast_1d(axes):
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)
        ax.spines['left'].set_color(LIGHT); ax.spines['bottom'].set_color(LIGHT)
        ax.tick_params(length=0)
    return fig, axes



REGION_ORDER = ['Sub-Saharan Africa', 'South Asia', 'East Asia & Pacific',
                'Middle East, North Africa, Afghanistan & Pakistan',
                'Latin America & Caribbean', 'Europe & Central Asia', 'North America']
REGION_SHORT = {'Sub-Saharan Africa': 'Sub-Saharan Africa', 'South Asia': 'South Asia',
                'East Asia & Pacific': 'East Asia & Pacific',
                'Middle East, North Africa, Afghanistan & Pakistan': 'M. East, N. Africa, Afg., Pak.',
                'Latin America & Caribbean': 'Latin America & Caribbean',
                'Europe & Central Asia': 'Europe & Central Asia', 'North America': 'North America'}
NAME = {'Congo, Dem. Rep.': 'DR Congo', 'Egypt, Arab Rep.': 'Egypt',
        'Iran, Islamic Rep.': 'Iran', 'Yemen, Rep.': 'Yemen',
        'Russian Federation': 'Russia', 'Viet Nam': 'Vietnam',
        'Korea, Rep.': 'South Korea', "Cote d'Ivoire": "Cote d'Ivoire",
        'Turkiye': 'Turkiye', 'United Kingdom': 'UK',
        'Venezuela, RB': 'Venezuela', 'Syrian Arab Republic': 'Syria'}


def fig11():
    # Energy commanded per person, expressed in human-body equivalents.
    # One body at rest is about 100 W, so one mark = 100 W of continuous power.
    rows = [('Hunter-gatherer', 120, 'the body, and a fire'),
            ('World, 1500', 180, ''),
            ('World, 1800', 300, 'the eve of coal'),
            ('World, 1900', 890, ''),
            ('World, 2024', 2430, ''),
            ('United States, 2024', 8767, 'about eighty-eight bodies working for one person')]
    PER = 100.0
    COLS = 24
    fig, ax = blank((7.6, 3.9))
    top = 0.0
    marks = []
    for nm, w, note in rows:
        n = int(round(w / PER))
        nrows = int(np.ceil(n / COLS))
        c = INK if nm.startswith('United') else ('#555555' if '2024' in nm else LIGHT)
        for k in range(n):
            cx, cy = k % COLS, k // COLS
            ax.add_patch(mp.Rectangle((cx * 1.0, -(top + cy) - 0.78), 0.62, 0.74,
                                      facecolor=c, edgecolor='none'))
        ymid = -(top + nrows / 2.0) - 0.4
        marks.append((nm, w, note, ymid))
        top += nrows + 1.15
    for nm, w, note, ymid in marks:
        ax.text(-1.4, ymid, nm, fontsize=10, ha='right', va='center', color=INK)
        ax.text(-1.4, ymid - 0.80, f'{w:,} W', fontsize=8.4, ha='right', va='center', color=MID)
        if note:
            ax.text(COLS + 1.0, ymid, note, fontsize=8.4, ha='left', va='center', color=MID)
    ax.set_xlim(-11.0, COLS + 17.0)
    ax.set_ylim(-top - 0.6, 4.4)
    ax.set_aspect('equal')
    ax.text(-11.0, 2.6, 'one mark = 100 watts of continuous power, roughly one human body at rest; each row is 24 marks',
            fontsize=9, color=MID, va='center', ha='left')
    ax.set_title('Figure 1-1 Energy commanded per person, in human-body equivalents')
    save(fig, 'fig1-1_energy_per_capita',
         'Our World in Data (CC BY 4.0); Smil, Energy and Civilization (2017).',
         'Twelve thousand years separate the top row from the bottom, and almost all of the difference arrives after 1800. '
         'Values before that date are order-of-magnitude estimates.')


def fig12():
    # 1-2 Japan: trade balance after the nuclear shutdown
    fig,ax=setup((6.8,3.8))
    yr=list(range(2008,2016)); tb=[2.1,4.0,5.4,-2.6,-6.9,-13.7,-12.8,-2.8]; lng=[12.6,9.1,10.91,14.7,16.75,16.0,16.2,10.3]
    ax.bar(yr,tb,color=[LIGHT if v>0 else INK for v in tb],width=.6)
    ax.axhline(0,color=LIGHT,lw=.9); ax.set_ylabel('Trade balance, trillion yen')
    a2=ax.twinx(); a2.plot(yr,lng,color=MID,lw=1.8,marker='o',ms=3.5); a2.set_ylabel('LNG import price, USD/MMBtu',color=MID)
    for s in ('top','right','left'): a2.spines[s].set_visible(False)
    a2.tick_params(length=0); a2.grid(False)
    ax.annotate('Fukushima, March 2011',xy=(2011,-2.6),xycoords='data',
     xytext=(0.05,0.93),textcoords='axes fraction',fontsize=8.5,ha='left',va='top',
     arrowprops=dict(arrowstyle='-',color=MID,lw=0.6))
    ax.set_title('Figure 1-2 Japan: the trade balance after the nuclear shutdown')
    save(fig,'fig1-2_japan_trade','Ministry of Finance trade statistics; IEEJ.',
     'A swing of roughly 20 trillion yen in three years, paid to foreign energy suppliers.')


def fig21():
    # ---- Fig 2-1 price of computing
    fig,ax=setup((6.6,3.9))
    y=np.array([1850,1900,1940,1960,1980,2000,2020])
    p=np.array([1e0,3e-1,1e-2,1e-6,1e-9,1e-12,1.3e-14])
    ax.semilogy(y,p,color=INK,lw=2,marker='o',ms=3.5)
    ax.set_ylabel('Cost per computation (log, 1850 = 1)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: '$10^{%d}$' % int(round(np.log10(x))) if x > 0 else ''))
    ax.annotate('improvement of 1.7 to 76 trillion times\nsince manual computation',(1980,1e-9),
     xytext=(0.50,0.05),textcoords='axes fraction',fontsize=9,ha='left',va='bottom',
     bbox=dict(boxstyle='round,pad=0.15',facecolor='white',edgecolor='none',zorder=10))
    ax.set_xlim(1840,2035)
    ax.set_title('Figure 2-1 Two centuries of the price of computing')
    save(fig,'fig2-1_computing_price','Nordhaus (2007), Journal of Economic History 67(1).')


# ============================================================== Figure 2-2 ===
def fig22():
    fig, (a1, a2) = panels((7.6, 3.9), 2)
    yrs = np.linspace(2023, 2030, 200)

    # Left: the load. IEA states 485 TWh in 2025 and 950 TWh in 2030.
    path = 485 * (950 / 485) ** ((yrs - 2025) / 5.0)
    a1.fill_between(yrs, 0, path, color=FAINT)
    a1.plot(yrs, path, color=INK, lw=2.2)
    a1.scatter([2025, 2030], [485, 950], color=INK, s=32, zorder=6)
    a1.annotate('485 TWh\n2025', (2025, 485), xytext=(-8, 12), textcoords='offset points',
                fontsize=9.2, ha='right')
    a1.annotate('950 TWh by 2030\nabout 3% of world electricity', (2030, 950),
                xytext=(-6, 12), textcoords='offset points', fontsize=9.2, ha='right')
    a1.annotate('+17% in 2025 alone;\nAI-specific sites +50%', (2026.0, 560),
                xytext=(6, -46), textcoords='offset points', fontsize=8.8, color=MID)
    a1.set_ylim(0, 1150); a1.set_xlim(2023, 2030.4)
    a1.set_xticks([2023, 2025, 2027, 2030]); a1.set_xticklabels(['2023', '2025', '2027', '2030'])
    a1.set_ylabel('Data-centre electricity, TWh a year')
    a1.set_title('The load', loc='left', fontsize=11, pad=10)
    a1.grid(color=FAINT, lw=0.9); a1.set_axisbelow(True)

    # Right: the efficiency. IEA reports at least an order of magnitude a year,
    # without stating a level, so this is drawn as a band and not as a series.
    hi = 10.0 ** (-(yrs - 2023) * 1.00)
    lo = 10.0 ** (-(yrs - 2023) * 1.55)
    a2.fill_between(yrs, lo, hi, color=FAINT)
    a2.plot(yrs, hi, color=INK, lw=1.6, ls=(0, (4, 3)))
    a2.plot(yrs, lo, color=MID, lw=1.2, ls=(0, (4, 3)))
    a2.set_yscale('log'); a2.set_ylim(1e-11, 3)
    a2.set_yticks([1, 1e-3, 1e-6, 1e-9])
    a2.set_yticklabels(['1', '1/1,000', '1/1,000,000', '1/1,000,000,000'])
    a2.set_xlim(2023, 2030.4)
    a2.set_xticks([2023, 2025, 2027, 2030]); a2.set_xticklabels(['2023', '2025', '2027', '2030'])
    a2.set_ylabel('Energy per AI task, 2023 = 1 (log)')
    a2.set_title('The efficiency', loc='left', fontsize=11, pad=10)
    a2.annotate('"at least an order of magnitude\na year" (IEA 2026)', (2026.2, 10 ** -3.4),
                xytext=(4, 4), textcoords='offset points', fontsize=8.8, color=MID)
    a2.grid(color=FAINT, lw=0.9); a2.set_axisbelow(True)

    fig.suptitle('Figure 2-2 Jevons, measured: the load rose while the task got cheaper',
                 x=0.005, y=1.02, ha='left', fontsize=12.5)
    save(fig, 'fig2-2_datacenter_demand',
         'IEA, Key Questions on Energy and AI (July 2026); IEA, Energy and AI (2025).',
         'Left: the two figures the IEA states, on a constant-growth path between them. Right: a band, not a series. '
         'The IEA reports the fall in energy per AI task without giving a level, so only its stated rate is drawn.')


def fig23():
    # ---- Fig 2-3 British agriculture
    fig,ax=setup((6.6,3.7))
    y=[1381,1522,1600,1700,1759,1801,1851,1901,1951,2001,2024]; s=[57,58,50,43,37,35,22,9,5,1.5,1]
    ax.plot(y,s,color=INK,lw=2,marker='o',ms=3.2)
    ax.set_ylabel('Agriculture, % of labour force'); ax.set_ylim(0,62)
    ax.annotate('1801: little more than one third',(1801,35),xytext=(10,14),textcoords='offset points',fontsize=9)
    ax.annotate('today: about 1%,\nsupplying ~60% of domestic food',(2024,1),xytext=(-10,44),textcoords='offset points',fontsize=9,ha='right')
    ax.set_title('Figure 2-3 Britain: agriculture\'s share of the labour force, 1381–2024')
    save(fig,'fig2-3_uk_agriculture','Broadberry et al. (2013, 2015); Bank of England, A Millennium of Macroeconomic Data; ONS.',
     'The industrial revolution never ended; it merely changed sectors.')


def fig31():
    # 3-1 US per-capita energy break (replaced with EIA actuals; formerly a linear-formula placeholder)
    fig,ax=setup((6.6,3.6))
    y=[1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]
    v=[232.1,244.8,238.4,240.6,231.1,249.0,254.3,250.0,244.8,251.1,256.4,256.4,263.8,270.1,277.5,285.9,298.6,303.9,319.7,332.3,339.7,341.8,355.6,367.2,354.5,340.8,357.7,366.1,369.3,369.3,353.4,340.8,322.8,318.6,332.3,329.2,327.1,335.5,349.2,353.4,348.2,342.9,345.0,346.1,349.2,351.3,357.7,355.6,354.5,356.6,361.9,349.2,350.3,348.2,353.4,350.3,343.9,347.1,335.5,315.5,325.0,318.6,308.1,314.4,316.5,311.2,307.0,304.9,314.4,310.2,282.8,296.5,299.6,293.3,293.3]
    ax.plot(y,v,color=INK,lw=1.9); ax.axvline(1979,color=LIGHT,lw=1)
    ax.annotate('the slope breaks, and never recovers',(1979,372),xytext=(12,16),textcoords='offset points',fontsize=9,
      bbox=dict(boxstyle='round,pad=0.16',facecolor='white',edgecolor='none'))
    ax.set_ylabel('US primary energy per capita, GJ/year'); ax.set_ylim(150,400)
    ax.set_title('Figure 3-1 A century and a half of growth, stopped in one decade')
    save(fig,'fig3-1_us_percapita_break','U.S. EIA, Monthly Energy Review, Table 1.7 (Million Btu per capita, converted at 1.055056 GJ/MMBtu).')


def fig32():
    # 3-2 wind value factor (rebuilt from Hirth 2013 published values; formerly hand-entered approximations
    # for both the value curve and a system-cost index that had no source)
    fig,ax=setup((6.8,3.9))
    # Empirical, German market data (Hirth 2013, Table 3): value factor against wind's market share.
    emp_share=[2,8]; emp_vf=[1.02,0.89]
    # Model results (Hirth 2013, mid-term EMMA): the two penetration levels the paper states explicitly.
    mod_share=[0,30]; mod_vf=[1.10,0.50]
    ax.plot(mod_share,mod_vf,color=INK,lw=1.8,ls=(0,(4,3)),marker='o',ms=4,
     label='Model, published endpoints (0% and 30%)')
    ax.plot(emp_share,emp_vf,color=MID,lw=1.8,marker='s',ms=4,
     label='German market, observed (2001 and 2012)')
    ax.axhline(1.0,color=LIGHT,lw=1)
    ax.annotate('at 30% share, wind earns half\nthe price of a constant source',(30,0.50),
     xytext=(-10,18),textcoords='offset points',fontsize=9,ha='right')
    ax.annotate('share 2% to 8%: value factor falls 13 points',(8,0.89),
     xytext=(10,10),textcoords='offset points',fontsize=9)
    ax.set_xlabel('Wind share of generation, %'); ax.set_ylabel('Value factor (1.0 = average price)')
    ax.set_ylim(0.3,1.3); ax.set_xlim(-1,34); ax.legend(loc='lower left',bbox_to_anchor=(0.02,0.02))
    ax.set_title('Figure 3-2 The more it generates, the less its output is worth')
    save(fig,'fig3-2_vre_value_system_cost','Hirth (2013), Energy Economics 38, Table 3 and the mid-term EMMA results.',
     'Only the values stated in the source are plotted. System costs at high VRE shares are treated in the text (OECD-NEA 2019).')


# ============================================================== Figure 3-3 ===
# Negative wholesale prices in Germany -- one mark per hour.
def fig33():
    yrs = [(2015, 126), (2017, 146), (2019, 211), (2020, 298), (2021, 139),
           (2022, 69), (2023, 301), (2024, 457), (2025, 573)]
    PER = 50
    fig, ax = blank((6.6, 6.4))
    top = 0.0
    ticks = []
    for y, n in yrs:
        rows = int(np.ceil(n / PER))
        c = INK if y >= 2024 else ('#8a8a8a' if y == 2023 else LIGHT)
        for i in range(n):
            cx, cy = i % PER, i // PER
            ax.add_patch(mp.Rectangle((cx, -(top + cy) - 0.82), 0.78, 0.78,
                                      facecolor=c, edgecolor='none'))
        ticks.append((y, n, -(top + rows / 2.0) - 0.4))
        top += rows + 1.25
    for y, n, yy in ticks:
        ax.text(-2.5, yy, str(y), fontsize=9.5, ha='right', va='center', color=INK)
        ax.text(PER + 2.5, yy, f'{n} h', fontsize=9, ha='left', va='center', color=MID)
    ax.set_xlim(-13, PER + 11)
    ax.set_ylim(-top - 2.0, 6.4)
    ax.set_aspect('equal')
    ax.text(-13, 3.4, 'one square = one hour in which German wholesale power sold below zero;\neach row is 50 hours',
            fontsize=9, color=MID, va='center', ha='left', linespacing=1.4)
    ax.set_title('Figure 3-3 When electricity costs less than nothing')
    save(fig, 'fig3-3_germany_negative_prices',
         'Bundesnetzagentur / SMARD; Bloomberg (2026); Montel.',
         'Congestion management cost EUR 3.3bn in 2023, passed through to consumers as network charges.')


def fig34():
    # 3-4 research productivity (rebuilt from the rates and endpoint factors published in Bloom et al. 2020;
    # formerly a single invented exponential with a 13-year halving)
    fig,ax=setup((6.6,3.8))
    y=np.arange(1970,2015)
    series=[('Semiconductors (Moore\'s law)',0.058,1971,2014,INK,1.8),
            ('Pharmaceuticals (new molecular entities)',0.035,1970,2014,MID,1.4),
            ('US agriculture',0.027,1970,2007,MID,1.2)]
    for lab,rate,y0,y1,c,lw in series:
     yy=np.arange(y0,y1+1)
     v=100*(1-rate)**(yy-y0)
     ax.semilogy(yy,v,color=c,lw=lw)
     ax.annotate(lab+'\n%.1f%% a year'%(rate*100),(yy[-1],v[-1]),xytext=(6,0),
      textcoords='offset points',fontsize=8.5,va='center',color=c)
    ax.set_ylabel('Research productivity, index (log, start = 100)')
    ax.set_xlim(1969,2030); ax.set_ylim(3,140)
    ax.annexpl=None
    ax.annotate('to hold Moore\'s law, 18 times the researchers of the early 1970s',(1990,12),fontsize=9,color=MID)
    ax.set_title('Figure 3-4 Ideas are getting harder to find')
    save(fig,'fig3-4_research_productivity','Bloom, Jones, Van Reenen & Webb (2020), American Economic Review 110(4), and its data appendix.',
     'Each line is drawn at the average annual rate of decline the paper reports for that sector, not at an assumed rate.')


# ============================================================== Figure 4-1 ===
# What got cheaper and what did not -- slope chart.
def fig41():
    items = [('Hospital services', 212), ('College tuition', 170), ('Childcare', 110),
             ('Housing', 95), ('Average (CPI)', 85), ('New cars', 25), ('Clothing', -5),
             ('Software', -70), ('Toys', -75), ('Televisions', -97)]
    fig, ax = setup((7.2, 5.4))
    x0, x1 = 0.0, 1.0
    ax.set_yscale('log')
    ax.set_ylim(2.0, 460); ax.set_xlim(-0.34, 1.86)

    # de-collide the right-hand labels in log space
    ends = [(nm, pc, 100 * (1 + pc / 100)) for nm, pc in items]
    ly = [np.log10(v) for _, _, v in ends]
    MIN = 0.088
    for _ in range(600):
        moved = False
        for k in range(len(ly) - 1):
            d = ly[k] - ly[k + 1]
            if d < MIN:
                sh = (MIN - d) / 2
                ly[k] += sh; ly[k + 1] -= sh; moved = True
        if not moved:
            break

    for (nm, pc, v), lyk in zip(ends, ly):
        heavy = pc >= 85
        c = INK if heavy else (MID if pc > 0 else LIGHT)
        lw = 2.0 if heavy else 1.2
        ax.plot([x0, x1], [100, v], color=c, lw=lw, solid_capstyle='round',
                zorder=5 if heavy else 3)
        ax.scatter([x1], [v], color=c, s=20, zorder=6)
        ty = 10 ** lyk
        ax.plot([x1 + 0.02, x1 + 0.10], [v, ty], color=c, lw=0.6, zorder=3)
        ax.annotate(f'{nm}  {pc:+d}%', (x1 + 0.12, ty), fontsize=9, va='center', color=c)
    ax.scatter([x0], [100], color=INK, s=24, zorder=6)
    ax.annotate('2000 = 100', (x0, 100), xytext=(-8, 0), textcoords='offset points',
                fontsize=9.5, ha='right', va='center')
    ax.axhline(100, color=LIGHT, lw=0.9, zorder=1)
    ax.set_yticks([3, 10, 30, 100, 300])
    ax.set_yticklabels(['3', '10', '30', '100', '300'])
    ax.set_ylabel('Price index, 2000 = 100 (log)')
    ax.set_xticks([x0, x1]); ax.set_xticklabels(['2000', '2024'])
    ax.grid(axis='x', visible=False)
    ax.annotate('the basket a child is bought from', (0.44, 300), fontsize=9.5,
                ha='center', color=INK,
                bbox=dict(boxstyle='round,pad=0.16', facecolor='white', edgecolor='none'))
    ax.annotate('what automation reached', (0.50, 3.4), fontsize=9.5, ha='center', color=MID)
    ax.set_title('Figure 4-1 What got cheaper, and what did not')
    save(fig, 'fig4-1_price_divergence',
         'US Bureau of Labor Statistics, consumer price data, 2000-2024.',
         'Log scale, so equal slopes are equal rates of change. Baumol sectors rise; automated goods collapse. '
         'Label positions on the right are spread for legibility; the line ends are exact.')


# ============================================================== Figure 4-2 ===
# The world's fertility distribution sliding across replacement -- ridgeline.
def fig42():
    T = {r['iso']: r for r in csv.DictReader(open('data_tfr_panel.csv'))}
    P = {r['iso']: r for r in csv.DictReader(open('data_pop_panel.csv'))}
    years = [1960, 1975, 1990, 2005, 2024]
    grid = np.linspace(0.3, 8.6, 400)

    fig, ax = setup((7.2, 5.0))
    step = 1.0
    for i, y in enumerate(years):
        s, w = [], []
        for iso in T:
            t = T[iso].get(str(y), '')
            p = P.get(iso, {}).get(str(y), '')
            if t == '' or p == '':
                continue
            s.append(float(t)); w.append(float(p))
        s, w = np.array(s), np.array(w)
        dens = charts.kde(s, w, grid, bw=0.38)
        dens = dens / dens.max() * 0.86
        base = (len(years) - 1 - i) * step
        shade = ['#fafafa', '#f2f2f2', '#e8e8e8', '#dcdcdc', '#cfcfcf'][i]
        ax.fill_between(grid, base, base + dens, color='white', zorder=10 + i)
        ax.fill_between(grid, base, base + dens, color=shade, zorder=10 + i)
        ax.plot(grid, base + dens, color=INK, lw=1.5, zorder=10 + i)
        ax.plot([grid[0], grid[-1]], [base, base], color=LIGHT, lw=0.8, zorder=10 + i)
        below = w[s < 2.1].sum() / w.sum() * 100
        ax.text(8.55, base + 0.06, str(y), fontsize=11.5, ha='right', va='bottom', zorder=40)
        ax.text(8.55, base + 0.40, f'{below:.0f}% of humanity\nbelow replacement',
                fontsize=8.4, ha='right', va='bottom', color=MID, zorder=40,
                bbox=dict(boxstyle='round,pad=0.10', facecolor='white', edgecolor='none'))

    ax.axvline(2.1, color=INK, lw=1.0, ls=(0, (3, 3)), zorder=30)
    ax.text(2.05, len(years) * step - 0.10, 'replacement, 2.1', fontsize=9,
            ha='right', va='top', color=INK, zorder=40)
    ax.set_xlim(0.3, 8.6); ax.set_ylim(-0.12, len(years) * step + 0.10)
    ax.set_yticks([]); ax.grid(False)
    ax.spines['left'].set_visible(False)
    ax.set_xlabel('Total fertility rate, births per woman')
    ax.set_title('Figure 4-2 The whole distribution moved: world fertility, 1960-2024')
    save(fig, 'fig4-2_tfr_distribution',
         'World Bank Open Data (SP.DYN.TFRT.IN and SP.POP.TOTL), 217 countries, retrieved 2026.',
         'Each ridge is the population-weighted distribution of national fertility in that year. '
         'The share of humanity living in a below-replacement country went from 3.9% to 67.4%.')


def fig43():
    # 4-3 Korea (cumulative spending rebuilt from published anchor points; formerly a hand-entered linear ramp)
    fig,ax=setup((6.8,3.8))
    y=list(range(2006,2026))
    tfr=[1.13,1.25,1.19,1.15,1.23,1.24,1.30,1.19,1.21,1.24,1.17,1.05,0.98,0.92,0.84,0.81,0.78,0.72,0.75,0.80]
    # Only cumulative totals are published: 280 trillion won by 2021, over 360 (362) trillion by 2023.
    anchor_y=[2006,2021,2023]; anchor_v=[0,280,362]
    cum=np.interp(y,anchor_y,anchor_v,right=362)
    ax.plot(y,tfr,color=INK,lw=2); ax.set_ylabel('Total fertility rate'); ax.set_ylim(0,1.5)
    a2=ax.twinx(); a2.fill_between(y,0,cum,color=FAINT,zorder=0)
    a2.scatter(anchor_y[1:],anchor_v[1:],color=MID,s=20,zorder=3)
    a2.set_ylabel('Cumulative spending, trillion won',color=MID)
    for s2 in ('top','right','left'): a2.spines[s2].set_visible(False)
    a2.tick_params(length=0); a2.grid(False); a2.set_ylim(0,520)
    ax.set_zorder(a2.get_zorder()+1); ax.patch.set_visible(False)
    ax.annotate('280tn won by 2021, over 360tn by 2023',(2018,0.98),xytext=(-8,-34),textcoords='offset points',fontsize=9,ha='right')
    ax.annotate('the 2024-25 uptick is small and contested;\nthis book does not read a mechanism into it',(2019.5,0.30),fontsize=8.5,ha='center',color=MID)
    ax.annotate('0.72 in 2023',(2023,0.72),xytext=(6,16),textcoords='offset points',fontsize=9,ha='left',
      bbox=dict(boxstyle='round,pad=0.15',facecolor='white',edgecolor='none'))
    ax.set_xticks([2006,2010,2014,2018,2022,2025])
    ax.set_xticklabels(['2006','2010','2014','2018','2022','2025'])
    ax.set_title('Figure 4-3 South Korea: money spent, and what it bought')
    save(fig,'fig4-3_korea_spend_tfr','Statistics Korea (TFR); cumulative low-fertility spending as published (280tn won to 2021; over 360tn to 2023).',
     'Only the published cumulative totals are marked; the shaded area interpolates between them.')


def fig44():
    # ---- Fig 4-4 China births, observed + projection
    fig,ax=setup((7.4,4.3))
    ys=sorted(B); ax.plot(ys,[B[y]/1000 for y in ys],color=INK,lw=1.9,label='Observed')
    py=[2025]+sorted(A); 
    ax.plot(py,[B[2025]/1000]+[A[y]/1000 for y in sorted(A)],color=INK,lw=1.6,ls=(0,(4,3)),label='Projection, TFR held at 0.93')
    ax.plot(py,[B[2025]/1000]+[Bs[y]/1000 for y in sorted(Bs)],color=MID,lw=1.4,ls=(0,(1.5,2.5)),label='Projection, TFR drifts to 0.75')
    ax.fill_between(sorted(A),[Bs[y]/1000 for y in sorted(A)],[A[y]/1000 for y in sorted(A)],color=FAINT,zorder=0)
    ax.annotate('20.7M (1996)\nthe mothers of 2025',(1996,20.67),xytext=(6,10),textcoords='offset points',fontsize=8.5)
    ax.annotate('7.92M (2025)\nlowest since 1949',(2025,7.92),xytext=(-6,28),textcoords='offset points',fontsize=8.5,ha='right',
     bbox=dict(boxstyle='round,pad=0.15',facecolor='white',edgecolor='none'))
    ax.annotate('plateau of roughly 5–6.5M\nthrough the 2040s',(2042,6.4),xytext=(0,34),textcoords='offset points',fontsize=8.5,ha='center',
     bbox=dict(boxstyle='round,pad=0.15',facecolor='white',edgecolor='none'))
    ax.annotate('then halving again',(2058,3.1),xytext=(-4,34),textcoords='offset points',fontsize=8.5,ha='right',
     bbox=dict(boxstyle='round,pad=0.15',facecolor='white',edgecolor='none'))
    ax.set_ylabel('Annual births, millions'); ax.set_xlim(1970,2061); ax.set_ylim(0,29)
    ax.set_title('Figure 4-4 China: annual births, 1970–2025 and projected to 2060')
    ax.legend(loc='lower left',bbox_to_anchor=(0.0,0.02))
    save(fig,'fig4-4_china_births','Observed: National Bureau of Statistics of China. Projection: author, cohort-component model.',
     'Projection applies an age-specific fertility schedule (mean age at childbearing 29.7, drifting to 30.5) to female cohorts already born, calibrated to the 2025 outturn.')


def fig45():
    # ---- Fig 4-5 women 20-34
    fig,ax=setup((6.6,3.7))
    yy=list(range(2025,2056))
    def w2034(y): return sum(cm.women(a,y) for a in range(20,35))/1000
    vals=[w2034(y) for y in yy]
    ax.fill_between(yy,0,vals,color=FAINT); ax.plot(yy,vals,color=INK,lw=2)
    ax.scatter([2025,2050],[vals[0],vals[25]],color=INK,s=24,zorder=5)
    ax.annotate(f'{vals[0]:.0f}M',(2025,vals[0]),xytext=(8,8),textcoords='offset points',fontsize=9.5)
    ax.annotate(f'{vals[25]:.0f}M',(2050,vals[25]),xytext=(-8,16),textcoords='offset points',fontsize=9.5,ha='right',
     bbox=dict(boxstyle='round,pad=0.15',facecolor='white',edgecolor='none'))
    ax.set_ylabel('Women aged 20–34, millions'); ax.set_ylim(0,130)
    ax.set_title('Figure 4-5 China: women of peak childbearing age, already determined')
    save(fig,'fig4-5_china_women','Derived from NBS birth series and census sex ratios.',
     'Every woman in this chart has already been born. The decline is arithmetic, not forecast.')


# ============================================================== Figure 4-6 ===
# Where the world's children are born, 2024 -- two-level Voronoi treemap.
REGION_ORDER = ['Sub-Saharan Africa', 'South Asia', 'East Asia & Pacific',
                'Middle East, North Africa, Afghanistan & Pakistan',
                'Latin America & Caribbean', 'Europe & Central Asia', 'North America']
REGION_SHORT = {'Sub-Saharan Africa': 'Sub-Saharan Africa', 'South Asia': 'South Asia',
                'East Asia & Pacific': 'East Asia & Pacific',
                'Middle East, North Africa, Afghanistan & Pakistan': 'M. East, N. Africa, Afg., Pak.',
                'Latin America & Caribbean': 'Latin America & Caribbean',
                'Europe & Central Asia': 'Europe & Central Asia', 'North America': 'North America'}
NAME = {'Congo, Dem. Rep.': 'DR Congo', 'Egypt, Arab Rep.': 'Egypt',
        'Iran, Islamic Rep.': 'Iran', 'Yemen, Rep.': 'Yemen',
        'Russian Federation': 'Russia', 'Viet Nam': 'Vietnam',
        'Korea, Rep.': 'South Korea', "Cote d'Ivoire": "Cote d'Ivoire",
        'Turkiye': 'Turkiye', 'United Kingdom': 'UK',
        'Venezuela, RB': 'Venezuela', 'Syrian Arab Republic': 'Syria'}


def fig46():
    rows = [r for r in csv.DictReader(
        l for l in open('data_worldbank_fertility_latest.csv') if not l.startswith('#'))]
    rows = [r for r in rows if r['births_est']]
    total = sum(int(r['births_est']) for r in rows)

    groups = {k: [] for k in REGION_ORDER}
    for r in rows:
        groups[r['region']].append((r['country'], int(r['births_est'])))
    reg_tot = {k: sum(v for _, v in g) for k, g in groups.items()}

    fig, ax = blank((7.2, 7.9))
    outer = charts.circle_boundary(r=1.0, n=220)
    ang = np.linspace(0, 2 * np.pi, len(REGION_ORDER), endpoint=False) + 0.55
    seed = np.c_[0.45 * np.cos(ang), 0.45 * np.sin(ang)]
    rcells = charts.voronoi_treemap([reg_tot[k] for k in REGION_ORDER], outer,
                                    iters=320, seed=11, sites=seed)

    ax.set_xlim(-1.06, 1.06); ax.set_ylim(-1.06, 1.40)
    placed = []
    for gi, (k, cell) in enumerate(zip(REGION_ORDER, rcells)):
        g = sorted(groups[k], key=lambda x: -x[1])
        # name the largest countries, but never so many that the cells vanish
        cap = max(2, min(8, int(round(reg_tot[k] / total * 26))))
        named = [c for c in g[:cap] if c[1] >= 0.006 * total]
        if not named:
            named = g[:1]
        rest = [c for c in g if c not in named]
        items = [(NAME.get(c, c), v) for c, v in named]
        if rest:
            items.append((f'{len(rest)} other\ncountries|{len(rest)} others', sum(v for _, v in rest)))
        base = GREYS[gi]
        ccells = [cell] if len(items) == 1 else charts.voronoi_treemap(
            [v for _, v in items], cell, iters=280, seed=31 + gi)
        for (nm, v), cc in zip(items, ccells):
            if len(cc) < 3:
                continue
            ax.add_patch(mp.Polygon(cc, closed=True, facecolor=base,
                                    edgecolor='white', lw=0.85, zorder=2))
            placed.append((nm, v, cc, gi))
        ax.add_patch(mp.Polygon(cell, closed=True, fill=False,
                                edgecolor='white', lw=2.6, zorder=6))

    # labels last, once the axes limits are final, so the fit test is exact
    for nm, v, cc, gi in placed:
        cen = charts._poly_centroid(cc)
        tc = 'white' if gi <= 2 else INK
        m = v / 1e6
        long, _, short = nm.partition('|')
        short = short or long
        cands = [f'{long}\n{m:.2f}M', long, short]
        charts.fit_label(ax, cc, cen[0], cen[1], cands, tc, max_fs=13.0, min_fs=5.2)

    # legend: one compact block above the circle
    ax.text(-1.04, 1.36, 'Region, share of world births', fontsize=9, color=MID, va='top')
    for gi, k in enumerate(REGION_ORDER):
        col = gi // 4
        row = gi % 4
        x = -1.04 + col * 1.06
        y = 1.26 - row * 0.075
        ax.add_patch(mp.Rectangle((x, y - 0.026), 0.055, 0.052,
                                  facecolor=GREYS[gi], edgecolor='none', zorder=8))
        ax.text(x + 0.075, y, f'{REGION_SHORT[k]}  {reg_tot[k]/total*100:.1f}%',
                fontsize=8.2, va='center', color=INK, zorder=8)
    ax.set_title("Figure 4-6 Where the world's children are born, 2024")
    save(fig, 'fig4-6_world_births',
         'World Bank Open Data, crude birth rate x population, 2024; 132.3M births across 217 countries.',
         "Voronoi treemap: every cell's area is proportional to that country's births, and every region's area to its share. "
         "Smaller countries are pooled inside their region. Sub-Saharan Africa and South Asia together hold more than half. "
         "China's own registration figure for 2025 is lower still, at 7.92M.")


# ============================================================== Figure 5-1 ===
# Two centuries of light: price collapses, spending share does not move.
def fig51():
    fig, (a1, a2) = panels((7.6, 4.0), 2, wr=[1.25, 1])
    y = [1800, 1850, 1900, 1950, 1992]
    p = [785, 180, 20, 1.5, 0.23]
    a1.semilogy(y, p, color=INK, lw=2.0, marker='o', ms=4)
    a1.set_ylabel('Price per 1,000 lumen-hours, 2018 USD (log)')
    a1.set_ylim(0.1, 2000)
    a1.annotate('a fall of 99.97%', (1900, 20), xytext=(12, 22),
                textcoords='offset points', fontsize=9.5)
    a1.annotate('$785', (1800, 785), xytext=(8, 6), textcoords='offset points', fontsize=8.8, color=MID)
    a1.annotate('$0.23', (1992, 0.23), xytext=(-6, 12), textcoords='offset points',
                fontsize=8.8, ha='right', color=MID)
    a1.set_xlim(1780, 2010)
    a1.set_title('The price of light fell by a factor of three thousand', loc='left',
                 fontsize=11, pad=10)
    a1.grid(color=FAINT, lw=0.9); a1.set_axisbelow(True)

    pts = [('United Kingdom\n1700', 0.72), ('World, off grid\n1999', 0.72),
           ('World, on grid\n2005', 0.72)]
    x = np.arange(len(pts))
    a2.fill_between([-0.6, 2.6], 0, [0.72, 0.72], color=FAINT)
    a2.plot([-0.6, 2.6], [0.72, 0.72], color=INK, lw=1.6)
    a2.scatter(x, [v for _, v in pts], color=INK, s=52, zorder=5)
    a2.set_xticks(x); a2.set_xticklabels([l for l, _ in pts], fontsize=8.6)
    a2.set_ylim(0, 1.55); a2.set_xlim(-0.6, 2.6)
    a2.set_ylabel('Spending on light, % of GDP')
    a2.annotate('0.72% of GDP in all three', (1, 0.72), xytext=(0, 16),
                textcoords='offset points', fontsize=9.5, ha='center')
    a2.annotate('the saving was never taken;\nit was spent on more light',
                (1, 0.26), fontsize=9, ha='center', color=MID)
    a2.set_title('The share of income spent on it did not move', loc='left',
                 fontsize=11, pad=10)
    a2.grid(axis='y', color=FAINT, lw=0.9); a2.set_axisbelow(True)

    fig.suptitle('Figure 5-1 Three centuries of light: the purest case of the cascade',
                 x=0.005, y=1.02, ha='left', fontsize=12.5)
    save(fig, 'fig5-1_price_of_light',
         'Left: Nordhaus (1996), in The Economics of New Goods. Right: Tsao et al. (2010), J. Phys. D 43(35), 354001.',
         'The three points on the right are the independent empirical settings the paper reports, three centuries apart, '
         'from tallow candles to grid electricity.')


# ============================================================== Figure 5-3 ===
# Launch cost: how many orders of magnitude have actually been crossed.
def fig52():
    steps = [('Space Shuttle', 54000, 'reusable, and not cheap'),
             ('Falcon 9', 2700, 'reuse, actually achieved'),
             ('Falcon Heavy', 1500, ''),
             ('Starship', 100, 'target, not yet demonstrated')]
    fig, ax = setup((6.8, 4.6))
    xs = np.arange(len(steps))
    ys = [v for _, v, _ in steps]
    for k in range(len(steps) - 1):
        st = '-' if k < 2 else (0, (4, 3))
        ax.plot([xs[k], xs[k + 1]], [ys[k], ys[k]], color=INK, lw=1.7, ls=st, zorder=4)
        ax.plot([xs[k + 1], xs[k + 1]], [ys[k], ys[k + 1]], color=INK, lw=1.7, ls=st, zorder=4)
    ax.scatter(xs[:3], ys[:3], color=INK, s=42, zorder=6)
    ax.scatter(xs[3:], ys[3:], facecolor='white', edgecolor=INK, s=50, lw=1.6, zorder=6)
    offs = [(6, -30), (8, -30), (8, 16), (-8, -34)]
    has = ['left', 'left', 'left', 'right']
    for k, (nm, v, note) in enumerate(steps):
        ax.annotate(f'{nm}\n${v:,}/kg' + (f'\n{note}' if note else ''),
                    (xs[k], v), xytext=offs[k], textcoords='offset points',
                    fontsize=9, ha=has[k], linespacing=1.3, zorder=8,
                    bbox=dict(boxstyle='round,pad=0.16', facecolor='white', edgecolor='none'))
    ax.set_yscale('log'); ax.set_ylim(55, 130000)
    ax.set_xlim(-0.30, 3.55)
    ax.set_xticks([]); ax.grid(axis='x', visible=False)
    ax.set_yticks([100, 1000, 10000, 100000])
    ax.set_yticklabels(['$100', '$1,000', '$10,000', '$100,000'])
    ax.set_ylabel('Cost to low Earth orbit, USD per kg (log)')
    ax.text(3.42, 42000,
            'Shuttle to Falcon 9\nis a factor of twenty.\n\nFalcon 9 to the Starship\ntarget is another\nfactor of twenty-seven.\n\nThe first has happened.\nThe second has not.',
            fontsize=9, ha='right', va='top', color=INK, linespacing=1.5)
    ax.set_title('Figure 5-2 Orbit: how many orders of magnitude have actually been crossed')
    save(fig, 'fig5-2_launch_costs',
         'Jones (2018), ICES-2018-81; CSIS Aerospace Security; published vehicle targets.',
         'Solid steps have flown and been priced. The dashed step is a target, not an achievement. '
         'Complete the third order of magnitude and orbit becomes an industrial location rather than a mission.')


def fig53():
    # ---- Fig 5-3 solar learning (replaced with OWID/IRENA actuals; formerly a synthetic power-law curve)
    # Our World in Data, "Solar (photovoltaic) panel prices vs. cumulative capacity" (CC BY 4.0).
    # year, module price (USD per watt), cumulative installed capacity (MW)
    SOLAR=[(1975,128.269,0.54),(1976,96.508,1.08),(1977,70.407,2.16),(1978,49.813,3.51),
    (1979,41.855,5.235),(1980,35.469,7.965),(1981,28.358,12.88),(1982,25.479,19.405),
    (1983,20.570,29.255),(1984,19.113,46.705),(1985,16.686,66.455),(1986,13.803,89.155),
    (1987,11.735,113.655),(1988,10.961,140.6),(1989,11.327,173.35),(1990,11.716,212.3),
    (1991,10.853,257.15),(1992,10.111,309.05),(1993,9.456,365.9),(1994,8.945,423.75),
    (1995,8.271,489.25),(1996,7.732,565.0),(1997,7.705,650.8),(1998,6.943,771.0),
    (1999,6.414,914.5),(2000,6.294,1103.0),(2001,6.089,1373.0),(2002,5.569,1738.5),
    (2003,5.294,2229.2),(2004,4.555,2915.3),(2005,4.604,4390.3),(2006,5.019,5911.6),
    (2007,5.056,8265.9),(2008,4.608,14444.9),(2009,3.080,22483.4),(2010,2.443,39732.8),
    (2011,2.005,70189.3),(2012,1.080,99017.2),(2013,0.833,134040.2),(2014,0.769,172168.7),
    (2015,0.716,219262.0),(2016,0.662,290561.2),(2017,0.556,384045.1),(2018,0.495,477686.5),
    (2019,0.454,578978.2),(2020,0.360,709092.7),(2021,0.323,851793.5),(2022,0.356,1044311.4),
    (2023,0.313,1400622.0),(2024,0.258,1852358.9)]
    fig,ax=setup((6.4,4.0))
    cap=np.array([r[2] for r in SOLAR]); pr=np.array([r[1] for r in SOLAR])
    ax.loglog(cap,pr,color=INK,lw=1.6,marker='o',ms=2.6)
    # learning rate from the data itself: price ratio per doubling of cumulative capacity
    b,_=np.polyfit(np.log2(cap),np.log2(pr),1)
    lr=(1-2**b)*100
    ax.annotate('learning rate %.0f%% over the whole record:\neach doubling of cumulative capacity\ntakes about a fifth off the price'%lr,
     (cap[25],pr[25]),xytext=(30,26),textcoords='offset points',fontsize=9.5)
    for i,t in ((0,'1975'),(len(SOLAR)-1,'2024')):
     ax.annotate(t+'\n$%.2f/W'%pr[i],(cap[i],pr[i]),xytext=(10,-18) if i==0 else (-10,20),
      textcoords='offset points',fontsize=9,ha='left' if i==0 else 'right',
      bbox=dict(boxstyle='round,pad=0.16',facecolor='white',edgecolor='none'))
    ax.set_xlabel('Cumulative installed capacity, MW (log)'); ax.set_ylabel('Module price, USD per watt (log)')
    ax.set_title('Figure 5-3 Wright\'s law in solar modules, 1975-2024')
    save(fig,'fig5-3_solar_learning','Our World in Data, solar PV prices vs. cumulative capacity (CC BY 4.0); IRENA.',
     'Observed series, not a fitted curve. The learning rate is estimated from these points.')


def fig54():

    # ---- Fig 5-4 the four headcounts: when does a birth arrive in each role?
    # Ridgeline of arrival ramps. NTA US 2011 per-capita age profiles (consumption,
    # labour income, net public transfers); Azoulay, Jones, Kim & Miranda (2020) for founders.
    fig,ax=setup((7.0,5.0))
    a=np.arange(0,71)

    def ramp(pts):
        x=[p[0] for p in pts]; y=[p[1] for p in pts]
        return np.interp(a,x,y)

    # per-capita consumption relative to the 20-64 mean (NTA US 2011)
    demand = ramp([(0,0.44),(2,0.46),(7,0.74),(12,0.84),(17,0.95),(22,0.95),
                   (30,1.00),(50,1.03),(67,1.35),(70,1.40)])
    # per-capita labour income as a share of its own peak (NTA US 2011)
    labour = ramp([(0,0.0),(15,0.03),(22,0.27),(26,0.50),(29,0.62),(34,0.80),
                   (44,0.97),(49,1.00),(57,0.88),(62,0.71),(67,0.41),(70,0.30)])
    # net public transfers, share of prime-age labour income (NTA US 2011): negative early
    fiscal = ramp([(0,-0.14),(3,-0.20),(7,-0.33),(12,-0.32),(17,-0.29),(21,-0.16),
                   (26,0.0),(32,0.14),(40,0.24),(50,0.30),(59,0.24),(64,0.05),
                   (66,-0.30),(70,-0.55)])
    # founder intensity: share of top-0.1%-growth firms founded at each age, scaled to peak
    founder = ramp([(0,0.0),(22,0.02),(25,0.14),(30,0.42),(35,0.62),(40,0.86),
                    (45,1.00),(50,0.96),(55,0.82),(60,0.66),(65,0.34),(70,0.16)])

    rows=[('Demand','arrives at birth, at 44% of an adult',demand,None,0),
          ('Labour supply','half of peak earnings at 26',labour,26,1),
          ('Net taxpayer','negative until 26, peak at 50',fiscal,26,2),
          ('Risk-taker','top-0.1% founders average 45',founder,45,3)]

    step=1.30
    AMP=0.80
    for lab,sub,v,mark,i in rows:
        base=(len(rows)-1-i)*step
        vv=np.clip(v,-1,1.6)
        pos=np.maximum(vv,0); neg=np.minimum(vv,0)
        ax.fill_between(a,base,base+pos*AMP,color=INK,alpha=0.13,lw=0)
        ax.fill_between(a,base,base+neg*AMP,color=INK,alpha=0.32,lw=0)
        ax.plot(a,base+vv*AMP,color=INK,lw=1.5)
        ax.axhline(base,color=LIGHT,lw=0.8,zorder=0)
        ax.text(-2.5,base+0.34,lab,ha='right',va='center',fontsize=10.5)
        ax.text(-2.5,base+0.13,sub,ha='right',va='center',fontsize=8.4,color=MID)
        if mark is not None:
            j=int(mark)
            ax.plot([mark],[base+vv[j]*AMP],'o',ms=4,color=INK,zorder=6)
            ax.annotate(str(mark),(mark,base+vv[j]*AMP),xytext=(0,7),
                        textcoords='offset points',fontsize=9,ha='center')
    for x in (26,45):
        ax.axvline(x,color=MID,lw=0.7,ls=(0,(3,3)),zorder=0)
    ax.set_xlim(-24,73); ax.set_ylim(-0.62,(len(rows)-1)*step+1.22)
    ax.set_yticks([]); ax.set_xticks([0,10,20,26,30,40,45,50,60,70])
    ax.set_xlabel('Years since birth')
    ax.grid(False)
    ax.spines['left'].set_visible(False)
    ax.set_title('Figure 5-4 The four headcounts do not return at the same speed')
    save(fig,'fig5-4_four_headcounts',
     'National Transfer Accounts, United States 2011 per-capita age profiles; Azoulay, Jones, Kim & Miranda (2020).',
     'Each band shows the level reached by that age, relative to its own peak. Demand alone starts at the origin; the fiscal band is below the line until 26.')


def fig61():
    # ---- Fig 6-1 labour share (replaced with Penn World Table actuals; formerly a synthetic curve with added noise)
    fig,ax=setup((6.6,3.6))
    y=list(range(1975,2024))
    s=[62.56,62.16,62.16,62.23,62.26,62.43,61.42,61.67,60.39,60.2,60.23,60.77,61.6,62.07,61.19,61.52,61.51,62.0,61.42,60.8,60.74,60.71,60.96,62.3,62.59,63.71,64.03,63.01,62.16,61.7,60.56,60.55,60.3,60.15,58.98,58.55,59.02,59.08,58.72,58.83,59.09,58.92,59.13,59.06,59.18,60.56,59.39,57.62,56.83]
    ax.plot(y,s,color=INK,lw=1.8); ax.set_ylabel('Labour share of income, %'); ax.set_ylim(52,68)
    ax.annotate('roughly half of the decline is explained by\nthe falling relative price of capital goods',(2005,58),
     xytext=(0,-30),textcoords='offset points',fontsize=9,ha='center')
    ax.set_title('Figure 6-1 The global decline of the labour share')
    save(fig,'fig6-1_labour_share','Penn World Table 10.01 (FRED series LABSHPUSA156NRUG); Karabarbounis & Neiman (2014), QJE 129(1).',
     'US series shown. Karabarbounis & Neiman document the same downward trend across most countries and industries.')


# ============================================================== Figure 6-3 ===
# The graveyard of the wealth tax -- one lifeline per country.
def fig62():
    # Perret (2021), Fiscal Studies 42(3); OECD (2018) Tax Policy Studies No. 26.
    rows = [('Austria', 1994), ('Denmark', 1997), ('Germany', 1997),
            ('Netherlands', 2001), ('Finland', 2006), ('Iceland', 2006),
            ('Luxembourg', 2006), ('Sweden', 2007), ('France', 2018)]
    alive = ['Norway', 'Spain', 'Switzerland']
    fig, ax = setup((7.2, 4.6))
    y = 0
    labels = []
    for nm, end in rows:
        ax.plot([1990, end], [y, y], color=LIGHT, lw=5.5, solid_capstyle='butt', zorder=2)
        ax.scatter([end], [y], marker='|', color=INK, s=170, lw=1.6, zorder=4)
        ax.text(end + 0.7, y, str(end), fontsize=8.6, va='center', color=INK)
        labels.append(nm); y += 1
    for nm in alive:
        ax.plot([1990, 2026], [y, y], color=INK, lw=5.5, solid_capstyle='butt', zorder=2)
        labels.append(nm); y += 1
    # Iceland's temporary reintroduction, and France's residual property tax
    iy = labels.index('Iceland')
    ax.plot([2010, 2014], [iy, iy], color=LIGHT, lw=5.5, solid_capstyle='butt', zorder=2)
    ax.text(2014.7, iy, 'reintroduced 2010-14', fontsize=7.6, va='center', color=MID)
    fy = labels.index('France')
    ax.text(2018.6, fy + 0.42, 'replaced by a property-only tax', fontsize=7.6,
            va='center', ha='left', color=MID)
    sy = labels.index('Spain')
    ax.text(2027.0, sy, 'suspended 2008, reinstated 2011', fontsize=7.6, va='center', color=MID)
    ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlim(1988, 2042); ax.set_xticks([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
    ax.set_xticklabels(['1990', '1995', '2000', '2005', '2010', '2015', '2020', '2025'])
    ax.grid(axis='y', visible=False)
    ax.set_ylim(len(labels) - 0.4, -0.8)
    ax.annotate('twelve in 1990', (1990, -0.62), fontsize=9.5, ha='left', color=INK)
    ax.annotate('three still standing', (2026, -0.62), fontsize=9.5, ha='right', color=INK)
    ax.set_title('Figure 6-2 The graveyard of the wealth tax')
    save(fig, 'fig6-2_wealth_tax',
         'Perret (2021), Fiscal Studies; OECD (2018), The Role and Design of Net Wealth Taxes in the OECD.',
         'Each bar is one country\'s individual net wealth tax. Black bars are still in force.')


def fig63():
    # 6-4 citizen capital timeline
    fig,ax=setup((9.0,4.0))
    ev=[(1862,'Homestead Act\n270M acres, 1.6M households'),
     (1946,'Japan land reform\n1.74M ha, 4.75M households'),
     (1982,'Alaska Permanent Fund\nuniversal dividend'),
     (1990,'Norway GPFG\ncollective sovereign capital'),
     (2023,'Connecticut\nBaby Bonds'),
     (2025,'Trump Accounts\n$1,000 at birth,\nindex funds')]
    ax.hlines(0,1850,2040,color=LIGHT,lw=1.2)
    # vertical stagger avoids any two adjacent labels sharing the same row
    row=[1,-1,1,-1,1.55,-1.05]
    for i,(yy,t) in enumerate(ev):
     up=row[i]
     ax.vlines(yy,0,up*0.5,color=LIGHT,lw=1)
     ax.scatter([yy],[0],color=INK,s=22,zorder=5)
     ax.annotate(t,(yy,up*0.58),ha='center',va='bottom' if up>0 else 'top',fontsize=7.8)
    ax.set_ylim(-1.9,1.9); ax.set_xlim(1845,2045); ax.set_yticks([]); ax.grid(False)
    ax.spines['left'].set_visible(False); ax.spines['bottom'].set_visible(False)
    ax.set_title('Figure 6-3 Making citizens owners: a lineage')
    save(fig,'fig6-3_citizen_capital','NARA/NPS; Dore (1959); Jones & Marinescu (2022); NBIM; US public law (2025).',
      'The nineteenth century distributed land. The twenty-first must distribute shares in automated capital.')


# ============================================================== Figure 7-1 ===
# The economy the accounts do not see -- proportional circles.
def fig71():
    data = [('Measured GDP', 100.0, 'the part that carries a price', FAINT, INK),
            ('Household\nproduction', 25.0, '23-26% of GDP\n(up to 50% on some\nOECD methods)', '#c2c2c2', INK),
            ('Free digital\ngoods', 9.0, 'consumer surplus of\nabout $48 a month\nfor a single platform', INK, 'white')]
    circles = charts.circle_pack([d[1] for d in data])[::-1]  # circlify returns smallest first
    fig, ax = blank((7.0, 5.4))
    xs = [c.x for c in circles]; ys = [c.y for c in circles]; rs = [c.r for c in circles]
    lo_x = min(x - r for x, r in zip(xs, rs)); hi_x = max(x + r for x, r in zip(xs, rs))
    lo_y = min(y - r for y, r in zip(ys, rs)); hi_y = max(y + r for y, r in zip(ys, rs))
    padx = (hi_x - lo_x) * 0.06
    ax.set_xlim(lo_x - padx, hi_x + padx)
    ax.set_ylim(lo_y - (hi_y - lo_y) * 0.30, hi_y + (hi_y - lo_y) * 0.10)
    for c, (nm, v, note, fc, tc) in zip(circles, data):
        ax.add_patch(plt.Circle((c.x, c.y), c.r, facecolor=fc, edgecolor='white', lw=1.8, zorder=2))
    for c, (nm, v, note, fc, tc) in zip(circles, data):
        big = c.r > 0.30
        if big:
            ax.text(c.x, c.y + c.r * 0.20, nm, ha='center', va='center',
                    fontsize=12.5, color=tc, zorder=5, linespacing=1.05)
            ax.text(c.x, c.y - c.r * 0.28, note, ha='center', va='center',
                    fontsize=8.4, color=tc, zorder=5, linespacing=1.25)
        else:
            th = np.deg2rad(172)
            ex, ey = c.x + c.r * np.cos(th), c.y + c.r * np.sin(th)
            ax.plot([ex, ex - 0.16], [ey, ey], color=MID, lw=0.8, zorder=5)
            ax.text(ex - 0.20, ey, nm.replace('\n', ' ') + '\n' + note,
                    ha='right', va='center', fontsize=8.6, color=INK, zorder=5, linespacing=1.25)
    ax.text((lo_x + hi_x) / 2, lo_y - (hi_y - lo_y) * 0.20,
            'the national accounts see only the pale circle',
            ha='center', fontsize=10, color=MID)
    ax.set_title('Figure 7-1 The economy the accounts do not see')
    save(fig, 'fig7-1_unmeasured_economy',
         'BEA household production satellite account; OECD; Brynjolfsson, Collis & Eggers (2019), PNAS 116(15).',
         'Areas are proportional to the published central estimates. The free-goods circle is drawn at the lower end of the consumer-surplus range.')


# ============================================================== Figure 7-2 ===
# Where a human day goes -- sunburst, inner ring = whether it enters GDP.
def fig72():
    seg = [('Sleep', 8.2), ('Paid work', 4.4), ('Unpaid work', 3.6), ('Leisure', 5.2), ('Other', 2.6)]
    day = sum(v for _, v in seg)
    inner = [('Counted in GDP', 4.4 / day, INK, 'white'),
             ('Not counted', (day - 4.4) / day, FAINT, INK)]
    fills = {'Paid work': INK, 'Sleep': '#ededed', 'Unpaid work': '#b4b4b4',
             'Leisure': '#d6d6d6', 'Other': '#f4f4f4'}
    # order the outer ring so paid work sits directly outside the GDP wedge
    order = ['Paid work', 'Unpaid work', 'Leisure', 'Other', 'Sleep']
    outer = [(k, dict(seg)[k] / day, fills[k], 'white' if fills[k] == INK else INK) for k in order]

    fig, ax = blank((6.6, 5.6))
    ax.set_xlim(-1.42, 1.42); ax.set_ylim(-1.30, 1.32)
    placed = charts.sunburst(ax, [inner, outer], r0=0.20, width=0.40, gap=0.018)
    for li, lab, mid, rmid, tc, span in placed:
        th = np.deg2rad(mid)
        hrs = dict(seg).get(lab)
        t = f'{lab}\n{hrs}h' if hrs else lab
        if span < 26:
            # too narrow for interior text: put it outside with a leader
            x, y = 1.02 * np.cos(th), 1.02 * np.sin(th)
            ha = 'left' if np.cos(th) >= 0 else 'right'
            ax.plot([0.86 * np.cos(th), 0.99 * np.cos(th)],
                    [0.86 * np.sin(th), 0.99 * np.sin(th)], color=MID, lw=0.7)
            ax.text(x + (0.03 if ha == 'left' else -0.03), y, t.replace('\n', ' '),
                    fontsize=8.4, ha=ha, va='center', color=INK)
        else:
            rr = rmid if li else rmid * 0.99
            ax.text(rr * np.cos(th), rr * np.sin(th), t, ha='center', va='center',
                    fontsize=9.6 if li else 8.8, color=tc, linespacing=1.1)
    ax.text(0, 0, '24h', ha='center', va='center', fontsize=11, color=INK)
    ax.set_title('Figure 7-2 Where a human day actually goes')
    save(fig, 'fig7-2_time_use', 'OECD Time Use Database, adult population averages.',
         'Inner ring: only paid work enters the national accounts. Cross-country variation is substantial.')


# ============================================================== Figure 8-1 ===
# The terms of the equation, and which cluster holds which -- bipartite chord.
def fig81():
    AXES = [('Institutions (I)', 'property, protection, permits, visas', 'I'),
            ('Energy abundance (E)', 'power drawn without watching the meter', 'E'),
            ('Deep tech: bits (T_1)', 'models, research, data, EDA, design IP', 'T1'),
            ('Deep tech: physical (T_2)',
             'materials, equipment, logic, memory, robots', 'T2'),
            ('Large capital (K)', 'balance moved by one decision', 'K')]
    KEYS = [k for _, _, k in AXES]
    LABEL = {k: l for l, _, k in AXES}
    ASUB = {k: sub for _, sub, k in AXES}
    CLUSTERS = [('United States (Bay Area, Texas, and BosWash)',
                 'models, capital, power, land, finance', 'US'),
                ('UAE', 'power, capital, speed of decision', 'US'),
                ('Northeast Asia (Japan-Korea-Taiwan)',
                 'equipment, materials, memory, logic, robots', 'US'),
                ('England (Loxbridge)', 'basic research, talent', 'US'),
                ('China (Yangtze Delta and GBA)',
                 'hardware, models, power, capital', 'CN'),
                ('India (Bengaluru-Hyderabad)', 'software services, talent pool, capital', 'IN')]
    LINKS = {
        'United States (Bay Area, Texas, and BosWash)':
            {'I': 5.0, 'E': 2.5, 'T1': 5.0, 'T2': 1.5, 'K': 5.0},
        'UAE':                                     {'I': 2.0, 'E': 3.0, 'K': 2.0},
        'Northeast Asia (Japan-Korea-Taiwan)':
                                                   {'I': 1.5, 'T2': 4.5},
        'England (Loxbridge)':                     {'I': 1.5, 'T1': 1.0},
        'China (Yangtze Delta and GBA)':
            {'E': 4.5, 'T1': 3.5, 'T2': 4.0, 'K': 2.5},
        'India (Bengaluru-Hyderabad)':         {'T1': 0.5, 'K': 0.5},
    }
    BLOC = {'US': '#d2d2d2', 'CN': '#242424', 'IN': '#8a8a8a'}
    names = [c for c, _, _ in CLUSTERS]
    ax_tot = {k: sum(LINKS[c].get(k, 0) for c in names) for k in KEYS}
    clu_tot = {c: sum(LINKS[c].values()) for c in names}
    grand = sum(ax_tot.values())

    R, RW, GAP = 1.0, 0.052, np.deg2rad(2.4)
    L0, L1 = np.deg2rad(100), np.deg2rad(260)
    span_L = (L1 - L0) - GAP * (len(KEYS) - 1)
    lp, t = {}, L0
    for k in KEYS:
        w = ax_tot[k] / grand * span_L
        lp[k] = (t, t + w); t += w + GAP
    C0, C1 = np.deg2rad(80), np.deg2rad(-80)
    span_C = (C0 - C1) - GAP * (len(CLUSTERS) - 1)
    cp, t = {}, C0
    for k in names:
        w = clu_tot[k] / grand * span_C
        cp[k] = (t - w, t); t -= (w + GAP)

    fig, ax = blank((8.5, 4.95))
    ax.set_xlim(-2.50, 2.50); ax.set_ylim(-1.50, 1.36)

    cur_l = {k: lp[k][1] for k in KEYS}
    cur_c = {c: cp[c][1] for c in names}
    for cname, _, bloc in CLUSTERS:
        for k in KEYS:
            w = LINKS[cname].get(k)
            if not w:
                continue
            wl = w / grand * span_L
            wc = w / grand * span_C
            a1, a0 = cur_l[k], cur_l[k] - wl
            b1, b0 = cur_c[cname], cur_c[cname] - wc
            cur_l[k] = a0; cur_c[cname] = b0
            fc = BLOC[bloc]
            charts.ribbon(ax, a0, a1, b0, b1, r=R, facecolor=fc,
                          edgecolor='white', lw=0.45, zorder=2)

    LXL = -1.24
    sub_texts, name_texts = [], []
    for k in KEYS:
        t0, t1 = lp[k]
        charts.arc_band(ax, t0, t1, R, R + RW, facecolor=INK, edgecolor='none', zorder=6)
        tm = (t0 + t1) / 2
        ax0, ay0 = (R + RW) * np.cos(tm), (R + RW) * np.sin(tm)
        ax.plot([ax0 - 0.03, LXL + 0.05], [ay0, ay0], color=LIGHT, lw=0.7, zorder=5)
        name_texts.append(
            ax.text(LXL, ay0 + 0.035, LABEL[k], fontsize=9.8, ha='right', va='center', color=INK))
        sub_texts.append(
            ax.text(LXL, ay0 - 0.062, ASUB[k], fontsize=8.0, ha='right', va='center', color=MID))
    anchors = []
    for cname, sub, bloc in CLUSTERS:
        t0, t1 = cp[cname]
        charts.arc_band(ax, t0, t1, R, R + RW,
                        facecolor='#5a5a5a', edgecolor='none', zorder=6)
        tm = (t0 + t1) / 2
        anchors.append([cname, sub, (R + RW) * np.cos(tm), (R + RW) * np.sin(tm)])
    MINGAP = 0.30
    ys = [a[3] for a in anchors]
    for _ in range(400):
        moved = False
        for k in range(len(ys) - 1):
            d = ys[k] - ys[k + 1]
            if d < MINGAP:
                sh = (MINGAP - d) / 2
                ys[k] += sh; ys[k + 1] -= sh; moved = True
        if not moved:
            break
    LX = 1.24
    for (cname, sub, ax0, ay0), ly in zip(anchors, ys):
        ax.plot([ax0 + 0.03, LX - 0.05], [ay0, ly], color=LIGHT, lw=0.7, zorder=5)
        ax.text(LX, ly, cname, fontsize=9.8, ha='left', va='center', color=INK)

    ax.text(LXL, 1.32, 'THE TERMS OF THE EQUATION', fontsize=9, color=MID, ha='right', va='top')
    ax.text(LX, 1.32, 'WHO HOLDS THEM', fontsize=9, color=MID, ha='left', va='top')
    # the legend is left-aligned, set so its longest line ends at the term labels' right edge
    fig.canvas.draw()
    inv = ax.transData.inverted()
    items = []
    for i, (fc, txt) in enumerate([('#d2d2d2', 'American techno-bloc'),
                                   ('#242424', 'Chinese techno-bloc'),
                                   ('#8a8a8a', 'Indian techno-bloc')]):
        yy = -1.28 - i * 0.088
        items.append((ax.add_patch(mp.Rectangle((0.0, yy - 0.022), 0.095, 0.044, facecolor=fc,
                                                edgecolor='none', clip_on=False)),
                      ax.text(0.13, yy, txt, fontsize=8.8, va='center', color=INK)))
    fig.canvas.draw()
    edge = max(inv.transform((t.get_window_extent().x1, 0))[0] for t in name_texts)
    dx = edge - max(inv.transform((t.get_window_extent().x1, 0))[0] for _, t in items)
    for r, t in items:
        r.set_x(r.get_x() + dx)
        t.set_x(t.get_position()[0] + dx)
    ax.set_title('Figure 8-1 The terms of the equation, and where each is held')
    save(fig, 'fig8-1_techno_blocs', 'Original to this book.',
         "Schematic. The nine clusters are grouped here by country and region. Each term is taken as a whole and divided\n"
         "into the shares the author judges each place to carry; the widths are ordinal judgements, not measured shares.\n"
         'No place carries every term at world level: over eighty per cent of T_2 lies outside the United States, and China\n'
         'does not reach institutions at all.')


PENTA = ['I', 'E', 'T_1', 'T_2', 'K']
HUES = ['#2a78d6', '#e34948', '#1baf7a', '#4a3aa7', '#eda100']
HUE_AT = {'Chengdu-Chongqing': 4}      # keep a place's colour where it reads best

# Levels, 0 to 10, on the same scale as each other and consistent with the
# world shares drawn in figure 8-1. (name, is_cluster, [I, E, T_1, T_2, K])
PANELS = [
    ('American techno-bloc (excl. Loxbridge)', [
        ('SF Bay Area',        1, [8.0, 3.0, 9.5, 2.0, 8.5]),
        ('Texas',              1, [9.5, 7.5, 5.5, 2.5, 5.5]),
        ('BosWash',            1, [8.0, 2.5, 6.0, 2.0, 9.0]),
        ('UAE',                1, [7.0, 9.5, 2.5, 1.0, 9.5]),
        ('Japan-Korea-Taiwan', 1, [5.0, 2.0, 3.5, 10.0, 4.0])]),
    ('China', [
        ('Yangtze Delta',      1, [3.0, 8.5, 9.0, 7.0, 8.0]),
        ('GBA',                1, [4.0, 8.5, 6.0, 9.0, 7.5]),
        ('Beijing',            0, [1.5, 7.0, 8.0, 5.0, 7.0]),
        ('Chengdu-Chongqing',  0, [4.5, 9.0, 4.0, 5.5, 4.5])]),
    ('Europe', [
        ('Loxbridge',          1, [6.5, 0.8, 5.0, 1.0, 5.0]),
        ('France',             0, [5.0, 5.5, 3.5, 2.0, 2.5]),
        ('Germany',            0, [5.0, 0.5, 1.0, 5.0, 2.5]),
        ('Netherlands',        0, [5.5, 1.0, 1.0, 7.0, 2.5]),
        ('Nordics',            0, [6.5, 6.0, 1.0, 1.5, 2.0])]),
    ('India', [
        ('Bengaluru-Hyderabad', 1, [4.0, 3.0, 4.5, 1.0, 3.5]),
        ('Delhi',              0, [2.5, 3.0, 3.0, 1.5, 4.5]),
        ('Mumbai',             0, [3.0, 3.0, 2.5, 1.5, 5.5])]),
    ('Global South', [
        ('Indonesia',          0, [3.0, 4.0, 1.0, 1.5, 3.0]),
        ('Vietnam',            0, [3.5, 3.5, 1.0, 3.0, 2.0]),
        ('Nigeria',            0, [2.0, 1.2, 0.5, 0.5, 1.5]),
        ('Kenya',              0, [3.0, 2.5, 1.0, 0.5, 1.2])]),
]


def _smooth_closed(pts, per=48):
    """Closed Catmull-Rom through the vertices, so a profile reads as a body
       rather than as a polygon."""
    n = len(pts)
    out = []
    for i in range(n):
        p0, p1 = pts[(i - 1) % n], pts[i]
        p2, p3 = pts[(i + 1) % n], pts[(i + 2) % n]
        t = np.linspace(0, 1, per, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    q = np.concatenate(out)
    return np.concatenate([q, q[:1]])


def fig82():
    # 8-2 the five terms, region by region. Absolute levels, so the plates compare.
    setup((1, 1)); plt.close()
    th = np.pi / 2 - np.arange(5) * 2 * np.pi / 5      # I at the top, clockwise
    fig = plt.figure(figsize=(10.5, 9.2))
    gs = fig.add_gridspec(2, 6)
    slots = [gs[0, 0:2], gs[0, 2:4], gs[0, 4:6], gs[1, 1:3], gs[1, 3:5]]
    axes = [fig.add_subplot(sl) for sl in slots]
    for ax, (title, rows) in zip(axes, PANELS):
        ax.set_aspect('equal'); ax.axis('off')
        ax.set_xlim(-13.2, 13.2); ax.set_ylim(-12.6, 12.6)
        for r in (2, 4, 6, 8, 10):
            ax.add_patch(mp.Circle((0, 0), r, fill=False,
                                   edgecolor='#e6e6e6', lw=0.7, zorder=1))
        for a in th:
            ax.plot([0, 10 * np.cos(a)], [0, 10 * np.sin(a)],
                    color='#e6e6e6', lw=0.7, zorder=1)
        for k, a in enumerate(th):
            ax.text(11.6 * np.cos(a), 11.6 * np.sin(a), PENTA[k], fontsize=11.5,
                    ha='center', va='center', color=INK)
        order = sorted(range(len(rows)), key=lambda k: -sum(rows[k][2]))
        for k in order:
            name, core, v = rows[k]
            w = np.array(v, float)
            pts = np.stack([w * np.cos(th), w * np.sin(th)], 1)
            q = _smooth_closed(pts)
            c = HUES[HUE_AT.get(name, k % 5)]
            ax.fill(q[:, 0], q[:, 1], facecolor=c,
                    alpha=0.26 if core else 0.17, edgecolor='none', zorder=2)
            ax.plot(q[:, 0], q[:, 1], color=c, lw=1.2 if core else 0.9,
                    alpha=0.85 if core else 0.6, zorder=3)
        ax.text(0, 13.9, title, fontsize=12.5, color=INK, ha='center', va='bottom')
        for k, (name, core, _) in enumerate(rows):
            y = -15.0 - k * 1.42
            ax.add_patch(mp.Rectangle((-11.6, y - 0.48), 1.5, 0.96,
                                      facecolor=HUES[HUE_AT.get(name, k % 5)],
                                      alpha=0.30 if core else 0.20,
                                      edgecolor='none', clip_on=False, zorder=4))
            ax.text(-9.6, y, name, fontsize=11, va='center', clip_on=False,
                    color=INK if core else MID)
    fig.subplots_adjust(left=0.035, right=0.975, top=0.895, bottom=0.215,
                        wspace=0.55, hspace=0.72)
    fig.text(0.038, 0.985, 'Figure 8-2 The five terms, region by region',
             fontsize=15.5, color=INK, ha='left', va='top')
    note = (
        "Schematic. Each plate shows one region at the five terms of the Chapter 1 equation: institutions I, energy abundance E,\n"
        "deep tech in bits T_1, deep tech in the physical T_2, and large capital K. The scale is absolute and the same on every\n"
        "plate, so a small shape is a small shape, and the levels are consistent with the world shares drawn in figure 8-1.\n"
        "Names set in black are the nine clusters of this chapter; names in grey are placed for reference. Levels are ordinal\n"
        "judgements from the coefficients set out in this chapter, not measured values.\n"
        "Source: Original to this book.")
    fig.text(0.038, 0.105, note, fontsize=10.5, color=MID, va='top', ha='left')
    import os as _os
    from bookstyle import OUT as _OUT
    for ext in ('png', 'svg'):
        fig.savefig(_os.path.join(_OUT, 'fig8-2_pentagons.' + ext),
                    bbox_inches='tight', facecolor='white')
    plt.close(fig)


ALL = [fig11, fig12,
       fig21, fig22, fig23,
       fig31, fig32, fig33, fig34,
       fig41, fig42, fig43, fig44, fig45, fig46,
       fig51, fig52, fig53, fig54,
       fig61, fig62, fig63,
       fig71, fig72,
       fig81, fig82]

if __name__ == '__main__':
    for f in ALL:
        f()
        print(f.__name__, 'ok')
    print(f'{len(ALL)} figures')
