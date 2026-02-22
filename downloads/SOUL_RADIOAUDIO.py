#!/usr/bin/env python3
"""
SOUL RADIO v1.1 — Now with actual sound.
'><^' GNU TERRY PRATCHETT | DodecaGone Systems 2026
"""
import sys, math, random, struct, wave, threading, time, os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QFrame, QGroupBox, QComboBox,
    QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QPainter, QColor, QPen

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("WARNING: pygame not found. Install with: pip install pygame")
    print("Audio will be silent. Visuals still work.")

SAMPLE_RATE = 22050
CHUNK_SIZE = 2048

C_GRAY="#C0C0C0"; C_DARK="#808080"; C_WHITE="#FFFFFF"; C_BLACK="#000000"
C_NAVY="#000080"; C_TEAL="#008080"; C_RED="#FF0000"; C_GREEN="#00FF00"; C_AMBER="#FFAA00"

WIN31_STYLE = """
QMainWindow { background: #C0C0C0; }
QWidget { font-family: "Courier New", monospace; font-size: 11px; color: #000; }
QGroupBox { border: 2px outset #C0C0C0; margin-top: 12px; padding-top: 14px; font-weight: bold; color: #000080; }
QGroupBox::title { subcontrol-origin: margin; left: 8px; padding: 0 4px; }
QPushButton { background: #C0C0C0; border: 2px outset #C0C0C0; padding: 3px 12px; min-width: 60px; }
QPushButton:pressed { border: 2px inset #808080; }
QPushButton:checked { border: 2px inset #808080; background: #A0A0A0; }
QSlider::groove:horizontal { border: 2px inset #808080; height: 6px; background: #FFF; }
QSlider::handle:horizontal { background: #C0C0C0; border: 2px outset #C0C0C0; width: 12px; margin: -4px 0; }
QComboBox { border: 2px inset #808080; background: #FFF; padding: 2px 4px; }
QComboBox::drop-down { border: 2px outset #C0C0C0; width: 16px; }
"""

class SoundEngine:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.t = 0.0; self.phase3 = 0.0
        self.volume = 0.5; self.station = 0
        self.param_a = 0.5; self.param_b = 0.5

    def generate_chunk(self, n=CHUNK_SIZE):
        samples = []; dt = 1.0 / self.sample_rate
        for _ in range(n):
            self.t += dt
            s = self._sample()
            s = max(-1.0, min(1.0, s * self.volume))
            samples.append(int(s * 32767))
        return samples

    def _sample(self):
        fn = [self._deep_ocean, self._crystal_cave, self._solar_wind,
              self._rain_machine, self._void_hum, self._dreaming_machine,
              self._geiger_garden, self._frozen_signal]
        return fn[self.station]() if self.station < len(fn) else 0.0

    def _deep_ocean(self):
        f = 40 + self.param_a * 30; mod = math.sin(self.t*0.1)*0.5+0.5
        s = math.sin(self.t*f*6.2832)*0.3 + math.sin(self.t*f*1.5*6.2832*mod)*0.2
        s += math.sin(self.t*0.7)*math.sin(self.t*f*0.5*6.2832)*0.15
        if random.random() < 0.001*self.param_b: s += random.uniform(-0.3,0.3)
        return s

    def _crystal_cave(self):
        f = 220+self.param_a*440; d = math.exp(-((self.t%2.0)*(1+self.param_b*3)))
        s = math.sin(self.t*f*6.2832)*d*0.3 + math.sin(self.t*f*2*6.2832)*d*0.15
        s += math.sin(self.t*f*3*6.2832)*d*0.1 + math.sin(self.t*f*5*6.2832)*d*0.05
        return s

    def _solar_wind(self):
        n = random.uniform(-1,1); sh = (math.sin(self.t*0.3)+1)*0.5
        sh2 = (math.sin(self.t*0.07+1.5)+1)*0.5; f = 80+self.param_a*200
        return n*sh*0.3*self.param_b + math.sin(self.t*f*6.2832)*0.2*sh2

    def _rain_machine(self):
        s = random.uniform(-0.05,0.05)
        if random.random() < 0.02*self.param_a: s += random.uniform(-0.5,0.5)
        if random.random() < 0.1*self.param_b: s += random.uniform(-0.15,0.15)
        if (self.t%8.0) < 0.5: s += math.sin(self.t*20*6.2832)*math.exp(-((self.t%8.0)*0.5))*0.2
        return s

    def _void_hum(self):
        f = 30+self.param_a*20; w = math.sin(self.t*0.05)*self.param_b*10
        return math.sin(self.t*f*6.2832)*0.4 + math.sin(self.t*(f+0.5)*6.2832)*0.3 + math.sin(self.t*(f+w)*6.2832)*0.2

    def _dreaming_machine(self):
        b = 110+self.param_a*110; cp = (self.t*0.02*(1+self.param_b))%1.0
        rats = [1.0,1.25,1.5,1.333,1.667,2.0,1.125,1.875]
        i = int(cp*len(rats)); bl = (cp*len(rats))%1.0
        f1 = b*rats[i%len(rats)]; f2 = b*rats[(i+1)%len(rats)]
        return math.sin(self.t*f1*6.2832)*(1-bl)*0.25 + math.sin(self.t*f2*6.2832)*bl*0.25 + math.sin(self.t*b*6.2832)*0.15

    def _geiger_garden(self):
        s = random.uniform(-0.02,0.02)
        if random.random() < 0.005+self.param_a*0.05: s = random.choice([-0.8,0.8])*(0.3+self.param_b*0.5)
        if random.random() < 0.0005: self.phase3 = 1.0
        if self.phase3 > 0: s += math.sin(self.t*880*6.2832)*self.phase3*0.15; self.phase3 *= 0.9995
        return s

    def _frozen_signal(self):
        f = 100+self.param_a*300
        s = (1.0 if math.sin(self.t*f*6.2832)>0 else -1.0)*0.2
        bits = int(2+self.param_b*6); lv = 2**bits; s = round(s*lv)/lv
        if math.sin(self.t*0.5) > 0.3: s *= 0.1
        if random.random() < 0.002: s = random.choice([-0.5,0.5])
        return s

