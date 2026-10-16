import html
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hello World Motion Lab",
    page_icon="✨",
    layout="wide",
)

st.title("✨ Hello World Motion Lab")
st.write("Make your name move! Choose a style, pick a background, and add animated weather or celebration effects.")

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Customize your scene")

name = st.sidebar.text_input("Enter your name", value="Hello World", max_chars=80)
font_family = st.sidebar.selectbox(
    "Font type",
    [
        "Arial",
        "Verdana",
        "Georgia",
        "Times New Roman",
        "Courier New",
        "Trebuchet MS",
        "Impact",
        "Comic Sans MS",
    ],
)
font_size = st.sidebar.slider("Font size", min_value=20, max_value=100, value=52, step=2)
font_weight = st.sidebar.select_slider(
    "Font weight", options=["Normal", "Bold", "Extra bold"], value="Bold"
)
name_mode = st.sidebar.selectbox(
    "Name display mode", ["Centered", "Smooth ticker tape", "Repeated pattern"]
)
background = st.sidebar.selectbox(
    "Background",
    ["Light", "Dark", "Sunset", "Ocean", "Forest", "Galaxy", "Paper"],
)
effect = st.sidebar.selectbox(
    "Dynamic action",
    ["None", "Rain", "Snow", "Hail", "Wind gust", "Confetti", "Tornado"],
)
speed = st.sidebar.slider(
    "Animation speed", min_value=0.5, max_value=2.5, value=1.0, step=0.1,
    help="Higher values make the effects move faster.",
)
density = st.sidebar.slider("Effect density", min_value=20, max_value=140, value=70, step=10)

st.sidebar.caption("Tip: try a dark background with snow, or a sunset background with confetti.")

# -----------------------------
# Build a safe configuration
# -----------------------------
backgrounds = {
    "Light": {"css": "linear-gradient(135deg, #f8fafc, #dbeafe)", "text": "#172033"},
    "Dark": {"css": "linear-gradient(135deg, #101827, #030712)", "text": "#ffffff"},
    "Sunset": {"css": "linear-gradient(135deg, #ffedd5, #fb7185 55%, #7c3aed)", "text": "#ffffff"},
    "Ocean": {"css": "linear-gradient(135deg, #082f49, #0e7490 55%, #67e8f9)", "text": "#ffffff"},
    "Forest": {"css": "linear-gradient(135deg, #052e16, #166534 55%, #a3e635)", "text": "#ffffff"},
    "Galaxy": {"css": "radial-gradient(circle at 20% 20%, #7c3aed, transparent 35%), linear-gradient(135deg, #020617, #172554 55%, #4c1d95)", "text": "#ffffff"},
    "Paper": {"css": "linear-gradient(135deg, #fff7ed, #fef3c7)", "text": "#292524"},
}
font_css = {
    "Arial": "Arial, Helvetica, sans-serif",
    "Verdana": "Verdana, Geneva, sans-serif",
    "Georgia": "Georgia, serif",
    "Times New Roman": "'Times New Roman', Times, serif",
    "Courier New": "'Courier New', Courier, monospace",
    "Trebuchet MS": "'Trebuchet MS', sans-serif",
    "Impact": "Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif",
    "Comic Sans MS": "'Comic Sans MS', 'Comic Sans', cursive",
}
weights = {"Normal": "400", "Bold": "700", "Extra bold": "900"}

config = {
    "name": name if name else "Hello World",
    "fontFamily": font_css[font_family],
    "fontSize": font_size,
    "fontWeight": weights[font_weight],
    "mode": name_mode,
    "background": backgrounds[background]["css"],
    "textColor": backgrounds[background]["text"],
    "effect": effect,
    "speed": speed,
    "density": density,
}
config_json = json.dumps(config).replace("</", "<\\/")

