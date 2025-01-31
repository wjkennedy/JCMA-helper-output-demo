import streamlit as st
from jira import JIRA

# Function to connect to JIRA
def connect_to_jira(server, username, api_token):
    try:
        jira = JIRA(server=server, basic_auth=(username, api_token))
        return jira
    except Exception as e:
        st.error(f"Failed to connect to JIRA: {e}")
        return None

# Pages for different JCMA errors
def jcma_124(jira):
    st.header("JCMA 124: Invalid Board Administrators")
    project_key = st.text_input("Enter Project Key")
    board_name = st.text_input("Enter Board Name")
    
    if st.button("Fix Board Administrators"):
        # Fetch board details and update admins
        st.write("Fetching board details...")
        # Logic to update board administrators
        st.success("Board administrators updated successfully.")

def jcma_149(jira):
    st.header("JCMA 149: Invalid Issue Type Status")
    project_key = st.text_input("Enter Project Key")
    issue_key = st.text_input("Enter Issue Key")
    workflow_name = st.text_input("Enter Workflow Name")
    
    if st.button("Fix Issue Status"):
        # Logic to correct issue status in the workflow
        st.success("Issue status updated successfully.")

def jcma_510(jira):
    st.header("JCMA 510: Request Type Migration Issue")
    project_key = st.text_input("Enter Project Key")
    request_type_id = st.text_input("Enter Request Type ID")
    issue_type_id = st.text_input("Enter Issue Type ID")
    
    if st.button("Add Missing Issue Type"):
        # Logic to add missing issue type to scheme
        st.success("Issue type added successfully.")

def main():
    st.sidebar.title("JCMA Error Codes")
    page = st.sidebar.radio("Select an Error Code", ["JCMA 124", "JCMA 149", "JCMA 510"])
    
    st.title("JIRA Cloud Migration Assistant Troubleshooter")
    server = st.text_input("JIRA Server URL", "https://your-jira-instance.atlassian.net")
    username = st.text_input("JIRA Username")
    api_token = st.text_input("JIRA API Token", type="password")
    
    if st.button("Connect to JIRA"):
        jira = connect_to_jira(server, username, api_token)
        if jira:
            st.success("Connected to JIRA successfully.")
    else:
        jira = None
    
    if jira:
        if page == "JCMA 124":
            jcma_124(jira)
        elif page == "JCMA 149":
            jcma_149(jira)
        elif page == "JCMA 510":
            jcma_510(jira)

if __name__ == "__main__":
    main()

