# pinecone-def-search

A Python toolkit to embed text data with OpenAI, upload it to Pinecone for vector search, and run semantic queries against the resulting index.

## Features

* Embeds text records using OpenAI's `text-embedding-3-small` model
* Creates a Pinecone vector index
* Uploads vectors in batches to Pinecone with metadata (case number, year, topic, etc.)
* Provides a simple query script to retrieve the most similar items for any query text

## Prerequisites

* Python 3.7 or higher
* An OpenAI API key
* A Pinecone account with an API key and environment
* A `database.json` file containing your text records

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/shriyanyamali/pinecone-def-search.git
   cd pinecone-def-search
   ```

2. **Create and activate a virtual environment**

   **macOS/Linux**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   **Windows PowerShell**

   ```powershell
   python -m venv .venv
   .\\.venv\\Scripts\\activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
## Docker Setup

This repository includes a `Dockerfile` to run the toolkit in a containerized environment. To build and run:

1. Build the Docker image:

   ```bash
   docker build -t pinecone-def-search .
   ```

2. Run the container for uploading data:

   ```bash
   docker run --rm \
     -e PINECONE_API_KEY=$PINECONE_API_KEY \
     -e PINECONE_ENV=$PINECONE_ENV \
     -e PINECONE_INDEX=$PINECONE_INDEX \
     -e OPENAI_API_KEY=$OPENAI_API_KEY \
     pinecone-def-search \
     python upload-pinecone.py
   ```

3. Run the container for querying:

   ```bash
   docker run --rm \
     -e PINECONE_API_KEY=$PINECONE_API_KEY \
     -e PINECONE_ENV=$PINECONE_ENV \
     -e PINECONE_INDEX=$PINECONE_INDEX \
     -e OPENAI_API_KEY=$OPENAI_API_KEY \
     -e QUERY_TEXT="energy market" \
     pinecone-def-search \
     python query-test.py
   ```

## Configuration

The scripts rely on environment variables to authenticate with OpenAI and Pinecone, and to set query parameters.

1. Create a `.env` file in the project root:

   ```dotenv
   PINECONE_API_KEY=           # Your Pinecone API key
   PINECONE_ENV=               # e.g. us-east-1-aws
   PINECONE_INDEX=             # Desired Pinecone index name
   OPENAI_API_KEY=             # Your OpenAI API key (sk-...)

   QUERY_TEXT="your query here"  # Default search query
   ```

2. (Optional) In PowerShell, you can set the same variables by running:

   ```powershell
   $env:PINECONE_API_KEY="your-key-here"
   $env:PINECONE_ENV="us-east-1-aws"
   $env:PINECONE_INDEX="my-index-name"
   $env:OPENAI_API_KEY="sk-..."
   $env:QUERY_TEXT="default search query"
   ```

## Usage

### 1. Upload Data to Pinecone

   ```bash
   python upload-pinecone.py
   ```

### 2. Query the Pinecone Index

   ```bash
   python query-test.py
   ```

## File Descriptions

* **.env**: Example environment settings for both Bash and PowerShell
* **upload-pinecone.py**: Embeds and uploads your text data to Pinecone
* **query-test.py**: Runs a semantic search against your Pinecone index
* **database.json**: Your input dataset; an array of objects with fields: case\_number, year, policy\_area, link, topic, text
