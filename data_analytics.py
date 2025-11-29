import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob
import json
import re

# ==============================================================================
# CONFIGURAÇÃO DE CAMINHOS POR LINGUAGEM
# ==============================================================================

# Mapeia caminhos para linguagens
PATHS_BY_LANG = {
    "Python": "/Users/pedro3pv/Documents/GitHub/nabor-trab6/trabalho-tecnologias-remotas-python",
    "TypeScript": "/Users/pedro3pv/Documents/GitHub/nabor-trab6/trabalho-tecnologias-remotas"
}

# Padrões das tecnologias (com curingas)
PATTERNS = {
    "REST": "*locust*rest*",
    "SOAP": "*locust*soap*",
    "GraphQL": "*locust*graphql*",
    "gRPC": "*locust*grpc*"
}

# ==============================================================================
# FUNÇÕES DE EXTRAÇÃO (PARSERS)
# ==============================================================================

def extract_json_from_html(content):
    """Parser robusto para extrair 'window.templateArgs' do HTML."""
    marker = 'window.templateArgs ='
    start_idx = content.find(marker)
    if start_idx == -1: return None
    
    json_start = content.find('{', start_idx)
    if json_start == -1: return None
        
    brace_count = 0
    json_end = -1
    
    for i, char in enumerate(content[json_start:], start=json_start):
        if char == '{': brace_count += 1
        elif char == '}': brace_count -= 1
        if brace_count == 0:
            json_end = i + 1
            break
            
    if json_end != -1:
        try:
            return json.loads(content[json_start:json_end])
        except:
            return None
    return None

def extract_history_from_html(file_path, limit_seconds=120):
    """Lê HTML e extrai métricas dos primeiros N segundos."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        data = extract_json_from_html(content)
        if not data or 'history' not in data: return None
        
        history = data['history']
        processed = []
        
        for row in history:
            try:
                # [Timestamp, Value] -> Pega Value
                rps = row['current_rps'][1] if row.get('current_rps') else 0
                avg_resp = row['total_avg_response_time'][1] if row.get('total_avg_response_time') else 0
                processed.append({'rps': rps, 'avg_resp': avg_resp})
            except: continue
                
        df = pd.DataFrame(processed)
        if df.empty: return None
        
        # Corte temporal
        df_cut = df.head(limit_seconds)
        
        return {
            "RPS": df_cut['rps'].mean(),
            "Latência": df_cut.iloc[-1]['avg_resp'] if not df_cut.empty else 0,
            "Fonte": "HTML (2min)"
        }
    except:
        return None

def find_file_in_dir(base_dir, pattern, extension):
    """Busca recursiva dentro de um diretório base específico."""
    search_str = os.path.join(base_dir, "**", f"{pattern}*{extension}")
    files = glob.glob(search_str, recursive=True)
    if not files: return None
    return max(files, key=os.path.getmtime)

def process_data():
    results = []
    
    print(f"{'='*80}")
    print(f"{'COMPARATIVO PYTHON vs TYPESCRIPT (CORTE 2 MINUTOS)':^80}")
    print(f"{'='*80}")

    for lang, base_path in PATHS_BY_LANG.items():
        print(f"\n📂 Processando Linguagem: {lang.upper()}")
        
        for tech, pattern in PATTERNS.items():
            # 1. Tenta HTML (Melhor precisão)
            html_file = find_file_in_dir(base_path, pattern, ".html")
            data_found = False
            
            if html_file:
                stats = extract_history_from_html(html_file)
                if stats:
                    results.append({
                        "Linguagem": lang,
                        "Tecnologia": tech,
                        "RPS": stats["RPS"],
                        "Latência": stats["Latência"],
                        "Fonte": stats["Fonte"]
                    })
                    print(f"   ✅ {tech}: HTML processado.")
                    data_found = True
            
            # 2. Fallback CSV (Resumo total)
            if not data_found:
                csv_file = find_file_in_dir(base_path, pattern, "_requests.csv")
                if csv_file:
                    try:
                        df = pd.read_csv(csv_file)
                        agg = df[df['Name'].astype(str).str.contains('Aggregated|Total', case=False, na=False)]
                        if agg.empty: agg = df.iloc[[-1]]
                        
                        results.append({
                            "Linguagem": lang,
                            "Tecnologia": tech,
                            "RPS": agg['Requests/s'].values[0],
                            "Latência": agg['Average Response Time'].values[0],
                            "Fonte": "CSV (Total)"
                        })
                        print(f"   ⚠️  {tech}: Usando CSV fallback.")
                    except:
                        print(f"   ❌ {tech}: Erro ao ler CSV.")
                else:
                    print(f"   ❌ {tech}: Nenhum arquivo encontrado.")

    return pd.DataFrame(results)

# ==============================================================================
# PLOTAGEM
# ==============================================================================

if __name__ == "__main__":
    df = process_data()

    if not df.empty:
        # Ordenar para visualização consistente
        df = df.sort_values(by=["Tecnologia", "Linguagem"])
        
        print("\n" + "="*80)
        print("TABELA DE RESULTADOS")
        print("="*80)
        print(df[["Linguagem", "Tecnologia", "RPS", "Latência", "Fonte"]].to_string(index=False))
        print("="*80 + "\n")

        sns.set_theme(style="whitegrid")
        
        # Gráfico 1: Throughput (RPS) - Agrupado
        plt.figure(figsize=(12, 6))
        ax1 = sns.barplot(
            data=df, 
            x="Tecnologia", 
            y="RPS", 
            hue="Linguagem", 
            palette="viridis"
        )
        ax1.set_title("Throughput: Python vs TypeScript (RPS)", fontsize=16, fontweight='bold')
        ax1.set_ylabel("Requisições / Segundo")
        for c in ax1.containers: ax1.bar_label(c, fmt='%.0f', padding=3)
        plt.tight_layout()
        plt.savefig("comparativo_lang_rps.png")
        print("📊 Salvo: comparativo_lang_rps.png")

        # Gráfico 2: Latência - Agrupado
        plt.figure(figsize=(12, 6))
        ax2 = sns.barplot(
            data=df, 
            x="Tecnologia", 
            y="Latência", 
            hue="Linguagem", 
            palette="rocket"
        )
        ax2.set_title("Latência Média: Python vs TypeScript (ms)", fontsize=16, fontweight='bold')
        ax2.set_ylabel("Tempo de Resposta (ms)")
        for c in ax2.containers: ax2.bar_label(c, fmt='%.2f', padding=3)
        plt.tight_layout()
        plt.savefig("comparativo_lang_latencia.png")
        print("📊 Salvo: comparativo_lang_latencia.png")
        
    else:
        print("Nenhum dado encontrado nos diretórios especificados.")