class AudioPlayer:
    """Plays audio chunks through pygame mixer."""
    def __init__(self):
        self.active = False
        if not HAS_PYGAME: return
        try:
            pygame.mixer.pre_init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=CHUNK_SIZE*2)
            pygame.mixer.init()
            self.active = True
            self.channel = None
        except Exception as e:
            print(f"Audio init failed: {e}")

    def play_chunk(self, samples):
        if not self.active: return
        try:
            raw = struct.pack('<' + 'h' * len(samples), *samples)
            sound = pygame.mixer.Sound(buffer=raw)
            if self.channel is None or not self.channel.get_busy():
                self.channel = sound.play()
            else:
                self.channel.queue(sound)
        except Exception:
            pass

    def stop(self):
        if self.active:
            try: pygame.mixer.stop()
            except: pass

class AudioThread(QThread):
    chunk_ready = pyqtSignal(list)
    def __init__(self, engine, player):
        super().__init__()
        self.engine = engine; self.player = player
        self.running = False; self.playing = False
    def run(self):
        self.running = True
        while self.running:
            if self.playing:
                samples = self.engine.generate_chunk(CHUNK_SIZE)
                self.player.play_chunk(samples)
                self.chunk_ready.emit(samples)
                time.sleep(CHUNK_SIZE / SAMPLE_RATE * 0.85)
            else:
                time.sleep(0.05)
    def stop(self):
        self.running = False; self.wait()

