from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    """
    Formato de carga em degraus:
    - Começa com 100 usuários
    - Aumenta 100 a cada 5 segundos
    - Máximo de 1000 usuários
    """
    
    step_time = 5
    step_load = 100
    spawn_rate = 100
    time_limit = 180  # 3 minutos
    
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time > self.time_limit:
            return None
        
        current_step = run_time // self.step_time
        user_count = min(100 + current_step * self.step_load, 1000)
        
        return (user_count, self.spawn_rate)
