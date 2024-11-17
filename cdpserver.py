from flask import Flask, render_template, request, jsonify, session
from chatbot import initialize_agent, run_chat_mode

app = Flask(__name__)
app.secret_key = 'cdp_secret_key'


# 用于处理聊天的路由
@app.route('/chat', methods=['POST'])
def chat():
    base_url = "https://llamatool.us.gaianet.network/v1"
    api_key = "LLAMAEDGE"
    model = "llama"
    cdp_api_key_name = request.json.get('cdp_key_name')
    cdp_api_key_private_key = request.json.get('cdp_key_private_key')
    agent_executor, config = initialize_agent(
        base_url, api_key, model, cdp_api_key_name, cdp_api_key_private_key
    )
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # 调用原本的聊天功能
    response = run_chat_mode(agent_executor, config, user_input)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True, port=413)
