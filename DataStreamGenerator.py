import math, random, time, numpy as np
import matplotlib.pyplot as plt
from collections import deque

class DataStreamGenerator:

    def __init__(self, num_points=1000, noise_level=4, seasonal_amplitude=20, seasonal_period=60) -> None:
        """
        Initialize the data stream simulator.
        
        Args:
            base_value (float): Base value for the stream
            noise_level (float): Amount of random noise
            seasonal_amplitude (float): Amplitude of seasonal variation
            seasonal_period (float): Period of seasonal variation
            anomaly_probability (float): Probability of generating an anomaly
        """
        self.num_data_points = num_points
        self.noise_level = noise_level
        self.season_amp = seasonal_amplitude
        self.seasonal_period = seasonal_period


    def generateStreamOfData(self):
        for i in range(self.num_data_points):
            # Create a regular pattern (sine graph wave) to simulate seasonality
            seasonal_value = self.season_amp * math.sin((2 * np.pi * i) / self.seasonal_period)
        
            noise = random.normalvariate(0, self.noise_level) # Add random noise
        
            # to fix: currently the data_point is not much different from seasonal values so come back and add more distinct noise if needed
            data_point = seasonal_value + noise # seasonal value + noise to get the final data point
        
            yield data_point
        
            # Simulate real-time data stream
            time.sleep(0.2) # 1 second is decent time to see matplotlib in action

    def visualizeStreamOfData(self):
        # Boiler plate code for matplotlib, I copied this
        max_points = 200  # Number of points to show in the window
        
        # Initialize data containers, deque because it's going to be efficient to remove data as time goes by and the data structure can do it itself
        times = deque(maxlen=max_points)
        values = deque(maxlen=max_points)
        
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots(figsize=(12, 6))
        line, = ax.plot([], [], 'b-', lw=2)
        
        ax.set_title('Real-time Data Stream Visualization')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.grid(True)
        
        # Set initial plot limits
        ax.set_xlim(0, max_points)
        ax.set_ylim(-self.season_amp * 1.5, self.season_amp * 1.5)
        
        # Show the plot window immediately
        plt.show(block=False)
        fig.canvas.draw()
        plt.pause(0.1)  # Short pause to ensure window appears
        
        try:
            for i, point in enumerate(self.generateStreamOfData()):
                # Update data containers
                times.append(i)
                values.append(point)
                
                # Update line data
                line.set_data(list(times), list(values))
                
                # Adjust x-axis limits to create scrolling effect
                if i > max_points:
                    ax.set_xlim(i - max_points, i)
                
                # Update y-axis limits if needed
                current_ymin, current_ymax = ax.get_ylim()
                data_min, data_max = min(values), max(values)
                if data_min < current_ymin or data_max > current_ymax:
                    margin = (data_max - data_min) * 0.1  # 10% margin
                    ax.set_ylim(data_min - margin, data_max + margin)
                
                # Update the display
                fig.canvas.draw_idle()
                fig.canvas.flush_events()
                plt.pause(0.01)

        except KeyboardInterrupt:
            print("\nVisualization stopped by user")
        finally:
            plt.ioff()  
            plt.show()



if __name__ == "__main__":
    # streamObj = DataStreamGenerator(2000, 6, 30, 80)
    streamObj = DataStreamGenerator()
    streamObj.visualizeStreamOfData()
    #for point in streamObj.generateStreamOfData():
    #    print(point)