# VanaTensor Satya Proof of Contribution

This repository creating a [proof of contribution](https://docs.vana.org/vana/core-concepts/key-elements/proof-of-contribution) tasks using Python. It is executed on Vana's Satya Network, a group of highly confidential and secure compute nodes that can validate data without revealing its contents to the node operator.

## Overview

This poc provides a basic structure for building proof tasks that:

1. Read input files from the `/input` directory.
2. Process the data securely, running any necessary validations to prove the data authentic, unique, high quality, etc.
3. Write proof results to the `/output/results.json`
The project is designed to work with Intel TDX (Trust Domain Extensions), providing hardware-level isolation and security guarantees for confidential computing workloads.

## Project Structure

- `my_proof/`: Contains the main proof logic
  - `proof.py`: Implements the proof generation logic
  - `__main__.py`: Entry point for the proof execution
  - `models/`: Data models for the proof system
- `Dockerfile`: Defines the container image for the proof task
- `requirements.txt`: Python package dependencies

## Customizing the Proof Logic

The main proof logic is implemented in `my_proof/proof.py`. To customize it, update the `Proof.generate()` function to change how input files are processed.

The proof can be configured using environment variables:

- `USER_EMAIL`: The email address of the data contributor, to verify data ownership

## Local Development

To setup venv and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
```

To run the proof locally for testing, you can use Docker:

```bash
docker build -t my-proof .
```

```bash
docker run --rm --volume $(pwd)/input:/input --volume $(pwd)/output:/output -e AWS_ACCESS_KEY_ID=<your-access-key-id> -e AWS_SECRET_ACCESS_KEY=<your-secret-access-key> my-proof
```

## Running with Intel TDX

Intel TDX (Trust Domain Extensions) provides hardware-based memory encryption and integrity protection for virtual machines. To run this container in a TDX-enabled environment, follow your infrastructure provider's specific instructions for deploying confidential containers.

Common volume mounts and environment variables:

```bash
docker run --rm --volume /path/to/input:/input --volume /path/to/output:/output -e AWS_ACCESS_KEY_ID=<your-access-key-id> -e AWS_SECRET_ACCESS_KEY=<your-secret-access-key> my-proof
```

Remember to populate the `/input` directory with the files you want to process.

[MIT License](LICENSE)
