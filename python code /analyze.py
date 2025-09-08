import numpy as np
import matplotlib.pyplot as plt
from math import ceil
import os

class NetworkAnalyzer:
    def __init__(self):
        self.throughput_data = np.zeros((4, 1000))
        self.rtt_data = np.zeros((4, 1000))
        self.lost_data = np.zeros((4, 1000))

    def data_collection(self, filename, keyword, init, convert_fn=float):
        def adjust_array(arr, init):
            for i in range(len(arr)):
                if arr[i] == init:
                    arr[i] = arr[i - 1] if i != 0 else 0
            return arr

        with open(filename, 'r') as file:
            data = [line.split() for line in file]

        result = np.full((2, 1000), init, dtype=np.float64 if convert_fn != int else object)
        if keyword == 'lost':
            last_lost = [0, 0]
            for line in data:
                if line[0] == 'd':
                    index = 0 if line[-4][0] == '0' else 1
                    last_lost[index] += 1
                    timestamp = ceil(float(line[1]))
                    if timestamp < result.shape[1]:
                        result[index, timestamp] = last_lost[index]
        else:
            for line in data:
                if keyword in line:
                    index = 0 if line[1] == '0' else 1
                    value = line[-1] if line[-1] != 'none' else init
                    timestamp = ceil(float(line[0]))
                    if timestamp < result.shape[1]:
                        try:
                            result[index, timestamp] = convert_fn(value)
                        except ValueError as e:
                            print(f"ValueError: {e} for line[0]: {line[0]}, value: {value}")
        return [adjust_array(result[i], init) for i in range(2)]

    def data_import(self, reno_filename, reno_bbr_filename, keyword, init, data_attr, convert_fn=float):
        data_reno = self.data_collection(reno_filename, keyword, init, convert_fn)
        data_reno_bbr = self.data_collection(reno_bbr_filename, keyword, init, convert_fn)
        data = getattr(self, data_attr)

        for i in range(1000):
            data[0, i] += float(data_reno[0][i])
            data[1, i] += float(data_reno_bbr[0][i])
            data[2, i] += float(data_reno[1][i])
            data[3, i] += float(data_reno_bbr[1][i])

    def avg_run(self):
        for i in range(10):
            print(f"###    { i+1 }     ###")
            os.system("ns reno.tcl")
            os.system("ns tcp-reno-bbr.tcl")

            self.data_import('projectTrace_reno.tr', 'project_trace_BBR.tr', 'ack_', 0, 'throughput_data', int)
            self.data_import('projectTrace_reno.tr', 'project_trace_BBR.tr', 'rtt_', -1.0, 'rtt_data', float)
            self.data_import('projectTrace_reno.tr', 'project_trace_BBR.tr', 'lost', -1, 'lost_data', int)

        self.throughput_data /= 10
        self.rtt_data /= 10
        self.lost_data /= 10

    def analyze_metric(self, metric_data, metric_name, metric_label, ylabel, derivative=False):
        plt.figure()
        for i, label in enumerate(["reno_flow_1", "reno_BBR_flow_1", "reno_flow_2", "reno_BBR_flow_2"]):
            data = metric_data[i]
            if derivative:
                result = np.zeros_like(data)
                result[1:] = data[1:] / np.arange(1, len(data))
                result[0] = data[0]
                data = result
            plt.plot(range(1000), data, label=label)
        plt.xlabel("time")
        plt.ylabel(ylabel)
        plt.title(f"{metric_label}")
        plt.legend()
        plt.show()

    def analyze_all_metrics(self):
        self.analyze_metric(self.rtt_data, "Rtt", "RTT", "RTT")
        self.analyze_metric(self.lost_data, "Lost", "Loss Rate", "Loss Rate", derivative=True)
        self.analyze_metric(self.throughput_data, "Throughput", "Throughput ", "Throughput", derivative=True)

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    analyzer.avg_run()
    analyzer.analyze_all_metrics()

