import datetime
import json
import openai

import db


def detect_variables(text: str, owner_id: int) -> (bool, db.Operation):
    messages = [
        {'role': 'system', 'content': 'Write answer:'},
        {"role": "user", "content": text}]
    functions = [
        {
            "name": "Function",
            "description": "Func description",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        'description': "Здесь указывай источник дохода одним словом (если есть) или пиши не установлен"
                    },
                    'amount': {
                        "type": "integer"
                    },
                    'is_income': {
                        "type": "string",
                        'enum': ['0', '1']
                    }
                },
                "required": ["description", 'amount', 'is_income'],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response["choices"][0]["message"]
    if response_message.get("function_call"):
        try:
            function_args = json.loads(response_message["function_call"]["arguments"])
        except:
            return False, None
        return True, db.Operation(
            owner=owner_id,
            description=function_args['description'].lower(), amount=abs(function_args['amount']),
            is_income=bool(int(function_args['is_income'])), date=datetime.datetime.now().date())
    else:
        return False, None
