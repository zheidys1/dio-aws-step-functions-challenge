import json
def lambda_handler(event, context):
    """
    Função para simular o envio de uma notificação (e-mail, SMS via SNS, etc.).
    Recebe os dados processados do estado anterior.
    """

    print("Dados finais para notificação:", event)

    # Simulação do Envio:
    notification_id = "MSG-ID-SUCCESS-" + str(context.aws_request_id)

    # 1. Retorno: O Step Function seguirá para o estado Succeed/End.
    return {
        "statusCode": 200,
        "notificationStatus": "SENT",
        "messageId": notification_id
    }