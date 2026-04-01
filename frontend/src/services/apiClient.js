import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1';

// Create a generic axios instance (if needed for interceptors)
export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Sends original payload to FastAPI to be structurally parsed and mapped
 * to the automatically determined target Bedrock format based on the sourceModel.
 */
export const translatePrompt = async ({ sourcePrompt, sourceModel }) => {
  // Placeholder mock response for now, wires up to your real backend soon.
  try {
    const response = await api.post('/translate', {
      source_payload: sourcePrompt,
      source_model: sourceModel
    });
    return response;
  } catch (error) {
    // Return a mocked success object if backend is offline to test UI
    return new Promise(resolve => setTimeout(() => resolve({
      data: {
        converted_schema: {
          messages: [
            { role: "user", content: [{ text: "Simulated Bedrock Translation of your prompt" }] }
          ],
          system: "Simulated System Rules",
          anthropic_version: "bedrock-2023-05-31",
          max_tokens: 4096,
        },
        // The backend KI determines this mapping automatically!
        target_model: "anthropic.claude-3-5-sonnet-20240620-v1:0"
      }
    }), 1500));
  }
};

/**
 * Triggers dual execution on the backend (executing both source OpenAI and Bedrock concurrently).
 */
export const executeComparison = async ({ translatedPrompt, targetModel }) => {
  try {
    const response = await api.post('/compare', {
      payload: translatedPrompt,
      model: targetModel
    });
    return response;
  } catch (error) {
    // Return a mocked success object if backend is offline to test UI
    return new Promise(resolve => setTimeout(() => resolve({
      data: {
        latency: 1240,
        sourceOutput: "This is a streamed simulation response from your selected OpenAI source model.",
        targetOutput: "This is a simulated execution from Amazon Bedrock returning via the dual-invoke execution engine."
      }
    }), 3000));
  }
};

/**
 * Fire-and-forget metrics save endpoint to funnel execution data
 * into the AWS DynamoDB table via your backend.
 */
export const saveComparisonMetrics = async ({ source, destination, comparisonData }) => {
  try {
    await api.post('/report/save', {
      source_model: source,
      destination_model: destination,
      metrics: comparisonData,
      timestamp: new Date().toISOString()
    });
    console.log("DynamoDB Payload Sent Successfully.");
  } catch (error) {
    console.warn("Could not save to DynamoDB. Backend /report/save likely offline.", error);
  }
};