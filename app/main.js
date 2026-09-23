/* Joshua Study — tab router + footnote interactions.
   Plain ES module, no build step. Paths are relative so it works from a GitHub
   Pages subpath.

   Reworked from Projects/Matthew/app/main.js (phase-4-5-plan.md §A1/§B):
   no discourse overlay -- Joshua has no confirmed sub-movement grouping, so
   discourseOf(), the discourse-bracket half of buildBookMap(), and the
   discourse half of renderPlacement() are dropped rather than adapted.
   Reads movements[] as {n, name, span, units} (data/units.json's own Phase 1
   shape) instead of Matthew's {id, label}.

   The `?v=N` on every same-origin module import below is manual cache-busting
   for GitHub Pages (which serves app/*.js with long-lived cache headers, no
   ETag revalidation to rely on). Bump every `?v=N` here AND in search.js's own
   threads.js import, together, whenever threads.js/spotlight.js/search.js
   changes -- a stale cached module is invisible in the DOM (data fetches are
   fine, they already cache-bust via bust()) and easy to mistake for a real
   bug. 2026-09-17: missed on the first ship of threads.js's `example` field,
   which silently never rendered until this bump. */

import { loadThreadData, resolveUnit, injectPalette, rebuildLegend, wireRoots } from "./threads.js?v=4";
import { enhanceSpotlights } from "./spotlight.js?v=4";
import { renderSearch } from "./search.js?v=4";

const UNITS_URL = new URL("../data/units.json", import.meta.url);

// always revalidate — a no-build static site changes the moment files are pushed
// no build step: always fetch the current file, never a cached copy
const bust = (u) => { const x = new URL(u); x.searchParams.set("v", Date.now()); return x; };

const content = document.getElementById("content");
const unitNav = document.getElementById("unit-nav");
const pager = document.getElementById("unit-pager");
const fabPrev = document.getElementById("fab-prev");
const fabNext = document.getElementById("fab-next");
const navToggle = document.getElementById("nav-toggle");
const navToggleCtx = document.getElementById("nav-toggle-ctx");

let manifest = null;

const CENTER_TEXT_KEY = "joshua:centerText";

applySettings();
init();

async function init() {
  try {
    [manifest] = await Promise.all([
      fetch(bust(UNITS_URL)).then((r) => r.json()),
      loadThreadData(),
    ]);
  } catch (e) {
    content.innerHTML = `<p class="missing">Could not load site data (<code>data/*.json</code>).</p>`;
    return;
  }
  buildUnitNav();
  wireNavToggle();
  wireSettingsToggle();
  window.addEventListener("hashchange", route);
  route();
}

/* --------------------------------------------------------------- settings */

function applySettings() {
  const centered = localStorage.getItem(CENTER_TEXT_KEY) === "1";
  document.body.classList.toggle("text-center", centered);
  const checkbox = document.getElementById("setting-center-text");
  if (checkbox) checkbox.checked = centered;
}

function wireSettingsToggle() {
  const toggle = document.getElementById("settings-toggle");
  const panel = document.getElementById("settings-panel");
  const backdrop = document.getElementById("nav-backdrop");
  const checkbox = document.getElementById("setting-center-text");
  if (!toggle || !panel) return;

  const set = (open) => {
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    if (open) {
      unitNav.hidden = true;
      navToggle.setAttribute("aria-expanded", "false");
      backdrop.hidden = false;
    } else if (unitNav.hidden) {
      backdrop.hidden = true;
    }
  };
  toggle.addEventListener("click", () => set(panel.hidden));
  backdrop.addEventListener("click", () => set(false));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") set(false); });

  checkbox?.addEventListener("change", () => {
    localStorage.setItem(CENTER_TEXT_KEY, checkbox.checked ? "1" : "0");
    document.body.classList.toggle("text-center", checkbox.checked);
  });
}

