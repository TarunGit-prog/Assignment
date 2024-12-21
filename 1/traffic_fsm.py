import time
import threading

class TrafficLightFSM:
    def __init__(self):
        self.state = "RED"  # Initial state
        self.start_time = time.time()
        self.timer = 0
        self.emergency_vehicle = False
        self.pedestrian_requested = False

    def transition(self):
        """
        Handles state transitions in the traffic light cycle, including priorities for pedestrians and emergency vehicles.
        """
        if self.emergency_vehicle:
            print(f"{self.get_current_time()} - Emergency vehicle detected! Immediate transition to GREEN.")
            self.state = "GREEN"
            time.sleep(5)  # Allow emergency vehicle to pass
            print(f"{self.get_current_time()} - Emergency vehicle passed. Transitioning to RED.")
            self.state = "RED"
            self.emergency_vehicle = False
            time.sleep(2)  # Pause before resuming normal cycle

        elif self.state == "RED":
            if self.pedestrian_requested:
                print(f"{self.get_current_time()} - Pedestrian crossing requested. Staying RED for pedestrians.")
                self.pedestrian_requested = False
                time.sleep(5)  # Allow pedestrians to cross
            else:
                print(f"{self.get_current_time()} - RED: Stopping traffic. Transitioning to YELLOW.")
                self.state = "YELLOW"
                time.sleep(2)

        elif self.state == "YELLOW":
            print(f"{self.get_current_time()} - YELLOW: Preparing to transition to GREEN.")
            self.state = "GREEN"
            time.sleep(5)

        elif self.state == "GREEN":
            if self.pedestrian_requested:
                print(f"{self.get_current_time()} - Pedestrian crossing requested. Transitioning to RED.")
                self.state = "RED"
                self.pedestrian_requested = False
                time.sleep(5)  # Allow pedestrians to cross
            else:
                print(f"{self.get_current_time()} - GREEN: Cars are passing. Transitioning to RED.")
                self.state = "RED"
                time.sleep(5)

    def detect_emergency_vehicle(self):
        """
        Automatically detects an emergency vehicle.
        """
        self.emergency_vehicle = True
        print(f"\n[System] Emergency vehicle detected.")

    def request_pedestrian_crossing(self):
        """
        Requests a pedestrian crossing.
        """
        self.pedestrian_requested = True
        print(f"\n[System] Pedestrian crossing requested.")

    def get_current_time(self):
        """
        Returns the current elapsed time since the start of the simulation.
        """
        elapsed_time = time.time() - self.start_time
        return f"{elapsed_time:.2f} seconds"

    def run(self):
        """
        Runs the traffic light system continuously.
        """
        print(f"Traffic Light FSM initialized in {self.state} state.")
        while True:
            self.transition()

# Background thread for automatic pedestrian requests
def simulate_pedestrian_requests(fsm, interval=15):
    while True:
        time.sleep(interval)  # Wait for the interval
        fsm.request_pedestrian_crossing()

# Background thread for automatic emergency vehicle detection
def simulate_emergency_vehicle_detection(fsm, interval=60):
    while True:
        time.sleep(interval)  # Wait for the interval
        fsm.detect_emergency_vehicle()

# Main execution
if __name__ == "__main__":
    fsm = TrafficLightFSM()

    # Start threads for automatic pedestrian requests and emergency vehicle detection
    threading.Thread(target=simulate_pedestrian_requests, args=(fsm,), daemon=True).start()
    threading.Thread(target=simulate_emergency_vehicle_detection, args=(fsm,), daemon=True).start()

    # Run the traffic light FSM
    fsm.run()