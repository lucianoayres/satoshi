# ⚡₿ Satoshi

![Satoshi Banner](https://github.com/lucianoayres/satoshi/blob/main/images/satoshi_banner_optimized.png?raw=true)

## Take Full Control of Your Automated Crypto Investments

[Features](#features) · [Prerequisites](#prerequisites) · [Installation](#installation) · [Usage](#usage) · [Order Details Storage](#order-details-storage) · [Automation with GitHub Actions](#automation-with-github-actions) · [Creating a Fully Automated Flow](#creating-a-fully-automated-flow) · [Contributing](#contributing) · [License](#license) · [Disclaimer](#disclaimer)

## What's Satoshi?

**Satoshi** is a crypto-bot that automates your monthly cryptocurrency investments on **Mercado Bitcoin**, making it effortless to grow your crypto portfolio. This solution is entirely under your control, relying solely on your own setup without dependency on third-party applications.

-   NOTE: Satoshi is **not an official application** of Mercado Bitcoin.

## Features

-   📅 **Flexible Investment Scheduling**: Customize your crypto purchase frequency.
-   🔒 **Secure Authentication**: Utilizes Mercado Bitcoin's API securely.
-   ⚙️ **Customizable Parameters**: Choose your crypto symbol, currency, and investment amount.
-   🛡️ **User-Controlled Solution**: Fully managed by you without reliance on third-party services.

## Prerequisites

-   **Software Requirements**
    -   Python 3.x
    -   Git
-   **API Credentials**
    -   [Mercado Bitcoin API](https://api.mercadobitcoin.net/) credentials (API ID and API Secret)
-   **GitHub Account**
    -   For setting up automation with GitHub Actions

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/lucianoayres/satoshi.git
    cd satoshi
    ```

2. **Set Up Virtual Environment and Install Dependencies**

    ```bash
    make setup
    ```

3. **Configure Environment Variables**

    - Create a `.env` file in the root directory using the provided example:

        ```bash
        cp .env.example .env
        ```

    - Open `.env` and add your Mercado Bitcoin API credentials and desired investment parameters:

        ```ini
        MERCADO_BITCOIN_API_ID=your_api_id
        MERCADO_BITCOIN_API_SECRET=your_api_secret
        ```

        - **IMPORTANT:** Add `.env` to `.gitignore` to protect your API keys from being exposed.

## Usage

Execute the script:

```bash
python src/main.py [SYMBOL] [CURRENCY] [COST]
```

**Example:**

```bash
python src/main.py BTC BRL 100
```

## Order Details Storage

After running the script **or** the GitHub Actions workflow successfully, the order details are saved in the `./data` directory located at the root of the project. The JSON files follow the `{SYMBOL}-{CURRENCY}-orders.json` naming pattern.

**Example File Path:**

-   `./data/BTC-BRL-orders.json`  
    [View Example File](./data/BTC-BRL-orders.json)

> **Note:** The `./data` directory and corresponding JSON files are generated whenever the script runs successfully, either manually or through the GitHub Actions workflow. When using the workflow, the JSON files are also committed and pushed to the remote repository.

**Example Order Detail JSON Structure:**

```json
{
    "symbol": "BTC",
    "currency": "BRL",
    "cost": 100,
    "order_id": "1234567890",
    "timestamp": "2024-12-01T07:15:00Z",
    "status": "completed"
}
```

This structure helps in organizing and easily locating your investment records based on the cryptocurrency symbol and the currency used for the investment.

## Automation with GitHub Actions

Automate your investments using GitHub Actions. The [workflow](.github/workflows/monthly_investment_automation.yml) is set to run monthly at 7:15 AM UTC on the 1st.

1. **Add Secrets to GitHub Repository**

    - Navigate to your repository settings.
    - Under **Secrets and variables** > **Actions**, add:
        - `MERCADO_BITCOIN_API_ID`
        - `MERCADO_BITCOIN_API_SECRET`

2. **Set Repository Variables**

    - Under **Variables**, add:
        - `SYMBOL` (e.g., `BTC`)
        - `CURRENCY` (e.g., `BRL`)
        - `COST` (e.g., `100`)

3. **Customize Workflow (Optional)**

    - Modify [`.github/workflows/monthly_investment_automation.yml`](.github/workflows/monthly_investment_automation.yml) to adjust the schedule or parameters.

## Creating a Fully Automated Flow

To create a seamless, fully automated investment process, follow these steps:

1. **Schedule Monthly PIX Transfers**

    - Set up recurring PIX payments in your bank app to Mercado Bitcoin, ensuring the amount and timing align with Satoshi’s investment schedule.

2. **Integrate with Satoshi**

    - Synchronize transfer dates a day before the automated investment runs, monitor transactions, and update settings if investment amounts change.

3. **Ensure Security and Reliability**
    - Enable transaction notifications, securely store API credentials, and perform test runs to confirm the automated system works smoothly.

This setup allows Satoshi to automatically invest your monthly funds, growing your crypto portfolio effortlessly.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. 🤝

## License

This project is licensed under the [MIT License](LICENSE). 📄

## Disclaimer

**Satoshi** is an independent project developed and maintained by the community. It is **not affiliated with or endorsed by Mercado Bitcoin**. All operations are conducted under your control, and you are responsible for managing your API credentials and ensuring the security of your investments. Use this tool at your own risk.