function wireNavToggle() {
  const backdrop = document.getElementById("nav-backdrop");
  const settingsPanel = document.getElementById("settings-panel");
  const settingsToggle = document.getElementById("settings-toggle");
  const set = (open) => {
    unitNav.hidden = !open;
    backdrop.hidden = !open;
    navToggle.setAttribute("aria-expanded", String(open));
    fabPrev.classList.toggle("nav-open", open);
    fabNext.classList.toggle("nav-open", open);
    if (open) {
      unitNav.scrollTop = 0;
      settingsPanel.hidden = true;
      settingsToggle.setAttribute("aria-expanded", "false");
    }
  };
  navToggle.addEventListener("click", () => set(unitNav.hidden));
  backdrop.addEventListener("click", () => set(false));
  unitNav.addEventListener("click", (e) => {
    if (e.target.closest("a.unit-chip, a.bm-tick")) set(false);
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") set(false); });
}

/* ----------------------------------------------------------------- unit nav */

function chip(u) {
  const a = document.createElement("a");
  a.className = "unit-chip" + (u.built ? "" : " unbuilt");
  a.dataset.slug = u.slug;
  if (u.built) a.href = `#/${u.slug}`;
  a.innerHTML =
    `<span class="n">${u.n}</span>${escapeHtml(u.title)}` +
    `<span class="passage">${escapeHtml(u.passage)}${u.built ? "" : " · not yet built"}</span>`;
  return a;
}

function unitsByMovement() {
  const m = new Map();
  for (const u of manifest.units) {
    if (!m.has(u.movement)) m.set(u.movement, []);
    m.get(u.movement).push(u);
  }
  return m;
}

/* A map of the whole book: 24 ticks grouped into the 4 movements. */
function buildBookMap() {
  const by = unitsByMovement();
  const wrap = document.createElement("div");
  wrap.className = "book-map";

  const scroller = document.createElement("div");
  scroller.className = "bm-scroll";
  const row = document.createElement("div");
  row.className = "bm-row";

  for (const m of manifest.movements) {
    const us = by.get(m.n) || [];
    if (!us.length) continue;
    const cols = `repeat(${us.length}, minmax(0, 1fr))`;

    const grp = document.createElement("div");
    grp.className = "bm-mv";
    grp.style.flex = String(us.length);

    const lab = document.createElement("div");
    lab.className = "bm-mv-label";
    lab.innerHTML = `<i></i><b>${roman(m.n)}</b><i></i>`;
    lab.title = `Movement ${roman(m.n)} — ${m.name}`;
    grp.appendChild(lab);

    const ticks = document.createElement("div");
    ticks.className = "bm-ticks";
    ticks.style.gridTemplateColumns = cols;
    for (const u of us) {
      const t = document.createElement(u.built ? "a" : "span");
      t.className = "bm-tick" + (u.built ? "" : " unbuilt");
      t.dataset.slug = u.slug;
      t.textContent = u.n;
      t.title = `Unit ${u.n} · ${u.title} · ${u.passage}${u.built ? "" : " (not yet built)"}`;
      if (u.built) t.href = `#/${u.slug}`;
      ticks.appendChild(t);
    }
    grp.appendChild(ticks);
    row.appendChild(grp);
  }

  scroller.appendChild(row);
  wrap.appendChild(scroller);

  const key = document.createElement("div");
  key.className = "bm-key";
  key.innerHTML =
    `<div class="bm-key-row"><span class="bm-key-h">Movements</span><span class="bm-key-items">` +
      manifest.movements.map((m) =>
        `<span class="bm-key-item"><b>${roman(m.n)}</b> ${escapeHtml(m.name)}</span>`).join("") +
    `</span></div>`;
  wrap.appendChild(key);
  return wrap;
}

function buildUnitNav() {
  const by = unitsByMovement();
  const frag = document.createDocumentFragment();
  frag.appendChild(buildBookMap());

  for (const m of manifest.movements) {
    const label = document.createElement("div");
    label.className = "movement-label";
    label.textContent = `Movement ${roman(m.n)} · ${m.name}`;
    frag.appendChild(label);

    const grid = document.createElement("div");
    grid.className = "unit-grid";
    for (const u of by.get(m.n) || []) grid.appendChild(chip(u));
    frag.appendChild(grid);
  }
  unitNav.innerHTML = "";
  unitNav.appendChild(frag);
}

/* ------------------------------------------------------------------- router */

function route() {
  const hash = location.hash.replace(/^#\/?/, "");
  const [slug, anchor] = hash.split("/");

  const searchLink = document.querySelector('.topbar-link[href="#/search"]');
  if (searchLink) {
    if (slug === "search") searchLink.setAttribute("aria-current", "page");
    else searchLink.removeAttribute("aria-current");
  }

  if (slug === "search") {
    markCurrent(null);
    pager.innerHTML = "";
    document.title = "Concordance — Joshua Study";
    renderSearch(content, manifest.units);
    content.scrollIntoView({ block: "start" });
    return;
  }

  const unit = manifest.units.find((u) => u.slug === slug && u.built);
  if (!unit) {
    const first = manifest.units.find((u) => u.built);
    if (first && !slug) { location.replace(`#/${first.slug}`); return; }
    content.innerHTML = `<p class="missing">Unit not found. Pick one above.</p>`;
    markCurrent(null);
    pager.innerHTML = "";
    return;
  }
  loadUnit(unit, anchor);
}

async function loadUnit(unit, anchor) {
  markCurrent(unit.slug);
  content.innerHTML = `<p class="loading">Loading ${escapeHtml(unit.title)}…</p>`;

  let html;
  try {
    const url = bust(new URL(`../units/${unit.slug}.html`, import.meta.url));
    html = await (await fetch(url)).text();
  } catch (e) {
    content.innerHTML = `<p class="missing">Could not load <code>units/${unit.slug}.html</code>.</p>`;
    return;
  }

  content.innerHTML = html;
  renderPlacement(content, unit);
  hoistStructureBlocks(content);
  const resolved = resolveUnit(unit);
  injectPalette(unit, resolved);
  rebuildLegend(content, resolved);
  enhanceSpotlights(content);
  wireRoots(content, unit, manifest.units);
  wireFootnotes();
  buildPager(unit);
  document.title = `Unit ${unit.n} · ${unit.title} — Joshua Study`;

  if (anchor) {
    const vm = anchor.match(/^v(\d+)$/);
    const el = vm
      ? [...content.querySelectorAll(".v")].find((v) => v.querySelector(".n")?.textContent.trim() === vm[1])
      : document.getElementById(anchor);
    if (el) requestAnimationFrame(() => jumpTo(el));
    else content.scrollIntoView({ block: "start" });
  } else {
    content.scrollIntoView({ block: "start" });
  }
}

/* Move every structural block (e.g. a boundary-list or map-style block, if a
   unit ever has one) to the top of the unit, just under the colour key,
   keeping their authored order. Explicitly does NOT touch section.block.legend
   or section.block.notes -- Joshua's endnotes carry the "block" class too
   (style reference §4: `<section class="block notes">`), unlike Matthew's
   bare `.notes`, so a naive "skip only .legend" port would wrongly hoist the
   endnotes to the top of every unit. */
function hoistStructureBlocks(root) {
  const article = root.querySelector("article.unit") || root;
  const anchor =
    article.querySelector("section.block.legend") ||
    article.querySelector("header.mast");
  if (!anchor || !anchor.parentNode) return;
  let ref = anchor;
  for (const b of article.querySelectorAll("section.block")) {
    if (b.classList.contains("legend") || b.classList.contains("notes")) continue;
    ref.after(b); // re-parents b to sit right after ref, in document order
    ref = b;
  }
}

function renderPlacement(root, unit) {
  const mast = root.querySelector("header.mast");
  if (!mast) return;
  const mv = manifest.movements.find((m) => m.n === unit.movement);
  if (!mv) return;
  const el = document.createElement("div");
  el.className = "unit-place";
  el.textContent = `Movement ${roman(mv.n)} · ${mv.name}`;
  mast.appendChild(el);
}

function markCurrent(slug) {
  for (const a of unitNav.querySelectorAll(".unit-chip, .bm-tick")) {
    if (a.dataset.slug === slug) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  }
  const u = manifest.units.find((x) => x.slug === slug);
  navToggleCtx.textContent = u ? `· Unit ${u.n} of ${manifest.unit_count}` : "";
}

/* --------------------------------------------------- footnote jump + return */

function wireFootnotes() {
  const origin = new Map(); // note id -> the <sup> the reader jumped from

  content.querySelectorAll("sup.en a[href*='#']").forEach((a) => {
    const id = a.getAttribute("href").split("#").pop();
    a.addEventListener("click", (e) => {
      e.preventDefault();
      const note = document.getElementById(id);
      if (!note) return;
      const sup = a.closest("sup.en");
      // click the same ref again while the note is on screen -> jump back
      if (origin.get(id) === sup && inView(note)) { back(id); return; }
      origin.set(id, sup);
      addBackLink(note, id);
      jumpTo(note);
    });
  });

  function addBackLink(note, id) {
    if (note.querySelector(".note-back")) return;
    const b = document.createElement("a");
    b.className = "note-back";
    b.href = "#";
    b.textContent = "↩ back";
    b.addEventListener("click", (e) => { e.preventDefault(); back(id); });
    note.append(" ", b);
  }

  function back(id) {
    const sup = origin.get(id);
    origin.delete(id);
    document.getElementById(id)?.querySelector(".note-back")?.remove();
    if (!sup) return;
    jumpTo(sup.closest(".v") || sup, sup);
  }
}

function jumpTo(el, flashEl) {
  const reduce = prefersReducedMotion();
  el.scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
  const target = flashEl || el;
  if (reduce) { flash(target); return; }
  // fire the highlight once the smooth scroll has settled (or after a cap)
  let last = null, still = 0, fired = false, start = performance.now();
  const done = () => { if (!fired) { fired = true; flash(target); } };
  const tick = () => {
    if (fired) return;
    const y = window.scrollY;
    still = y === last ? still + 1 : 0;
    last = y;
    if (still > 2 || performance.now() - start > 700) done();
    else requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function flash(el) {
  clearTimeout(el._flashT);
  el.classList.remove("flash");
  void el.offsetWidth; // restart the animation
  el.classList.add("flash");
  el._flashT = setTimeout(() => el.classList.remove("flash"), 2100);
}

function inView(el) {
  const r = el.getBoundingClientRect();
  return r.top < window.innerHeight * 0.9 && r.bottom > window.innerHeight * 0.1;
}

function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/* -------------------------------------------------------------- prev / next */

function buildPager(unit) {
  const built = manifest.units.filter((u) => u.built);
  const i = built.findIndex((u) => u.slug === unit.slug);
  const prev = built[i - 1];
  const next = built[i + 1];
  pager.innerHTML =
    (prev ? link(prev, "prev", "← Previous") : "<span></span>") +
    (next ? link(next, "next", "Next →") : "<span></span>");
  fab(fabPrev, prev, `Previous — Unit ${prev ? prev.n : ""}`);
  fab(fabNext, next, `Next — Unit ${next ? next.n : ""}`);

  function link(u, cls, dir) {
    return `<a class="${cls}" href="#/${u.slug}">` +
      `<span class="dir">${dir}</span>Unit ${u.n} · ${escapeHtml(u.title)}</a>`;
  }
  function fab(el, u, label) {
    el.hidden = !u;
    if (!u) return;
    el.href = `#/${u.slug}`;
    el.title = `${label} · ${u.title}`;
    el.setAttribute("aria-label", `${label}: ${u.title}`);
  }
}

/* ------------------------------------------------------------------- utils */

function roman(n) { return ["", "I", "II", "III", "IV", "V"][n] || String(n); }
function escapeHtml(s) { return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
