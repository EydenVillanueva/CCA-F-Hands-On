import { loadEnvFile } from "node:process";

loadEnvFile();

import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const MODEL = "claude-sonnet-4-6";
const messages: Anthropic.MessageParam[] = [];

const chat = async (
  messages: Anthropic.MessageParam[],
  max_tokens: number = 1024,
): Promise<Anthropic.Message> => {

  const params = {
    model: MODEL,
    max_tokens,
    messages,
  };

  const message = await client.messages.create(params);
  return message;
}

const addUserMessage = (
  messages: Anthropic.MessageParam[],
  content: string | Anthropic.ContentBlockParam[]
) => {
  messages.push({ 
    role: "user", 
    content
  });
}

const addAssistantMessage = (messages : Anthropic.MessageParam[], message: Anthropic.Message) => {
  messages.push({ 
    role: "assistant",
    content: message.content,
  });
}


const agentLoop = async () => {
  const initial_prompt = "Hola mundo! como estás?";
  addUserMessage(messages, initial_prompt);

  while(true) {
    const response = await chat(messages);

    addAssistantMessage(messages, response)

    if(response.stop_reason !== "tool_use") break;
  }
}

agentLoop();