# Pinecone-OpenAI Project

This project provides a comprehensive solution for generating embeddings from text data using OpenAI and storing them in a Pinecone index for efficient retrieval. It includes a script for ingesting and processing data, as well as a Flask web application for conversational retrieval using the generated embeddings.

## Features

- **Data Ingestion and Embeddings Generation**: The ingestion script loads text data from the specified directory, splits the documents into smaller chunks, generates embeddings for each chunk using OpenAI, and stores the embeddings in a Pinecone index.

- **Conversational Retrieval**: The Flask web application provides an interface for conversational retrieval. It retrieves relevant responses based on user input using the embeddings stored in the Pinecone index.

- **Docker Support**: Both the ingestion script and the Flask web application can be containerized and deployed as Docker containers for easy deployment and scaling.

- **Environment Configuration**: The project uses environment variables for configuration, making it easy to customize and deploy in different environments.

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

## Installation and Usage

Detailed installation and usage instructions for the ingestion script and the Flask web application are provided in their respective directories:

- For the ingestion script, see the `README.md` file in the `ingestion` directory.
- For the Flask web application, see the `README.md` file in the `web-app` directory.
