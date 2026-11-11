"""Rebuild Evgenii's portrait from the 650x812 original (crown cut by the frame).

    git show 9eb23d3:static/img/founders/abramov.jpg > /tmp/abramov-src.jpg
    python3 tools/rebuild_abramov_portrait.py /tmp/abramov-src.jpg static/img/founders/abramov.jpg

Extends the frame upward: background by inpainting + blur, the crown as an
elliptical continuation of the head outline filled with the hair texture
mirrored from just below the edge. Output 453x567 at 1:1, eyes level with
Iliya's portrait."""
import sys, numpy as np, cv2
SRC, OUT = sys.argv[1], sys.argv[2]
EXT = 70                                   # rows added above the original
src = cv2.imread(SRC)                      # BGR 812x650
h, w = src.shape[:2]

# head outline points read off the original (x, y), y=0 is the top edge
pts = np.array([(165,100),(175,70),(190,45),(210,25),(235,10),(255,2),
                (360,4),(375,10),(395,25),(415,45),(430,70),(437,95)], float)
# least-squares ellipse x-axis aligned: ((x-cx)/a)^2 + ((y-cy)/b)^2 = 1
from scipy.optimize import least_squares
def res(p):
    cx, cy, a, b = p
    return ((pts[:,0]-cx)/a)**2 + ((pts[:,1]-cy)/b)**2 - 1
cx, cy, a, b = least_squares(res, [302, 140, 140, 150]).x
apex = cy - b
print(f"ellipse cx={cx:.0f} cy={cy:.0f} a={a:.0f} b={b:.0f}  apex y={apex:.1f}")

# canvas with the band: the top rows mirrored (used for the crown texture)
band = src[:EXT][::-1].copy()
canvas = np.vstack([band, src])
Y, X = np.mgrid[0:h+EXT, 0:w]
yy = Y - EXT                                # original coordinates
inside = ((X-cx)/a)**2 + ((yy-cy)/b)**2 <= 1

# 1. background in the band: built from the top rows' background only.
#    Per column, the median of rows 0..8; across the head (and a margin, so
#    no hair colour leaks in) the two sides are joined linearly; then blurred
#    hard, as the real background is, and repeated upward.
row = np.median(src[0:9].astype(np.float32), axis=0)          # w x 3
lo, hi = 222, 390                                             # head at y=0 is 245..360
for c in range(3):
    row[lo:hi, c] = np.linspace(row[lo-1, c], row[hi, c], hi-lo)
row = cv2.GaussianBlur(row[None], (0,0), sigmaX=18, sigmaY=0)[0]
band_bg = np.repeat(row[None], EXT, axis=0)
# fine grain like the photograph's, so the band is not plastic-smooth
rng = np.random.default_rng(7)
band_bg += rng.normal(0, 1.6, band_bg.shape).astype(np.float32)
out = canvas.astype(np.float32)
out[:EXT] = band_bg
# outside the head, ease from the real top rows into the new band
ease = np.clip(np.arange(12)/12.0, 0, 1)[:, None, None]       # 12 rows below the edge
real = canvas[EXT:EXT+12].astype(np.float32)
blend = band_bg[-1][None] * (1-ease) + real * ease
outside = (~inside[EXT:EXT+12])[..., None]
out[EXT:EXT+12] = np.where(outside, blend, real)

# 2. the crown: inside the ellipse above the edge, mirrored hair, soft edge
crown = np.zeros((h+EXT, w), np.float32)
crown[:EXT][inside[:EXT]] = 1
crown = cv2.GaussianBlur(crown, (0,0), 1.6)   # hair edge is soft, not a cut
crown[EXT:] = 0
hair = canvas.astype(np.float32)               # rows < EXT are the mirror of hair rows
out = out * (1-crown[...,None]) + hair * crown[...,None]

# 3. blend the seam at the original top edge over 6 rows
out = np.clip(out, 0, 255).astype(np.uint8)
seam = out.copy(); seam[EXT-3:EXT+3] = cv2.GaussianBlur(out, (0,0), 1.2)[EXT-3:EXT+3]
out = seam

# 4. crop 453x567 at 1:1, eyes level with Iliya's (y≈245), face centred
eye_y_src = 195
top = EXT + eye_y_src - 245
left = int(round(cx - 453/2 + 2))
crop = out[top:top+567, left:left+453]
assert crop.shape[:2] == (567, 453), crop.shape
# same grade as the portrait it replaces (slightly warmer, a touch darker)
crop = np.clip(crop.astype(np.float32) * np.array([0.956, 0.977, 0.973], np.float32), 0, 255).astype(np.uint8)
cv2.imwrite(OUT, crop, [cv2.IMWRITE_JPEG_QUALITY, 92])
print("top", top, "left", left)
