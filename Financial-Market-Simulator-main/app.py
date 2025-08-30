import streamlit as st
import subprocess
import os
from components.auth import authenticate_user, register_user, get_current_user
from components.news import display_news
from components.quiz import stock_market_description
from components.stock_simulation import simulate_stocks



st.set_page_config(page_title="Stock Market Simulation", layout="wide")


st.markdown(
    """
    <style>
    .main {
        background-color: #800080; /* Purple color */
        color: white; /* Optional: Set text color to white for better contrast */
    }

    /* General Reset */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    /* Body and background */
    body {
      font-family: Arial, sans-serif;
      background: #f0f0f0;
      padding: 50px 0;
      text-align: center;
    }

    /* Single large container */
    .single-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }

    /* Styling for the single item */
    .single-item {
      display: flex;
      overflow: hidden;
      border-radius: 10px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
      transform: scale(1);
      transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
      width: 100%;
      background: linear-gradient(to right, #e0e0e0, #ffffff); /* Light gradient */
    }

    /* Content and image styling */
    .content, .image {
      width: 50%;
      padding: 20px;
    }

    .content {
      background-color: #f5f5f5; /* Gray color */
      color: #333; /* Dark text */
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: left;
      font-family: 'Arial', sans-serif;
    }

    .content h2 {
      font-size: 28px;
      margin-bottom: 10px;
    }

    .content p {
      font-size: 16px;
      line-height: 1.5;
    }

    .image {
      background-color: #ffebcd; /* Soft beige background */
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      position: relative;
    }

    .image img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease-in-out;
    }

    /* Hover Effects */
    .single-item:hover {
      transform: scale(1.05);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }

    .single-item:hover .image img {
      transform: scale(1.2);
      filter: brightness(0.9); /* Slight darkening */
    }

    /* Animation for hover */
    .single-item:hover .content {
      animation: fadeInText 0.5s ease-in-out;
    }

    @keyframes fadeInText {
      from {
        opacity: 0.8;
      }
      to {
        opacity: 1;
      }
    }

    /* Responsive */
    @media (max-width: 768px) {
      .single-container {
        flex-direction: column;
      }
      .single-item {
        flex-direction: column;
      }
    }



    .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(45deg, #ff6ec4, #7873f5, #4facfe);
            animation: gradient-move 6s infinite;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
            transition: transform 0.3s ease;
        }

        .header-container:hover {
            transform: scale(1.05);
        }

        @keyframes gradient-move {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        
        

        .header-title {
            font-size: 3em;
            color: white;
            text-align: center;
            margin: 0;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
        }
 .slider-container {
        max-width: 1000px; /* Maintain wider container width */
        margin: 20px auto 0 auto; /* Add top margin for slight upward adjustment */
        overflow: hidden;
        position: relative;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    /* Slider track (holding the images) */
    .slider-track {
        display: flex;
        animation: slide 12s ease-in-out infinite; /* Circular slide effect */
    }

    /* Individual image styling */
    .slider-item {
        min-width: 90%; /* Maintain large width for images */
        padding: 10px;
        margin: 0 10px;
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    }

    /* Styling for images */
    .slider-item img {
        width: 100%; /* Ensure image fits inside container */
        height: 450px; /* Maintain increased height */
        object-fit: cover; /* Ensures aspect ratio is preserved */
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease-in-out, filter 0.3s ease-in-out;
    }

    /* Slight scaling effect on hover */
    .slider-item:hover {
        transform: scale(1.1);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    .slider-item:hover img {
        transform: scale(1.1);
        filter: brightness(1.2);
    }

    /* Circular sliding animation */
    @keyframes slide {
        0% { transform: translateX(0); }
        20% { transform: translateX(0); }
        25% { transform: translateX(-100%); }
        45% { transform: translateX(-100%); }
        50% { transform: translateX(-200%); }
        70% { transform: translateX(-200%); }
        75% { transform: translateX(-300%); }
        95% { transform: translateX(-300%); }
        100% { transform: translateX(0); }
    }

    /* Add spacing adjustments to the overall page */
    body {
        margin-top: -50px; /* Push entire page content upwards */
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
        """
        <br><br><br><br>
        <div class="header-container"><br><br><br>
            <h1 class="header-title">📈 Stock Market Simulation Platform</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


html_content = """
<div class="slider-container">
    <div class="slider-track">
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/6772077/pexels-photo-6772077.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 1">
        </div>
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/6802052/pexels-photo-6802052.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 2">
        </div>
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/6801650/pexels-photo-6801650.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 3">
        </div>
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/7567228/pexels-photo-7567228.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 4">
        </div>
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/7567529/pexels-photo-7567529.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 5">
        </div>
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/6780789/pexels-photo-6780789.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 5">
        </div>
        <div class="slider-item">
            <img src="https://images.pexels.com/photos/7567441/pexels-photo-7567441.jpeg?auto=compress&cs=tinysrgb&w=600" alt="Image 5">
        </div>
    </div>
</div>
<br><br><br>


<div class="single-container">
    <div class="single-item">
        <div class="content">
            <h2>Trade Smart, Win Big</h2>
            <p>A dynamic marketplace where investors buy, sell, and trade company shares.</p>
        </div>
        <div class="image">
            <img src="https://www.bing.com/th?id=OIP.8GhLfxN0ED5LVVqQgWqzYgHaE7&w=159&h=106&c=8&rs=1&qlt=90&o=6&dpr=1.3&pid=3.1&rm=2" alt="Image 1">
        </div>
    </div>
</div>






<script>
    // Add a little hover effect animation on page load
    document.querySelectorAll('.single-item').forEach((item) => {
      item.addEventListener('mouseenter', () => {
        item.style.transform = 'scale(1.05)';
      });

      item.addEventListener('mouseleave', () => {
        item.style.transform = 'scale(1)';
      });
    });
</script>
"""

# Display the HTML content in Streamlit
st.markdown(html_content, unsafe_allow_html=True)





# Authentication Section
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    st.sidebar.header("User Authentication")
    action = st.sidebar.radio("Select an option", ["Login", "Register"])

    if action == "Login":
        user = authenticate_user()
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome back, {user}!")
    elif action == "Register":
        if register_user():
            st.success("Registration successful! Please log in.")
else:
    # User logged in
    st.sidebar.write(f"Logged in as: {st.session_state['user']}")
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
        st.rerun()  # Changed from experimental_rerun() to rerun()

    # Display sections
    display_news()
    simulate_stocks()
    
    stock_market_description()
    # Add Let's Trade Now button
    st.markdown("---")
    if st.button("Let's learn Now! 🚀"):
        try:
            # Specify the full path to the Streamlit app
            app_path = r"quiz2.py"
            
            # Ensure the path exists
            if not os.path.exists(app_path):
                st.error(f"Error: The file {app_path} does not exist.")
            else:
                # Run the Streamlit app using subprocess
                subprocess.Popen(["streamlit", "run", app_path], 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
                st.success("Trading platform is launching in a new window!")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    

    
