# RAG-Based Customer Service ChatBot

A simple MERN (MongoDB, Express, React, Node.js) chatbot that uses a Retrieval-Augmented Generation (RAG) setup to give more accurate answers.

## Why I Built This

I read a BBC article about chatbot mistakes in travel services and wanted to try fixing wrong or made-up answers. the link of the article is here: 
https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know
By adding RAG, the bot checks real documents before answering.

## What It Does

* **Fetches Info:** Finds related text from a document store.
* **Grounded Replies:** Uses that text to guide the language model.
* **Real-Time Chat:** Chat interface built with WebSocket.

## Tech Stack

* **Backend:** Node.js, Express, WebSocket, MongoDB
* **Frontend:** React, Context API
* **RAG:** OpenAI embeddings + simple vector database

## Quick Start

1. Clone:

   ```bash
   git clone https://github.com/Siva-K67/RAG-Based-Customer-Service-ChatBot.git
   ```
2. Install:

   ```bash
   # Server
   cd chatserver && npm install
   # Client
   cd ../chat-frontend && npm install
   ```
3. Set environment variables in `chatserver/.env`:

   ```env
   MONGODB_URI=...
   OPENAI_API_KEY=...
   VECTOR_DB_URL=...
   ```
4. Run:

   ```bash
   # In one terminal
   cd chatserver && npm start
   # In another
   cd chat-frontend && npm start
   ```
5. Open `http://localhost:3000` in your browser and chat!

## Contributing

Feel free to file issues or PRs. If you want more details here, just ask.

## License

MIT License

**Inspired by:** BBC Travel article "Air Canada Chatbot Misinformation" (Feb 22, 2024).
