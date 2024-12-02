# ₿⚡ Satoshi

![Satoshi Banner](https://github.com/lucianoayres/satoshi/blob/main/images/satoshi_banner_optimized.png?raw=true)

Automate your monthly cryptocurrency investments on **Mercado Bitcoin** effortlessly! 💰

## Table of Contents

-   [Features](#features)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Automation with GitHub Actions](#automation-with-github-actions)
-   [Makefile Commands](#makefile-commands)
-   [Contributing](#contributing)
-   [License](#license)

## Features

-   📅 **Automated Monthly Investments**: Schedule your crypto purchases monthly.
-   🔒 **Secure Authentication**: Utilizes Mercado Bitcoin's API securely.
-   ⚙️ **Customizable Parameters**: Choose your crypto symbol, currency, and investment amount.
-   🛠️ **Easy Setup**: Simple installation with provided Makefile and requirements.

## Prerequisites

-   Python 3.x
-   Mercado Bitcoin API credentials (API ID and API Secret)
-   GitHub account (for automation)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/satoshi.git
    cd satoshi
    ```

2. **Set Up Virtual Environment and Install Dependencies**

    ```bash
    make setup
    ```

3. **Configure Environment Variables**

    - Create a `.env` file in the root directory.
    - Add your Mercado Bitcoin API credentials and desired investment parameters:

        ```ini
        MERCADO_BITCOIN_API_ID=your_api_id
        MERCADO_BITCOIN_API_SECRET=your_api_secret
        SYMBOL=BTC
        CURRENCY=BRL
        COST=100
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

Example:

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

    - Modify `.github/workflows/main.yml` to adjust the schedule or parameters.

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

---

_Happy Investing!_
