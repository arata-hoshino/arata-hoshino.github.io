"""
Advanced chart primitives for the book's figures.

Implemented here rather than pulled from a library so that every drawing
step is auditable and the monochrome ET Book house style is preserved.

  voronoi_treemap  - additively weighted (power) Voronoi treemap, area-accurate,
                     clipped to an arbitrary convex boundary, one or two levels
  sunburst         - nested polar wedges
  circle_pack      - hierarchical circle packing (via circlify)
  chord            - bipartite/complete chord diagram with bezier ribbons
  ridgeline        - weighted kernel-density ridgeline (joyplot)
  waffle           - unit chart, one mark per unit
"""
import numpy as np

# ---------------------------------------------------------------- geometry ---
def _clip_halfplane(poly, a, b):
    """Sutherland-Hodgman clip of polygon `poly` (Nx2) to the half-plane a.x <= b."""
    if len(poly) == 0:
        return poly
    out = []
    n = len(poly)
    d = poly @ a - b                      # <=0 means inside
    for i in range(n):
        j = (i + 1) % n
        di, dj = d[i], d[j]
        if di <= 0:
            out.append(poly[i])
        if (di < 0 < dj) or (dj < 0 < di):
            t = di / (di - dj)
            out.append(poly[i] + t * (poly[j] - poly[i]))
    return np.array(out) if out else np.empty((0, 2))


def _poly_area(p):
    if len(p) < 3:
        return 0.0
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def _poly_centroid(p):
    if len(p) < 3:
        return p.mean(axis=0) if len(p) else np.zeros(2)
    x, y = p[:, 0], p[:, 1]
    cr = x * np.roll(y, -1) - np.roll(x, -1) * y
    A = cr.sum() / 2.0
    if abs(A) < 1e-12:
        return p.mean(axis=0)
    cx = ((x + np.roll(x, -1)) * cr).sum() / (6 * A)
    cy = ((y + np.roll(y, -1)) * cr).sum() / (6 * A)
    return np.array([cx, cy])


def _power_cells(sites, weights, boundary):
    """Clipped power diagram. Returns a list of polygons, one per site."""
    n = len(sites)
    cells = []
    for i in range(n):
        poly = boundary
        pi, wi = sites[i], weights[i]
        for j in range(n):
            if i == j or len(poly) == 0:
                continue
            pj, wj = sites[j], weights[j]
            a = 2.0 * (pj - pi)
            b = pj @ pj - wj - pi @ pi + wi
            poly = _clip_halfplane(poly, a, b)
        cells.append(poly)
    return cells


def circle_boundary(cx=0.0, cy=0.0, r=1.0, n=160):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[cx + r * np.cos(t), cy + r * np.sin(t)]


def rect_boundary(x0, y0, x1, y1):
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float)


def voronoi_treemap(values, boundary, iters=220, seed=0, sites=None):
    """
    Area-accurate additively weighted Voronoi treemap.

    values   : target weights (any positive scale; normalised internally)
    boundary : convex polygon (Nx2) to tessellate
    returns  : list of polygons, one per value, whose areas are proportional
               to `values` to within a fraction of a percent.
    """
    values = np.asarray(values, float)
    n = len(values)
    total = _poly_area(boundary)
    target = values / values.sum() * total

    rng = np.random.default_rng(seed)
    if sites is None:
        # seed sites by rejection sampling inside the boundary
        lo, hi = boundary.min(axis=0), boundary.max(axis=0)
        pts = []
        while len(pts) < n:
            c = rng.uniform(lo, hi, size=(4 * n, 2))
            for p in c:
                if len(_clip_halfplane(boundary, np.zeros(2), 0)) >= 0:
                    pass
                # point-in-polygon by winding
                if _point_in_poly(p, boundary):
                    pts.append(p)
                if len(pts) == n:
                    break
        sites = np.array(pts[:n])
    else:
        sites = np.array(sites, float)

    w = np.zeros(n)
    scale = total / n
    for it in range(iters):
        cells = _power_cells(sites, w, boundary)
        areas = np.array([_poly_area(c) for c in cells])
        # move sites to centroids (Lloyd); keep empty cells where they are
        for i, c in enumerate(cells):
            if len(c) >= 3:
                sites[i] = _poly_centroid(c)
        # adapt weights toward target areas
        err = target - areas
        step = 0.55 if it < iters * 0.6 else 0.30
        w += step * err / max(target.mean(), 1e-12) * scale
        w -= w.min()
        # rescue starved cells
        dead = areas < target * 0.02
        if dead.any():
            w[dead] += 0.35 * scale
    cells = _power_cells(sites, w, boundary)
    return cells


def _point_in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)):
            xint = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < xint:
                inside = not inside
    return inside


