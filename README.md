# ₿⚡ Satoshi

![Satoshi Banner](https://github.com/lucianoayres/satoshi/blob/main/images/satoshi_banner_optimized.png?raw=true)

**Satoshi** automates your monthly cryptocurrency investments on **Mercado Bitcoin**, making it effortless to grow your crypto portfolio with scheduled PIX transfers. This solution is entirely under your control, relying solely on your own setup without dependency on third-party applications. Please note that Satoshi is **not an official application** of Mercado Bitcoin.

## Table of Contents

-   [Features](#features)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Automation with GitHub Actions](#automation-with-github-actions)
-   [Creating a Fully Automated Flow](#creating-a-fully-automated-flow)
-   [Makefile Commands](#makefile-commands)
-   [Contributing](#contributing)
-   [License](#license)
-   [Disclaimer](#disclaimer)
-   [Quick Links](#quick-links)

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

1. **Set Up PIX Transfer Scheduling in Your Bank App**

    - **Access Your Bank’s PIX Scheduling Feature:**
        - Open your bank’s mobile app or online banking portal.
        - Navigate to the PIX transfer section.
    - **Schedule Recurring PIX Transfers:**
        - Set up a recurring monthly PIX transfer to your Mercado Bitcoin account.
        - Ensure the transfer amount matches your investment parameters in the Satoshi project (e.g., BRL 100).
        - Confirm the transfer details and schedule the date and time to align with the GitHub Actions workflow (e.g., a day before the investment script runs).

2. **Integrate PIX Transfers with Satoshi’s Automated Workflow**

    - **Synchronize Transfer Timing:**
        - Schedule PIX transfers to occur a day before the GitHub Actions workflow executes to ensure funds are available for investment.
    - **Monitor Transactions:**
        - Regularly check both your bank app and Mercado Bitcoin account to ensure transfers and investments are processed successfully.
    - **Adjust Parameters as Needed:**
        - If you change your investment amount, update both the PIX transfer and the Satoshi configuration to maintain consistency.

3. **Enhance Security and Reliability**

    - **Enable Notifications:**
        - Set up notifications for both PIX transfers and Mercado Bitcoin investments to stay informed about each transaction.
    - **Backup API Credentials:**
        - Securely store your Mercado Bitcoin API credentials and regularly update them to prevent unauthorized access.
    - **Test the Workflow:**
        - Perform a manual test run to ensure that PIX transfers and automated investments work seamlessly together.

By combining PIX's reliable transfer scheduling with Satoshi's automated investment workflow, you can create a hands-free system that ensures your cryptocurrency portfolio grows consistently every month.

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