# -----------------------------
# Self-contained HTML + canvas animation.
# The iframe runs its own animation loop; Streamlit does not need st.rerun().
# -----------------------------
html_doc = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; width: 100%; height: 100%; overflow: hidden; }
  body { font-family: system-ui, sans-serif; }
  #scene {
    position: relative; width: 100%; height: 590px; overflow: hidden;
    background: var(--scene-bg); color: var(--scene-text);
    border-radius: 18px; isolation: isolate;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.18);
  }
  #effects { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 1; }
  #glow {
    position: absolute; width: 70%; height: 55%; left: 15%; top: 22%;
    border-radius: 50%; filter: blur(55px); opacity: .16;
    background: currentColor; pointer-events: none; z-index: 0;
  }
  #name-wrap {
    position: absolute; inset: 0; display: flex; align-items: center;
    justify-content: center; overflow: hidden; z-index: 2; padding: 28px;
  }
  #name {
    font-family: var(--font-family); font-size: var(--font-size);
    font-weight: var(--font-weight); color: var(--scene-text);
    text-align: center; line-height: 1.15; overflow-wrap: anywhere;
    max-width: 100%; text-shadow: 0 3px 16px rgba(0,0,0,.18);
    position: relative; z-index: 2;
  }
  #name.ticker {
    max-width: none; white-space: nowrap; overflow-wrap: normal;
    animation: ticker 12s linear infinite;
    padding-left: 100%;
  }
  #ticker-clip { width: 100%; overflow: hidden; }
  #name.repeated { display: flex; flex-direction: column; gap: .18em; }
  .repeat-line { white-space: nowrap; opacity: .9; }
  .repeat-line:nth-child(2n) { opacity: .62; transform: translateX(3%); }
  .repeat-line:nth-child(3n) { opacity: .42; transform: translateX(-3%); }
  #hint {
    position: absolute; left: 16px; right: 16px; bottom: 12px;
    z-index: 3; text-align: center; font-size: 12px; letter-spacing: .08em;
    text-transform: uppercase; opacity: .7; pointer-events: none;
  }
  @keyframes ticker {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
  }
  @media (prefers-reduced-motion: reduce) {
    #name.ticker { animation-duration: 28s; }
  }
</style>
</head>
<body>
<div id="scene">
  <div id="glow"></div>
  <canvas id="effects"></canvas>
  <div id="name-wrap">
    <div id="ticker-clip"><div id="name"></div></div>
  </div>
  <div id="hint">HELLO WORLD MOTION LAB · LIVE ANIMATION</div>
</div>
<script>
const cfg = __CONFIG__;
const scene = document.getElementById("scene");
const nameEl = document.getElementById("name");
const tickerClip = document.getElementById("ticker-clip");
const canvas = document.getElementById("effects");
const ctx = canvas.getContext("2d");

scene.style.setProperty("--scene-bg", cfg.background);
scene.style.setProperty("--scene-text", cfg.textColor);
scene.style.setProperty("--font-family", cfg.fontFamily);
scene.style.setProperty("--font-size", cfg.fontSize + "px");
scene.style.setProperty("--font-weight", cfg.fontWeight);

const safeName = String(cfg.name || "Hello World");
if (cfg.mode === "Repeated pattern") {
  tickerClip.style.overflow = "visible";
  nameEl.className = "repeated";
  nameEl.innerHTML = "";
  for (let i = 0; i < 6; i++) {
    const line = document.createElement("div");
    line.className = "repeat-line";
    line.textContent = safeName;
    nameEl.appendChild(line);
  }
} else {
  nameEl.textContent = safeName;
  if (cfg.mode === "Smooth ticker tape") {
    nameEl.classList.add("ticker");
    nameEl.style.animationDuration = (12 / cfg.speed) + "s";
    tickerClip.style.justifyContent = "flex-start";
  } else {
    nameEl.style.whiteSpace = "normal";
  }
}

let w = 0, h = 0, particles = [], lastTime = 0, gust = 0;
function resize() {
  const rect = scene.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  w = rect.width; h = rect.height;
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(h * dpr);
  canvas.style.width = w + "px"; canvas.style.height = h + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  initParticles();
}
window.addEventListener("resize", resize);

