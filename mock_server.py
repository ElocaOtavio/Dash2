"""
Servidor mock para simular a API da Eloca durante os testes
"""
from flask import Flask, send_file, request, jsonify
import os
from test_data_generator import TestDataGenerator

app = Flask(__name__)

@app.route('/Relatorios/excel')
def mock_eloca_api():
    """Simula a API da Eloca retornando arquivo Excel"""
    
    # Verificar token (simulado)
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token não fornecido"}), 400
    
    # Verificar header DeskManager (simulado)
    desk_manager = request.headers.get('DeskManager')
    if not desk_manager:
        return jsonify({"error": "Header DeskManager não fornecido"}), 400
    
    # Gerar dados de teste se não existir o arquivo
    arquivo_teste = "/home/ubuntu/eloca-dashboard/dados_teste.xlsx"
    if not os.path.exists(arquivo_teste):
        generator = TestDataGenerator()
        generator.salvar_excel_teste(arquivo_teste)
    
    # Retornar arquivo Excel
    return send_file(
        arquivo_teste,
        as_attachment=True,
        download_name="relatorio_eloca.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        "status": "ok",
        "message": "Mock server da Eloca funcionando",
        "endpoints": ["/Relatorios/excel", "/health"]
    })

if __name__ == "__main__":
    print("🚀 Iniciando servidor mock da Eloca...")
    print("📍 Endpoints disponíveis:")
    print("  - GET /Relatorios/excel?token=<token> (com header DeskManager)")
    print("  - GET /health")
    print("🌐 Servidor rodando em: http://localhost:5000")
    
    app.run(host="0.0.0.0", port=5000, debug=True)