# ---------------------------------------------------------------- sunburst ---
def sunburst(ax, rings, r0=0.28, width=0.34, gap=0.012, start=90.0):
    """
    rings : list of levels, each a list of (label, fraction_of_whole, facecolor,
            textcolor). Fractions within a level must sum to 1.
    Draws wedges outward. Returns list of (level, label, mid_angle, r_mid).
    """
    import matplotlib.patches as mp
    out = []
    for li, level in enumerate(rings):
        rin = r0 + li * (width + gap)
        rout = rin + width
        a = start
        for (lab, frac, fc, tc) in level:
            span = -360.0 * frac
            ax.add_patch(mp.Wedge((0, 0), rout, a + span, a, width=width,
                                  facecolor=fc, edgecolor='white', lw=1.1))
            out.append((li, lab, a + span / 2.0, (rin + rout) / 2.0, tc, abs(span)))
            a += span
    return out


# ------------------------------------------------------------ circle pack ---
def circle_pack(hierarchy):
    """Thin wrapper over circlify; returns circles with .x .y .r .ex"""
    import circlify
    return circlify.circlify(hierarchy, show_enclosure=False,
                             target_enclosure=circlify.Circle(x=0, y=0, r=1))


# ---------------------------------------------------------------- ridgeline --
def kde(samples, weights, grid, bw):
    s = np.asarray(samples, float)
    w = np.asarray(weights, float)
    w = w / w.sum()
    d = (grid[:, None] - s[None, :]) / bw
    return (np.exp(-0.5 * d * d) * w[None, :]).sum(axis=1) / (bw * np.sqrt(2 * np.pi))


# ------------------------------------------------------------------- chord ---
def ribbon(ax, a0, a1, b0, b1, r=1.0, bend=0.12, **kw):
    """
    Closed chord ribbon between arc [a0,a1] and arc [b0,b1] on a circle of
    radius r. Angles in radians. `bend` is the pull of the bezier toward the
    centre: 0 gives straight chords, 1 collapses them onto the origin.
    """
    from matplotlib.path import Path
    import matplotlib.patches as mp
    P = Path

    def pt(t, rr=None):
        rr = r if rr is None else rr
        return (rr * np.cos(t), rr * np.sin(t))

    def arc(t0, t1, n=26):
        return [pt(t) for t in np.linspace(t0, t1, n)]

    verts = arc(a0, a1)
    codes = [P.MOVETO] + [P.LINETO] * (len(verts) - 1)
    verts += [(0.0, 0.0), pt(b0)]
    codes += [P.CURVE3, P.CURVE3]
    seg = arc(b0, b1)[1:]
    verts += seg
    codes += [P.LINETO] * len(seg)
    verts += [(0.0, 0.0), pt(a0)]
    codes += [P.CURVE3, P.CURVE3]
    ax.add_patch(mp.PathPatch(P(verts, codes), **kw))


def arc_band(ax, t0, t1, r_in, r_out, **kw):
    """A thick arc segment (the outer ring of a chord diagram)."""
    from matplotlib.path import Path
    import matplotlib.patches as mp
    P = Path
    outer = [(r_out * np.cos(t), r_out * np.sin(t)) for t in np.linspace(t0, t1, 40)]
    inner = [(r_in * np.cos(t), r_in * np.sin(t)) for t in np.linspace(t1, t0, 40)]
    v = outer + inner + [outer[0]]
    c = [P.MOVETO] + [P.LINETO] * (len(v) - 2) + [P.CLOSEPOLY]
    ax.add_patch(mp.PathPatch(P(v, c), **kw))


# ------------------------------------------------------------------ waffle ---
def waffle_grid(n, per_row):
    """Return (x, y) arrays for n unit marks laid out in rows of `per_row`."""
    i = np.arange(n)
    return i % per_row, i // per_row


# --------------------------------------------------------- label fitting ----
def fit_label(ax, poly, cx, cy, lines, color, max_fs=13.0, min_fs=5.6,
              linespacing=1.05, weight=None):
    """
    Place `lines` (a list of strings, longest-first preference) at (cx, cy) and
    keep only a version whose rendered bounding box lies wholly inside `poly`.
    Tries each candidate label from richest to plainest, shrinking the font.
    Returns the Text artist, or None if nothing fits.
    """
    fig = ax.figure
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    disp = ax.transData.transform(poly)

    def inside(pt):
        return _point_in_poly(np.asarray(pt, float), disp)

    for text in lines:
        fs = max_fs
        while fs >= min_fs:
            t = ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
                        color=color, linespacing=linespacing, zorder=20)
            if weight:
                t.set_fontweight(weight)
            bb = t.get_window_extent(renderer=ren)
            pad = 1.5
            corners = [(bb.x0 - pad, bb.y0 - pad), (bb.x1 + pad, bb.y0 - pad),
                       (bb.x1 + pad, bb.y1 + pad), (bb.x0 - pad, bb.y1 + pad)]
            if all(inside(c) for c in corners):
                return t
            t.remove()
            fs -= 0.5
    return None
