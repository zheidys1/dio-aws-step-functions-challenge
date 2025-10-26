import json

def lambda_handler(event, context):
    """
    Função para simular o processamento principal dos dados.
    Recebe os dados do estado anterior (Validate Input).
    """
    
    print("Processando dados recebidos:", event)
    
    # 1. Simulação de Sucesso: Assumimos que o processamento funcionou.
    processing_successful = True 
    
    # 2. Se a Lambda for bem-sucedida, ela apenas retorna uma confirmação
    return {
        "statusCode": 200,
        "processingStatus": "COMPLETED",
        "wasSuccessful": processing_successful,
        # Você pode passar adiante a entrada original para a notificação
        "final_data": event.get('original_input')
    }