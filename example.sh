# --- Configuration ---
# Use your LAN IP (e.g., "192.168.18.88") 
VLLM_SERVER_IP="192.168.18.88" 

VLLM_SERVER_PORT="8000"

# --- Define your prompts following the ChatML format for Phi-3 Instruct ---


PROMPT_TEXT_1="<|user|>\nWrite what you think are the best scenes of the bee movie<|end|>\n<|assistant|>"


# --- Choose which prompt to use ---

SELECTED_PROMPT="${PROMPT_TEXT_1}"

# --- Generation Parameters ---
MAX_TOKENS=256
TEMPERATURE=0.7
N_COMPLETIONS=1
# Stop sequences for Phi-3 Instruct
STOP_SEQUENCES='["<|endoftext|>", "<|end|>"]'

# --- Construct the JSON payload ---
JSON_PAYLOAD=$(printf '{
  "prompt": "%s",
  "max_tokens": %d,
  "temperature": %.1f,
  "n": %d,
  "stop": %s
}' "${SELECTED_PROMPT}" "${MAX_TOKENS}" "${TEMPERATURE}" "${N_COMPLETIONS}" "${STOP_SEQUENCES}")

# --- Execute the curl command ---
echo "Querying vLLM server at http://${VLLM_SERVER_IP}:${VLLM_SERVER_PORT}"
echo "Prompt: $(echo "${SELECTED_PROMPT}" | sed 's/<|user|>//g; s/<|end|>//g; s/<|assistant|>//g')" # Print cleaned prompt for readability

JSON_PAYLOAD='{
  "prompt": "Your input prompt here",
  "max_tokens": 2000,      
  "temperature": 0.7,     
  "n": 1
}'

curl -X POST \
     -H "Content-Type: application/json" \
     -d "${JSON_PAYLOAD}" \
     http://${VLLM_SERVER_IP}:${VLLM_SERVER_PORT}/v1/completions

echo ""