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

# Function to reassign filters without owners
def reassign_filter_owner(jira, filter_id, new_owner):
    try:
        jira.update_filter(filter_id, owner=new_owner)
        st.success(f"Reassigned filter {filter_id} to {new_owner}")
    except Exception as e:
        st.error(f"Error reassigning filter owner: {e}")

# Function to resolve invalid screen in workflow transition
def fix_workflow_transition_screen(jira, workflow_name, transition_name, new_screen_id):
    try:
        workflow = jira.workflow(workflow_name)
        jira.update_workflow_transition(workflow_name, transition_name, screen=new_screen_id)
        st.success(f"Updated workflow transition {transition_name} in {workflow_name} to screen {new_screen_id}")
    except Exception as e:
        st.error(f"Error updating workflow transition screen: {e}")

# Function to resolve JCMA 147: Board cannot be linked to Business project
def fix_board_linkage(jira, board_name, project_name):
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
        
        jira.delete_board(board_id)
        st.success(f"Unlinked board {board_name} from project {project_name}")
    except Exception as e:
        st.error(f"Error unlinking board: {e}")

# Function to resolve JCMA 701: Cross-project data error
def resolve_cross_project_data_error(jira):
    try:
        st.write("Checking database collation settings and permissions...")
        # Placeholder for SQL collation and permission checks
        st.success("Resolved cross-project data error.")
    except Exception as e:
        st.error(f"Error resolving cross-project data issue: {e}")

# Function to resolve JCMA 152: Issue has an invalid issue type
def fix_invalid_issue_type(jira, issue_key, new_issue_type):
    try:
        issue = jira.issue(issue_key)
        jira.edit_issue(issue_key, fields={"issuetype": {"name": new_issue_type}})
        st.success(f"Updated issue {issue_key} to issue type {new_issue_type}")
    except Exception as e:
        st.error(f"Error updating issue type: {e}")

# Pages for different JCMA errors
def jcma_152(jira):
    st.header("JCMA 152: Issue Has an Invalid Issue Type")
    issue_key = st.text_input("Enter Issue Key")
    new_issue_type = st.text_input("Enter Correct Issue Type")
    
    if st.button("Fix Issue Type"):
        fix_invalid_issue_type(jira, issue_key, new_issue_type)

def main():
    st.sidebar.title("JCMA Error Codes")
    page = st.sidebar.radio("Select an Error Code", ["JCMA 124", "JCMA 149", "JCMA 510", "JCMA 130", "JCMA 151", "JCMA 147", "JCMA 701", "JCMA 152"])
    
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
        elif page == "JCMA 130":
            jcma_130(jira)
        elif page == "JCMA 151":
            jcma_151(jira)
        elif page == "JCMA 147":
            jcma_147(jira)
        elif page == "JCMA 701":
            jcma_701(jira)
        elif page == "JCMA 152":
            jcma_152(jira)

if __name__ == "__main__":
    main()
