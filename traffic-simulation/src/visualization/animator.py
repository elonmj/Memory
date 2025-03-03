import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class TrafficAnimator:
    """
    Class to handle the animation of traffic simulation results.
    """

    def __init__(self, density, grid_x, grid_t, rho_max):
        """
        Initializes the animator with density data and grid information.

        Args:
            density: 2D array of traffic density over time and space.
            grid_x: 1D array of spatial coordinates.
            grid_t: 1D array of temporal coordinates.
            rho_max: Maximum density for scaling the visualization.
        """
        self.density = density
        self.grid_x = grid_x
        self.grid_t = grid_t
        self.rho_max = rho_max

    def animate_density(self, filename=None):
        """
        Creates an animation of the density evolution over time.

        Args:
            filename: If provided, saves the animation to this file.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        line, = ax.plot([], [], 'b-', lw=2)

        ax.set_xlim(self.grid_x.min(), self.grid_x.max())
        ax.set_ylim(0, self.rho_max * 1.1)
        ax.set_xlabel('Position (km)')
        ax.set_ylabel('Density (vehicles/km)')
        ax.grid(True)

        text_time = ax.text(0.02, 0.95, '', transform=ax.transAxes)

        def init():
            line.set_data([], [])
            text_time.set_text('')
            return line, text_time

        def update(frame):
            line.set_data(self.grid_x, self.density[frame])
            text_time.set_text(f'Time: {self.grid_t[frame]:.2f} h')
            return line, text_time

        ani = FuncAnimation(fig, update, frames=len(self.grid_t), init_func=init,
                            interval=50, blit=True)

        plt.tight_layout()

        if filename:
            ani.save(filename, writer='ffmpeg')

        plt.show()