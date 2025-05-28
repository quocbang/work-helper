
payload = {
    "name": "Thòng Quốc Bằng - 6ee6e92e-44fa-4ebc-b484-8e75fb85a5d2 - Recall",
    "nodes": [
        {
            "parameters": {
                "conditions": {
                    "options": {
                        "caseSensitive": True,
                        "leftValue": "",
                        "typeValidation": "strict",
                        "version": 2,
                    },
                    "conditions": [
                        {
                            "id": "afb17e62-f67e-4d60-aae4-d74ac20f9a7f",
                            "leftValue": "={{ $json.message.reply_to_message }}",
                            "rightValue": "",
                            "operator": {
                                "type": "object",
                                "operation": "exists",
                                "singleValue": True,
                            },
                        }
                    ],
                    "combinator": "and",
                },
                "options": {},
            },
            "type": "n8n-nodes-base.if",
            "typeVersion": 2.2,
            "position": [-420, 120],
            "id": "f5fb8677-fe3c-48e8-88f1-bc52aeae40bf",
            "name": "If",
        },
        {
            "parameters": {
                "resource": "audio",
                "operation": "transcribe",
                "options": {},
            },
            "type": "@n8n/n8n-nodes-langchain.openAi",
            "typeVersion": 1.8,
            "position": [320, 220],
            "id": "e97df86d-7061-4350-b18f-56aa556587aa",
            "name": "STT",
            "credentials": {
                "openAiApi": {"id": "tPwD7FhrZhxXH0um", "name": "OpenAi account"}
            },
        },
        {
            "parameters": {
                "mode": "raw",
                "jsonOutput": '={\n  "message": {\n    "message_id": {{ $(\'Check message type\').item.json.message.message_id }},\n    "text": {{ $json.text.toJsonString() }},\n    "reply_to_message": {\n      "text": {{ $(\'Check message type\').item.json.message.reply_to_message.text.toJsonString() }}\n    }\n  }\n}',
                "options": {},
            },
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.4,
            "position": [540, 220],
            "id": "277d99d3-f529-49bc-8162-82002c1cf0e6",
            "name": "Edit Fields",
        },
        {
            "parameters": {
                "language": "python",
                "pythonCode": '# Loop over input items and add a new field called \'myNewField\' to the JSON of each one\nimport re\n\nresult = []\nfor item in _input.all():\n  if not item.json:\n    return {\n      "is_sucesss": "false",\n      "error_message": "There is not a reply message"\n    }\n    \n  if not item.json.message.reply_to_message:\n    return {\n      "is_sucesss": "false",\n      "error_message": "There is not a reply message"\n    }\n    \n  match = re.search(r\'"[^"]*"\', item.json.message.reply_to_message.text)\n  if match:\n      result.append({\n        "is_success": "true",\n        "learning_content": match.group(0).replace(\'"\', \'\'),\n        "chat_id": item.json.message.message_id,\n        "text": item.json.message.text,\n      })\n    \nreturn result\n\n',
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [880, 120],
            "id": "53a7fba1-b831-46bb-8dfe-7ce381a42181",
            "name": "Code",
        },
        {
            "parameters": {"updates": ["message"], "additionalFields": {}},
            "type": "n8n-nodes-base.telegramTrigger",
            "typeVersion": 1.1,
            "position": [-680, 120],
            "id": "8b1857fd-c0be-40fd-9287-9d2c067c912a",
            "name": "Listen message from telegram",
            "webhookId": "07020580-f138-4623-a747-80211f724a71",
            "credentials": {"telegramApi": {"id": "lgZKVlRqLEZuaL5G", "name": ""}},
        },
        {
            "parameters": {
                "rules": {
                    "values": [
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict",
                                    "version": 2,
                                },
                                "conditions": [
                                    {
                                        "leftValue": "={{ $json.message.text }}",
                                        "rightValue": "",
                                        "operator": {
                                            "type": "string",
                                            "operation": "exists",
                                            "singleValue": True,
                                        },
                                        "id": "ff444a08-243e-4db0-8ae6-d39c13612813",
                                    }
                                ],
                                "combinator": "and",
                            },
                            "renameOutput": True,
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": True,
                                    "leftValue": "",
                                    "typeValidation": "strict",
                                    "version": 2,
                                },
                                "conditions": [
                                    {
                                        "id": "7ba13994-9f54-4d0b-8fc4-684507f765af",
                                        "leftValue": "={{ $json.message.voice }}",
                                        "rightValue": "",
                                        "operator": {
                                            "type": "object",
                                            "operation": "exists",
                                            "singleValue": True,
                                        },
                                    }
                                ],
                                "combinator": "and",
                            },
                            "renameOutput": True,
                        },
                    ]
                },
                "options": {},
            },
            "type": "n8n-nodes-base.switch",
            "typeVersion": 3.2,
            "position": [-80, 120],
            "id": "5d1946b9-5e6f-4317-8348-73eba2a46311",
            "name": "Check message type",
        },
        {
            "parameters": {
                "operation": "executeQuery",
                "query": "SELECT trigger_config\n\tFROM account_triggers\n  WHERE lower(account_triggers.trigger_type) = 'telegram' AND account_triggers.account_id = '6ee6e92e-44fa-4ebc-b484-8e75fb85a5d2'",
                "options": {},
            },
            "type": "n8n-nodes-base.postgres",
            "typeVersion": 2.6,
            "position": [1120, 260],
            "id": "3ca6a405-5549-4679-83e0-522c3f2e55d9",
            "name": "Get Trigger Config",
            "credentials": {
                "postgres": {"id": "RXCaL5ue473L9k7m", "name": "Postgres account"}
            },
        },
        {
            "parameters": {"mode": "combine", "combineBy": "combineAll", "options": {}},
            "type": "n8n-nodes-base.merge",
            "typeVersion": 3.1,
            "position": [1460, 140],
            "id": "1f0de9d9-0c31-44e6-b712-eac0440a2e60",
            "name": "Merge",
        },
        {
            "parameters": {
                "method": "POST",
                "url": "http://host.docker.internal:5678/webhook/core-evaluator",
                "authentication": "genericCredentialType",
                "genericAuthType": "httpHeaderAuth",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "learning_content",
                            "value": "={{ $json.learning_content }}",
                        },
                        {"name": "chat_id", "value": "={{ $json.chat_id }}"},
                        {"name": "text", "value": "={{ $json.text }}"},
                        {"name": "account_id", "value": "ssss"},
                    ]
                },
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [1840, 140],
            "id": "c4841b1a-db0d-4942-b478-e6d7a71e111b",
            "name": "Do Evaluate",
            "credentials": {
                "httpHeaderAuth": {
                    "id": "k3Z3mAFD1Su4vbNU",
                    "name": "Work Helper API Key",
                }
            },
        },
        {
            "parameters": {
                "chatId": "={{ $('Merge').item.json.trigger_config.recall_bot.chat_id }}",
                "text": "={{ $json.message }}",
                "additionalFields": {
                    "parse_mode": "Markdown",
                    "reply_to_message_id": "={{ $('Merge').item.json.chat_id }}",
                },
            },
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.2,
            "position": [2120, 140],
            "id": "866b624b-c24a-47b7-a770-5c3268831535",
            "name": "Reply",
            "webhookId": "59a568bb-0c2e-4acf-93cc-b27c327d4479",
            "credentials": {"telegramApi": {"id": "lgZKVlRqLEZuaL5G", "name": ""}},
        },
        {
            "parameters": {
                "resource": "file",
                "fileId": "={{ $json.message.voice.file_id }}",
            },
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.2,
            "position": [140, 220],
            "id": "4f5585d8-682d-4c91-ab47-bc5aebd962a1",
            "name": "Get audio file",
            "webhookId": "9321d023-41bb-4a03-9a25-c5381b902489",
            "credentials": {"telegramApi": {"id": "lgZKVlRqLEZuaL5G", "name": ""}},
        },
    ],
    "connections": {
        "If": {"main": [[{"node": "Check message type", "type": "main", "index": 0}]]},
        "STT": {"main": [[{"node": "Edit Fields", "type": "main", "index": 0}]]},
        "Edit Fields": {"main": [[{"node": "Code", "type": "main", "index": 0}]]},
        "Code": {
            "main": [
                [
                    {"node": "Get Trigger Config", "type": "main", "index": 0},
                    {"node": "Merge", "type": "main", "index": 0},
                ]
            ]
        },
        "Listen message from telegram": {
            "main": [[{"node": "If", "type": "main", "index": 0}]]
        },
        "Check message type": {
            "main": [
                [{"node": "Code", "type": "main", "index": 0}],
                [{"node": "Get audio file", "type": "main", "index": 0}],
            ]
        },
        "Get Trigger Config": {
            "main": [[{"node": "Merge", "type": "main", "index": 1}]]
        },
        "Merge": {
            "main": [
                [
                    {"node": "Do Evaluate", "type": "main", "index": 0},
                    {"node": "HTTP Request", "type": "main", "index": 0},
                ]
            ]
        },
        "Do Evaluate": {"main": [[{"node": "Reply", "type": "main", "index": 0}]]},
        "Get audio file": {"main": [[{"node": "STT", "type": "main", "index": 0}]]},
        "HTTP Request": {"main": [[{"node": "Reply", "type": "main", "index": 0}]]},
    },
    "settings": {"executionOrder": "v1"},
}

