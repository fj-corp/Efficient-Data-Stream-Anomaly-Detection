from collections import deque
import numpy as np

class AnomalyDetector:
    def __init__(self, decay_alpha=0.05, threshold=3, window_size=200) -> None:
        """
        Initialize the anomaly detector.
        
        Args:
            decayAlpha (float): Controls how quickly the detector adapts to changes, Lower = smoother, higher = more reactive (0 < alpha < 1)
            threshold (float): Z-score threshold for anomaly detection (Essentially, how far is the distance from the mean and the data point, we want
                        it to be atleast twice in difference for more catches)
            window_size (int): Size of the rolling window for visualization
        """
        self.decay_alpha = decay_alpha
        self.threshold = threshold
        self.window_size = window_size

        # Initialize EMA statistics, we keep these alive as long as the program is alive and subsequent update calls will know the EMA values
        self.ema_mean = None
        self.ema_std_variance = None

        # Store recent values for visualization
        self.recent_values = deque(maxlen=window_size)
        self.recent_z_scores = deque(maxlen=window_size)
        self.anomaly_points = deque(maxlen=window_size)
        self.anomaly_scores = deque(maxlen=window_size)

        # I have some plans with this but I don't know yet
        self.total_points = 0
        self.total_anomalies = 0

    def addDataPoint(self, point):
        """
        Process a new data point and detect if it's an anomaly.
        
        Args:
            point (float): New data point to process
        """
        self.total_points += 1
        z_score = 0
        is_anomaly = False

        if not self.ema_mean:
            self.ema_mean = point
            self.ema_std_variance = 0
        else:
            # EMA = Closing price * multiplier + EMA (previous day) * (1-multiplier)
            self.ema_mean = point * self.decay_alpha + self.ema_mean * (1 - self.decay_alpha)

            # EMA standard deviation
            deviation = point - self.ema_mean
            self.ema_std_variance = (1 - self.decay_alpha) * self.ema_std_variance + self.decay_alpha * (deviation ** 2)
            self.ema_std_variance = np.sqrt(self.ema_std_variance)

            # Z-score calculation, point - mean over standard deviation
            z_score = 0 if self.ema_std_variance == 0 else (point - self.ema_mean) / self.ema_std_variance

            is_anomaly = abs(z_score) > self.threshold # simple enough, just check if it's greater than the threshold we've set
            if is_anomaly:
                self.total_anomalies += 1

            
        self.recent_values.append(point)
        self.recent_z_scores.append(z_score)

        if is_anomaly:
            self.anomaly_points.append(point)
            self.anomaly_scores.append(z_score)

        return is_anomaly, z_score
    
    def getStatistics(self):
        """
        Get current detection statistics.
        
        Returns:
            dict: Dictionary containing current statistics
        """
        return {
            'total_points': self.total_points,
            'total_anomalies': self.total_anomalies,
            'anomaly_rate': (self.total_anomalies / self.total_points * 100) if self.total_points > 0 else 0,
            'current_mean': self.ema_mean,
            'current_std': self.ema_std_variance,
        }
    
    def getVisualizationData(self):
        """
        Get data for visualization.
        
        Returns:
            tuple: (recent_values, recent_z_scores, anomaly_points, anomaly_scores)
        """
        return (list(self.recent_values), 
                list(self.recent_z_scores), 
                list(self.anomaly_points), 
                list(self.anomaly_scores))
