# JCMA Error Troubleshooter

![](jiroctopus.png)

## Overview
This **JCMA Error Troubleshooter** is a Streamlit-based tool that helps diagnose and resolve common errors encountered during Jira Cloud Migration. It automates fixes for JCMA error codes using the Jira REST API.

## Features
- **Automated Fixes**: Provides solutions for the following JCMA errors:
  - JCMA 124: Invalid Board Administrators
  - JCMA 149: Invalid Issue Type Status
  - JCMA 510: Request Type Migration Issue
  - JCMA 130: Filter Has No Owner Assigned
  - JCMA 151: Workflow Transition Linked to Invalid Screen
  - JCMA 147: Board Cannot Be Linked to Business Project
  - JCMA 701: Cross-Project Data Error
  - JCMA 152: Issue Has an Invalid Issue Type
- **Easy-to-Use Interface**: Navigate through error codes via the sidebar and apply automated fixes.
- **Secure Authentication**: Uses Jira API Bearer Token for secure API requests.

## Installation
### Prerequisites
- Python 3.7+
- `pip`

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/jcma-error-troubleshooter.git
   cd jcma-error-troubleshooter
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run jcma_error_app.py
   ```

## Usage
1. Enter your **JIRA Server URL**, **API Token**, and click **Connect to JIRA**.
2. Select a JCMA error code from the sidebar.
3. Provide necessary inputs (like project keys, issue types, etc.).
4. Click the respective **Fix** button to apply an automated solution.

## License
This project is licensed under the MIT License.

## Author
Developed by [Your Name]. Contributions are welcome!
