import streamlit as st
from jira import JIRA

# Function to connect to JIRA using Bearer Token
def connect_to_jira(server, api_token):
    try:
        options = {"server": server}
        jira = JIRA(options=options, token_auth=api_token)
        return jira
    except Exception as e:
        st.error(f"Failed to connect to JIRA: {e}")
        return None

# Function to update board administrators
def update_board_admins(jira, board_name, new_admins):
    try:
        boards = jira.boards()
        board_id = None
        for board in boards:
            if board.name == board_name:
                board_id = board.id
                break
        
        if board_id is None:
            st.error("Board not found")
            return
        
        board_config = jira.board(board_id)
        board_config.update(administrators=new_admins)
        st.success(f"Updated administrators for board {board_name}")
    except Exception as e:
        st.error(f"Error updating board administrators: {e}")

# Function to correct issue status in the workflow
def update_issue_status(jira, issue_key, new_status):
    try:
        issue = jira.issue(issue_key)
        transitions = jira.transitions(issue)
        transition_id = None
        for transition in transitions:
            if transition['name'].lower() == new_status.lower():
                transition_id = transition['id']
                break
        
        if transition_id is None:
            st.error("Invalid status transition")
            return
        
        jira.transition_issue(issue, transition_id)
        st.success(f"Updated issue {issue_key} to status {new_status}")
    except Exception as e:
        st.error(f"Error updating issue status: {e}")

# Function to add missing issue type to scheme
def add_issue_type_to_scheme(jira, project_key, issue_type_id):
    try:
        project = jira.project(project_key)
        issue_type_scheme = jira.issue_type_scheme(project)
        
        if issue_type_id in issue_type_scheme.issue_types:
            st.info("Issue type already exists in the scheme.")
            return
        
        issue_type_scheme.issue_types.append(issue_type_id)
        jira.update_issue_type_scheme(issue_type_scheme.id, issue_type_scheme.issue_types)
        st.success(f"Added issue type {issue_type_id} to project {project_key}")
    except Exception as e:
        st.error(f"Error adding issue type to scheme: {e}")

# Pages for different JCMA errors
def jcma_124(jira):
    st.header("JCMA 124: Invalid Board Administrators")
    board_name = st.text_input("Enter Board Name")
    new_admins = st.text_area("Enter New Administrators (comma-separated)")
    
    if st.button("Fix Board Administrators"):
        new_admins_list = [admin.strip() for admin in new_admins.split(',')]
        update_board_admins(jira, board_name, new_admins_list)

def jcma_149(jira):
    st.header("JCMA 149: Invalid Issue Type Status")
    issue_key = st.text_input("Enter Issue Key")
    new_status = st.text_input("Enter Correct Status")
    
    if st.button("Fix Issue Status"):
        update_issue_status(jira, issue_key, new_status)

def jcma_510(jira):
    st.header("JCMA 510: Request Type Migration Issue")
    project_key = st.text_input("Enter Project Key")
    issue_type_id = st.text_input("Enter Issue Type ID")
    
    if st.button("Add Missing Issue Type"):
        add_issue_type_to_scheme(jira, project_key, issue_type_id)


def main():
    st.sidebar.title("JCMA Error Codes")
    page = st.sidebar.radio("Select an Error Code", ["JCMA 124", "JCMA 149", "JCMA 510"])
    
    st.title("JIRA Cloud Migration Assistant Troubleshooter")
    server = st.text_input("JIRA Server URL", "https://your-jira-instance.atlassian.net")
    api_token = st.text_input("JIRA API Token", type="password")
    
    if st.button("Connect to JIRA"):
        jira = connect_to_jira(server, api_token)
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

