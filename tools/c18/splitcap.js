/* a feed caption, reduced to what the photo shows plus its credit: wire datelines and trailing desk notes
   are removed, the credit is lifted out of the caption (or taken from the image metadata); nothing is added */
const splitCap = (raw, meta) => {
  let s = String(raw || "").replace(/\s+/g, " ").trim(), cr = "";
  const m = s.match(/\(([^()]*(?:AP Photo|via AP|Photo by|Getty|Reuters)[^()]*)\)/i) || s.match(/(Photo by [^.]*?)(?=\s*(?:$|(?:Ph\.D\.|Jr\.)\s*$))/);
  if (m) { cr = m[1].trim(); s = s.replace(m[0], " "); }
  for (let k = 0; k < 4; k++) {
    const d = s.match(/^\s*([^a-z]{1,80}?)\s*(?:[–—]|:)\s+/);
    if (!d || !/[A-Z0-9]/.test(d[1])) break;
    s = s.slice(d[0].length);
  }
  s = s.replace(/\s+[A-Z]{4,}:.*$/, "").replace(/\s+(?:Ph\.D\.|Jr\.)\s*$/, "").replace(/\s+/g, " ").trim();
  if (!cr && meta) cr = /^[^,]+, [^,]+$/.test(meta) ? meta.replace(/^([^,]+), (.+)$/, "$2 $1") : meta;
  return { cap: s, cr };
};
