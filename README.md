# Bank-Statement-Visualizer
## Overview

The HDFC Bank Statement Analyzer is an advanced financial data analysis tool designed to provide comprehensive insights into personal banking transactions. This enterprise-grade application processes HDFC Bank statements, offering users a detailed visualization of their financial activities through an interactive dashboard.

## Features

- **Data Processing**: Automated cleaning and transformation of raw bank statement data.
- **Interactive Dashboard**: Built with Streamlit for an intuitive user experience.
- **Advanced Visualizations**: Utilizing Plotly for creating insightful charts and graphs.
- **Database Integration**: SQLite backend for efficient data storage and retrieval.
- **Long-term Trend Analysis**: Track financial patterns over extended periods.
- **Customizable Analysis**:
  - Monthly filtering
  - Custom date range selection
  - Merchant transaction summaries
- **Key Insights**:
  - Spending heatmaps
  - Income vs. expense comparisons
  - Day-of-week spending patterns
  - Merchant-wise transaction analysis

## Technology Stack

- **Backend**: Python 3.8+
- **Frontend**: Streamlit
- **Data Processing**: Pandas
- **Data Visualization**: Plotly
- **Database**: SQLite
- **Version Control**: Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hdfc-bank-analyzer.git
   cd hdfc-bank-analyzer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python database.py
   ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open a web browser and navigate to `http://localhost:8501`.

3. Upload your HDFC Bank statement (XLS format) using the file uploader in the sidebar.

4. Explore the various visualizations and insights provided in the dashboard.

## Data Privacy and Security

This application processes sensitive financial data. It is designed to run locally on your machine, ensuring that your bank statements and personal information never leave your system. Always exercise caution when handling financial data and avoid uploading your statements to any third-party services.

## Contributing

We welcome contributions to improve the HDFC Bank Statement Analyzer. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- HDFC Bank for providing the statement format
- The Streamlit team for their excellent data app framework
- Contributors and maintainers of Pandas and Plotly

## Contact

For any queries or support, please open an issue in the GitHub repository or contact the maintainer at [monish.emailbox@gmail.com](mailto: monish.emailbox@gmail.com).