function rand(min, max) { return Math.random() * (max - min) + min; }
function makeParticle(initial) {
  const type = cfg.effect;
  const p = { x: rand(0, w), y: initial ? rand(0, h) : rand(-h * .25, -10),
    vx: 0, vy: 0, size: rand(2, 6), rot: rand(0, Math.PI * 2),
    spin: rand(-.08, .08), hue: rand(0, 360), phase: rand(0, Math.PI * 2) };
  if (type === "Rain") { p.vx = rand(-1, 1); p.vy = rand(7, 13); p.size = rand(10, 20); }
  else if (type === "Snow") { p.vx = rand(-1, 1); p.vy = rand(0.7, 2.3); p.size = rand(2, 5); }
  else if (type === "Hail") { p.vx = rand(-1.5, 1.5); p.vy = rand(4, 8); p.size = rand(3, 7); }
  else if (type === "Wind gust") { p.x = initial ? rand(0,w) : -30; p.y = rand(0,h); p.vx = rand(5, 12); p.vy = rand(-.5,.5); p.size = rand(12, 28); }
  else if (type === "Confetti") { p.vx = rand(-2, 2); p.vy = rand(1, 4); p.size = rand(4, 9); p.spin = rand(-.14,.14); }
  else if (type === "Tornado") { p.angle = rand(0, Math.PI*2); p.radius = rand(8, Math.min(w*.36, 180)); p.orbit = rand(.02,.06); p.y = rand(0,h); p.size = rand(2,5); }
  return p;
}
function initParticles() {
  const count = cfg.effect === "None" ? 0 : cfg.density;
  particles = Array.from({length: count}, () => makeParticle(true));
}
function drawParticle(p) {
  const type = cfg.effect;
  if (type === "Rain") {
    ctx.strokeStyle = "rgba(125,211,252,.78)"; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(p.x-4,p.y+p.size); ctx.stroke();
  } else if (type === "Snow") {
    ctx.fillStyle = "rgba(255,255,255,.9)"; ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill();
  } else if (type === "Hail") {
    ctx.fillStyle = "rgba(224,242,254,.9)"; ctx.strokeStyle = "rgba(255,255,255,.9)";
    ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill(); ctx.stroke();
  } else if (type === "Wind gust") {
    ctx.strokeStyle = "rgba(255,255,255,.55)"; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.bezierCurveTo(p.x+8,p.y-5,p.x+14,p.y+5,p.x+p.size,p.y); ctx.stroke();
  } else if (type === "Confetti") {
    ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot);
    ctx.fillStyle = `hsl(${p.hue},90%,65%)`; ctx.fillRect(-p.size/2,-p.size/3,p.size,p.size*.65); ctx.restore();
  } else if (type === "Tornado") {
    ctx.fillStyle = "rgba(226,232,240,.72)"; ctx.beginPath(); ctx.arc(p.x,p.y,p.size,0,Math.PI*2); ctx.fill();
  }
}
function animate(now) {
  const dt = Math.min((now - (lastTime || now)) / 16.67, 2);
  lastTime = now;
  ctx.clearRect(0,0,w,h);
  if (cfg.effect === "Wind gust") {
    gust = (Math.sin(now * .0008) + 1) / 2;
    ctx.fillStyle = `rgba(226,232,240,${.025 + gust*.06})`;
    ctx.fillRect(0,0,w,h);
  }
  for (const p of particles) {
    if (cfg.effect === "Tornado") {
      p.angle += p.orbit * cfg.speed * dt;
      const centerX = w * .5 + Math.sin(now*.0007) * w*.04;
      const centerY = h * .53;
      const vertical = ((p.y + dt * (1.2 + p.radius*.008) * cfg.speed) % (h + 20));
      p.y = vertical;
      const taper = .22 + .78 * (p.y / h);
      p.x = centerX + Math.cos(p.angle) * p.radius * taper;
      p.x += Math.sin(now*.002 + p.phase) * 2;
    } else {
      p.x += (p.vx + (cfg.effect === "Wind gust" ? gust*4 : 0)) * cfg.speed * dt;
      p.y += p.vy * cfg.speed * dt;
      if (cfg.effect === "Snow") p.x += Math.sin(now*.001 + p.phase) * .8;
      if (cfg.effect === "Confetti") p.rot += p.spin * dt;
    }
    drawParticle(p);
    if (cfg.effect === "Wind gust" && p.x > w + 35) Object.assign(p, makeParticle(false));
    else if (cfg.effect !== "Tornado" && cfg.effect !== "Wind gust" && p.y > h + 25) {
      Object.assign(p, makeParticle(false));
    }
    if (cfg.effect === "Tornado" && p.y > h + 20) p.y = -10;
  }
  requestAnimationFrame(animate);
}
resize();
requestAnimationFrame(animate);
</script>
</body>
</html>
"""
html_doc = html_doc.replace("__CONFIG__", config_json)
components.html(html_doc, height=610, scrolling=False)

with st.expander("How this beginner app works"):
    st.markdown(
        """
        - **Streamlit controls** collect your name and style choices in Python.
        - **Configuration** passes those choices into the embedded scene as JSON.
        - **HTML and CSS** create the layered display, fonts, backgrounds, and smooth ticker.
        - **JavaScript canvas** draws and continuously animates the selected effect in the browser.
        - **No `time.sleep()` or repeated `st.rerun()` loop is needed**: the animation runs inside the embedded browser frame, so the page stays responsive.
        """
    )
st.caption("Built with Python + Streamlit. Animations run locally in your browser after the page loads.")
