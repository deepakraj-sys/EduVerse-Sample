import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from modules_data import (all_modules, get_module_distribution, get_modules_by_category, 
                         get_module_by_name, get_all_categories, get_all_module_names)
from api_integrations import (api_integrations, get_all_api_categories, get_apis_by_category,
                             get_api_by_name, get_api_distribution, get_all_api_names,
                             get_complexity_distribution)

# Configure the page
st.set_page_config(
    page_title="EduVerse Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and logo
col1, col2 = st.columns([1, 3])
with col1:
    st.image("assets/eduverse_logo.svg", width=150)
with col2:
    st.title("EduVerse: Modular Learning Ecosystem")
    st.subheader("Interactive Dashboard")

# Sidebar navigation
st.sidebar.header("Navigation")
section = st.sidebar.radio(
    "Select a section:",
    ["Overview", "Module Explorer", "API Integrations"]
)

# Overview section
if section == "Overview":
    st.header("🎓 EduVerse Overview")
    
    st.write("""
    EduVerse is a comprehensive modular learning ecosystem designed to provide
    innovative educational experiences across various disciplines. The platform
    offers specialized modules targeting K-12 education, cybersecurity, and
    engineering disciplines, with integration capabilities for numerous educational APIs.
    """)
    
    # Display module distribution chart
    st.subheader("Module Distribution by Category")
    
    distribution = get_module_distribution()
    df_distribution = pd.DataFrame({
        "Category": distribution["categories"],
        "Number of Modules": distribution["counts"]
    })
    
    chart = alt.Chart(df_distribution).mark_bar().encode(
        x=alt.X('Category', sort='-y'),
        y='Number of Modules',
        color=alt.Color('Category', scale=alt.Scale(scheme='category10'))
    ).properties(
        height=400
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Display API integration distribution
    st.subheader("API Integration Categories")
    
    api_dist = get_api_distribution()
    df_api_dist = pd.DataFrame({
        "Category": api_dist["categories"],
        "Number of APIs": api_dist["counts"]
    })
    
    api_chart = px.pie(
        df_api_dist, 
        values="Number of APIs", 
        names="Category",
        title="API Distribution by Category",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    st.plotly_chart(api_chart, use_container_width=True)
    
    # Technology stack
    st.subheader("Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Web Framework**")
        st.write("Django/Flask for backend development")
        
        st.markdown("**Frontend Integration**")
        st.write("React/Vue.js for dynamic user interfaces")
        
        st.markdown("**Database**")
        st.write("Supabase for managing user data and content")
    
    with col2:
        st.markdown("**Authentication**")
        st.write("Supabase/PyAuth for secure user authentication")
        
        st.markdown("**API Consumption**")
        st.write("Python's requests library for external API interaction")
        
        st.markdown("**Gamification**")
        st.write("Pygame or Unity integration for advanced features")

# Module Explorer section
elif section == "Module Explorer":
    st.header("📚 Module Explorer")
    
    tab1, tab2 = st.tabs(["Browse by Category", "Search Modules"])
    
    with tab1:
        # Category selection
        category = st.selectbox(
            "Select a module category",
            get_all_categories()
        )
        
        # Display modules in the selected category
        st.subheader(f"Modules in {category}")
        
        modules = get_modules_by_category(category)
        
        for i, module in enumerate(modules):
            with st.expander(f"{module['name']} - {module['age_range']}"):
                st.markdown(f"**Description:** {module['description']}")
                
                st.markdown("**Key Features:**")
                for feature in module['features']:
                    st.markdown(f"- {feature}")
    
    with tab2:
        # Search by module name
        module_name = st.selectbox(
            "Select a module",
            get_all_module_names()
        )
        
        module = get_module_by_name(module_name)
        
        if module:
            st.subheader(module['name'])
            st.markdown(f"**Category:** {module['category']}")
            st.markdown(f"**Age Range:** {module['age_range']}")
            st.markdown(f"**Description:** {module['description']}")
            
            st.markdown("**Key Features:**")
            for feature in module['features']:
                st.markdown(f"- {feature}")
        else:
            st.error("Module not found. Please select a valid module name.")

# API Integrations section
elif section == "API Integrations":
    st.header("🔌 API Integrations")
    
    st.write("""
    EduVerse integrates with various free public APIs to enhance its functionality
    and provide rich educational experiences. Explore the available API integrations below.
    """)
    
    tab1, tab2, tab3 = st.tabs(["Browse by Category", "Search APIs", "Implementation Complexity"])
    
    with tab1:
        # Category selection
        api_category = st.selectbox(
            "Select an API category",
            get_all_api_categories()
        )
        
        # Display APIs in the selected category
        st.subheader(f"APIs in {api_category}")
        
        apis = get_apis_by_category(api_category)
        
        for api in apis:
            with st.expander(api['name']):
                st.markdown(f"**Description:** {api['description']}")
                
                st.markdown("**Use Cases:**")
                for use_case in api['use_cases']:
                    st.markdown(f"- {use_case}")
                
                st.markdown(f"**Implementation Complexity:** {api['implementation_complexity']}")
                st.markdown(f"**Documentation:** [Link]({api['documentation_url']})")
    
    with tab2:
        # Search by API name
        api_name = st.selectbox(
            "Select an API",
            get_all_api_names()
        )
        
        api = get_api_by_name(api_name)
        
        if api:
            st.subheader(api['name'])
            st.markdown(f"**Category:** {api['category']}")
            st.markdown(f"**Description:** {api['description']}")
            
            st.markdown("**Use Cases:**")
            for use_case in api['use_cases']:
                st.markdown(f"- {use_case}")
            
            st.markdown(f"**Implementation Complexity:** {api['implementation_complexity']}")
            st.markdown(f"**Documentation:** [Link]({api['documentation_url']})")
        else:
            st.error("API not found. Please select a valid API name.")
    
    with tab3:
        # Display API complexity distribution
        st.subheader("API Implementation Complexity")
        
        complexity = get_complexity_distribution()
        df_complexity = pd.DataFrame({
            "Complexity": complexity["complexities"],
            "Number of APIs": complexity["counts"]
        })
        
        complexity_chart = px.bar(
            df_complexity,
            x="Complexity",
            y="Number of APIs",
            color="Complexity",
            color_discrete_map={
                "Low": "#4CAF50",
                "Medium": "#FFC107",
                "High": "#F44336"
            }
        )
        
        st.plotly_chart(complexity_chart, use_container_width=True)
        
        # Implementation notes
        st.markdown("### Implementation Notes")
        st.write("""
        When integrating these APIs, consider the following:
        
        - **Low complexity**: Typically requires basic HTTP requests and simple response parsing.
        - **Medium complexity**: May involve authentication, pagination, or more complex data structures.
        - **High complexity**: Requires complex authentication, webhook implementations, or extensive data processing.
        
        All API integrations should implement proper error handling, rate limiting consideration, and caching where appropriate.
        """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>EduVerse: Modular Learning Ecosystem Dashboard | Created with Streamlit</p>
    </div>
    """, 
    unsafe_allow_html=True
)
