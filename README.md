## AI Lead Qualification Automation

## Overview

This project automates the process of analyzing and qualifying sales leads using AI. The system reads leads from a CSV file, evaluates them using an AI model, scores them, and outputs the results into a structured CSV for the sales team.

## Goal:
Automatically determine lead quality, business needs, and recommended sales actions to reduce manual work.

## Workflow Diagram
        +------------+
        | New Leads  |  <- leads.csv
        +------------+
              |
              v
   +--------------------+
   | Python Script      |
   | Reads CSV & Sends  |
   | Each Lead to AI    |
   +--------------------+
              |
              v
   +--------------------+
   | AI Analysis        |
   | (Industry, Lead    |
   | Score, Business    |
   | Need, Action)      |
   +--------------------+
              |
              v
   +--------------------+
   | Lead Scoring &     |
   | Priority (High /   |
   | Medium / Low)      |
   +--------------------+
              |
              v
   +--------------------+
   | Output CSV         |
   | (output.csv)       |
   +--------------------+

## Features

* Fully automated analysis of leads from a CSV file

* Generates:

  * Industry

  * Lead Score (0–100)

  * Lead Priority (High / Medium / Low)

  * Business Need

  * Recommended Sales Action

* Handles invalid AI output safely

* Ready-to-use output.csv for sales team

## Setup Instructions

1. Clone the repository: 
    git clone <your-repo-url>
    cd AI-Lead-Qualification

2. Install dependencies
    pip install openai pandas

3. Add your API key in analyze_leads.py:
    client = OpenAI(
    api_key="YOUR_GROQ_KEY",
    base_url="https://api.groq.com/openai/v1"
)

4. Prepare your leads CSV (leads.csv) with columns:
    * Name
    * Email
    * Company Name
    * Job Title
    * Message

5. Run the automation script
    python analyze_leads.py

6. Check the output (output.csv will include:)
    * Name
    * Email
    * Company Name
    * Job Title
    * Industry
    * Lead Score
    * Lead Priority
    * Business Need
    * Recommended Action
    
