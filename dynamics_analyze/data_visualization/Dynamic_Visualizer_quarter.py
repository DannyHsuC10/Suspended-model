import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Visualizer:
    
    def __init__(self, result):

        # =====================================================
        # Data
        # =====================================================

        self.time = np.asarray(result["t"])

        self.zr = np.asarray(result["zr"])

        self.zs = np.asarray(result["zs"])
        self.zu = np.asarray(result["zu"])

        self.vzs = np.asarray(result["vzs"])
        self.vzu = np.asarray(result["vzu"])

        self.azs = np.asarray(result["azs"])
        self.azu = np.asarray(result["azu"])

        self.Fs = np.asarray(result["Fs"])
        self.Ft = np.asarray(result["Ft"])


        self.window = 2.0

        # 動畫偏移
        self.ms_offset = 0.2
        self.zr_offset = 0.0595

        self.fig = plt.figure(figsize=(14,8))


        gs = self.fig.add_gridspec(
            4,
            2,
            width_ratios=[1.2,1],
            hspace=0.4
        )


        # 左動畫
        self.ax_state = self.fig.add_subplot(gs[:,0])


        # 右邊四張圖
        self.ax_pos = self.fig.add_subplot(gs[0,1])
        self.ax_vel = self.fig.add_subplot(gs[1,1],sharex=self.ax_pos)
        self.ax_acc = self.fig.add_subplot(gs[2,1],sharex=self.ax_pos)
        self.ax_force = self.fig.add_subplot(gs[3,1],sharex=self.ax_pos)

        self._create_signal_plot(
            self.ax_pos,
            "Displacement",
            [
                (self.zr,"Road"),
                (self.zu,"Unsprung"),
                (self.zs,"Sprung")
            ],
            "m")

        self._create_signal_plot(
            self.ax_vel,
            "Velocity",
            [
                (self.vzu,"vzu"),
                (self.vzs,"vzs")
            ],
            "m/s")

        self._create_signal_plot(
            self.ax_acc,
            "Acceleration",
            [
                (self.azu,"azu"),
                (self.azs,"azs")
            ],
            "m/s²")

        self._create_signal_plot(
            self.ax_force,
            "Force",
            [
                (self.Ft,"Tire Force"),
                (self.Fs,"Suspension Force")
            ],
            "N")

        self.vline_pos = self._create_cursor(self.ax_pos)
        self.vline_vel = self._create_cursor(self.ax_vel)
        self.vline_acc = self._create_cursor(self.ax_acc)
        self.vline_force = self._create_cursor(self.ax_force)

        # =====================================================
        # Left Animation
        # =====================================================

        ymin = min(
            self.zu.min() + self.zr_offset,
            self.zr.min() + self.zr_offset,
            self.zs.min() + self.ms_offset)

        ymax = max(
            self.zr.max() + self.zr_offset,
            self.zu.max() + self.zr_offset,
            self.zs.max() + self.ms_offset)

        self.ax_state.set_xlim(-self.window, self.window)
        self.ax_state.set_ylim(ymin-0.3, ymax+0.3)

        self.ax_state.set_title("Suspension Animation")
        self.ax_state.set_xlabel("Relative Position")
        self.ax_state.set_ylabel("Height")

        self.ax_state.axvline(
            0,
            color='gray',
            linestyle='--')

        # ---------------- Road ----------------

        self.wave_artist, = self.ax_state.plot(
            [],
            [],
            color='black',
            lw=2,
            label="Road")

        # ---------------- Wheel ----------------

        self.wheel_artist, = self.ax_state.plot(
            [],
            [],
            marker='o',
            color='black',
            markersize=70,
            label='Wheel'
        )

        # ---------------- Unsprung ----------------

        self.mu_artist, = self.ax_state.plot(
            [],
            [],
            marker='o',
            color='gray',
            markersize=40,
            label='mu'
        )

        # ---------------- Sprung ----------------

        self.ms_artist, = self.ax_state.plot(
            [],
            [],
            marker='s',
            color='blue',
            markersize=70,
            label='ms'
        )

    def _create_signal_plot(
        self,
        ax,
        title,
        signals,
        ylabel=None
    ):

        ax.set_title(title)

        for data, label in signals:
            ax.plot(
                self.time,
                data,
                label=label
            )

        if ylabel:
            ax.set_ylabel(ylabel)

        ax.legend()
        ax.grid()

    def _create_cursor(self, ax):
        
        return ax.axvline(
            self.time[0],
            color="k",
            linestyle="--"
        )

    def update(self, frame):
        
        t_now = self.time[frame]

        # ----------------------
        # Road wave
        # ----------------------

        x = self.time - t_now
        mask = np.abs(x) < self.window

        self.wave_artist.set_data(x[mask], self.zr[mask])


        # ----------------------
        # Animation
        # ----------------------

        self.wheel_artist.set_data([0],[self.zr[frame]+self.zr_offset])
        self.mu_artist.set_data([0],[self.zu[frame]+self.zr_offset])
        self.ms_artist.set_data([0],[self.zs[frame]+self.ms_offset])


        # ----------------------
        # Cursor
        # ----------------------

        self.vline_pos.set_xdata([t_now,t_now])
        self.vline_vel.set_xdata([t_now,t_now])
        self.vline_acc.set_xdata([t_now,t_now])
        self.vline_force.set_xdata([t_now,t_now])


        return (
            self.wave_artist,
            self.wheel_artist,
            self.mu_artist,
            self.ms_artist,
            self.vline_pos,
            self.vline_vel,
            self.vline_acc,
            self.vline_force)

    def get_animation_frames(self, fps=30):
        
        total_time = self.time[-1]-self.time[0]

        target_frames = int(
            total_time * fps
        )

        step = max(
            1,
            len(self.time)//target_frames
        )

        return range(
            0,
            len(self.time),
            step
        )

    def show(self, fps=30):
        
        frames = self.get_animation_frames(fps)

        self.ani = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=1000/fps,
            blit=True
        )

        plt.show()
