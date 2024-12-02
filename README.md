# ₿⚡ Satoshi

![Satoshi Banner](https://github.com/lucianoayres/satoshi/blob/main/images/satoshi_banner_optimized.png?raw=true)

## Take Full Control of Your Automated Crypto Investments

[Features](#features) · [Prerequisites](#prerequisites) · [Installation](#installation) · [Usage](#usage) · [Automation with GitHub Actions](#automation-with-github-actions) · [Creating a Fully Automated Flow](#creating-a-fully-automated-flow) · [Makefile Commands](#makefile-commands) · [Contributing](#contributing) · [License](#license) · [Disclaimer](#disclaimer)

## What's Satoshi?

**Satoshi** automates your monthly cryptocurrency investments on **Mercado Bitcoin**, making it effortless to grow your crypto portfolio with scheduled PIX transfers. This solution is entirely under your control, relying solely on your own setup without dependency on third-party applications. Please note that Satoshi is **not an official application** of Mercado Bitcoin.

## Features

-   📅 **Automated Monthly Investments**: Schedule your crypto purchases monthly.
-   🔒 **Secure Authentication**: Utilizes Mercado Bitcoin's API securely.
-   ⚙️ **Customizable Parameters**: Choose your crypto symbol, currency, and investment amount.
-   🛠️ **Easy Setup**: Simple installation with provided Makefile and requirements.
-   🔗 **Comprehensive Documentation**: Clear instructions and links to essential files for easy replication.
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

## Usage

Run the application manually:

```bash
make run
```

Or directly execute the script:

```bash
python src/main.py [SYMBOL] [CURRENCY] [COST]
```

**Example:**

```bash
python src/main.py BTC BRL 100
```

## Automation with GitHub Actions

Automate your investments using GitHub Actions. The workflow is set to run monthly at 7:15 AM UTC on the 1st.

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

    - Modify [`.github/workflows/automated_monthly_investment.yml`](.github/workflows/automated_monthly_investment.yml) to adjust the schedule or parameters.

## Creating a Fully Automated Flow

To create a seamless, fully automated investment process, follow these steps:

1. **Schedule Monthly PIX Transfers**

    - Set up recurring PIX payments in your bank app to Mercado Bitcoin, ensuring the amount and timing align with Satoshi’s investment schedule.

2. **Integrate with Satoshi**

    - Synchronize transfer dates a day before the automated investment runs, monitor transactions, and update settings if investment amounts change.

3. **Ensure Security and Reliability**
    - Enable transaction notifications, securely store API credentials, and perform test runs to confirm the automated system works smoothly.

This setup allows Satoshi to automatically invest your monthly funds, growing your crypto portfolio effortlessly.

## Makefile Commands

-   **Setup Environment**

    ```bash
    make setup
    ```

-   **Run Application**

    ```bash
    make run
    ```

-   **Run Tests**

    ```bash
    make test
    ```

-   **Build Package**

    ```bash
    make build
    ```

-   **Clean Environment**

    ```bash
    make clean
    ```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. 🤝

## License

This project is licensed under the [MIT License](LICENSE). 📄

## Disclaimer

**Satoshi** is an independent project developed and maintained by the community. It is **not affiliated with or endorsed by Mercado Bitcoin**. All operations are conducted under your control, and you are responsible for managing your API credentials and ensuring the security of your investments. Use this tool at your own risk.