for item in _input.all():
    nodes = payload["nodes"]
    for idx, node in enumerate(nodes):
        if node.get("credentials"):
            # replace telegram listener credential
            if node["credentials"].get("telegramApi"):
                nodes[idx]["credentials"]["telegramApi"]["id"] = item.json.credential_id
                nodes[idx]["credentials"]["telegramApi"][
                    "name"
                ] = item.json.credential_name

        # replace get trigger query
        match node["name"].lower():
            case "get trigger config":
                if (
                    node["parameters"].get("operation")
                    and node["parameters"]["operation"] == "executeQuery"
                ):
                    raw_get_trigger_config = f"SELECT trigger_config\n\tFROM account_triggers\n  WHERE lower(account_triggers.trigger_type) = 'telegram' AND account_triggers.account_id = '{item.json.body.account_id}'"
                    nodes[idx]["parameters"]["query"] = raw_get_trigger_config
            case "do evaluate":
                nodes[idx]["parameters"].update(
                    {
                        "bodyParameters": {
                            "parameters": [
                                {
                                    "name": "learning_content",
                                    "value": "{{ $json.learning_content }}",
                                },
                                {"name": "chat_id", "value": "{{ $json.chat_id }}"},
                                {
                                    "name": "text",
                                    "value": "{{ $json.text }}",
                                },
                                {
                                    "name": "account_id",
                                    "value": item.json.body.account_id,
                                },
                            ]
                        },
                    }
                )

    payload.update(
        {
            "name": item.json.workflow_name,
            "nodes": nodes,
        }
    )

return payload
