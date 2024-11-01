import matplotlib.pyplot as plt
from DataStreamGenerator import DataStreamGenerator
from AnomalyDetector import AnomalyDetector

def main():
    # Initialize Data Generator and Anomaly Detector
    data_generator = DataStreamGenerator(num_points=1000, noise_level=6, seasonal_amplitude=20, seasonal_period=60)
    anomaly_detector = AnomalyDetector(decay_alpha=0.05, threshold=4, window_size=200)
    
    # Setup Matplotlib for real-time plotting
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots(figsize=(12, 6))
    line, = ax.plot([], [], 'b-', lw=1, label="Data Stream")
    anomaly_line, = ax.plot([], [], 'ro', label="Anomalies")  # Red dots for anomalies
    
    ax.set_title('Real-time Data Stream with Anomaly Detection')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend()
    ax.grid(True)
    
    max_points = 200  # Number of points to show in the window
    ax.set_xlim(0, max_points)
    ax.set_ylim(-40, 40)
    
    # Initialize data containers
    times = []
    values = []
    anomaly_times = []
    anomaly_values = []
    
    try:
        for i, data_point in enumerate(data_generator.generateStreamOfData()):
            # Update anomaly detection
            is_anomaly, z_score = anomaly_detector.addDataPoint(data_point)
            
            # Append data for visualization
            times.append(i)
            values.append(data_point)
            if is_anomaly:
                anomaly_times.append(i)
                anomaly_values.append(data_point)
            
            # Update line data
            line.set_data(times[-max_points:], values[-max_points:])
            anomaly_line.set_data(anomaly_times[-max_points:], anomaly_values[-max_points:])
            
            # Adjust x-axis for scrolling effect
            if i > max_points:
                ax.set_xlim(i - max_points, i)
            
            # Adjust y-axis dynamically
            current_ymin, current_ymax = ax.get_ylim()
            data_min, data_max = min(values[-max_points:]), max(values[-max_points:])
            if data_min < current_ymin or data_max > current_ymax:
                ax.set_ylim(data_min - 5, data_max + 5)
            
            # Draw the updated plot
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.01)  # Small pause for real-time update speed

    except KeyboardInterrupt:
        print("\nVisualization stopped by user")
    finally:
        plt.ioff()
        plt.show()

# Run the real-time visualization with anomaly detection
if __name__ == "__main__":
    main()