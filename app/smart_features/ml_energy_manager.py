from sklearn.linear_model import LinearRegression
import numpy as np

class MLEnergyManager:
    def __init__(self):
        self.comfort_model = LinearRegression()
        self.training_data = []
        
    def learn_comfort_preferences(self, room_id: str, temperature: float, 
                                humidity: float, occupancy: bool, 
                                user_feedback: int):
        """Learn from user comfort feedback (1-5 scale)"""
        self.training_data.append([temperature, humidity, occupancy, user_feedback])
        
        if len(self.training_data) >= 10:  # Minimum training samples
            X = np.array(self.training_data)[:, :-1]
            y = np.array(self.training_data)[:, -1]
            self.comfort_model.fit(X, y)
            
    def get_optimal_temperature(self, humidity: float, occupancy: bool) -> float:
        """Predict optimal temperature based on learned preferences"""
        if not self.comfort_model.coef_.any():
            return 24.0  # Default if not enough training data
            
        # Test range of temperatures
        test_temps = np.linspace(20, 28, 80)
        best_temp = 24.0
        best_score = 0
        
        for temp in test_temps:
            score = self.comfort_model.predict([[temp, humidity, occupancy]])[0]
            if score > best_score:
                best_score = score
                best_temp = temp
                
        return best_temp 