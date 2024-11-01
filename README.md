# Efficient-Data-Stream-Anomaly-Detection

If you don't have numpy, simply execute ```pip install -r requirements.txt``` while in the directory.

```main.py``` is the entry point and it contains matplotlib boiler plate code for visualizing data. Simply run that to see the anomaly detection in real time.

The data stream generation file ```DataStreamGenerator.py``` just simulates a sine graph with data that experiences random noise (Random noise is added to each data point to simulate fluctuations typical in real-world data) and seasonal variations. You can modify these values to better see how Z-score bolstered with exponential moving average (EMA) impacts adaptability. Just the Z-score alone using the mean and standard deviation isn't enough. Exponential moving average allows for recent data points to have more weight than a simple moving average (SMA). This means that EMA is more sensitive to changes and can identify trends earlier than an SMA.

The anomaly detection logic is in ```AnomalyDetector.py``` and has a method ```addDataPoint``` which gets called with the new point and this keeps track of recent EMA mean/std variance.

Z-score simply quantifies the difference between a new data point and the historic mean of a dataset. Adding EMA just adds adaptability which can be good for long seasons (period of the sine graph). The idea to use Z-score comes from Local Outlier Factor (LOF) which takes the local deviation of a data point's density in relation to its neighbors. It considers data points with a significantly lower density than their neighbors to be outliers. Compared to LOF this algorithm is able to pick up more anomalies that may not be outliers in comparison to LOF. The subtle changes allows for more finer analysis on where data points are out of range.
