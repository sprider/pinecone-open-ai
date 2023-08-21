
# Pinecone-OpenAI Embeddings Generator

This script generates embeddings for files stored in the `pinecone-open-ai/ingestion/data` folder using OpenAI and stores the embeddings in a Pinecone index.

## Prerequisites

- Python 3.9 or higher
- Docker (optional)
- OpenAI API Key
- Pinecone API Key
- Pinecone Index Configuration:
  - Pod Type: Starter
  - Number of Pods: 1
  - Dimension: 1536
  - Metric: Cosine

## Clone the repository

```bash
   git clone https://github.com/sprider/pinecone-open-ai.git
```

## Setup virtual environment

Navigate to your project directory and create a virtual environment:

```bash
cd pinecone-open-ai/ingestion
python3 -m venv venv
```

This creates a new virtual environment named `venv` in your project directory.

## Activate the virtual environment

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific `python` and `pip` executables into your shell’s `PATH`.

On macOS and Linux:

```bash
source venv/bin/activate
```

## Install requirements

To install the Python packages that the application depends on, run the following command:

```bash
pip3 install -r requirements.txt
```

## Set environment variables

The application uses several environment variables that you'll need to set. You can set them in your shell, or you can put them in a `.env` file in the ingestion directory of the project. Here's what your `.env` file should look like:

```sh
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENV=your-pinecone-environment
PINECONE_INDEX_NAME=your-pinecone-index-name
```

Replace `your-openai-api-key`, `your-pinecone-api-key`, `your-pinecone-environment` and `your-pinecone-index-name` with your actual OpenAI API key, Pinecone API key, Pinecone Environment, and Pinecone Index Name.

## Running the script locally

You're now ready to run the scripts.

To ingest the data and generate embeddings for files stored in the `pinecone-open-ai/ingestion/data` folder using OpenAI, and then store the embeddings in a Pinecone index, use the following command:

```bash
python3 ingest.py
```

This script will load the documents from the specified directory, split the documents into smaller chunks, generate embeddings for each chunk using OpenAI, and store the embeddings in the Pinecone index specified in the environment variables.

## Running the Script in a Docker Container

Build the Docker image:

```bash
docker build -t pinecone_openai_embeddings_generator .
```

Run the Docker container with the necessary environment variables:

```bash
docker run -e OPENAI_API_KEY=your-openai-api-key -e PINECONE_API_KEY=your-openai-api-key -e PINECONE_ENV=your-pinecone-environment -e PINECONE_INDEX_NAME=your-pinecone-index-name -v $(pwd)/data:/app/data pinecone_openai_embeddings_generator
```
