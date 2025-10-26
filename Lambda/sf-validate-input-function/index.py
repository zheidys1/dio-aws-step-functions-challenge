import json 

def lambda_handler(event, context):
    """
    Função para simular a validação de entrada e retornar um status.
    O Step Function (Choice State) usará o campo 'isValid' para tomar a decisão.
    """

    print("Evento recebido do Step Functions:", event)

    # 1. Simulação de Lógica: Assumimos que o input é válido
    # ...

    validation_status = True  

    # 2. Retorno: O retorno da Lambda é a entrada para o próximo estado do Step Function
    return {
        "statusCode": 200,
        # ESTE CAMPO É O MAIS IMPORTANTE para o Choice State:
        "isValid": validation_status,  
        "original_input": event 
    }