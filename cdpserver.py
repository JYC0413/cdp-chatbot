from flask import Flask, render_template, request, jsonify, session
from chatbot import initialize_agent, run_chat_mode
import pickle

app = Flask(__name__)
app.secret_key = 'cdp_secret_key'

global agent_executor, config


# 用于处理聊天的路由
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # 调用原本的聊天功能
    response = run_chat_mode(agent_executor, config, user_input)
    return jsonify({"response": response})


@app.route('/initialize', methods=['POST'])
def initialize():
    # 获取用户输入的五个值
    base_url = request.json.get('base_url')
    api_key = request.json.get('api_key')
    model = request.json.get('model')
    cdp_api_key_name = request.json.get('cdp_api_key_name')
    cdp_api_key_private_key = request.json.get('cdp_api_key_private_key')

    if not all([base_url, api_key, model, cdp_api_key_name, cdp_api_key_private_key]):
        return jsonify({"error": "All fields are required!"}), 400

    # 调用 initialize_agent 来初始化代理
    agent_executor, config = initialize_agent(
        base_url, api_key, model, cdp_api_key_name, cdp_api_key_private_key
    )

    print(agent_executor)
    print(config)

    return jsonify({"message": "Agent initialized successfully!"}), 200

# 页面渲染的路由
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=413)