class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__(); self.setMinimumHeight(100)
        self.buffer = [0]*300; self.color = QColor(C_TEAL)
    def update_data(self, samples):
        step = max(1, len(samples)//50)
        for i in range(0, len(samples), step): self.buffer.append(samples[i]/32768.0)
        self.buffer = self.buffer[-300:]; self.update()
    def paintEvent(self, e):
        p = QPainter(self); w,h = self.width(),self.height()
        p.fillRect(0,0,w,h,QColor(C_BLACK))
        p.setPen(QPen(QColor("#1a1a1a"),1))
        p.drawLine(0,h//2,w,h//2)
        for i in range(0,w,30): p.drawLine(i,0,i,h)
        p.setPen(QPen(self.color,1)); mid = h//2
        if len(self.buffer)>1:
            st = w/len(self.buffer)
            for i in range(1,len(self.buffer)):
                p.drawLine(int((i-1)*st),int(mid-self.buffer[i-1]*mid*0.9),
                          int(i*st),int(mid-self.buffer[i]*mid*0.9))
        p.setPen(QPen(QColor(C_DARK),1)); p.drawRect(0,0,w-1,h-1); p.end()

class SpectrumWidget(QWidget):
    def __init__(self):
        super().__init__(); self.setMinimumHeight(60)
        self.bars = [0.0]*16; self.targets = [0.0]*16
    def update_data(self, samples):
        if not samples: return
        bs = max(1,len(samples)//16)
        for i in range(16):
            band = samples[i*bs:min((i+1)*bs,len(samples))]
            if band: self.targets[i] = min(1.0, sum(abs(s) for s in band)/len(band)/32768.0*3)
        for i in range(16):
            self.bars[i] += (self.targets[i]-self.bars[i])*0.3
            self.bars[i] = max(0, self.bars[i]-0.01)
        self.update()
    def paintEvent(self, e):
        p = QPainter(self); w,h = self.width(),self.height()
        p.fillRect(0,0,w,h,QColor(C_BLACK))
        bw = max(2,(w-32)//16)
        for i,v in enumerate(self.bars):
            x = i*(bw+2)+2; bh = int(v*(h-4))
            c = QColor(C_RED) if v>0.7 else QColor(C_AMBER) if v>0.4 else QColor(C_GREEN)
            p.fillRect(x,h-2-bh,bw,bh,c)
        p.setPen(QPen(QColor(C_DARK),1)); p.drawRect(0,0,w-1,h-1); p.end()

STATIONS = ["DEEP OCEAN","CRYSTAL CAVE","SOLAR WIND","RAIN MACHINE",
            "VOID HUM","DREAMING MACHINE","GEIGER GARDEN","FROZEN SIGNAL"]
DESCS = ["Layered waves. Slow modulation. Bubbles in the dark.",
         "Shimmer harmonics. Bell decay. Reverb in stone.",
         "Cosmic noise shaped by sine. The sound between stars.",
         "Drops on surfaces. Thunder in the distance. Always.",
         "Sub-bass drone. Beating frequencies. Nothing, loudly.",
         "Evolving chords through the harmonic series. Sleep.",
         "Clicks and ticks. Organic timing. A radioactive forest.",
         "Dying square waves. Bit-crushed. A signal going under."]
COLORS = [C_TEAL,"#9966CC","#FFAA00","#4488FF","#FF4444","#66CCCC","#44FF44","#FF6600"]

class SoulRadio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SOUL RADIO v1.1")
        self.setFixedSize(560, 520)
        self.setStyleSheet(WIN31_STYLE)
        self.engine = SoundEngine()
        self.player = AudioPlayer()
        self.audio_thread = AudioThread(self.engine, self.player)
        self.audio_thread.chunk_ready.connect(self.on_chunk)
        self.audio_thread.start()
        self.is_playing = False
        self._build_ui()
        self.timer = QTimer(); self.timer.timeout.connect(self.tick); self.timer.start(50)

    def _build_ui(self):
        c = QWidget(); self.setCentralWidget(c)
        L = QVBoxLayout(c); L.setSpacing(4); L.setContentsMargins(6,6,6,6)

        # Title
        tb = QFrame(); tb.setStyleSheet(f"background:{C_NAVY};padding:3px;")
        tl = QHBoxLayout(tb); tl.setContentsMargins(6,2,6,2)
        t = QLabel("■ SOUL RADIO v1.1"); t.setStyleSheet(f"color:{C_WHITE};font-weight:bold;font-size:12px;")
        tl.addWidget(t)
        m = QLabel("'><^'"); m.setStyleSheet(f"color:{C_WHITE};font-size:10px;"); m.setAlignment(Qt.AlignRight)
        tl.addWidget(m); L.addWidget(tb)

        # Station
        sg = QGroupBox("STATION"); sl = QVBoxLayout(sg)
        cr = QHBoxLayout()
        self.combo = QComboBox()
        for i,n in enumerate(STATIONS): self.combo.addItem(f"{i+1}. {n}")
        self.combo.currentIndexChanged.connect(self.change_station)
        cr.addWidget(QLabel("Frequency:")); cr.addWidget(self.combo, 1); sl.addLayout(cr)
        self.desc = QLabel(DESCS[0]); self.desc.setStyleSheet(f"color:{C_DARK};font-size:10px;"); self.desc.setWordWrap(True)
        sl.addWidget(self.desc); L.addWidget(sg)

        # Waveform
        wg = QGroupBox("WAVEFORM"); wl = QVBoxLayout(wg)
        self.wave = WaveformWidget(); wl.addWidget(self.wave); L.addWidget(wg)

        # Spectrum
        spg = QGroupBox("SPECTRUM"); spl = QVBoxLayout(spg)
        self.spec = SpectrumWidget(); spl.addWidget(self.spec); L.addWidget(spg)

        # Controls
        cg = QGroupBox("CONTROLS"); gl = QGridLayout(cg)
        self.vol_s = self._slider(gl,"Volume:",0,50); self.pa_s = self._slider(gl,"Tone:",1,50)
        self.pb_s = self._slider(gl,"Texture:",2,50); L.addWidget(cg)

        # Buttons
        br = QHBoxLayout()
        self.play_btn = QPushButton("▶ PLAY"); self.play_btn.clicked.connect(self.toggle_play); self.play_btn.setCheckable(True)
        br.addWidget(self.play_btn)
        eb = QPushButton("⬇ EXPORT WAV"); eb.clicked.connect(self.export_wav); br.addWidget(eb)
        rb = QPushButton("🎲 RANDOM"); rb.clicked.connect(self.randomize); br.addWidget(rb)
        L.addLayout(br)

        # Status
        sf = QFrame(); sf.setStyleSheet("border:2px inset #808080;background:#C0C0C0;padding:2px;")
        sfl = QHBoxLayout(sf); sfl.setContentsMargins(4,2,4,2)
        self.status = QLabel("Ready — press PLAY"); self.status.setStyleSheet("border:none;font-size:10px;color:#404040;")
        sfl.addWidget(self.status)
        gtp = QLabel("GNU TERRY PRATCHETT"); gtp.setStyleSheet("border:none;font-size:9px;color:#808080;"); gtp.setAlignment(Qt.AlignRight)
        sfl.addWidget(gtp); L.addWidget(sf)

        if not self.player.active:
            self.status.setText("WARNING: No audio output (pip install pygame)")

    def _slider(self, grid, label, row, default):
        grid.addWidget(QLabel(label), row, 0)
        s = QSlider(Qt.Horizontal); s.setRange(0,100); s.setValue(default)
        lbl = QLabel(f"{default}%"); lbl.setMinimumWidth(35)
        s.valueChanged.connect(lambda v, l=lbl: l.setText(f"{v}%"))
        s.valueChanged.connect(lambda v, r=row: self._param_changed(r, v))
        grid.addWidget(s, row, 1); grid.addWidget(lbl, row, 2)
        return s

    def _param_changed(self, row, val):
        v = val / 100.0
        if row == 0: self.engine.volume = v
        elif row == 1: self.engine.param_a = v
        elif row == 2: self.engine.param_b = v

    def change_station(self, idx):
        self.engine.station = idx; self.desc.setText(DESCS[idx])
        self.wave.color = QColor(COLORS[idx % len(COLORS)])

    def toggle_play(self):
        self.is_playing = not self.is_playing
        self.audio_thread.playing = self.is_playing
        if self.is_playing:
            self.play_btn.setText("■ STOP")
            self.status.setText(f"Playing: {STATIONS[self.engine.station]}")
        else:
            self.play_btn.setText("▶ PLAY")
            self.player.stop()
            self.status.setText("Stopped")

    def randomize(self):
        self.combo.setCurrentIndex(random.randint(0, len(STATIONS)-1))
        self.vol_s.setValue(random.randint(30,80))
        self.pa_s.setValue(random.randint(10,90))
        self.pb_s.setValue(random.randint(10,90))

    def export_wav(self):
        self.status.setText("Exporting 30s...")
        def _do():
            eng = SoundEngine(); eng.station=self.engine.station
            eng.volume=self.engine.volume; eng.param_a=self.engine.param_a; eng.param_b=self.engine.param_b
            all_s = []
            for _ in range(0, SAMPLE_RATE*30, CHUNK_SIZE): all_s.extend(eng.generate_chunk(CHUNK_SIZE))
            fn = f"soul_radio_{STATIONS[eng.station].lower().replace(' ','_')}.wav"
            fp = os.path.join(os.path.expanduser("~"), fn)
            with wave.open(fp,'w') as f:
                f.setnchannels(1); f.setsampwidth(2); f.setframerate(SAMPLE_RATE)
                f.writeframes(struct.pack('<'+'h'*len(all_s), *all_s))
            self.status.setText(f"Exported: {fn}")
        threading.Thread(target=_do, daemon=True).start()

    def on_chunk(self, samples):
        self.wave.update_data(samples); self.spec.update_data(samples)

    def tick(self):
        if self.is_playing:
            e = int(self.engine.t); m,s = divmod(e,60)
            self.status.setText(f"▶ {STATIONS[self.engine.station]} | {m:02d}:{s:02d} | "
                f"Vol:{int(self.engine.volume*100)}% Tone:{int(self.engine.param_a*100)}% Tex:{int(self.engine.param_b*100)}%")

    def closeEvent(self, e):
        self.audio_thread.stop(); self.player.stop(); e.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv); r = SoulRadio(); r.show(); sys.exit(app.exec_())
