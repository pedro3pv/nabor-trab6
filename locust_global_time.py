from locust import LoadTestShape

class StepLoadShape(LoadTestShape):
    """
    Formato de carga em degraus:
    - Começa com 100 usuários
    - Aumenta 100 a cada 5 segundos
    - Máximo de 1000 usuários
    - Para exatamente após 2 minutos
    """
    
    step_time = 5
    step_load = 100
    spawn_rate = 100
    time_limit = 120  # 2 minutos (120 segundos)
    
    def tick(self):
        run_time = self.get_run_time()
        
        # Para o teste se passar de 2 minutos
        if run_time > self.time_limit:
            return None
        
        current_step = run_time // self.step_time
        user_count = min(100 + current_step * self.step_load, 1000)
        
        return (user_count, self.spawn_rate)
